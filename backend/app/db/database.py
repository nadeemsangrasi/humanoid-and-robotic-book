"""Database connection and user verification for Neon PostgreSQL.

This module provides async database operations for user verification.
Uses asyncpg for async PostgreSQL connections.
"""

from typing import Optional
from functools import lru_cache

import asyncpg
from pydantic import BaseModel

from app.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)


class User(BaseModel):
    """User model from database."""

    id: str
    name: str
    email: str
    email_verified: bool
    image: Optional[str] = None


class DatabasePool:
    """Singleton database connection pool."""

    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def get_pool(cls) -> asyncpg.Pool:
        """Get or create the database connection pool."""
        if cls._pool is None:
            settings = get_settings()
            logger.info("Creating database connection pool")
            cls._pool = await asyncpg.create_pool(
                settings.database_url,
                min_size=1,
                max_size=10,
                command_timeout=30,
            )
            logger.info("Database connection pool created")
        return cls._pool

    @classmethod
    async def close_pool(cls) -> None:
        """Close the database connection pool."""
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None
            logger.info("Database connection pool closed")


async def get_db() -> asyncpg.Pool:
    """Get database connection pool."""
    return await DatabasePool.get_pool()


async def get_user_by_email(email: str) -> Optional[User]:
    """
    Get user from database by email.

    Args:
        email: The user's email address.

    Returns:
        User if found, None otherwise.
    """
    try:
        pool = await get_db()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, name, email, email_verified, image
                FROM "user"
                WHERE email = $1
                """,
                email,
            )

            if row is None:
                logger.debug(f"User not found for email: {email}")
                return None

            return User(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                email_verified=row["email_verified"],
                image=row["image"],
            )

    except Exception as e:
        logger.error(f"Database error getting user by email: {e}")
        return None


async def close_db() -> None:
    """Close database connections. Call on app shutdown."""
    await DatabasePool.close_pool()
