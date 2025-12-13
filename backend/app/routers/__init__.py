"""API routers for the RAG chatbot backend.

This package contains FastAPI routers for:
- chat: POST /chat endpoint for RAG-based Q&A
- health: GET /health endpoint for service health checks

Usage:
    from app.routers import chat_router, health_router

    app.include_router(chat_router, prefix="/api/v1")
    app.include_router(health_router)  # No prefix, mounted at root
"""

from app.routers.chat import router as chat_router
from app.routers.health import router as health_router

__all__ = ["chat_router", "health_router"]
