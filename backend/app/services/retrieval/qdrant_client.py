"""Qdrant vector database client for semantic search.

This module provides the QdrantRetriever class for interacting with Qdrant Cloud
to store and retrieve textbook content embeddings. It supports:
- Collection creation with cosine similarity
- Deterministic UUID generation for idempotent upserts
- Score-threshold filtered semantic search
- Batch upsert operations with configurable batch sizes

Usage:
    from app.services.retrieval.qdrant_client import QdrantRetriever

    retriever = QdrantRetriever()
    results = await retriever.search(query_vector, k=5, threshold=0.7)
"""

import hashlib
import time
import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)

# Gemini text-embedding-004 produces 768-dimensional vectors
VECTOR_SIZE = 768

# Maximum points per upsert batch (Qdrant recommendation)
DEFAULT_BATCH_SIZE = 100


class QdrantRetriever:
    """Handles Qdrant operations for textbook content retrieval.

    This class manages the connection to Qdrant Cloud and provides methods
    for storing and searching textbook content embeddings. It uses cosine
    similarity for vector comparison and supports optional module-based filtering.

    Attributes:
        client: The Qdrant client instance.
        collection_name: Name of the Qdrant collection for book chunks.

    Example:
        >>> retriever = QdrantRetriever()
        >>> # Search for similar content
        >>> results = await retriever.search(query_vector, k=5)
        >>> for result in results:
        ...     print(f"{result['title']}: {result['score']:.2f}")
    """

    def __init__(self) -> None:
        """Initialize the Qdrant client and ensure collection exists.

        Raises:
            ConnectionError: If unable to connect to Qdrant Cloud.
            ValueError: If Qdrant configuration is invalid.
        """
        settings = get_settings()

        logger.info(
            "Initializing Qdrant client",
            extra={"url": settings.qdrant_url, "collection": settings.collection_name},
        )

        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=30,
        )
        self.collection_name = settings.collection_name
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Create the collection if it does not exist.

        Creates a new collection with cosine distance metric and the configured
        vector size (768 dimensions for Gemini text-embedding-004).

        The operation is idempotent - if the collection already exists with
        the correct configuration, no changes are made.
        """
        try:
            if not self.client.collection_exists(self.collection_name):
                logger.info(
                    "Creating Qdrant collection",
                    extra={
                        "collection": self.collection_name,
                        "vector_size": VECTOR_SIZE,
                        "distance": "COSINE",
                    },
                )

                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=VECTOR_SIZE,
                        distance=Distance.COSINE,
                    ),
                )

                logger.info(
                    "Qdrant collection created successfully",
                    extra={"collection": self.collection_name},
                )
            else:
                logger.debug(
                    "Qdrant collection already exists",
                    extra={"collection": self.collection_name},
                )
        except Exception as e:
            logger.error(
                "Failed to ensure Qdrant collection",
                extra={"collection": self.collection_name, "error": str(e)},
            )
            raise

    @staticmethod
    def generate_point_id(url: str, chunk_index: int) -> str:
        """Generate a deterministic UUID from URL and chunk index.

        This ensures idempotent upserts - the same content will always
        produce the same point ID, allowing re-indexing without duplicates.

        Args:
            url: The source URL of the content chunk.
            chunk_index: The index of the chunk within the page.

        Returns:
            A deterministic UUID string derived from the URL and chunk index.

        Example:
            >>> point_id = QdrantRetriever.generate_point_id(
            ...     "https://example.com/page", 0
            ... )
            >>> print(point_id)
            '550e8400-e29b-41d4-a716-446655440000'
        """
        content = f"{url}::{chunk_index}"
        hash_bytes = hashlib.md5(content.encode()).digest()
        return str(uuid.UUID(bytes=hash_bytes))

    async def search(
        self,
        query_vector: list[float],
        k: int = 5,
        threshold: float = 0.7,
        module_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search for similar content chunks using vector similarity.

        Performs a cosine similarity search against the stored embeddings,
        returning results that meet the score threshold. Optionally filters
        results by module name.

        Args:
            query_vector: The query embedding vector (768 dimensions).
            k: Maximum number of results to return. Defaults to 5.
            threshold: Minimum similarity score (0.0 to 1.0). Defaults to 0.7.
            module_filter: Optional module name to filter results.

        Returns:
            A list of dictionaries containing:
                - content: The text content of the chunk
                - url: Source URL for citation
                - title: Page/section title
                - score: Similarity score (0.0 to 1.0)
                - heading: Section heading (if available)
                - module: Module name (if available)
                - chapter: Chapter identifier (if available)

        Example:
            >>> results = await retriever.search(
            ...     query_vector=embedding,
            ...     k=5,
            ...     threshold=0.7,
            ...     module_filter="module-1"
            ... )
            >>> for r in results:
            ...     print(f"[{r['score']:.2f}] {r['title']}: {r['url']}")
        """
        # Build optional filter for module-based search
        query_filter = None
        if module_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="module",
                        match=MatchValue(value=module_filter),
                    )
                ]
            )
            logger.debug(
                "Applying module filter to search",
                extra={"module": module_filter},
            )

        try:
            logger.debug(
                "Executing Qdrant search",
                extra={
                    "collection": self.collection_name,
                    "k": k,
                    "threshold": threshold,
                    "has_filter": query_filter is not None,
                },
            )

            # Execute the search with score threshold
            # Note: QdrantClient.search is synchronous, but we wrap it for
            # consistency with the async interface used elsewhere in the app
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=k,
                score_threshold=threshold,
                query_filter=query_filter,
                with_payload=True,
            )

            logger.info(
                "Qdrant search completed",
                extra={
                    "results_count": len(results),
                    "k": k,
                    "threshold": threshold,
                },
            )

            # Transform results to standardized format with all available metadata
            return [
                {
                    "content": hit.payload.get("content", ""),
                    "url": hit.payload.get("url", ""),
                    "title": hit.payload.get("title", ""),
                    "score": hit.score,
                    "heading": hit.payload.get("heading", ""),
                    "module": hit.payload.get("module", ""),
                    "chapter": hit.payload.get("chapter", ""),
                    "chunk_index": hit.payload.get("chunk_index", 0),
                }
                for hit in results
            ]

        except Exception as e:
            logger.error(
                "Qdrant search failed",
                extra={"error": str(e), "collection": self.collection_name},
            )
            raise

    def upsert_points(
        self,
        points: list[PointStruct],
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> int:
        """Insert or update points in the collection with batching.

        Handles large uploads by splitting into batches to avoid timeout
        issues and stay within Qdrant's recommended limits.

        Args:
            points: List of PointStruct objects to upsert.
            batch_size: Number of points per batch. Defaults to 100.

        Returns:
            Total number of points successfully upserted.

        Raises:
            Exception: If any batch fails to upsert.

        Example:
            >>> points = [
            ...     PointStruct(
            ...         id=QdrantRetriever.generate_point_id(url, 0),
            ...         vector=embedding,
            ...         payload={"content": "...", "url": url, "title": "..."}
            ...     )
            ...     for url, embedding in data
            ... ]
            >>> count = retriever.upsert_points(points)
            >>> print(f"Upserted {count} points")
        """
        if not points:
            logger.warning("No points to upsert")
            return 0

        total_points = len(points)
        total_batches = (total_points + batch_size - 1) // batch_size
        upserted_count = 0

        logger.info(
            "Starting batch upsert",
            extra={
                "total_points": total_points,
                "batch_size": batch_size,
                "total_batches": total_batches,
                "collection": self.collection_name,
            },
        )

        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, total_points)
            batch = points[start_idx:end_idx]

            try:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch,
                    wait=True,  # Wait for operation to complete
                )
                upserted_count += len(batch)

                logger.debug(
                    "Batch upsert completed",
                    extra={
                        "batch": batch_num + 1,
                        "total_batches": total_batches,
                        "batch_size": len(batch),
                        "upserted_so_far": upserted_count,
                    },
                )

            except Exception as e:
                logger.error(
                    "Batch upsert failed",
                    extra={
                        "batch": batch_num + 1,
                        "total_batches": total_batches,
                        "error": str(e),
                    },
                )
                raise

        logger.info(
            "Batch upsert completed successfully",
            extra={
                "total_upserted": upserted_count,
                "collection": self.collection_name,
            },
        )

        return upserted_count

    def health_check(self) -> tuple[bool, int | None]:
        """Check Qdrant connection health and measure latency.

        Performs a simple operation to verify the Qdrant connection is
        working and measures the round-trip time.

        Returns:
            A tuple of (is_healthy, latency_ms):
                - is_healthy: True if connection is working
                - latency_ms: Round-trip time in milliseconds, or None if unhealthy

        Example:
            >>> healthy, latency = retriever.health_check()
            >>> if healthy:
            ...     print(f"Qdrant healthy, latency: {latency}ms")
            ... else:
            ...     print("Qdrant connection failed")
        """
        try:
            start_time = time.time()

            # Simple operation to verify connection
            self.client.get_collections()

            latency_ms = int((time.time() - start_time) * 1000)

            logger.debug(
                "Qdrant health check passed",
                extra={"latency_ms": latency_ms},
            )

            return True, latency_ms

        except Exception as e:
            logger.error(
                "Qdrant health check failed",
                extra={"error": str(e)},
            )
            return False, None

    def get_collection_info(self) -> dict[str, Any]:
        """Get information about the current collection.

        Returns:
            Dictionary containing collection statistics:
                - name: Collection name
                - vectors_count: Number of vectors stored
                - points_count: Number of points stored
                - status: Collection status (green/yellow/red)

        Example:
            >>> info = retriever.get_collection_info()
            >>> print(f"Collection has {info['points_count']} points")
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)

            return {
                "name": self.collection_name,
                "vectors_count": collection_info.vectors_count,
                "points_count": collection_info.points_count,
                "status": collection_info.status.value,
            }

        except Exception as e:
            logger.error(
                "Failed to get collection info",
                extra={"collection": self.collection_name, "error": str(e)},
            )
            raise

    def delete_collection(self) -> bool:
        """Delete the current collection.

        WARNING: This operation is irreversible and will delete all stored vectors.

        Returns:
            True if deletion was successful, False otherwise.
        """
        try:
            logger.warning(
                "Deleting Qdrant collection",
                extra={"collection": self.collection_name},
            )

            self.client.delete_collection(self.collection_name)

            logger.info(
                "Qdrant collection deleted successfully",
                extra={"collection": self.collection_name},
            )

            return True

        except Exception as e:
            logger.error(
                "Failed to delete collection",
                extra={"collection": self.collection_name, "error": str(e)},
            )
            return False


# Module-level singleton for convenient access
_retriever_instance: QdrantRetriever | None = None


def get_retriever() -> QdrantRetriever:
    """Get the singleton QdrantRetriever instance.

    Creates a new instance on first call, then returns the cached instance
    on subsequent calls. This ensures a single connection is shared across
    the application.

    Returns:
        The singleton QdrantRetriever instance.

    Example:
        >>> from app.services.retrieval.qdrant_client import get_retriever
        >>> retriever = get_retriever()
        >>> results = await retriever.search(query_vector)
    """
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = QdrantRetriever()
    return _retriever_instance


# Export public API
__all__ = [
    "QdrantRetriever",
    "get_retriever",
    "VECTOR_SIZE",
    "DEFAULT_BATCH_SIZE",
]
