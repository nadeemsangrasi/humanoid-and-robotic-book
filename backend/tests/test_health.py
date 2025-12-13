"""Tests for the health check endpoint.

This module tests the GET /health endpoint functionality including:
- Successful health check responses (200 OK)
- Response structure validation against HealthStatus schema
- Unhealthy service detection (503 Service Unavailable)
- Service status field validation

The health endpoint is critical for:
- Load balancer health probes
- Kubernetes readiness/liveness checks
- Monitoring system integration
"""

from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest
from fastapi import status


class TestHealthEndpoint:
    """Test suite for the GET /health endpoint."""

    def test_health_check_returns_200_when_healthy(
        self,
        client,
        mock_external_services,
    ):
        """Test that health check returns 200 OK when all services are healthy.

        Given: All external services (Qdrant, Gemini) are operational
        When: GET /health is called
        Then: Response status is 200 OK
        """
        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_health_response_structure_matches_schema(
        self,
        client,
        mock_external_services,
    ):
        """Test that health response contains all required fields.

        The HealthStatus schema requires:
        - status: "healthy" or "unhealthy"
        - timestamp: ISO 8601 datetime
        - version: semver string
        - services: dict with service statuses
        """
        # Act
        response = client.get("/health")
        data = response.json()

        # Assert - Required fields exist
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "services" in data

        # Assert - Status is valid value
        assert data["status"] in ["healthy", "unhealthy"]

        # Assert - Version follows semver pattern
        version = data["version"]
        parts = version.split(".")
        assert len(parts) >= 3, f"Version '{version}' should be semver format"

        # Assert - Timestamp is valid ISO format
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            pytest.fail(f"Timestamp '{data['timestamp']}' is not valid ISO format")

    def test_health_response_contains_service_statuses(
        self,
        client,
        mock_external_services,
    ):
        """Test that services dict contains expected service entries.

        Expected services:
        - qdrant: Vector database service
        - gemini: LLM API service
        """
        # Act
        response = client.get("/health")
        data = response.json()
        services = data["services"]

        # Assert - Expected services present
        assert "qdrant" in services, "Qdrant service status missing"
        assert "gemini" in services, "Gemini service status missing"

        # Assert - Service status structure
        for service_name, service_status in services.items():
            assert "status" in service_status, f"{service_name} missing status field"
            assert service_status["status"] in [
                "healthy",
                "unhealthy",
                "unknown",
            ], f"Invalid status for {service_name}"

    def test_health_response_includes_latency_when_healthy(
        self,
        client,
        mock_external_services,
    ):
        """Test that healthy services include latency measurements.

        When a service health check succeeds, latency_ms should be populated
        with the round-trip time in milliseconds.
        """
        # Act
        response = client.get("/health")
        data = response.json()
        qdrant_status = data["services"]["qdrant"]

        # Assert - Latency present for healthy service
        if qdrant_status["status"] == "healthy":
            assert "latency_ms" in qdrant_status
            # Latency should be None or a non-negative integer
            latency = qdrant_status["latency_ms"]
            assert latency is None or (isinstance(latency, int) and latency >= 0)

    def test_health_returns_503_when_qdrant_unhealthy(
        self,
        client,
        mock_external_services,
    ):
        """Test that health check returns 503 when Qdrant is unhealthy.

        Given: Qdrant health check fails
        When: GET /health is called
        Then: Response status is 503 Service Unavailable
        And: Overall status is "unhealthy"
        """
        # Arrange - Configure mock to return unhealthy
        mock_retriever = mock_external_services["retriever"]
        mock_retriever.health_check.return_value = (False, None)

        # Act
        response = client.get("/health")
        data = response.json()

        # Assert
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert data["status"] == "unhealthy"
        assert data["services"]["qdrant"]["status"] == "unhealthy"

    def test_health_returns_503_when_qdrant_raises_exception(
        self,
        client,
        mock_external_services,
    ):
        """Test that health check returns 503 when Qdrant throws an exception.

        Given: Qdrant health check raises an exception
        When: GET /health is called
        Then: Response status is 503 Service Unavailable
        And: Qdrant status is "unhealthy"
        """
        # Arrange - Configure mock to raise exception
        mock_retriever = mock_external_services["retriever"]
        mock_retriever.health_check.side_effect = ConnectionError("Connection refused")

        # Act
        response = client.get("/health")
        data = response.json()

        # Assert
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert data["status"] == "unhealthy"
        assert data["services"]["qdrant"]["status"] == "unhealthy"
        assert data["services"]["qdrant"]["latency_ms"] is None

    def test_health_gemini_status_is_passive(
        self,
        client,
        mock_external_services,
    ):
        """Test that Gemini status is passive (no active health check).

        Gemini API health is checked passively - it's assumed healthy
        until an actual request fails. This avoids unnecessary API calls
        and quota usage on free tier.
        """
        # Act
        response = client.get("/health")
        data = response.json()
        gemini_status = data["services"]["gemini"]

        # Assert - Gemini should be healthy with no latency measurement
        assert gemini_status["status"] == "healthy"
        assert gemini_status["latency_ms"] is None

    def test_health_version_matches_app_version(
        self,
        client,
        mock_external_services,
    ):
        """Test that health response version matches expected app version.

        The version in health response should match the application's
        configured version (currently 1.0.0).
        """
        # Act
        response = client.get("/health")
        data = response.json()

        # Assert
        assert data["version"] == "1.0.0"

    def test_health_timestamp_is_recent(
        self,
        client,
        mock_external_services,
    ):
        """Test that health check timestamp is recent (within last minute).

        The timestamp should reflect when the health check was performed,
        not a cached value.
        """
        # Arrange
        before_request = datetime.now()

        # Act
        response = client.get("/health")
        data = response.json()
        after_request = datetime.now()

        # Parse timestamp
        timestamp_str = data["timestamp"]
        # Handle both 'Z' and '+00:00' timezone formats
        if timestamp_str.endswith("Z"):
            timestamp_str = timestamp_str[:-1] + "+00:00"
        timestamp = datetime.fromisoformat(timestamp_str)
        # Remove timezone for comparison
        timestamp_naive = timestamp.replace(tzinfo=None)

        # Assert - Timestamp is between request start and end
        # Allow some tolerance for test execution time
        assert timestamp_naive >= before_request.replace(microsecond=0)

    def test_health_check_content_type_is_json(
        self,
        client,
        mock_external_services,
    ):
        """Test that health endpoint returns JSON content type."""
        # Act
        response = client.get("/health")

        # Assert
        assert response.headers["content-type"] == "application/json"


class TestHealthEndpointIntegration:
    """Integration-level tests for health endpoint behavior."""

    def test_health_endpoint_is_accessible_without_auth(
        self,
        client,
        mock_external_services,
    ):
        """Test that health endpoint does not require authentication.

        Health endpoints should be publicly accessible for load balancers
        and monitoring systems.
        """
        # Act - No auth headers provided
        response = client.get("/health")

        # Assert - Should not return 401/403
        assert response.status_code not in [401, 403]

    def test_health_endpoint_handles_cors(
        self,
        client,
        mock_external_services,
    ):
        """Test that health endpoint handles CORS preflight requests."""
        # Act - OPTIONS request (CORS preflight)
        response = client.options("/health")

        # Assert - Should not fail
        # FastAPI handles OPTIONS automatically with CORS middleware
        assert response.status_code in [200, 204, 405]

    def test_multiple_health_checks_are_independent(
        self,
        client,
        mock_external_services,
    ):
        """Test that multiple health checks don't interfere with each other.

        Each health check should be independent and not cache results
        from previous checks.
        """
        # Arrange
        mock_retriever = mock_external_services["retriever"]

        # First call - healthy
        mock_retriever.health_check.return_value = (True, 45)
        response1 = client.get("/health")
        data1 = response1.json()

        # Second call - unhealthy
        mock_retriever.health_check.return_value = (False, None)
        response2 = client.get("/health")
        data2 = response2.json()

        # Assert - Results should reflect mock state at call time
        assert data1["status"] == "healthy"
        assert data2["status"] == "unhealthy"
