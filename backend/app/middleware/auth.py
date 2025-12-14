"""Authentication middleware for JWT token validation.

This middleware extracts and validates JWT tokens from the Authorization header
for protected routes. It integrates with Better Auth tokens from the frontend.

Features:
- Extracts Bearer tokens from Authorization header
- Validates JWT tokens using BETTER_AUTH_SECRET
- Attaches user info to request.state for downstream use
- Skips authentication for health check endpoints
- Logs authentication failures without exposing sensitive data

Public endpoints (no auth required):
- /health
- /api/v1/health
- /docs
- /redoc
- /openapi.json
- / (root)

Usage:
    from app.middleware import AuthMiddleware

    app.add_middleware(AuthMiddleware)
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.security import User, verify_token
from app.utils.logging import get_logger

logger = get_logger(__name__)

# Paths that do not require authentication
PUBLIC_PATHS = frozenset([
    "/",
    "/health",
    "/api/v1/health",
    "/docs",
    "/redoc",
    "/openapi.json",
])

# Path prefixes that do not require authentication
PUBLIC_PATH_PREFIXES = (
    "/docs",
    "/redoc",
)


def get_client_ip(request: Request) -> str:
    """Extract client IP address from request.

    Handles X-Forwarded-For header for proxied requests.

    Args:
        request: The incoming FastAPI request.

    Returns:
        str: Client IP address or "unknown" if not available.
    """
    # Check X-Forwarded-For header (common when behind a proxy/load balancer)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take the first IP in the chain (original client)
        return forwarded_for.split(",")[0].strip()

    # Fall back to direct client
    if request.client and request.client.host:
        return request.client.host

    return "unknown"


def is_public_path(path: str) -> bool:
    """Check if a path is public (no authentication required).

    Args:
        path: The request path to check.

    Returns:
        bool: True if the path is public, False otherwise.
    """
    # Check exact matches
    if path in PUBLIC_PATHS:
        return True

    # Check prefixes
    for prefix in PUBLIC_PATH_PREFIXES:
        if path.startswith(prefix):
            return True

    return False


def log_auth_failure(
    request: Request,
    reason: str,
    detail: Optional[str] = None,
) -> None:
    """Log authentication failure without exposing sensitive data.

    Logs include:
    - Timestamp (via logger)
    - Client IP
    - Request path
    - Failure reason
    - HTTP method

    IMPORTANT: This function NEVER logs token values or secrets.

    Args:
        request: The incoming FastAPI request.
        reason: Brief description of why authentication failed.
        detail: Optional additional detail (must not contain sensitive data).
    """
    client_ip = get_client_ip(request)
    timestamp = datetime.now(timezone.utc).isoformat()

    log_extra = {
        "client_ip": client_ip,
        "path": request.url.path,
        "method": request.method,
        "timestamp": timestamp,
        "auth_failure_reason": reason,
    }

    if detail:
        log_extra["detail"] = detail

    logger.warning(
        f"Authentication failed: {reason}",
        extra=log_extra,
    )


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for JWT authentication.

    This middleware:
    1. Skips authentication for public endpoints
    2. Extracts Bearer token from Authorization header
    3. Validates the JWT token
    4. Attaches user info to request.state.user if valid
    5. Logs authentication failures for monitoring

    The middleware does NOT return 401 errors directly - it only populates
    request.state.user. The actual authentication enforcement is done by
    the get_current_user dependency in protected endpoints.

    This design allows for:
    - Optional authentication on some endpoints
    - Consistent error handling in endpoint dependencies
    - Cleaner separation of concerns

    Example:
        # In main.py
        from app.middleware import AuthMiddleware
        app.add_middleware(AuthMiddleware)

        # In endpoint
        from app.dependencies.auth import get_current_user
        @router.post("/chat")
        async def chat(current_user: User = Depends(get_current_user)):
            # current_user is guaranteed to be valid here
            pass
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process the request and validate authentication.

        Args:
            request: The incoming FastAPI request.
            call_next: The next middleware or route handler.

        Returns:
            Response: The response from the route handler.
        """
        # Skip authentication for public paths
        if is_public_path(request.url.path):
            return await call_next(request)

        # Initialize user as None (not authenticated)
        request.state.user = None

        # Extract Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            log_auth_failure(
                request,
                reason="missing_authorization_header",
                detail="No Authorization header provided",
            )
            return await call_next(request)

        # Validate Bearer token format
        if not auth_header.startswith("Bearer "):
            log_auth_failure(
                request,
                reason="invalid_auth_format",
                detail="Authorization header does not start with 'Bearer '",
            )
            return await call_next(request)

        # Extract token (everything after "Bearer ")
        token = auth_header[7:]  # len("Bearer ") = 7

        if not token:
            log_auth_failure(
                request,
                reason="empty_token",
                detail="Bearer token is empty",
            )
            return await call_next(request)

        # Validate the token
        payload = verify_token(token)

        if payload is None:
            log_auth_failure(
                request,
                reason="invalid_token",
                detail="Token validation failed",
            )
            return await call_next(request)

        # Token is valid - create User and attach to request state
        request.state.user = User(
            id=payload.sub,
            email=payload.email,
            name=payload.name,
        )

        logger.debug(
            "User authenticated successfully",
            extra={
                "user_id": payload.sub,
                "path": request.url.path,
            },
        )

        return await call_next(request)


# Export public API
__all__ = ["AuthMiddleware", "is_public_path", "log_auth_failure"]
