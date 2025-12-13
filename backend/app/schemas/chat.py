"""Pydantic schemas for chat endpoint request/response models.

This module defines the data models for the RAG chatbot API:

- ChatRequest: User's question submission with validation
- ChatResponse: System's response with answer and citations
- Citation: Reference to source passages used in answers
- ResponseMetadata: Metadata about response generation
- ErrorResponse: Standard error response format

All schemas use Pydantic v2 with proper validation, type hints, and documentation.
"""

from typing import Any

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    """User's question submission to the chat endpoint.

    Attributes:
        query: The user's question or message (1-2000 characters).
            Will be stripped of leading/trailing whitespace.
        k: Number of chunks to retrieve from vector database (1-10, default 5).
    """

    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's question or message to the RAG chatbot",
        examples=["What is inverse kinematics?", "Explain the difference between ROS1 and ROS2"],
    )
    k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of relevant chunks to retrieve from the vector database",
    )

    @field_validator("query")
    @classmethod
    def query_not_whitespace(cls, v: str) -> str:
        """Validate that query is not empty or whitespace-only.

        Args:
            v: The query string to validate.

        Returns:
            The stripped query string.

        Raises:
            ValueError: If the query is empty or whitespace-only.
        """
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "What are the main components of a humanoid robot?",
                    "k": 5,
                }
            ]
        }
    }


class Citation(BaseModel):
    """A reference to a source passage used in an answer.

    Citations provide traceability back to the original textbook content
    that was used to generate the response.

    Attributes:
        url: URL to the source document/chapter in the textbook.
        title: Title of the source section or chapter.
        snippet: Relevant text excerpt from the source (max 200 characters).
        score: Similarity/relevance score from vector search (0.0-1.0).
    """

    url: str = Field(
        ...,
        description="URL to the source document or chapter",
        examples=["https://textbook.example.com/chapters/kinematics"],
    )
    title: str = Field(
        ...,
        description="Title of the source section or chapter",
        examples=["Chapter 3: Forward and Inverse Kinematics"],
    )
    snippet: str = Field(
        ...,
        max_length=200,
        description="Relevant text excerpt from the source passage",
        examples=["Inverse kinematics is the mathematical process of calculating..."],
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Similarity/relevance score from vector search (0.0-1.0)",
        examples=[0.92],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://textbook.example.com/chapters/kinematics",
                    "title": "Chapter 3: Forward and Inverse Kinematics",
                    "snippet": "Inverse kinematics is the mathematical process of calculating the joint angles needed to place the end-effector at a desired position.",
                    "score": 0.92,
                }
            ]
        }
    }


class ResponseMetadata(BaseModel):
    """Metadata about the response generation.

    Provides information about the RAG pipeline execution for
    debugging, monitoring, and performance analysis.

    Attributes:
        chunks_retrieved: Number of text chunks retrieved from vector database.
        processing_time_ms: Total response generation time in milliseconds.
        model: Name of the LLM model used for generation.
    """

    chunks_retrieved: int = Field(
        ...,
        ge=0,
        description="Number of text chunks retrieved from the vector database",
        examples=[5],
    )
    processing_time_ms: int = Field(
        ...,
        ge=0,
        description="Total response generation time in milliseconds",
        examples=[1250],
    )
    model: str = Field(
        ...,
        description="Name of the LLM model used for response generation",
        examples=["gemini-2.5-flash", "gemini-1.5-flash"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "chunks_retrieved": 5,
                    "processing_time_ms": 1250,
                    "model": "gemini-2.5-flash",
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """The system's response to a user question.

    Contains the generated answer along with citations to source material
    and metadata about the response generation process.

    Attributes:
        answer: The generated answer from the RAG agent.
        citations: List of source references from the textbook used to generate the answer.
        metadata: Information about the response generation process.
    """

    answer: str = Field(
        ...,
        description="The generated answer from the RAG agent",
        examples=["Inverse kinematics (IK) is the mathematical technique used to determine the joint parameters..."],
    )
    citations: list[Citation] = Field(
        default_factory=list,
        description="Source references from the textbook used in the answer",
    )
    metadata: ResponseMetadata = Field(
        ...,
        description="Metadata about the response generation process",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "Inverse kinematics (IK) is the mathematical technique used to determine the joint parameters needed to place a robot's end-effector at a desired position and orientation.",
                    "citations": [
                        {
                            "url": "https://textbook.example.com/chapters/kinematics",
                            "title": "Chapter 3: Forward and Inverse Kinematics",
                            "snippet": "Inverse kinematics is the mathematical process of calculating...",
                            "score": 0.92,
                        }
                    ],
                    "metadata": {
                        "chunks_retrieved": 5,
                        "processing_time_ms": 1250,
                        "model": "gemini-2.5-flash",
                    },
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Standard error response format.

    Provides a consistent structure for API error responses
    with machine-readable error codes and human-readable messages.

    Attributes:
        error: Machine-readable error code or type.
        message: Human-readable error description.
        details: Optional additional error context and debugging information.
    """

    error: str = Field(
        ...,
        description="Machine-readable error code or type",
        examples=["validation_error", "rate_limit_exceeded", "internal_error"],
    )
    message: str = Field(
        ...,
        description="Human-readable error description",
        examples=["Query exceeds maximum length of 2000 characters"],
    )
    details: dict[str, Any] | None = Field(
        default=None,
        description="Optional additional error context and debugging information",
        examples=[{"field": "query", "max_length": 2000, "actual_length": 2500}],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "validation_error",
                    "message": "Query exceeds maximum length of 2000 characters",
                    "details": {"field": "query", "max_length": 2000, "actual_length": 2500},
                },
                {
                    "error": "rate_limit_exceeded",
                    "message": "Too many requests. Please wait before trying again.",
                    "details": {"retry_after_seconds": 60},
                },
            ]
        }
    }


__all__ = [
    "ChatRequest",
    "ChatResponse",
    "Citation",
    "ResponseMetadata",
    "ErrorResponse",
]
