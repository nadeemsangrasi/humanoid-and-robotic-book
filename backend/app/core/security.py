"""JWT validation utilities for Better Auth integration.

This module provides functions to decode and validate JWT tokens issued by
Better Auth on the frontend. It handles:
- Token decoding using PyJWT
- Signature verification using BETTER_AUTH_SECRET
- Expiration validation with clock skew tolerance
- Malformed token handling

The JWT tokens from Better Auth contain:
- sub: user ID
- email: user email address
- name: user display name
- iat: issued at timestamp
- exp: expiration timestamp

Usage:
    from app.core.security import verify_token, User

    payload = verify_token(token)
    if payload:
        user = User(id=payload.sub, email=payload.email, name=payload.name)
"""

from datetime import datetime, timezone
from typing import Optional

import jwt
from pydantic import BaseModel

from app.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)

# Clock skew tolerance in seconds (60 seconds to handle minor time differences)
CLOCK_SKEW_LEEWAY = 60


class TokenPayload(BaseModel):
    """Validated JWT token payload from Better Auth.

    Attributes:
        sub: User ID (subject claim).
        email: User email address (optional).
        name: User display name (optional).
        exp: Token expiration timestamp.
        iat: Token issued-at timestamp.
    """

    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    exp: int
    iat: int


class User(BaseModel):
    """Authenticated user model.

    This model represents an authenticated user extracted from a valid JWT token.

    Attributes:
        id: Unique user identifier.
        email: User email address (optional).
        name: User display name (optional).
    """

    id: str
    email: Optional[str] = None
    name: Optional[str] = None


def decode_jwt(token: str) -> Optional[dict]:
    """Decode and validate a JWT token.

    Decodes the token using the BETTER_AUTH_SECRET from configuration.
    Validates the signature and expiration with clock skew tolerance.

    Args:
        token: The JWT token string to decode.

    Returns:
        dict: The decoded token payload if valid, None otherwise.

    Note:
        This function does NOT log the token value for security.
        Only logs non-sensitive information like error types.

    Example:
        >>> payload = decode_jwt("eyJhbGciOiJIUzI1NiIs...")
        >>> if payload:
        ...     print(f"User ID: {payload['sub']}")
    """
    settings = get_settings()

    try:
        # Decode and verify the token
        # PyJWT automatically validates exp claim with leeway
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
                "require": ["sub", "exp", "iat"],
            },
            leeway=CLOCK_SKEW_LEEWAY,
        )
        return payload

    except jwt.ExpiredSignatureError:
        logger.warning(
            "JWT token expired",
            extra={"error_type": "expired_signature"},
        )
        return None

    except jwt.InvalidSignatureError:
        logger.warning(
            "JWT signature validation failed",
            extra={"error_type": "invalid_signature"},
        )
        return None

    except jwt.DecodeError:
        logger.warning(
            "JWT decode error - malformed token",
            extra={"error_type": "decode_error"},
        )
        return None

    except jwt.InvalidTokenError as e:
        logger.warning(
            "JWT validation failed",
            extra={"error_type": "invalid_token", "detail": str(e)},
        )
        return None

    except Exception as e:
        # Catch any unexpected errors without exposing sensitive data
        logger.error(
            "Unexpected error during JWT validation",
            extra={"error_type": type(e).__name__},
        )
        return None


def verify_token(token: str) -> Optional[TokenPayload]:
    """Verify a JWT token and return the validated payload.

    This is the primary function for token verification. It decodes the token
    and returns a structured TokenPayload object if valid.

    Args:
        token: The JWT token string to verify.

    Returns:
        TokenPayload: Validated token payload if the token is valid.
        None: If the token is invalid, expired, or malformed.

    Example:
        >>> payload = verify_token(auth_header.split(" ")[1])
        >>> if payload:
        ...     user = User(id=payload.sub, email=payload.email)
        ...     print(f"Authenticated user: {user.id}")
    """
    payload = decode_jwt(token)

    if payload is None:
        return None

    try:
        # Validate required fields and create TokenPayload
        return TokenPayload(
            sub=payload.get("sub"),
            email=payload.get("email"),
            name=payload.get("name"),
            exp=payload.get("exp"),
            iat=payload.get("iat"),
        )
    except Exception as e:
        logger.warning(
            "Failed to parse token payload",
            extra={"error_type": type(e).__name__},
        )
        return None


def is_token_expired(payload: TokenPayload) -> bool:
    """Check if a token payload has expired.

    Utility function to check token expiration without re-decoding.
    Includes clock skew tolerance.

    Args:
        payload: The TokenPayload to check.

    Returns:
        bool: True if the token is expired, False otherwise.

    Example:
        >>> payload = verify_token(token)
        >>> if payload and not is_token_expired(payload):
        ...     # Token is valid and not expired
        ...     pass
    """
    current_time = datetime.now(timezone.utc).timestamp()
    return payload.exp < (current_time - CLOCK_SKEW_LEEWAY)


# Export public API
__all__ = [
    "TokenPayload",
    "User",
    "decode_jwt",
    "verify_token",
    "is_token_expired",
    "CLOCK_SKEW_LEEWAY",
]
