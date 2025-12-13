"""Retrieval service using Qdrant vector database.

This package provides vector search functionality via the Qdrant client
with configurable similarity thresholds and result limits.

Components:
    - QdrantRetriever: Main class for Qdrant operations
    - get_retriever: Factory function for singleton access
    - VECTOR_SIZE: Embedding dimension constant (768 for Gemini)
    - DEFAULT_BATCH_SIZE: Recommended batch size for upserts
"""

from app.services.retrieval.qdrant_client import (
    DEFAULT_BATCH_SIZE,
    VECTOR_SIZE,
    QdrantRetriever,
    get_retriever,
)

__all__ = [
    "QdrantRetriever",
    "get_retriever",
    "VECTOR_SIZE",
    "DEFAULT_BATCH_SIZE",
]
