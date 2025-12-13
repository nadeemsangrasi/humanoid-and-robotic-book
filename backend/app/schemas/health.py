"""Pydantic schemas for health check endpoint response models.

This module contains schemas for the /health endpoint:

- ServiceStatus: Status of a single service dependency (Qdrant, Gemini)
- HealthStatus: Overall health check response with timestamp and service details

These schemas follow the data model defined in specs/001-rag-chatbot-backend/data-model.md.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ServiceStatus(BaseModel):
    """Status of a single service dependency.

    Represents the health status of an external service such as Qdrant
    or the Gemini API that the backend depends on.

    Attributes:
        status: Current health state of the service.
            - "healthy": Service is operational
            - "unhealthy": Service is not responding or erroring
            - "unknown": Service status could not be determined
        latency_ms: Round-trip time to the service in milliseconds,
            or None if the service is unhealthy or not checked.

    Example:
        >>> service = ServiceStatus(status="healthy", latency_ms=45)
        >>> service.model_dump()
        {'status': 'healthy', 'latency_ms': 45}
    """

    status: Literal["healthy", "unhealthy", "unknown"] = Field(
        ...,
        description="Service health status",
        examples=["healthy", "unhealthy", "unknown"],
    )
    latency_ms: int | None = Field(
        default=None,
        description="Service response latency in milliseconds",
        ge=0,
        examples=[45, 120, None],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"status": "healthy", "latency_ms": 45},
                {"status": "unhealthy", "latency_ms": None},
            ]
        }
    }


class HealthStatus(BaseModel):
    """Overall health check response for monitoring.

    Provides comprehensive health information about the API and all its
    dependent services. Used by monitoring systems and load balancers
    to determine service availability.

    Attributes:
        status: Overall health status of the API.
            - "healthy": All critical services are operational
            - "unhealthy": One or more critical services are down
        timestamp: Current server time in ISO 8601 format (UTC).
        version: Application version string (semver format).
        services: Dictionary mapping service names to their status.
            Expected keys: "qdrant", "gemini"

    Example:
        >>> from datetime import datetime, timezone
        >>> health = HealthStatus(
        ...     status="healthy",
        ...     timestamp=datetime.now(timezone.utc),
        ...     version="1.0.0",
        ...     services={
        ...         "qdrant": ServiceStatus(status="healthy", latency_ms=45),
        ...         "gemini": ServiceStatus(status="healthy", latency_ms=None),
        ...     }
        ... )
    """

    status: Literal["healthy", "unhealthy"] = Field(
        ...,
        description="Overall API health status",
        examples=["healthy", "unhealthy"],
    )
    timestamp: datetime = Field(
        ...,
        description="Current server timestamp (ISO 8601 UTC)",
        examples=["2025-12-13T10:30:00Z"],
    )
    version: str = Field(
        ...,
        description="Application version (semver format)",
        pattern=r"^\d+\.\d+\.\d+",
        examples=["1.0.0", "1.2.3"],
    )
    services: dict[str, ServiceStatus] = Field(
        ...,
        description="Status of dependent services",
        examples=[
            {
                "qdrant": {"status": "healthy", "latency_ms": 45},
                "gemini": {"status": "healthy", "latency_ms": None},
            }
        ],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "timestamp": "2025-12-13T10:30:00Z",
                    "version": "1.0.0",
                    "services": {
                        "qdrant": {"status": "healthy", "latency_ms": 45},
                        "gemini": {"status": "healthy", "latency_ms": None},
                    },
                }
            ]
        }
    }


# Export public API
__all__ = ["HealthStatus", "ServiceStatus"]
