"""Chat router for RAG-based Q&A.

This module implements the POST /chat endpoint for the Physical AI & Humanoid
Robotics textbook chatbot. The endpoint:

1. Accepts user questions via ChatRequest
2. Embeds the query using Google's text-embedding-004
3. Searches Qdrant for relevant textbook passages
4. Uses the Agent SDK with Gemini to generate answers
5. Returns formatted responses with source citations

The endpoint includes comprehensive error handling for validation errors,
rate limits, and service unavailability.

Usage:
    POST /api/v1/chat
    {
        "query": "What is inverse kinematics?",
        "k": 5
    }

Response:
    {
        "answer": "Inverse kinematics (IK) is the mathematical technique...",
        "citations": [...],
        "metadata": {...}
    }
"""

import time
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from app.config import get_settings
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    Citation,
    ErrorResponse,
    ResponseMetadata,
)
from app.services.agent import get_orchestrator
from app.services.embedding import get_embedding_service
from app.services.retrieval import get_retriever
from app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


def truncate_snippet(content: str, max_length: int = 200) -> str:
    """Truncate content to a maximum length with word boundary preservation.

    Ensures snippets are cleanly truncated at word boundaries with ellipsis
    when content exceeds the maximum length.

    Args:
        content: The text content to truncate.
        max_length: Maximum characters for the snippet (default: 200).

    Returns:
        Truncated string with ellipsis if needed, or original if within limit.

    Example:
        >>> truncate_snippet("This is a long text that needs truncation", 20)
        'This is a long...'
    """
    if not content:
        return ""

    content = content.strip()

    if len(content) <= max_length:
        return content

    # Truncate to max_length and find last word boundary
    truncated = content[:max_length]

    # Find the last space to avoid cutting words
    last_space = truncated.rfind(" ")

    if last_space > max_length // 2:
        # Use word boundary if it's not too far back
        truncated = truncated[:last_space]

    return truncated.rstrip() + "..."


def format_citation_url(url: str) -> str:
    """Ensure citation URL is properly formatted.

    Validates and formats URLs for citations. Handles edge cases like
    missing protocols or malformed URLs.

    Args:
        url: The source URL to format.

    Returns:
        Properly formatted URL string.

    Example:
        >>> format_citation_url("example.com/page")
        'https://example.com/page'
    """
    if not url:
        return ""

    url = url.strip()

    # Add protocol if missing
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    return url


def build_citations_from_results(
    search_results: list[dict[str, Any]],
) -> list[Citation]:
    """Build Citation objects from Qdrant search results.

    Transforms raw search results into properly formatted Citation objects
    with truncated snippets and formatted URLs.

    Args:
        search_results: List of search result dictionaries from Qdrant.
            Each dict should contain: content, url, title, score.

    Returns:
        List of Citation objects ready for the response.

    Example:
        >>> results = [{"content": "...", "url": "...", "title": "...", "score": 0.95}]
        >>> citations = build_citations_from_results(results)
        >>> len(citations)
        1
    """
    citations = []

    for result in search_results:
        # Extract and format fields
        content = result.get("content", "")
        url = result.get("url", "")
        title = result.get("title", "Untitled")
        score = result.get("score", 0.0)

        # Build snippet with proper truncation
        snippet = truncate_snippet(content, max_length=200)

        # Format URL
        formatted_url = format_citation_url(url)

        # Skip results with missing essential fields
        if not snippet or not formatted_url:
            logger.warning(
                "Skipping citation with missing data",
                extra={"has_content": bool(content), "has_url": bool(url)},
            )
            continue

        citations.append(
            Citation(
                url=formatted_url,
                title=title or "Untitled",
                snippet=snippet,
                score=round(score, 4),  # Round for cleaner output
            )
        )

    return citations


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        429: {"model": ErrorResponse, "description": "Rate limited"},
        503: {"model": ErrorResponse, "description": "Service unavailable"},
    },
    summary="Ask a question about the textbook",
    description=(
        "Send a question and receive an answer with source citations from the "
        "Physical AI & Humanoid Robotics textbook. The endpoint uses RAG "
        "(Retrieval-Augmented Generation) to find relevant passages and generate "
        "accurate answers with proper citations."
    ),
)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a user question and return an answer with citations.

    This endpoint implements the RAG pipeline:
    1. Validates the incoming request
    2. Embeds the query using Google's text-embedding-004
    3. Searches Qdrant for relevant textbook chunks
    4. Invokes the Gemini-powered agent to generate an answer
    5. Builds and returns formatted citations

    Args:
        request: ChatRequest containing the user's query and optional k value.

    Returns:
        ChatResponse with the answer, citations, and metadata.

    Raises:
        HTTPException: 400 for validation errors, 429 for rate limits,
            503 for service unavailability.

    Example:
        >>> # POST /api/v1/chat
        >>> request = ChatRequest(query="What is inverse kinematics?", k=5)
        >>> response = await chat(request)
        >>> print(response.answer)
        Inverse kinematics (IK) is the mathematical technique...
    """
    start_time = time.time()
    settings = get_settings()

    logger.info(
        "Processing chat request",
        extra={
            "query_length": len(request.query),
            "k": request.k,
        },
    )

    try:
        # ---------------------------------------------------------------------
        # Get singleton service instances
        # ---------------------------------------------------------------------
        orchestrator = get_orchestrator()
        embedding_service = get_embedding_service()
        retriever = get_retriever()

        # ---------------------------------------------------------------------
        # Step 1: Embed the query
        # ---------------------------------------------------------------------
        logger.debug("Embedding query")
        query_vector = embedding_service.embed_query(request.query)

        # ---------------------------------------------------------------------
        # Step 2: Search for relevant chunks in Qdrant
        # ---------------------------------------------------------------------
        logger.debug("Searching for relevant chunks")
        search_results = await retriever.search(
            query_vector=query_vector,
            k=request.k,
            threshold=settings.score_threshold,
        )

        logger.info(
            "Search completed",
            extra={
                "results_count": len(search_results),
                "threshold": settings.score_threshold,
            },
        )

        # ---------------------------------------------------------------------
        # Step 3: Run the agent to generate answer
        # ---------------------------------------------------------------------
        logger.debug("Invoking agent orchestrator")
        agent_result = await orchestrator.chat(request.query, k=request.k)

        # ---------------------------------------------------------------------
        # Step 4: Build citations from search results
        # ---------------------------------------------------------------------
        citations = build_citations_from_results(search_results)

        # ---------------------------------------------------------------------
        # Step 5: Calculate processing time and build response
        # ---------------------------------------------------------------------
        processing_time_ms = int((time.time() - start_time) * 1000)

        # Extract model name from agent result
        model_name = agent_result.get("model", settings.llm_model)
        if hasattr(model_name, "model"):
            # Handle case where model is an object with a model attribute
            model_name = model_name.model

        response = ChatResponse(
            answer=agent_result["answer"],
            citations=citations,
            metadata=ResponseMetadata(
                chunks_retrieved=len(search_results),
                processing_time_ms=processing_time_ms,
                model=str(model_name),
            ),
        )

        logger.info(
            "Chat request completed successfully",
            extra={
                "processing_time_ms": processing_time_ms,
                "citations_count": len(citations),
                "answer_length": len(agent_result["answer"]),
            },
        )

        return response

    except ValidationError as e:
        # Handle Pydantic validation errors
        logger.warning(
            "Validation error in chat request",
            extra={"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                error="validation_error",
                message="Invalid request data",
                details={"errors": e.errors()},
            ).model_dump(),
        )

    except ValueError as e:
        # Handle value errors (e.g., empty query after validation)
        logger.warning(
            "Value error in chat request",
            extra={"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                error="validation_error",
                message=str(e),
                details=None,
            ).model_dump(),
        )

    except ConnectionError as e:
        # Handle connection errors to external services
        logger.error(
            "Connection error in chat endpoint",
            extra={"error": str(e)},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=ErrorResponse(
                error="service_unavailable",
                message="Unable to connect to required services. Please try again later.",
                details={"error_type": "connection_error"},
            ).model_dump(),
        )

    except Exception as e:
        # Handle all other exceptions
        error_type = type(e).__name__

        # Check for rate limit errors (common with Gemini API)
        error_str = str(e).lower()
        if "rate" in error_str and "limit" in error_str:
            logger.warning(
                "Rate limit error in chat endpoint",
                extra={"error": str(e)},
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=ErrorResponse(
                    error="rate_limit_exceeded",
                    message="Too many requests. Please wait before trying again.",
                    details={"retry_after_seconds": 60},
                ).model_dump(),
            )

        # Generic error handling
        logger.error(
            "Unexpected error in chat endpoint",
            extra={"error": str(e), "error_type": error_type},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=ErrorResponse(
                error="service_unavailable",
                message="An error occurred processing your request. Please try again.",
                details={"error_type": error_type},
            ).model_dump(),
        )


# Export public API
__all__ = ["router"]
