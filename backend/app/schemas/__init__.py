"""Pydantic schemas for API request/response models.

This package contains schema definitions for the RAG chatbot backend:
- chat: Request/response models for the /chat endpoint
- health: Health check response models for the /health endpoint
"""

from .chat import (
    ChatRequest,
    ChatResponse,
    Citation,
    ErrorResponse,
    ResponseMetadata,
)
from .health import HealthStatus, ServiceStatus

__all__ = [
    # Chat schemas
    "ChatRequest",
    "ChatResponse",
    "Citation",
    "ResponseMetadata",
    "ErrorResponse",
    # Health schemas
    "HealthStatus",
    "ServiceStatus",
]
