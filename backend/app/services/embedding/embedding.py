"""Google Gemini embeddings service via LangChain.

This module provides text embedding functionality using Google's Generative AI
embeddings model (text-embedding-004) through the LangChain integration.

The service supports both query and document embeddings with appropriate task
types for optimal retrieval performance:
- Query embeddings: optimized for search queries
- Document embeddings: optimized for indexed documents

Features:
- Automatic retry with exponential backoff for rate limit handling
- Separate embedding configurations for queries and documents
- Singleton pattern for efficient resource usage
- Comprehensive logging for monitoring and debugging

Usage:
    from app.services.embedding import EmbeddingService
    from app.services.embedding.embedding import get_embedding_service

    # Get singleton instance
    service = get_embedding_service()

    # Embed a search query
    query_vector = service.embed_query("What is inverse kinematics?")

    # Embed multiple documents
    doc_vectors = service.embed_documents([
        "Inverse kinematics is the mathematical process...",
        "Forward kinematics computes the position..."
    ])
"""

from typing import Any

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """Handles text embedding using Google Gemini via LangChain.

    This service provides text-to-vector conversion using Google's
    text-embedding-004 model through LangChain's GoogleGenerativeAIEmbeddings.

    The service maintains two embedding instances:
    - Document embeddings with task_type="retrieval_document"
    - Query embeddings with task_type="retrieval_query"

    This separation optimizes embedding quality for asymmetric retrieval tasks
    where queries are typically short and documents are longer passages.

    Attributes:
        embeddings: Embedding instance for documents.
        query_embeddings: Embedding instance for search queries.

    Example:
        >>> service = EmbeddingService()
        >>> vector = service.embed_query("What is ROS2?")
        >>> len(vector)
        768
    """

    def __init__(self) -> None:
        """Initialize the embedding service with Google Gemini embeddings.

        Creates two embedding instances with appropriate task types:
        - retrieval_document: For embedding documents to be indexed
        - retrieval_query: For embedding search queries

        Raises:
            ValueError: If GOOGLE_API_KEY is not configured or invalid.
        """
        settings = get_settings()

        logger.info(
            "Initializing embedding service",
            extra={
                "model": settings.embedding_model,
                "dimensions": settings.embedding_dimensions,
            },
        )

        # Document embeddings with retrieval_document task type
        # This optimizes embeddings for indexed content
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
            task_type="retrieval_document",
        )

        # Query embeddings with retrieval_query task type
        # This optimizes embeddings for search queries
        self.query_embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
            task_type="retrieval_query",
        )

        self._dimensions = settings.embedding_dimensions

        logger.info("Embedding service initialized successfully")

    @property
    def dimensions(self) -> int:
        """Return the embedding vector dimensions.

        Returns:
            The number of dimensions in the embedding vectors (768 for text-embedding-004).
        """
        return self._dimensions

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        retry=retry_if_exception_type((Exception,)),
        before_sleep=lambda retry_state: logger.warning(
            "Retrying embed_query after error",
            extra={
                "attempt": retry_state.attempt_number,
                "wait_seconds": retry_state.next_action.sleep if retry_state.next_action else 0,
            },
        ),
    )
    def embed_query(self, text: str) -> list[float]:
        """Embed a single query text.

        Uses the query-optimized embedding model with task_type="retrieval_query"
        for optimal search performance.

        Args:
            text: The query text to embed.

        Returns:
            A list of floats representing the 768-dimensional embedding vector.

        Raises:
            ValueError: If text is empty or None.
            Exception: If embedding fails after all retry attempts.

        Example:
            >>> service = get_embedding_service()
            >>> vector = service.embed_query("What is inverse kinematics?")
            >>> len(vector)
            768
        """
        if not text or not text.strip():
            raise ValueError("Query text cannot be empty")

        logger.debug(
            "Embedding query",
            extra={"text_length": len(text)},
        )

        vector = self.query_embeddings.embed_query(text)

        logger.debug(
            "Query embedded successfully",
            extra={"vector_dimensions": len(vector)},
        )

        return vector

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        retry=retry_if_exception_type((Exception,)),
        before_sleep=lambda retry_state: logger.warning(
            "Retrying embed_documents after error",
            extra={
                "attempt": retry_state.attempt_number,
                "wait_seconds": retry_state.next_action.sleep if retry_state.next_action else 0,
            },
        ),
    )
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple document texts.

        Uses the document-optimized embedding model with task_type="retrieval_document"
        for optimal indexing. Handles batching internally through the LangChain
        integration.

        Args:
            texts: A list of document texts to embed.

        Returns:
            A list of embedding vectors, one for each input text.
            Each vector is a list of 768 floats.

        Raises:
            ValueError: If texts is empty or contains empty strings.
            Exception: If embedding fails after all retry attempts.

        Example:
            >>> service = get_embedding_service()
            >>> vectors = service.embed_documents([
            ...     "Inverse kinematics is the mathematical process...",
            ...     "Forward kinematics computes the position..."
            ... ])
            >>> len(vectors)
            2
            >>> len(vectors[0])
            768
        """
        if not texts:
            raise ValueError("Document texts list cannot be empty")

        # Filter out empty texts and warn
        non_empty_texts = [t for t in texts if t and t.strip()]
        if len(non_empty_texts) < len(texts):
            logger.warning(
                "Some empty texts were filtered out",
                extra={
                    "original_count": len(texts),
                    "filtered_count": len(non_empty_texts),
                },
            )

        if not non_empty_texts:
            raise ValueError("All document texts are empty")

        logger.info(
            "Embedding documents",
            extra={
                "document_count": len(non_empty_texts),
                "total_chars": sum(len(t) for t in non_empty_texts),
            },
        )

        vectors = self.embeddings.embed_documents(non_empty_texts)

        logger.info(
            "Documents embedded successfully",
            extra={
                "document_count": len(vectors),
                "vector_dimensions": len(vectors[0]) if vectors else 0,
            },
        )

        return vectors

    def embed_texts_batched(
        self,
        texts: list[str],
        batch_size: int = 100,
    ) -> list[list[float]]:
        """Embed multiple texts with explicit batching.

        Useful for large document sets where you want explicit control over
        batch sizes to manage memory and API rate limits.

        Args:
            texts: A list of document texts to embed.
            batch_size: Maximum number of texts per batch (default: 100).

        Returns:
            A list of embedding vectors, one for each input text.

        Raises:
            ValueError: If texts is empty or batch_size < 1.

        Example:
            >>> service = get_embedding_service()
            >>> vectors = service.embed_texts_batched(
            ...     ["text1", "text2", ..., "text500"],
            ...     batch_size=100
            ... )
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")
        if batch_size < 1:
            raise ValueError("Batch size must be at least 1")

        logger.info(
            "Starting batched embedding",
            extra={
                "total_texts": len(texts),
                "batch_size": batch_size,
                "num_batches": (len(texts) + batch_size - 1) // batch_size,
            },
        )

        all_vectors: list[list[float]] = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_num = i // batch_size + 1

            logger.debug(
                "Processing batch",
                extra={
                    "batch_number": batch_num,
                    "batch_size": len(batch),
                },
            )

            batch_vectors = self.embed_documents(batch)
            all_vectors.extend(batch_vectors)

        logger.info(
            "Batched embedding complete",
            extra={"total_vectors": len(all_vectors)},
        )

        return all_vectors


# Singleton instance for efficient reuse
_embedding_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    """Get or create the embedding service singleton.

    Returns a cached instance of the EmbeddingService to avoid
    redundant initialization and API configuration overhead.

    Returns:
        The singleton EmbeddingService instance.

    Raises:
        ValueError: If required configuration is missing.

    Example:
        >>> service = get_embedding_service()
        >>> vector = service.embed_query("test query")
    """
    global _embedding_service
    if _embedding_service is None:
        logger.info("Creating new embedding service singleton")
        _embedding_service = EmbeddingService()
    return _embedding_service


def reset_embedding_service() -> None:
    """Reset the embedding service singleton.

    Useful for testing or when configuration changes require
    re-initialization of the service.
    """
    global _embedding_service
    if _embedding_service is not None:
        logger.info("Resetting embedding service singleton")
        _embedding_service = None


# Export public API
__all__ = [
    "EmbeddingService",
    "get_embedding_service",
    "reset_embedding_service",
]
