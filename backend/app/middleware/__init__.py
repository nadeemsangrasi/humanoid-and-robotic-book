"""Middleware components for the RAG Textbook Chatbot backend.

This package contains FastAPI middleware:
- auth: Authentication middleware for JWT validation

Usage:
    from app.middleware import AuthMiddleware

    app.add_middleware(AuthMiddleware)
"""

from app.middleware.auth import AuthMiddleware

__all__ = ["AuthMiddleware"]
