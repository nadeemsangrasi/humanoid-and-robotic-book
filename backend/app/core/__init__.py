"""Core utilities for the RAG Textbook Chatbot backend.

This package contains core functionality:
- security: JWT validation and authentication utilities

Usage:
    from app.core.security import decode_jwt, verify_token, TokenPayload, User
"""

from app.core.security import decode_jwt, verify_token, TokenPayload, User

__all__ = ["decode_jwt", "verify_token", "TokenPayload", "User"]
