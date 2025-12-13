"""Function tools for the RAG agent using OpenAI Agent SDK.

This module provides function tools that the RAG agent can invoke to search
and retrieve content from the Physical AI & Humanoid Robotics textbook.

The primary tool is `search_textbook`, which performs semantic search against
the Qdrant vector database and returns formatted results with source citations.

Usage:
    from app.services.agent.tools import search_textbook

    # The tool is used by the agent automatically when added to tools list
    agent = Agent(
        name="RAG Agent",
        tools=[search_textbook],
    )

Note:
    Tools are decorated with @function_tool from the OpenAI Agent SDK.
    The decorator automatically generates JSON schemas from function signatures
    and docstrings for the LLM to understand how to call the tools.
"""

from typing import Annotated

from agents import function_tool

from app.config import get_settings
from app.services.embedding import get_embedding_service
from app.services.retrieval import get_retriever
from app.utils.logging import get_logger

logger = get_logger(__name__)


@function_tool
async def search_textbook(
    query: Annotated[str, "The search query to find relevant textbook content"],
    k: Annotated[int, "Number of results to return (1-10, default 5)"] = 5,
) -> str:
    """Search the Physical AI & Humanoid Robotics textbook for relevant passages.

    Use this tool to find information from the textbook about robotics topics
    including kinematics, dynamics, control systems, ROS2, URDF, simulation,
    sensors, actuators, and humanoid robotics.

    The search uses semantic similarity to find the most relevant passages
    based on the meaning of the query, not just keyword matching.

    Args:
        query: The search query describing what information you need.
               Be specific and descriptive for better results.
        k: Maximum number of results to return (1-10). Defaults to 5.
           Use fewer results for focused queries, more for broader topics.

    Returns:
        A formatted string containing search results with:
        - Numbered results with titles and relevance scores
        - Source URLs for citation
        - Content excerpts from the textbook

        Returns a message if no relevant content is found.

    Example queries:
        - "What is inverse kinematics and how is it used in robotics?"
        - "Explain the ROS2 navigation stack"
        - "How do servo motors work in humanoid robots?"
    """
    # Validate and clamp k to acceptable range
    k = max(1, min(10, k))

    logger.info(
        "search_textbook tool invoked",
        extra={"query": query[:100], "k": k},
    )

    try:
        settings = get_settings()

        # Step 1: Embed the query using query-optimized embeddings
        logger.debug("Embedding search query")
        embedding_service = get_embedding_service()
        query_vector = embedding_service.embed_query(query)

        logger.debug(
            "Query embedded successfully",
            extra={"vector_dimensions": len(query_vector)},
        )

        # Step 2: Search Qdrant for similar content
        logger.debug("Searching Qdrant for similar content")
        retriever = get_retriever()
        results = await retriever.search(
            query_vector=query_vector,
            k=k,
            threshold=settings.score_threshold,
        )

        logger.info(
            "Qdrant search completed",
            extra={"results_count": len(results), "threshold": settings.score_threshold},
        )

        # Step 3: Handle no results case
        if not results:
            logger.info(
                "No relevant content found for query",
                extra={"query": query[:100]},
            )
            return (
                "No relevant content found in the textbook for this query. "
                "Try rephrasing your question or using different keywords related to "
                "robotics, kinematics, dynamics, control systems, ROS2, URDF, "
                "simulation, sensors, actuators, or humanoid robotics."
            )

        # Step 4: Format results for the agent
        formatted_results = _format_search_results(results)

        logger.debug(
            "Search results formatted",
            extra={"formatted_length": len(formatted_results)},
        )

        return formatted_results

    except ValueError as e:
        # Handle validation errors (e.g., empty query)
        logger.warning(
            "Validation error in search_textbook",
            extra={"error": str(e), "query": query[:100]},
        )
        return f"Search error: {e}. Please provide a valid search query."

    except Exception as e:
        # Handle unexpected errors gracefully
        logger.error(
            "Error in search_textbook tool",
            extra={"error": str(e), "query": query[:100]},
        )
        return (
            "An error occurred while searching the textbook. "
            "Please try again or rephrase your query."
        )


def _format_search_results(results: list[dict]) -> str:
    """Format search results into a readable string for the LLM.

    Transforms raw search results into a structured format that the LLM
    can easily parse and use for generating responses with citations.

    Args:
        results: List of search result dictionaries from Qdrant containing:
            - content: The text content of the chunk
            - url: Source URL for citation
            - title: Page/section title
            - score: Similarity score (0.0 to 1.0)
            - heading: Section heading (optional)
            - module: Module name (optional)
            - chapter: Chapter identifier (optional)

    Returns:
        A formatted string with numbered results, each containing:
        - Result number and title
        - Relevance score
        - Source URL
        - Module/chapter context if available
        - Content excerpt (truncated to 600 characters)
    """
    formatted_parts = []

    for i, result in enumerate(results, 1):
        # Extract metadata with defaults
        title = result.get("title", "Untitled")
        score = result.get("score", 0.0)
        url = result.get("url", "")
        content = result.get("content", "")
        heading = result.get("heading", "")
        module = result.get("module", "")
        chapter = result.get("chapter", "")

        # Build the formatted result
        parts = [f"[{i}] {title}"]

        # Add heading if different from title and non-empty
        if heading and heading != title:
            parts[0] += f" - {heading}"

        parts.append(f"Relevance Score: {score:.2f}")
        parts.append(f"Source URL: {url}")

        # Add module/chapter context if available
        if module or chapter:
            context_parts = []
            if module:
                context_parts.append(f"Module: {module}")
            if chapter:
                context_parts.append(f"Chapter: {chapter}")
            parts.append(" | ".join(context_parts))

        # Truncate content to reasonable length for LLM context
        # Use 600 chars to balance detail with context window efficiency
        content_preview = content[:600]
        if len(content) > 600:
            content_preview += "..."

        parts.append(f"Content:\n{content_preview}")

        formatted_parts.append("\n".join(parts))

    # Join all results with clear separator
    header = f"Found {len(results)} relevant passage(s) from the textbook:\n"
    return header + "\n\n---\n\n".join(formatted_parts)


# Export public API
__all__ = ["search_textbook"]
