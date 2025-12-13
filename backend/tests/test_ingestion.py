"""Tests for the book ingestion script.

This module tests the ingestion utilities in scripts/ingest-book.py including:
- Sitemap URL extraction from XML
- Content chunking algorithm (500-1000 tokens)
- Deterministic ID generation for idempotent upserts
- Metadata extraction from URL paths

The ingestion script is responsible for:
1. Fetching the sitemap from the published textbook
2. Extracting content from each page
3. Chunking content into semantic segments
4. Embedding and uploading to Qdrant
"""

import hashlib
import uuid
from unittest.mock import patch, MagicMock

import pytest


class TestSitemapUrlExtraction:
    """Test suite for sitemap URL extraction functionality."""

    def test_fetch_sitemap_urls_extracts_loc_elements(
        self,
        sample_sitemap_xml,
    ):
        """Test that sitemap parser extracts all <loc> elements.

        Given: Valid sitemap XML with multiple URL entries
        When: fetch_sitemap_urls is called (with mocked HTTP)
        Then: All URLs from <loc> elements are returned
        """
        # Import must happen after conftest sets up environment
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts import ingest_book

        # Arrange - Mock HTTP response
        with patch("scripts.ingest_book.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.content = sample_sitemap_xml.encode()
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.__enter__.return_value.get.return_value = mock_response

            # Act
            urls = ingest_book.fetch_sitemap_urls("https://example.com/sitemap.xml")

            # Assert
            assert len(urls) == 4
            assert "https://textbook.example.com/" in urls
            assert "https://textbook.example.com/module-1-robotics/01-introduction" in urls
            assert "https://textbook.example.com/module-1-robotics/02-kinematics" in urls
            assert "https://textbook.example.com/module-2-ros2/01-nodes-topics" in urls

    def test_fetch_sitemap_urls_handles_empty_sitemap(self):
        """Test handling of empty sitemap."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts import ingest_book

        # Arrange - Empty sitemap
        empty_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        </urlset>"""

        with patch("scripts.ingest_book.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.content = empty_sitemap.encode()
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.__enter__.return_value.get.return_value = mock_response

            # Act
            urls = ingest_book.fetch_sitemap_urls("https://example.com/sitemap.xml")

            # Assert
            assert urls == []

    def test_fetch_sitemap_urls_strips_whitespace(self):
        """Test that URLs are stripped of whitespace."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts import ingest_book

        # Arrange - Sitemap with whitespace in URLs
        sitemap_with_spaces = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>  https://example.com/page1  </loc>
            </url>
        </urlset>"""

        with patch("scripts.ingest_book.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.content = sitemap_with_spaces.encode()
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.__enter__.return_value.get.return_value = mock_response

            # Act
            urls = ingest_book.fetch_sitemap_urls("https://example.com/sitemap.xml")

            # Assert
            assert urls[0] == "https://example.com/page1"
            assert not urls[0].startswith(" ")
            assert not urls[0].endswith(" ")


class TestMetadataExtraction:
    """Test suite for URL metadata extraction."""

    def test_extract_metadata_from_url_finds_module(self):
        """Test extraction of module identifier from URL path."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import extract_metadata_from_url

        # Arrange
        url = "https://textbook.example.com/module-1-robotics/01-introduction"

        # Act
        module, chapter = extract_metadata_from_url(url)

        # Assert
        assert module == "module-1-robotics"

    def test_extract_metadata_from_url_finds_chapter(self):
        """Test extraction of chapter identifier from URL path."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import extract_metadata_from_url

        # Arrange
        url = "https://textbook.example.com/module-2-ros2/02-nodes-and-topics"

        # Act
        module, chapter = extract_metadata_from_url(url)

        # Assert
        assert chapter == "02-nodes-and-topics"

    def test_extract_metadata_from_url_handles_no_module(self):
        """Test handling of URLs without module pattern."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import extract_metadata_from_url

        # Arrange
        url = "https://textbook.example.com/introduction"

        # Act
        module, chapter = extract_metadata_from_url(url)

        # Assert
        assert module is None

    def test_extract_metadata_from_url_handles_root_url(self):
        """Test handling of root URL with no path segments."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import extract_metadata_from_url

        # Arrange
        url = "https://textbook.example.com/"

        # Act
        module, chapter = extract_metadata_from_url(url)

        # Assert
        assert module is None
        assert chapter is None


class TestDeterministicIdGeneration:
    """Test suite for deterministic point ID generation."""

    def test_generate_point_id_is_deterministic(self):
        """Test that same input produces same UUID.

        Deterministic IDs enable idempotent upserts - re-indexing
        the same content produces the same IDs.
        """
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import generate_point_id

        # Arrange
        url = "https://textbook.example.com/chapter-1"
        chunk_index = 0

        # Act
        id1 = generate_point_id(url, chunk_index)
        id2 = generate_point_id(url, chunk_index)

        # Assert
        assert id1 == id2

    def test_generate_point_id_different_for_different_chunks(self):
        """Test that different chunk indices produce different IDs."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import generate_point_id

        # Arrange
        url = "https://textbook.example.com/chapter-1"

        # Act
        id0 = generate_point_id(url, 0)
        id1 = generate_point_id(url, 1)
        id2 = generate_point_id(url, 2)

        # Assert
        assert id0 != id1
        assert id1 != id2
        assert id0 != id2

    def test_generate_point_id_different_for_different_urls(self):
        """Test that different URLs produce different IDs."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import generate_point_id

        # Arrange
        url1 = "https://textbook.example.com/chapter-1"
        url2 = "https://textbook.example.com/chapter-2"
        chunk_index = 0

        # Act
        id1 = generate_point_id(url1, chunk_index)
        id2 = generate_point_id(url2, chunk_index)

        # Assert
        assert id1 != id2

    def test_generate_point_id_returns_valid_uuid(self):
        """Test that generated ID is a valid UUID string."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import generate_point_id

        # Arrange
        url = "https://textbook.example.com/chapter-1"
        chunk_index = 0

        # Act
        point_id = generate_point_id(url, chunk_index)

        # Assert - Should be valid UUID format
        try:
            uuid.UUID(point_id)
        except ValueError:
            pytest.fail(f"Generated ID '{point_id}' is not a valid UUID")

    def test_generate_point_id_uses_md5_hash(self):
        """Test that ID generation uses MD5 hash as documented."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import generate_point_id

        # Arrange
        url = "https://textbook.example.com/chapter-1"
        chunk_index = 5

        # Act
        point_id = generate_point_id(url, chunk_index)

        # Calculate expected ID using same algorithm
        content = f"{url}::{chunk_index}"
        hash_bytes = hashlib.md5(content.encode()).digest()
        expected_id = str(uuid.UUID(bytes=hash_bytes))

        # Assert
        assert point_id == expected_id


class TestContentChunking:
    """Test suite for content chunking algorithm."""

    def test_chunk_content_creates_chunks(
        self,
        sample_chunk_content,
    ):
        """Test that content is split into chunks."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import chunk_content

        # Act
        chunks = chunk_content(
            content=sample_chunk_content,
            url="https://example.com/intro",
            title="Introduction to Robotics",
            module="module-1",
            chapter="01-intro",
        )

        # Assert
        assert len(chunks) >= 1
        assert all(hasattr(chunk, "content") for chunk in chunks)

    def test_chunk_content_preserves_metadata(
        self,
        sample_chunk_content,
    ):
        """Test that chunks preserve source metadata."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import chunk_content

        # Arrange
        url = "https://example.com/intro"
        title = "Introduction to Robotics"
        module = "module-1"
        chapter = "01-intro"

        # Act
        chunks = chunk_content(
            content=sample_chunk_content,
            url=url,
            title=title,
            module=module,
            chapter=chapter,
        )

        # Assert - Each chunk has correct metadata
        for chunk in chunks:
            assert chunk.url == url
            assert chunk.title == title
            assert chunk.module == module
            assert chunk.chapter == chapter

    def test_chunk_content_assigns_sequential_indices(
        self,
        sample_chunk_content,
    ):
        """Test that chunks have sequential indices starting from 0."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import chunk_content

        # Act
        chunks = chunk_content(
            content=sample_chunk_content * 5,  # Make content longer
            url="https://example.com/intro",
            title="Introduction",
            module="module-1",
            chapter="01-intro",
        )

        # Assert
        if len(chunks) > 1:
            indices = [chunk.chunk_index for chunk in chunks]
            assert indices == list(range(len(chunks)))

    def test_chunk_content_handles_empty_content(self):
        """Test handling of empty content."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import chunk_content

        # Act
        chunks = chunk_content(
            content="",
            url="https://example.com/empty",
            title="Empty Page",
            module=None,
            chapter=None,
        )

        # Assert
        assert chunks == []

    def test_chunk_content_handles_short_content(self):
        """Test that short content creates at least one chunk."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import chunk_content

        # Arrange - Content shorter than MIN_TOKENS
        short_content = "This is a very short piece of content."

        # Act
        chunks = chunk_content(
            content=short_content,
            url="https://example.com/short",
            title="Short Page",
            module=None,
            chapter=None,
        )

        # Assert - Should still create a chunk even if below minimum
        assert len(chunks) == 1
        assert short_content in chunks[0].content

    def test_chunk_content_extracts_headings(self):
        """Test that chunk extracts heading from content."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import chunk_content

        # Arrange
        content_with_heading = """# Main Title

Some introductory content here.

## Section Heading

This section has specific content about the topic.
More content follows in this section with enough words to make it substantial.
We need to ensure there is sufficient content to meet the minimum token requirement.
"""

        # Act
        chunks = chunk_content(
            content=content_with_heading,
            url="https://example.com/page",
            title="Main Title",
            module=None,
            chapter=None,
        )

        # Assert
        assert len(chunks) >= 1
        # First chunk should have heading
        assert chunks[0].heading is not None


class TestChunkDataclass:
    """Test suite for the Chunk dataclass."""

    def test_chunk_has_required_fields(self):
        """Test that Chunk dataclass has all required fields."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import Chunk

        # Act
        chunk = Chunk(
            content="Test content",
            url="https://example.com",
            title="Test Title",
            module="module-1",
            chapter="01-test",
            heading="Test Heading",
            chunk_index=0,
        )

        # Assert
        assert chunk.content == "Test content"
        assert chunk.url == "https://example.com"
        assert chunk.title == "Test Title"
        assert chunk.module == "module-1"
        assert chunk.chapter == "01-test"
        assert chunk.heading == "Test Heading"
        assert chunk.chunk_index == 0

    def test_chunk_allows_none_for_optional_fields(self):
        """Test that Chunk allows None for module and chapter."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import Chunk

        # Act
        chunk = Chunk(
            content="Test content",
            url="https://example.com",
            title="Test Title",
            module=None,
            chapter=None,
            heading="Heading",
            chunk_index=0,
        )

        # Assert
        assert chunk.module is None
        assert chunk.chapter is None


class TestIngestionResult:
    """Test suite for the IngestionResult dataclass."""

    def test_ingestion_result_default_values(self):
        """Test that IngestionResult has correct default values."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import IngestionResult

        # Act
        result = IngestionResult()

        # Assert
        assert result.pages_processed == 0
        assert result.chunks_created == 0
        assert result.chunks_upserted == 0
        assert result.errors == []
        assert result.completed_at is None
        assert result.duration_seconds == 0.0

    def test_ingestion_result_tracks_errors(self):
        """Test that IngestionResult accumulates errors."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import IngestionResult

        # Act
        result = IngestionResult()
        result.errors.append("Error 1")
        result.errors.append("Error 2")

        # Assert
        assert len(result.errors) == 2
        assert "Error 1" in result.errors
        assert "Error 2" in result.errors


class TestContentExtraction:
    """Test suite for HTML content extraction."""

    def test_extract_content_finds_article_markdown(
        self,
        sample_page_html,
    ):
        """Test extraction of content from Docusaurus article.markdown class."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import extract_content

        # Arrange
        with patch("scripts.ingest_book.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.content = sample_page_html.encode()
            mock_response.raise_for_status = MagicMock()

            mock_client_instance = MagicMock()
            mock_client_instance.get.return_value = mock_response

            # Act
            with patch("scripts.ingest_book.time.sleep"):  # Skip rate limiting
                result = extract_content(
                    "https://example.com/page",
                    mock_client_instance,
                )

            # Assert
            assert result is not None
            assert "url" in result
            assert "title" in result
            assert "content" in result
            assert "Introduction to Robotics" in result["title"]
            assert "robot" in result["content"].lower()

    def test_extract_content_removes_nav_elements(
        self,
        sample_page_html,
    ):
        """Test that nav, footer, and other non-content elements are removed."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from scripts.ingest_book import extract_content

        # Arrange
        with patch("scripts.ingest_book.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.content = sample_page_html.encode()
            mock_response.raise_for_status = MagicMock()

            mock_client_instance = MagicMock()
            mock_client_instance.get.return_value = mock_response

            # Act
            with patch("scripts.ingest_book.time.sleep"):
                result = extract_content(
                    "https://example.com/page",
                    mock_client_instance,
                )

            # Assert
            if result:
                assert "Navigation" not in result["content"]
                assert "Footer content" not in result["content"]
