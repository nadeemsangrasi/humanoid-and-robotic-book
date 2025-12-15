"""Authentication middleware for user verification.

This middleware extracts user email from X-User-Email header and verifies
the user exists in the Neon PostgreSQL database.

Features:
- Extracts X-User-Email header from frontend proxy requests
- Verifies user exists in database
- Attaches user info to request.state for downstream use
- Skips authentication for health check endpoints

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
from starlette.responses import JSONResponse, Response

from app.db import get_user_by_email, User
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
    """Extract client IP address from request."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def is_public_path(path: str) -> bool:
    """Check if a path is public (no authentication required)."""
    if path in PUBLIC_PATHS:
        return True
    for prefix in PUBLIC_PATH_PREFIXES:
        if path.startswith(prefix):
            return True
    return False


def log_auth_failure(request: Request, reason: str, detail: Optional[str] = None) -> None:
    """Log authentication failure."""
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

    logger.warning(f"Authentication failed: {reason}", extra=log_extra)


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for user authentication via email verification.

    This middleware:
    1. Skips authentication for public endpoints
    2. Extracts X-User-Email header from frontend proxy
    3. Verifies user exists in Neon PostgreSQL database
    4. Attaches user info to request.state.user if valid
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process the request and validate authentication."""
        # Step 1: Log incoming request
        logger.info(
            "[AUTH STEP 1] Incoming request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client_ip": get_client_ip(request),
            },
        )

        # Step 2: Check if path is public
        if is_public_path(request.url.path):
            logger.info(
                "[AUTH STEP 2] Public path - skipping authentication",
                extra={"path": request.url.path},
            )
            return await call_next(request)

        logger.info(
            "[AUTH STEP 2] Protected path - proceeding with authentication",
            extra={"path": request.url.path},
        )

        # Step 3: Initialize user as None (not authenticated)
        request.state.user = None
        logger.info("[AUTH STEP 3] Initialized request.state.user = None")

        # Step 4: Extract X-User-Email header from frontend proxy
        user_email = request.headers.get("X-User-Email")
        logger.info(
            "[AUTH STEP 4] Extracting X-User-Email header",
            extra={
                "header_present": user_email is not None,
                "email": user_email if user_email else "NOT PROVIDED",
            },
        )

        if not user_email:
            log_auth_failure(
                request,
                reason="missing_email_header",
                detail="No X-User-Email header provided",
            )
            logger.info(
                "[AUTH STEP 4] FAILED - No email header, returning 401 Unauthorized"
            )
            return JSONResponse(
                status_code=401,
                content={
                    "error": "unauthorized",
                    "message": "Authentication required. Please log in.",
                },
            )

        # Step 5: Verify user exists in database
        logger.info(
            "[AUTH STEP 5] Querying database for user",
            extra={"email": user_email},
        )
        db_user = await get_user_by_email(user_email)

        if db_user is None:
            log_auth_failure(
                request,
                reason="user_not_found",
                detail=f"User with email {user_email} not found in database",
            )
            logger.info(
                "[AUTH STEP 5] FAILED - User not found in database, returning 401 Unauthorized",
                extra={"email": user_email},
            )
            return JSONResponse(
                status_code=401,
                content={
                    "error": "unauthorized",
                    "message": "User not found. Please log in with a valid account.",
                },
            )

        logger.info(
            "[AUTH STEP 5] SUCCESS - User found in database",
            extra={
                "user_id": db_user.id,
                "user_name": db_user.name,
                "user_email": db_user.email,
                "email_verified": db_user.email_verified,
            },
        )

        # Step 6: Attach user to request state
        request.state.user = db_user
        logger.info(
            "[AUTH STEP 6] User attached to request.state",
            extra={"user_id": db_user.id},
        )

        # Step 7: Proceed with request
        logger.info(
            "[AUTH STEP 7] Authentication complete - proceeding with request",
            extra={
                "user_id": db_user.id,
                "user_email": db_user.email,
                "path": request.url.path,
            },
        )

        return await call_next(request)


# Export public API
__all__ = ["AuthMiddleware", "is_public_path", "log_auth_failure"]
