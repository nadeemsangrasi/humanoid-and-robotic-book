"""Health check router for the RAG Textbook Chatbot API.

This module provides the GET /health endpoint that checks:
- Overall API health status
- Qdrant vector database connectivity
- Gemini API readiness (passive check)

The endpoint returns a 200 OK with health details when healthy,
or a 503 Service Unavailable when critical services are down.

Usage:
    from app.routers.health import router as health_router

    app.include_router(health_router)
"""

from datetime import datetime, timezone

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.schemas.health import HealthStatus, ServiceStatus
from app.services.retrieval import get_retriever
from app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthStatus,
    summary="Health check endpoint",
    description=(
        "Check the health of the API and its dependencies. "
        "Returns 200 OK when healthy, 503 Service Unavailable when unhealthy. "
        "Used by monitoring systems and load balancers."
    ),
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2025-12-13T10:30:00Z",
                        "version": "1.0.0",
                        "services": {
                            "qdrant": {"status": "healthy", "latency_ms": 45},
                            "gemini": {"status": "healthy", "latency_ms": None},
                        },
                    }
                }
            },
        },
        503: {
            "description": "Service is unhealthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "unhealthy",
                        "timestamp": "2025-12-13T10:30:00Z",
                        "version": "1.0.0",
                        "services": {
                            "qdrant": {"status": "unhealthy", "latency_ms": None},
                            "gemini": {"status": "healthy", "latency_ms": None},
                        },
                    }
                }
            },
        },
    },
)
async def health_check() -> HealthStatus | JSONResponse:
    """Check health of all services and return comprehensive status.

    Performs health checks on:
    1. Qdrant: Active connection test with latency measurement
    2. Gemini: Passive check (assumes healthy - actual validation on first request)

    The overall status is "healthy" only if all critical services are healthy.
    Qdrant is considered critical; Gemini is checked passively.

    Returns:
        HealthStatus: Health status with 200 OK if healthy.
        JSONResponse: Health status with 503 if unhealthy.

    Example Response (healthy):
        {
            "status": "healthy",
            "timestamp": "2025-12-13T10:30:00.123456Z",
            "version": "1.0.0",
            "services": {
                "qdrant": {"status": "healthy", "latency_ms": 45},
                "gemini": {"status": "healthy", "latency_ms": null}
            }
        }
    """
    logger.debug("Starting health check")

    # -------------------------------------------------------------------------
    # Check Qdrant Health
    # -------------------------------------------------------------------------
    qdrant_status: ServiceStatus
    try:
        retriever = get_retriever()
        qdrant_healthy, qdrant_latency = retriever.health_check()

        qdrant_status = ServiceStatus(
            status="healthy" if qdrant_healthy else "unhealthy",
            latency_ms=qdrant_latency,
        )

        logger.debug(
            "Qdrant health check completed",
            extra={
                "healthy": qdrant_healthy,
                "latency_ms": qdrant_latency,
            },
        )

    except Exception as e:
        logger.error(
            "Qdrant health check failed with exception",
            extra={"error": str(e)},
        )
        qdrant_status = ServiceStatus(status="unhealthy", latency_ms=None)

    # -------------------------------------------------------------------------
    # Check Gemini Health (Passive)
    # -------------------------------------------------------------------------
    # We do not actively ping Gemini API to avoid unnecessary costs/quota usage.
    # The Gemini service is assumed healthy until an actual request fails.
    # This is a reasonable approach for free-tier deployments.
    gemini_status = ServiceStatus(
        status="healthy",
        latency_ms=None,
    )

    logger.debug("Gemini health check: passive (assumed healthy)")

    # -------------------------------------------------------------------------
    # Build Response
    # -------------------------------------------------------------------------
    services = {
        "qdrant": qdrant_status,
        "gemini": gemini_status,
    }

    # Determine overall health
    # Only consider services with known status (not "unknown")
    critical_services = [s for s in services.values() if s.status != "unknown"]
    overall_healthy = all(s.status == "healthy" for s in critical_services)

    health = HealthStatus(
        status="healthy" if overall_healthy else "unhealthy",
        timestamp=datetime.now(timezone.utc),
        version="1.0.0",
        services=services,
    )

    logger.info(
        "Health check completed",
        extra={
            "status": health.status,
            "qdrant": qdrant_status.status,
            "gemini": gemini_status.status,
        },
    )

    # Return 503 if unhealthy
    if not overall_healthy:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health.model_dump(mode="json"),
        )

    return health


# Export public API
__all__ = ["router"]
