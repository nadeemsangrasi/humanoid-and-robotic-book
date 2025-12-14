"""Authentication dependencies for FastAPI endpoints.

This module provides FastAPI dependency functions for authentication:
- get_current_user: Requires authenticated user, raises 401 if not authenticated
- get_optional_user: Returns user if authenticated, None otherwise

These dependencies work with the AuthMiddleware which populates request.state.user
after validating the JWT token.

Usage:
    from fastapi import Depends
    from app.dependencies import get_current_user, get_optional_user
    from app.core.security import User

    # Require authentication
    @router.post("/chat")
    async def chat(current_user: User = Depends(get_current_user)):
        # current_user is guaranteed to be valid
        print(f"Request from user: {current_user.id}")

    # Optional authentication
    @router.get("/info")
    async def info(user: User | None = Depends(get_optional_user)):
        if user:
            print(f"Authenticated user: {user.id}")
        else:
            print("Anonymous request")
"""

from typing import Optional

from fastapi import HTTPException, Request, status

from app.core.security import User
from app.utils.logging import get_logger

logger = get_logger(__name__)


async def get_current_user(request: Request) -> User:
    """Get the current authenticated user from request state.

    This dependency extracts the user from request.state.user, which is
    populated by the AuthMiddleware after validating the JWT token.

    Args:
        request: The incoming FastAPI request.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: 401 Unauthorized if the user is not authenticated.

    Example:
        @router.post("/chat")
        async def chat(current_user: User = Depends(get_current_user)):
            logger.info(f"Chat request from user {current_user.id}")
            # ... process chat request
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
                "message": "Authentication required. Please provide a valid Bearer token.",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_optional_user(request: Request) -> Optional[User]:
    """Get the current user if authenticated, None otherwise.

    This dependency extracts the user from request.state.user without
    raising an error if the user is not authenticated. Useful for
    endpoints that work with or without authentication.

    Args:
        request: The incoming FastAPI request.

    Returns:
        User | None: The authenticated user, or None if not authenticated.

    Example:
        @router.get("/info")
        async def info(user: User | None = Depends(get_optional_user)):
            if user:
                return {"message": f"Hello, {user.name}"}
            return {"message": "Hello, anonymous user"}
    """
    return getattr(request.state, "user", None)


# Export public API
__all__ = ["get_current_user", "get_optional_user", "User"]
