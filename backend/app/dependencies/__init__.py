"""FastAPI dependencies for the RAG Textbook Chatbot backend.

This package contains reusable FastAPI dependencies:
- auth: Authentication dependencies for protected endpoints

Usage:
    from app.dependencies import get_current_user

    @router.post("/chat")
    async def chat(current_user: User = Depends(get_current_user)):
        pass
"""

from app.dependencies.auth import get_current_user, get_optional_user

__all__ = ["get_current_user", "get_optional_user"]
