"""Authentication dependencies for FastAPI endpoints.

This module provides FastAPI dependency functions for authentication:
- get_current_user: Requires authenticated user, raises 401 if not authenticated
- get_optional_user: Returns user if authenticated, None otherwise

These dependencies work with the AuthMiddleware which populates request.state.user
after verifying the user email against the database.
"""

from typing import Optional

from fastapi import HTTPException, Request, status

from app.db import User
from app.utils.logging import get_logger

logger = get_logger(__name__)


async def get_current_user(request: Request) -> User:
    """Get the current authenticated user from request state.

    Args:
        request: The incoming FastAPI request.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: 401 Unauthorized if the user is not authenticated.
    """
    user: Optional[User] = getattr(request.state, "user", None)

    if user is None:
        logger.debug(
            "Authentication required but no user in request state",
            extra={"path": request.url.path, "method": request.method},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "unauthorized",
                "message": "Authentication required. Please log in.",
            },
        )

    return user


async def get_optional_user(request: Request) -> Optional[User]:
    """Get the current user if authenticated, None otherwise.

    Args:
        request: The incoming FastAPI request.

    Returns:
        User | None: The authenticated user, or None if not authenticated.
    """
    return getattr(request.state, "user", None)


# Export public API
__all__ = ["get_current_user", "get_optional_user", "User"]
