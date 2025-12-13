"""Embedding service using Google Generative AI.

This package provides embedding functionality via LangChain's
GoogleGenerativeAIEmbeddings for text vectorization.

The service uses Google's text-embedding-004 model (768 dimensions)
with separate task types for queries and documents to optimize
retrieval performance.

Usage:
    from app.services.embedding import get_embedding_service

    service = get_embedding_service()
    query_vector = service.embed_query("What is ROS2?")
    doc_vectors = service.embed_documents(["Document 1...", "Document 2..."])
"""

from app.services.embedding.embedding import (
    EmbeddingService,
    get_embedding_service,
    reset_embedding_service,
)

__all__ = [
    "EmbeddingService",
    "get_embedding_service",
    "reset_embedding_service",
]
