"""
Application configuration using pydantic-settings.

This module provides centralized environment variable management with type validation,
default values, and a singleton pattern for efficient access throughout the application.

Environment variables can be set directly or loaded from a .env file in the backend directory.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Required environment variables:
        - GOOGLE_API_KEY: Google AI API key for Gemini models
        - QDRANT_URL: Qdrant Cloud cluster URL
        - QDRANT_API_KEY: Qdrant Cloud API key
        - BETTER_AUTH_SECRET: Secret key for JWT validation (must match frontend)

    Optional environment variables (with defaults):
        - OPENROUTER_API_KEY: OpenRouter API key (default: None)
        - OPENROUTER_BASE_URL: OpenRouter API base URL (default: https://openrouter.ai/api/v1)
        - LOG_LEVEL: Logging level (default: INFO)
        - COLLECTION_NAME: Qdrant collection name (default: book_chunks)
        - EMBEDDING_MODEL: Google embedding model (default: models/text-embedding-004)
        - LLM_MODEL: Gemini LLM model (default: gemini-2.0-flash)
        - SCORE_THRESHOLD: Similarity score threshold (default: 0.7)
        - HOST: Server host (default: 0.0.0.0)
        - PORT: Server port (default: 7860)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # -------------------------------------------------------------------------
    # Required: API Keys and URLs
    # -------------------------------------------------------------------------

    google_api_key: str = Field(
        ...,
        description="Google AI API key for Gemini models (embedding and LLM inference)",
    )

    qdrant_url: str = Field(
        ...,
        description="Qdrant Cloud cluster URL (e.g., https://xxx.aws.cloud.qdrant.io)",
    )

    qdrant_api_key: str = Field(
        ...,
        description="Qdrant Cloud API key for authentication",
    )

    database_url: str = Field(
        ...,
        description="PostgreSQL database URL (Neon) for user verification",
    )

    # -------------------------------------------------------------------------
    # Optional: OpenRouter Configuration
    # -------------------------------------------------------------------------

    openrouter_api_key: str | None = Field(
        default=None,
        description="OpenRouter API key for accessing various LLM models via OpenRouter",
    )

    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenRouter API base URL",
    )

    # -------------------------------------------------------------------------
    # Optional: Logging Configuration
    # -------------------------------------------------------------------------

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Application logging level",
    )

    # -------------------------------------------------------------------------
    # Optional: Qdrant Collection Configuration
    # -------------------------------------------------------------------------

    collection_name: str = Field(
        default="book_chunks",
        description="Name of the Qdrant collection storing book chunk embeddings",
    )

    # -------------------------------------------------------------------------
    # Optional: Model Configuration
    # -------------------------------------------------------------------------

    embedding_model: str = Field(
        default="models/text-embedding-004",
        description="Google embedding model for vector similarity search",
    )

    llm_model: str = Field(
        default="gemini-2.0-flash",
        description="Google Gemini LLM model for chat responses",
    )

    # -------------------------------------------------------------------------
    # Optional: Retrieval Configuration
    # -------------------------------------------------------------------------

    score_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score threshold for retrieved chunks (0.0 to 1.0)",
    )

    # -------------------------------------------------------------------------
    # Optional: Server Configuration
    # -------------------------------------------------------------------------

    host: str = Field(
        default="0.0.0.0",
        description="Host address for the FastAPI server",
    )

    port: int = Field(
        default=7860,
        ge=1,
        le=65535,
        description="Port for the FastAPI server (7860 for Hugging Face Spaces)",
    )

    # -------------------------------------------------------------------------
    # Validators
    # -------------------------------------------------------------------------

    @field_validator("google_api_key", "qdrant_api_key")
    @classmethod
    def validate_not_placeholder(cls, v: str, info) -> str:
        """Ensure API keys and secrets are not placeholder values."""
        placeholder_patterns = [
            "your_",
            "xxx",
            "placeholder",
            "api_key_here",
            "insert_",
            "secret_here",
        ]
        v_lower = v.lower()
        for pattern in placeholder_patterns:
            if pattern in v_lower:
                raise ValueError(
                    f"{info.field_name} appears to be a placeholder value. "
                    "Please set a valid value in your .env file."
                )
        return v

    @field_validator("qdrant_url")
    @classmethod
    def validate_qdrant_url(cls, v: str) -> str:
        """Ensure Qdrant URL is a valid HTTPS URL."""
        if not v.startswith(("https://", "http://")):
            raise ValueError(
                "qdrant_url must be a valid URL starting with https:// or http://"
            )
        # Remove trailing slash for consistency
        return v.rstrip("/")

    # -------------------------------------------------------------------------
    # Computed Properties
    # -------------------------------------------------------------------------

    @property
    def gemini_base_url(self) -> str:
        """
        Base URL for OpenAI SDK compatibility with Google Gemini.

        This URL enables the OpenAI Agent SDK to communicate with Google's
        Generative Language API using the OpenAI-compatible endpoint.
        """
        return "https://generativelanguage.googleapis.com/v1beta/openai/"

    @property
    def embedding_dimensions(self) -> int:
        """
        Return the embedding dimensions for the configured model.

        Google's text-embedding-004 model produces 768-dimensional vectors.
        """
        # text-embedding-004 produces 768-dimensional vectors
        if "text-embedding-004" in self.embedding_model:
            return 768
        # Default fallback for other models
        return 768


@lru_cache
def get_settings() -> Settings:
    """
    Get the application settings singleton.

    Uses lru_cache to ensure settings are only loaded once from environment
    variables and .env file, providing efficient access throughout the application.

    Returns:
        Settings: The validated application settings instance.

    Raises:
        pydantic.ValidationError: If required environment variables are missing
            or values fail validation.

    Example:
        >>> from app.config import get_settings
        >>> settings = get_settings()
        >>> print(settings.llm_model)
        gemini-2.0-flash
    """
    return Settings()


class ConfigurationError(Exception):
    """Raised when application configuration is invalid."""

    pass


def validate_settings() -> Settings:
    """
    Validate all application settings on startup.

    This function should be called during application startup to ensure all
    required environment variables are properly configured before the application
    begins handling requests.

    Returns:
        Settings: The validated settings instance if all validations pass.

    Raises:
        ConfigurationError: If any required environment variables are missing,
            empty, or fail validation. The error message includes specific
            details about which variables failed and how to fix them.

    Example:
        >>> from app.config import validate_settings
        >>> try:
        ...     settings = validate_settings()
        ...     print("Configuration valid!")
        ... except ConfigurationError as e:
        ...     print(f"Configuration error: {e}")
        ...     sys.exit(1)
    """
    import sys

    errors: list[str] = []

    try:
        settings = get_settings()
    except Exception as e:
        # Parse pydantic validation errors for user-friendly messages
        error_msg = str(e)

        # Check for specific missing required variables
        required_vars = ["GOOGLE_API_KEY", "QDRANT_URL", "QDRANT_API_KEY", "DATABASE_URL"]
        missing_vars = []

        for var in required_vars:
            if var.lower() in error_msg.lower() and "field required" in error_msg.lower():
                missing_vars.append(var)

        if missing_vars:
            errors.append(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
            errors.append(
                "Please set these in your .env file or environment. "
                "See README.md for details on how to obtain these values."
            )
        else:
            errors.append(f"Configuration validation failed: {error_msg}")

        raise ConfigurationError("\n".join(errors)) from e

    # Additional validation: Check that required fields are not empty strings
    if not settings.google_api_key.strip():
        errors.append("GOOGLE_API_KEY is set but empty. Please provide a valid API key.")

    if not settings.qdrant_url.strip():
        errors.append("QDRANT_URL is set but empty. Please provide a valid Qdrant cluster URL.")

    if not settings.qdrant_api_key.strip():
        errors.append("QDRANT_API_KEY is set but empty. Please provide a valid API key.")

    # Validate QDRANT_URL format more strictly
    if settings.qdrant_url:
        url = settings.qdrant_url.lower()
        if not (url.startswith("https://") or url.startswith("http://")):
            errors.append(
                f"QDRANT_URL '{settings.qdrant_url}' is not a valid URL. "
                "It must start with https:// or http://"
            )
        # Check for common placeholder patterns in URL
        placeholder_patterns = ["example.com", "localhost:6333", "your-cluster"]
        for pattern in placeholder_patterns:
            if pattern in url and "cloud.qdrant.io" not in url:
                errors.append(
                    f"QDRANT_URL appears to contain a placeholder value '{pattern}'. "
                    "Please set your actual Qdrant Cloud cluster URL."
                )
                break

    # Validate SCORE_THRESHOLD range (already validated by pydantic, but double-check)
    if not (0.0 <= settings.score_threshold <= 1.0):
        errors.append(
            f"SCORE_THRESHOLD must be between 0.0 and 1.0, got {settings.score_threshold}"
        )

    if errors:
        error_header = "Configuration validation failed with the following errors:"
        error_details = "\n  - ".join([""] + errors)
        raise ConfigurationError(f"{error_header}{error_details}")

    return settings


def print_settings_summary(settings: Settings) -> None:
    """
    Print a summary of the current settings (with sensitive values masked).

    Useful for debugging and verifying configuration on startup.

    Args:
        settings: The validated settings instance to summarize.
    """

    def mask_secret(value: str) -> str:
        """Mask sensitive values, showing only first and last 4 characters."""
        if len(value) <= 8:
            return "***"
        return f"{value[:4]}...{value[-4:]}"

    print("=" * 60)
    print("Application Configuration Summary")
    print("=" * 60)
    print(f"  GOOGLE_API_KEY:     {mask_secret(settings.google_api_key)}")
    print(f"  QDRANT_URL:         {settings.qdrant_url}")
    print(f"  QDRANT_API_KEY:     {mask_secret(settings.qdrant_api_key)}")
    print(f"  DATABASE_URL:       {mask_secret(settings.database_url)}")
    print(f"  OPENROUTER_API_KEY: {mask_secret(settings.openrouter_api_key) if settings.openrouter_api_key else 'Not set'}")
    print(f"  OPENROUTER_BASE_URL:{settings.openrouter_base_url}")
    print(f"  LOG_LEVEL:          {settings.log_level}")
    print(f"  COLLECTION_NAME:    {settings.collection_name}")
    print(f"  EMBEDDING_MODEL:    {settings.embedding_model}")
    print(f"  LLM_MODEL:          {settings.llm_model}")
    print(f"  SCORE_THRESHOLD:    {settings.score_threshold}")
    print(f"  HOST:               {settings.host}")
    print(f"  PORT:               {settings.port}")
    print("=" * 60)


# Export public API
__all__ = [
    "Settings",
    "get_settings",
    "validate_settings",
    "print_settings_summary",
    "ConfigurationError",
]
