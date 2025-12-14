"""FastAPI application entry point for RAG Textbook Chatbot.

This module creates and configures the FastAPI application with:
- CORS middleware for cross-origin requests
- Lifespan context manager for startup/shutdown events
- Router registration for API endpoints
- OpenAPI documentation configuration

The application serves as the backend for the Physical AI & Humanoid Robotics
textbook chatbot, providing RAG-powered Q&A capabilities.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings, validate_settings, ConfigurationError, print_settings_summary
from app.middleware import AuthMiddleware
from app.routers import chat_router, health_router
from app.utils.logging import setup_logging, get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup/shutdown events.

    Startup:
        - Configures structured logging
        - Logs application startup with configuration details

    Shutdown:
        - Logs application shutdown
        - Cleanup resources if needed

    Args:
        app: The FastAPI application instance.

    Yields:
        None: Control returns to the application during its lifecycle.
    """
    # -------------------------------------------------------------------------
    # Startup
    # -------------------------------------------------------------------------
    setup_logging()

    # Validate all environment variables on startup
    try:
        settings = validate_settings()
    except ConfigurationError as e:
        logger.critical(
            "Application startup failed due to configuration errors",
            extra={"error": str(e)},
        )
        print(f"\n{'='*60}")
        print("CONFIGURATION ERROR - Application cannot start")
        print("=" * 60)
        print(str(e))
        print("=" * 60)
        print("\nPlease fix the configuration errors and restart the application.")
        print("See backend/README.md for environment variable documentation.\n")
        raise SystemExit(1) from e

    # Print configuration summary (with masked secrets) for debugging
    if settings.log_level == "DEBUG":
        print_settings_summary(settings)

    logger.info(
        "Starting RAG Textbook Chatbot API",
        extra={
            "model": settings.llm_model,
            "host": settings.host,
            "port": settings.port,
            "collection": settings.collection_name,
        },
    )

    yield

    # -------------------------------------------------------------------------
    # Shutdown
    # -------------------------------------------------------------------------
    logger.info("Shutting down RAG Textbook Chatbot API")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    This factory function creates a new FastAPI application instance with:
    - OpenAPI metadata (title, description, version)
    - Lifespan context manager for startup/shutdown
    - CORS middleware configuration
    - Router registration

    Returns:
        FastAPI: Configured application instance ready to serve requests.

    Example:
        >>> app = create_app()
        >>> # Run with uvicorn
        >>> # uvicorn app.main:app --host 0.0.0.0 --port 7860
    """
    settings = get_settings()

    app = FastAPI(
        title="Physical AI Textbook Chatbot API",
        description=(
            "RAG-powered Q&A API for the Physical AI & Humanoid Robotics textbook. "
            "This API enables natural language queries about the textbook content, "
            "providing accurate answers with source citations from the book."
        ),
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # -------------------------------------------------------------------------
    # CORS Middleware
    # -------------------------------------------------------------------------
    # Configure Cross-Origin Resource Sharing for frontend access.
    # In production, restrict allow_origins to specific frontend domains.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Restrict in production to specific origins
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # -------------------------------------------------------------------------
    # Authentication Middleware
    # -------------------------------------------------------------------------
    # Validates JWT tokens from Better Auth and populates request.state.user.
    # Note: Middleware order matters - AuthMiddleware runs after CORS
    # so that preflight OPTIONS requests are handled correctly.
    app.add_middleware(AuthMiddleware)

    # -------------------------------------------------------------------------
    # Router Registration
    # -------------------------------------------------------------------------
    # Register the chat router under /api/v1 prefix
    app.include_router(chat_router, prefix="/api/v1")

    # Register the health router at root level (no prefix)
    app.include_router(health_router)

    # -------------------------------------------------------------------------
    # Root Endpoint
    # -------------------------------------------------------------------------
    @app.get(
        "/",
        summary="API Root",
        description="Returns API information and links to documentation.",
        tags=["Info"],
    )
    async def root() -> dict:
        """Root endpoint providing API information.

        Returns:
            dict: API information with links to documentation and health endpoint.
        """
        return {
            "name": "Physical AI Textbook Chatbot API",
            "version": "1.0.0",
            "description": "RAG-powered Q&A for the Physical AI & Humanoid Robotics textbook",
            "documentation": {
                "swagger": "/docs",
                "redoc": "/redoc",
                "openapi": "/openapi.json",
            },
            "endpoints": {
                "health": "/health",
                "chat": "/api/v1/chat",
            },
        }

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower(),
    )
