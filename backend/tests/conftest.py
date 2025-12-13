"""Pytest fixtures for the RAG chatbot backend tests.

This module provides shared fixtures for testing the Physical AI & Humanoid Robotics
textbook chatbot backend, including:

- Mock external services (Qdrant, Gemini embeddings)
- Test client configuration
- Common test data fixtures
- Environment variable mocking

The fixtures use unittest.mock to isolate tests from external dependencies,
ensuring tests can run without API keys or network access.

Usage:
    # In test files, fixtures are automatically available via pytest injection
    def test_example(client, mock_external_services):
        response = client.get("/health")
        assert response.status_code == 200
"""

import os
import sys
from typing import Any, Generator
from unittest.mock import MagicMock, AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


# -----------------------------------------------------------------------------
# Environment Setup - Must run before any app imports
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables before any imports.

    This fixture runs once per test session and sets required environment
    variables with test values to allow Settings validation to pass.
    """
    test_env = {
        "GOOGLE_API_KEY": "test-google-api-key-12345",
        "QDRANT_URL": "https://test-cluster.cloud.qdrant.io",
        "QDRANT_API_KEY": "test-qdrant-api-key-12345",
        "LOG_LEVEL": "DEBUG",
        "COLLECTION_NAME": "test_book_chunks",
        "EMBEDDING_MODEL": "models/text-embedding-004",
        "LLM_MODEL": "gemini-2.0-flash",
        "SCORE_THRESHOLD": "0.7",
        "HOST": "0.0.0.0",
        "PORT": "7860",
    }

    # Store original values
    original_env = {}
    for key, value in test_env.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value

    yield

    # Restore original values
    for key, original_value in original_env.items():
        if original_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_value


# -----------------------------------------------------------------------------
# Mock Qdrant Client
# -----------------------------------------------------------------------------
@pytest.fixture
def mock_qdrant_client():
    """Create a mock Qdrant client with common operations.

    Returns:
        MagicMock: A mock QdrantClient instance with configured return values.
    """
    mock_client = MagicMock()

    # Mock get_collections for health check
    mock_collections = MagicMock()
    mock_collections.collections = []
    mock_client.get_collections.return_value = mock_collections

    # Mock collection_exists
    mock_client.collection_exists.return_value = True

    # Mock collection info
    mock_collection_info = MagicMock()
    mock_collection_info.vectors_count = 100
    mock_collection_info.points_count = 100
    mock_collection_info.status = MagicMock(value="green")
    mock_client.get_collection.return_value = mock_collection_info

    # Mock search results
    mock_search_result = MagicMock()
    mock_search_result.score = 0.85
    mock_search_result.payload = {
        "content": "Inverse kinematics is the mathematical process of calculating joint angles.",
        "url": "https://textbook.example.com/chapters/kinematics",
        "title": "Chapter 3: Kinematics",
        "heading": "Inverse Kinematics",
        "module": "module-1-robotics",
        "chapter": "03-kinematics",
        "chunk_index": 0,
    }
    mock_client.search.return_value = [mock_search_result]

    # Mock upsert
    mock_client.upsert.return_value = None

    return mock_client


# -----------------------------------------------------------------------------
# Mock Embedding Service
# -----------------------------------------------------------------------------
@pytest.fixture
def mock_embedding_service():
    """Create a mock embedding service.

    Returns:
        MagicMock: A mock EmbeddingService with configured return values.
    """
    mock_service = MagicMock()

    # Return 768-dimensional vector for queries
    mock_service.embed_query.return_value = [0.1] * 768

    # Return list of 768-dimensional vectors for documents
    mock_service.embed_documents.return_value = [[0.1] * 768]

    # Dimensions property
    mock_service.dimensions = 768

    return mock_service


# -----------------------------------------------------------------------------
# Mock Agent Orchestrator
# -----------------------------------------------------------------------------
@pytest.fixture
def mock_orchestrator():
    """Create a mock agent orchestrator.

    Returns:
        MagicMock: A mock orchestrator with async chat method.
    """
    mock_orch = MagicMock()

    # Configure async chat method
    async def mock_chat(query: str, k: int = 5) -> dict[str, Any]:
        return {
            "answer": f"Based on the textbook content, here is information about: {query}",
            "model": "gemini-2.0-flash",
        }

    mock_orch.chat = AsyncMock(side_effect=mock_chat)

    return mock_orch


# -----------------------------------------------------------------------------
# Mock Retriever
# -----------------------------------------------------------------------------
@pytest.fixture
def mock_retriever(mock_qdrant_client):
    """Create a mock QdrantRetriever.

    Args:
        mock_qdrant_client: The mock Qdrant client fixture.

    Returns:
        MagicMock: A mock retriever with search and health check methods.
    """
    mock_ret = MagicMock()
    mock_ret.client = mock_qdrant_client
    mock_ret.collection_name = "test_book_chunks"

    # Configure health check
    mock_ret.health_check.return_value = (True, 45)

    # Configure async search
    async def mock_search(
        query_vector: list[float],
        k: int = 5,
        threshold: float = 0.7,
        module_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        return [
            {
                "content": "Inverse kinematics is the mathematical process of calculating joint angles.",
                "url": "https://textbook.example.com/chapters/kinematics",
                "title": "Chapter 3: Kinematics",
                "score": 0.85,
                "heading": "Inverse Kinematics",
                "module": "module-1-robotics",
                "chapter": "03-kinematics",
                "chunk_index": 0,
            }
        ]

    mock_ret.search = AsyncMock(side_effect=mock_search)

    # Configure upsert
    mock_ret.upsert_points.return_value = 10

    return mock_ret


# -----------------------------------------------------------------------------
# Combined External Services Mock
# -----------------------------------------------------------------------------
@pytest.fixture
def mock_external_services(
    mock_qdrant_client,
    mock_embedding_service,
    mock_orchestrator,
    mock_retriever,
):
    """Mock all external service connections for isolated testing.

    This fixture patches the singleton getters to return mock instances,
    ensuring tests don't make real API calls.

    Args:
        mock_qdrant_client: Mock Qdrant client.
        mock_embedding_service: Mock embedding service.
        mock_orchestrator: Mock agent orchestrator.
        mock_retriever: Mock retriever service.

    Yields:
        dict: Dictionary containing all mock instances for inspection.
    """
    with patch("app.services.retrieval.qdrant_client.QdrantClient") as patched_qdrant, \
         patch("app.services.retrieval.get_retriever") as patched_get_retriever, \
         patch("app.services.embedding.embedding.get_embedding_service") as patched_get_embedding, \
         patch("app.services.agent.orchestrator.get_orchestrator") as patched_get_orchestrator, \
         patch("app.routers.health.get_retriever") as patched_health_retriever, \
         patch("app.routers.chat.get_retriever") as patched_chat_retriever, \
         patch("app.routers.chat.get_embedding_service") as patched_chat_embedding, \
         patch("app.routers.chat.get_orchestrator") as patched_chat_orchestrator:

        # Configure patched getters to return mock instances
        patched_qdrant.return_value = mock_qdrant_client
        patched_get_retriever.return_value = mock_retriever
        patched_get_embedding.return_value = mock_embedding_service
        patched_get_orchestrator.return_value = mock_orchestrator
        patched_health_retriever.return_value = mock_retriever
        patched_chat_retriever.return_value = mock_retriever
        patched_chat_embedding.return_value = mock_embedding_service
        patched_chat_orchestrator.return_value = mock_orchestrator

        yield {
            "qdrant_client": mock_qdrant_client,
            "embedding_service": mock_embedding_service,
            "orchestrator": mock_orchestrator,
            "retriever": mock_retriever,
        }


# -----------------------------------------------------------------------------
# Test Client
# -----------------------------------------------------------------------------
@pytest.fixture
def client(mock_external_services) -> Generator[TestClient, None, None]:
    """Create a TestClient with mocked external services.

    This fixture ensures the FastAPI app is imported after mocks are set up,
    preventing real service initialization.

    Args:
        mock_external_services: The combined mocks fixture.

    Yields:
        TestClient: A test client for making requests to the API.
    """
    # Import app after mocks are in place
    from app.main import app

    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


# -----------------------------------------------------------------------------
# Sample Test Data
# -----------------------------------------------------------------------------
@pytest.fixture
def sample_chat_request() -> dict[str, Any]:
    """Return a sample valid chat request payload.

    Returns:
        dict: A valid ChatRequest payload for testing.
    """
    return {
        "query": "What is inverse kinematics?",
        "k": 5,
    }


@pytest.fixture
def sample_search_results() -> list[dict[str, Any]]:
    """Return sample Qdrant search results.

    Returns:
        list: A list of search result dictionaries.
    """
    return [
        {
            "content": "Inverse kinematics (IK) is the mathematical process of calculating the variable joint parameters needed to place the end of a kinematic chain in a given position.",
            "url": "https://textbook.example.com/chapters/kinematics",
            "title": "Chapter 3: Forward and Inverse Kinematics",
            "score": 0.92,
            "heading": "Inverse Kinematics Fundamentals",
            "module": "module-1-robotics",
            "chapter": "03-kinematics",
            "chunk_index": 0,
        },
        {
            "content": "Common methods for solving inverse kinematics include analytical solutions, numerical methods like Jacobian-based techniques, and machine learning approaches.",
            "url": "https://textbook.example.com/chapters/kinematics",
            "title": "Chapter 3: Forward and Inverse Kinematics",
            "score": 0.88,
            "heading": "IK Solution Methods",
            "module": "module-1-robotics",
            "chapter": "03-kinematics",
            "chunk_index": 1,
        },
    ]


@pytest.fixture
def sample_chunk_content() -> str:
    """Return sample textbook content for chunking tests.

    Returns:
        str: A sample of textbook content with headings.
    """
    return """# Introduction to Robotics

This chapter introduces the fundamental concepts of robotics and physical AI systems.

## What is a Robot?

A robot is a programmable machine capable of carrying out a series of actions autonomously or semi-autonomously. Modern robots integrate sensors, actuators, and computing systems.

## Key Components

### Sensors
Sensors allow robots to perceive their environment. Common sensor types include cameras, LiDAR, IMUs, and force/torque sensors.

### Actuators
Actuators convert energy into motion. Electric motors, hydraulic systems, and pneumatic actuators are commonly used in robotics.

### Control Systems
Control systems coordinate sensor input with actuator output to achieve desired behavior.

## Summary

This chapter covered the basics of robotic systems and their key components."""


# -----------------------------------------------------------------------------
# Sitemap Test Data
# -----------------------------------------------------------------------------
@pytest.fixture
def sample_sitemap_xml() -> str:
    """Return sample sitemap XML content.

    Returns:
        str: Valid sitemap XML with loc elements.
    """
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://textbook.example.com/</loc>
    </url>
    <url>
        <loc>https://textbook.example.com/module-1-robotics/01-introduction</loc>
    </url>
    <url>
        <loc>https://textbook.example.com/module-1-robotics/02-kinematics</loc>
    </url>
    <url>
        <loc>https://textbook.example.com/module-2-ros2/01-nodes-topics</loc>
    </url>
</urlset>"""


@pytest.fixture
def sample_page_html() -> str:
    """Return sample Docusaurus page HTML.

    Returns:
        str: Valid HTML content resembling a Docusaurus page.
    """
    return """<!DOCTYPE html>
<html>
<head><title>Introduction to Robotics</title></head>
<body>
    <nav>Navigation</nav>
    <main>
        <article class="markdown">
            <h1>Introduction to Robotics</h1>
            <p>This chapter introduces fundamental concepts.</p>
            <h2>What is a Robot?</h2>
            <p>A robot is a programmable machine capable of autonomous action.</p>
        </article>
    </main>
    <footer>Footer content</footer>
</body>
</html>"""


# Export fixtures for test discovery
__all__ = [
    "setup_test_environment",
    "mock_qdrant_client",
    "mock_embedding_service",
    "mock_orchestrator",
    "mock_retriever",
    "mock_external_services",
    "client",
    "sample_chat_request",
    "sample_search_results",
    "sample_chunk_content",
    "sample_sitemap_xml",
    "sample_page_html",
]
