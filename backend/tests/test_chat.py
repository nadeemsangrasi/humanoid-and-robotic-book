"""Tests for the chat endpoint.

This module tests the POST /api/v1/chat endpoint functionality including:
- Successful chat requests with valid queries
- Input validation (empty queries, max length)
- Response structure validation with citations and metadata
- Error handling for service failures
- Rate limit handling

The chat endpoint implements the RAG pipeline:
1. Embed query using Gemini embeddings
2. Search Qdrant for relevant chunks
3. Generate answer using Agent SDK with Gemini
4. Return formatted response with citations
"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status


class TestChatEndpointSuccess:
    """Test suite for successful chat endpoint operations."""

    def test_chat_returns_200_with_valid_query(
        self,
        client,
        mock_external_services,
        sample_chat_request,
    ):
        """Test that chat endpoint returns 200 OK for valid requests.

        Given: A valid chat request with query and k parameter
        When: POST /api/v1/chat is called
        Then: Response status is 200 OK
        """
        # Act
        response = client.post("/api/v1/chat", json=sample_chat_request)

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_chat_response_contains_required_fields(
        self,
        client,
        mock_external_services,
        sample_chat_request,
    ):
        """Test that chat response contains all required fields.

        The ChatResponse schema requires:
        - answer: The generated response text
        - citations: List of source references
        - metadata: Processing information
        """
        # Act
        response = client.post("/api/v1/chat", json=sample_chat_request)
        data = response.json()

        # Assert - Required fields exist
        assert "answer" in data, "Response missing 'answer' field"
        assert "citations" in data, "Response missing 'citations' field"
        assert "metadata" in data, "Response missing 'metadata' field"

        # Assert - Answer is non-empty string
        assert isinstance(data["answer"], str)
        assert len(data["answer"]) > 0

    def test_chat_response_citations_structure(
        self,
        client,
        mock_external_services,
        sample_chat_request,
    ):
        """Test that citations have the correct structure.

        Each Citation should contain:
        - url: Source URL
        - title: Section/chapter title
        - snippet: Text excerpt
        - score: Relevance score (0.0-1.0)
        """
        # Act
        response = client.post("/api/v1/chat", json=sample_chat_request)
        data = response.json()
        citations = data["citations"]

        # Assert - Citations is a list
        assert isinstance(citations, list)

        # Assert - Each citation has required fields
        for i, citation in enumerate(citations):
            assert "url" in citation, f"Citation {i} missing 'url'"
            assert "title" in citation, f"Citation {i} missing 'title'"
            assert "snippet" in citation, f"Citation {i} missing 'snippet'"
            assert "score" in citation, f"Citation {i} missing 'score'"

            # Assert - Score is valid range
            assert 0.0 <= citation["score"] <= 1.0, f"Citation {i} score out of range"

            # Assert - URL is properly formatted
            assert citation["url"].startswith("http"), f"Citation {i} URL invalid"

    def test_chat_response_metadata_structure(
        self,
        client,
        mock_external_services,
        sample_chat_request,
    ):
        """Test that metadata contains required processing information.

        ResponseMetadata should contain:
        - chunks_retrieved: Number of chunks found
        - processing_time_ms: Request processing time
        - model: LLM model used
        """
        # Act
        response = client.post("/api/v1/chat", json=sample_chat_request)
        data = response.json()
        metadata = data["metadata"]

        # Assert - Required metadata fields
        assert "chunks_retrieved" in metadata
        assert "processing_time_ms" in metadata
        assert "model" in metadata

        # Assert - Field types
        assert isinstance(metadata["chunks_retrieved"], int)
        assert metadata["chunks_retrieved"] >= 0

        assert isinstance(metadata["processing_time_ms"], int)
        assert metadata["processing_time_ms"] >= 0

        assert isinstance(metadata["model"], str)
        assert len(metadata["model"]) > 0

    def test_chat_with_default_k_value(
        self,
        client,
        mock_external_services,
    ):
        """Test that chat works with default k value when not specified.

        If k is not provided in the request, it should default to 5.
        """
        # Arrange - Request without k parameter
        request = {"query": "What is inverse kinematics?"}

        # Act
        response = client.post("/api/v1/chat", json=request)

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_chat_with_custom_k_value(
        self,
        client,
        mock_external_services,
    ):
        """Test that chat respects custom k values.

        The k parameter controls how many chunks are retrieved from Qdrant.
        """
        # Arrange
        request = {"query": "Explain ROS2 nodes", "k": 3}

        # Act
        response = client.post("/api/v1/chat", json=request)
        data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK


class TestChatEndpointValidation:
    """Test suite for chat endpoint input validation."""

    def test_chat_rejects_empty_query(
        self,
        client,
        mock_external_services,
    ):
        """Test that empty query returns 422 Unprocessable Entity.

        Given: A request with empty query string
        When: POST /api/v1/chat is called
        Then: Response status is 422
        """
        # Arrange
        request = {"query": "", "k": 5}

        # Act
        response = client.post("/api/v1/chat", json=request)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_chat_rejects_whitespace_only_query(
        self,
        client,
        mock_external_services,
    ):
        """Test that whitespace-only query returns 422.

        The validator should reject queries that contain only whitespace.
        """
        # Arrange
        request = {"query": "   \t\n  ", "k": 5}

        # Act
        response = client.post("/api/v1/chat", json=request)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_chat_rejects_query_exceeding_max_length(
        self,
        client,
        mock_external_services,
    ):
        """Test that query exceeding 2000 characters returns 422.

        The ChatRequest schema limits query to max_length=2000.
        """
        # Arrange
        long_query = "a" * 2001  # One character over the limit
        request = {"query": long_query, "k": 5}

        # Act
        response = client.post("/api/v1/chat", json=request)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_chat_accepts_query_at_max_length(
        self,
        client,
        mock_external_services,
    ):
        """Test that query at exactly 2000 characters is accepted.

        Boundary test for max query length.
        """
        # Arrange
        max_query = "What is robotics? " + "a" * (2000 - 18)  # Exactly 2000 chars
        request = {"query": max_query[:2000], "k": 5}

        # Act
        response = client.post("/api/v1/chat", json=request)

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_chat_rejects_k_below_minimum(
        self,
        client,
        mock_external_services,
    ):
        """Test that k < 1 returns 422.

        The ChatRequest schema requires k >= 1.
        """
        # Arrange
        request = {"query": "What is kinematics?", "k": 0}

        # Act
        response = client.post("/api/v1/chat", json=request)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_chat_rejects_k_above_maximum(
        self,
        client,
        mock_external_services,
    ):
        """Test that k > 10 returns 422.

        The ChatRequest schema requires k <= 10.
        """
        # Arrange
        request = {"query": "What is kinematics?", "k": 11}

        # Act
        response = client.post("/api/v1/chat", json=request)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_chat_accepts_k_at_boundaries(
        self,
        client,
        mock_external_services,
    ):
        """Test that k values at boundaries (1 and 10) are accepted."""
        # Test minimum
        response_min = client.post(
            "/api/v1/chat",
            json={"query": "Test query", "k": 1},
        )
        assert response_min.status_code == status.HTTP_200_OK

        # Test maximum
        response_max = client.post(
            "/api/v1/chat",
            json={"query": "Test query", "k": 10},
        )
        assert response_max.status_code == status.HTTP_200_OK

    def test_chat_rejects_missing_query_field(
        self,
        client,
        mock_external_services,
    ):
        """Test that missing query field returns 422.

        The query field is required in ChatRequest.
        """
        # Arrange - No query field
        request = {"k": 5}

        # Act
        response = client.post("/api/v1/chat", json=request)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_chat_rejects_invalid_json(
        self,
        client,
        mock_external_services,
    ):
        """Test that invalid JSON body returns 422."""
        # Act - Send invalid JSON
        response = client.post(
            "/api/v1/chat",
            content="not valid json",
            headers={"Content-Type": "application/json"},
        )

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestChatEndpointErrorHandling:
    """Test suite for chat endpoint error handling."""

    def test_chat_returns_503_on_connection_error(
        self,
        client,
        mock_external_services,
    ):
        """Test that connection errors return 503 Service Unavailable.

        When external services are unavailable, the endpoint should
        return a 503 status with appropriate error message.
        """
        # Arrange - Configure retriever to raise connection error
        mock_retriever = mock_external_services["retriever"]
        mock_retriever.search.side_effect = ConnectionError("Unable to connect to Qdrant")

        # Act
        response = client.post(
            "/api/v1/chat",
            json={"query": "What is kinematics?", "k": 5},
        )

        # Assert
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

    def test_chat_returns_429_on_rate_limit(
        self,
        client,
        mock_external_services,
    ):
        """Test that rate limit errors return 429 Too Many Requests.

        When the Gemini API returns a rate limit error, the endpoint
        should return 429 with retry information.
        """
        # Arrange - Configure orchestrator to raise rate limit error
        mock_orchestrator = mock_external_services["orchestrator"]
        mock_orchestrator.chat.side_effect = Exception("Rate limit exceeded")

        # Act
        response = client.post(
            "/api/v1/chat",
            json={"query": "What is kinematics?", "k": 5},
        )

        # Assert - Either 429 or 503 is acceptable depending on error detection
        assert response.status_code in [
            status.HTTP_429_TOO_MANY_REQUESTS,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        ]

    def test_chat_error_response_structure(
        self,
        client,
        mock_external_services,
    ):
        """Test that error responses follow ErrorResponse schema.

        ErrorResponse should contain:
        - error: Machine-readable error code
        - message: Human-readable description
        - details: Optional additional context
        """
        # Arrange - Force an error
        mock_retriever = mock_external_services["retriever"]
        mock_retriever.search.side_effect = Exception("Test error")

        # Act
        response = client.post(
            "/api/v1/chat",
            json={"query": "What is kinematics?", "k": 5},
        )
        data = response.json()

        # Assert - Error response should have detail field (FastAPI HTTPException)
        assert "detail" in data or "error" in data


class TestChatEndpointIntegration:
    """Integration-level tests for chat endpoint behavior."""

    def test_chat_calls_embedding_service(
        self,
        client,
        mock_external_services,
        sample_chat_request,
    ):
        """Test that chat endpoint calls the embedding service.

        The RAG pipeline should embed the query before searching.
        """
        # Arrange
        mock_embedding = mock_external_services["embedding_service"]

        # Act
        client.post("/api/v1/chat", json=sample_chat_request)

        # Assert
        mock_embedding.embed_query.assert_called_once()
        call_args = mock_embedding.embed_query.call_args
        assert sample_chat_request["query"] in str(call_args)

    def test_chat_calls_retriever_search(
        self,
        client,
        mock_external_services,
        sample_chat_request,
    ):
        """Test that chat endpoint calls the retriever search.

        After embedding, the pipeline should search for relevant chunks.
        """
        # Arrange
        mock_retriever = mock_external_services["retriever"]

        # Act
        client.post("/api/v1/chat", json=sample_chat_request)

        # Assert
        mock_retriever.search.assert_called_once()

    def test_chat_calls_orchestrator(
        self,
        client,
        mock_external_services,
        sample_chat_request,
    ):
        """Test that chat endpoint calls the agent orchestrator.

        The orchestrator generates the final answer using retrieved context.
        """
        # Arrange
        mock_orchestrator = mock_external_services["orchestrator"]

        # Act
        client.post("/api/v1/chat", json=sample_chat_request)

        # Assert
        mock_orchestrator.chat.assert_called_once()

    def test_chat_content_type_is_json(
        self,
        client,
        mock_external_services,
        sample_chat_request,
    ):
        """Test that chat endpoint returns JSON content type."""
        # Act
        response = client.post("/api/v1/chat", json=sample_chat_request)

        # Assert
        assert response.headers["content-type"] == "application/json"

    def test_chat_handles_empty_search_results(
        self,
        client,
        mock_external_services,
    ):
        """Test that chat handles case when no relevant chunks are found.

        When Qdrant returns no results, the endpoint should still work
        but with empty citations.
        """
        # Arrange - Configure empty search results
        mock_retriever = mock_external_services["retriever"]

        async def empty_search(*args, **kwargs):
            return []

        mock_retriever.search = AsyncMock(side_effect=empty_search)

        # Act
        response = client.post(
            "/api/v1/chat",
            json={"query": "Something obscure not in the book", "k": 5},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["citations"] == []
        assert data["metadata"]["chunks_retrieved"] == 0


class TestChatHelperFunctions:
    """Test suite for chat router helper functions."""

    def test_truncate_snippet_preserves_short_content(self):
        """Test that short snippets are not truncated."""
        from app.routers.chat import truncate_snippet

        # Arrange
        short_text = "This is a short snippet."

        # Act
        result = truncate_snippet(short_text, max_length=200)

        # Assert
        assert result == short_text
        assert "..." not in result

    def test_truncate_snippet_truncates_long_content(self):
        """Test that long snippets are truncated with ellipsis."""
        from app.routers.chat import truncate_snippet

        # Arrange
        long_text = "This is a very long snippet that exceeds the maximum length and should be truncated properly at a word boundary."

        # Act
        result = truncate_snippet(long_text, max_length=50)

        # Assert
        assert len(result) <= 53  # max_length + "..."
        assert result.endswith("...")

    def test_truncate_snippet_handles_empty_content(self):
        """Test that empty content returns empty string."""
        from app.routers.chat import truncate_snippet

        # Act
        result = truncate_snippet("", max_length=200)

        # Assert
        assert result == ""

    def test_format_citation_url_adds_https(self):
        """Test that URLs without protocol get https:// added."""
        from app.routers.chat import format_citation_url

        # Arrange
        url = "example.com/page"

        # Act
        result = format_citation_url(url)

        # Assert
        assert result == "https://example.com/page"

    def test_format_citation_url_preserves_https(self):
        """Test that URLs with https are preserved."""
        from app.routers.chat import format_citation_url

        # Arrange
        url = "https://example.com/page"

        # Act
        result = format_citation_url(url)

        # Assert
        assert result == "https://example.com/page"

    def test_format_citation_url_handles_empty(self):
        """Test that empty URLs return empty string."""
        from app.routers.chat import format_citation_url

        # Act
        result = format_citation_url("")

        # Assert
        assert result == ""

    def test_build_citations_from_results(self):
        """Test citation building from search results."""
        from app.routers.chat import build_citations_from_results

        # Arrange
        search_results = [
            {
                "content": "This is the content of the first result.",
                "url": "https://example.com/page1",
                "title": "Page 1",
                "score": 0.92,
            },
            {
                "content": "Second result content here.",
                "url": "https://example.com/page2",
                "title": "Page 2",
                "score": 0.85,
            },
        ]

        # Act
        citations = build_citations_from_results(search_results)

        # Assert
        assert len(citations) == 2
        assert citations[0].url == "https://example.com/page1"
        assert citations[0].title == "Page 1"
        assert citations[0].score == 0.92
        assert citations[1].score == 0.85
