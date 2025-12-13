"""Structured logging configuration for the RAG chatbot backend.

Provides JSON-formatted logging suitable for production environments
with support for log level configuration via environment variables.

Usage:
    from app.utils.logging import get_logger

    logger = get_logger(__name__)
    logger.info("Processing request", extra={"query": "test"})
"""

import logging
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging output.

    Produces JSON-formatted log records with consistent fields:
    - timestamp: ISO 8601 format in UTC
    - level: Log level name (INFO, ERROR, etc.)
    - logger: Logger name (typically module path)
    - message: Log message
    - Additional fields from extra parameter
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as JSON.

        Args:
            record: The log record to format.

        Returns:
            JSON-formatted string representation of the log record.
        """
        log_data: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields from the record
        # These are fields passed via extra={} in logging calls
        reserved_attrs = {
            "name", "msg", "args", "created", "filename", "funcName",
            "levelname", "levelno", "lineno", "module", "msecs",
            "pathname", "process", "processName", "relativeCreated",
            "stack_info", "exc_info", "exc_text", "thread", "threadName",
            "taskName", "message"
        }

        for key, value in record.__dict__.items():
            if key not in reserved_attrs and not key.startswith("_"):
                log_data[key] = value

        return json.dumps(log_data, default=str)


class ConsoleFormatter(logging.Formatter):
    """Human-readable console formatter for development.

    Produces formatted output: [TIMESTAMP] LEVEL - LOGGER - MESSAGE
    """

    def __init__(self) -> None:
        super().__init__(
            fmt="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )


def get_log_level() -> int:
    """Get the configured log level from environment.

    Reads LOG_LEVEL environment variable and maps it to logging constants.
    Defaults to INFO if not set or invalid.

    Returns:
        Logging level constant (e.g., logging.INFO).
    """
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return level_map.get(level_name, logging.INFO)


def get_log_format() -> str:
    """Get the configured log format from environment.

    Reads LOG_FORMAT environment variable.
    Defaults to 'json' for production, supports 'console' for development.

    Returns:
        Format string: 'json' or 'console'.
    """
    return os.environ.get("LOG_FORMAT", "json").lower()


def setup_logging() -> None:
    """Configure the root logger with appropriate handlers.

    Sets up logging based on environment configuration:
    - LOG_LEVEL: Sets minimum log level (default: INFO)
    - LOG_FORMAT: Sets output format - 'json' or 'console' (default: json)

    This function should be called once at application startup,
    typically in main.py before creating the FastAPI app.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(get_log_level())

    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(get_log_level())

    # Set formatter based on configuration
    log_format = get_log_format()
    if log_format == "console":
        console_handler.setFormatter(ConsoleFormatter())
    else:
        console_handler.setFormatter(JSONFormatter())

    root_logger.addHandler(console_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance.

    Returns a logger that inherits configuration from the root logger.
    If setup_logging() has not been called, logging will use Python defaults.

    Args:
        name: Logger name, typically __name__ of the calling module.

    Returns:
        Configured logger instance.

    Example:
        from app.utils.logging import get_logger

        logger = get_logger(__name__)
        logger.info("Request processed", extra={"user_id": "123"})
    """
    return logging.getLogger(name)
