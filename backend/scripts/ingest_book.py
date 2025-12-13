#!/usr/bin/env python3
"""Textbook content ingestion script for RAG chatbot.

This script:
1. Fetches the sitemap from the published textbook
2. Extracts content from each page
3. Chunks content into 500-1000 token segments
4. Embeds chunks using Google Gemini embeddings
5. Upserts to Qdrant with deterministic IDs

Usage:
    python scripts/ingest-book.py

Environment:
    Requires GOOGLE_API_KEY, QDRANT_URL, QDRANT_API_KEY in .env
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import hashlib
import re
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Generator

import httpx
import tiktoken
from bs4 import BeautifulSoup
from qdrant_client.models import PointStruct

from app.config import get_settings
from app.services.embedding import get_embedding_service
from app.services.retrieval import get_retriever, QdrantRetriever
from app.utils.logging import setup_logging, get_logger

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Constants
SITEMAP_URL = "https://nadeemsangrasi.github.io/humanoid-and-robotic-book/sitemap.xml"
MIN_TOKENS = 500
MAX_TOKENS = 1000
RATE_LIMIT_DELAY = 0.5  # seconds between requests
EMBEDDING_BATCH_SIZE = 50
UPSERT_BATCH_SIZE = 100


@dataclass
class Chunk:
    """A chunk of textbook content with metadata."""
    content: str
    url: str
    title: str
    module: str | None
    chapter: str | None
    heading: str
    chunk_index: int


@dataclass
class IngestionResult:
    """Result of the ingestion process."""
    pages_processed: int = 0
    chunks_created: int = 0
    chunks_upserted: int = 0
    errors: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    duration_seconds: float = 0.0


def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    """Extract all page URLs from sitemap.xml.

    Args:
        sitemap_url: URL to the sitemap.xml file

    Returns:
        List of page URLs found in the sitemap
    """
    logger.info(f"Fetching sitemap from: {sitemap_url}")

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(sitemap_url)
            response.raise_for_status()
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch sitemap: {e}")
        raise

    soup = BeautifulSoup(response.content, "xml")
    urls = [loc.text.strip() for loc in soup.find_all("loc") if loc.text]

    logger.info(f"Found {len(urls)} pages in sitemap")
    return urls


def extract_metadata_from_url(url: str) -> tuple[str | None, str | None]:
    """Extract module and chapter from URL path.

    Args:
        url: Page URL

    Returns:
        Tuple of (module, chapter) extracted from URL path
    """
    path_parts = url.split("/")

    # Look for module pattern like "module-1-ros2"
    module = next((p for p in path_parts if p.startswith("module-")), None)

    # Look for chapter pattern like "02-nodes-and-topics" (starts with digit)
    chapter = None
    for part in path_parts:
        if part and part[0].isdigit() and "-" in part:
            chapter = part
            break

    return module, chapter


def extract_content(url: str, client: httpx.Client) -> dict | None:
    """Extract main content from Docusaurus page.

    Args:
        url: Page URL to fetch
        client: HTTP client for making requests

    Returns:
        Dict with url, title, module, chapter, content or None on error
    """
    logger.debug(f"Extracting content from: {url}")

    # Rate limiting
    time.sleep(RATE_LIMIT_DELAY)

    try:
        response = client.get(url)
        response.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Find main content - Docusaurus specific selectors
    main = soup.select_one("article.markdown")
    if not main:
        main = soup.select_one("article")
    if not main:
        main = soup.select_one("main")
    if not main:
        main = soup.select_one(".docMainContainer")
    if not main:
        logger.warning(f"Could not find main content in {url}")
        return None

    # Remove non-content elements
    selectors_to_remove = [
        "nav",
        "footer",
        "aside",
        ".sidebar",
        ".toc",
        ".tocCollapsible",
        ".pagination-nav",
        ".theme-doc-footer",
        ".theme-doc-toc-mobile",
        ".breadcrumbs",
        "script",
        "style",
    ]
    for selector in selectors_to_remove:
        for elem in main.select(selector):
            elem.decompose()

    # Extract title
    title_elem = soup.select_one("h1")
    title = title_elem.get_text(strip=True) if title_elem else ""

    # Extract module/chapter from URL
    module, chapter = extract_metadata_from_url(url)

    # Get text content
    content = main.get_text(separator="\n", strip=True)

    # Clean up excessive whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r' {2,}', ' ', content)

    if not content.strip():
        logger.warning(f"Empty content extracted from {url}")
        return None

    return {
        "url": url,
        "title": title,
        "module": module,
        "chapter": chapter,
        "content": content,
    }


def chunk_content(
    content: str,
    url: str,
    title: str,
    module: str | None,
    chapter: str | None,
) -> list[Chunk]:
    """Split content into chunks of 500-1000 tokens.

    Uses tiktoken for accurate token counting and splits on heading boundaries
    when possible to preserve semantic coherence.

    Args:
        content: Full page content
        url: Source URL
        title: Page title
        module: Module identifier
        chapter: Chapter identifier

    Returns:
        List of Chunk objects
    """
    encoder = tiktoken.get_encoding("cl100k_base")

    # Split by headings (markdown style)
    sections = re.split(r'\n(?=#{1,6}\s)', content)

    chunks: list[Chunk] = []
    current_chunk = ""
    current_heading = title

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Extract heading if present
        heading_match = re.match(r'^(#{1,6})\s+(.+?)(?:\n|$)', section)
        if heading_match:
            current_heading = heading_match.group(2).strip()

        section_tokens = len(encoder.encode(section))
        current_tokens = len(encoder.encode(current_chunk)) if current_chunk else 0

        # If adding this section would exceed max tokens
        if current_tokens + section_tokens > MAX_TOKENS:
            # Save current chunk if it meets minimum
            if current_tokens >= MIN_TOKENS:
                chunks.append(Chunk(
                    content=current_chunk.strip(),
                    url=url,
                    title=title,
                    module=module,
                    chapter=chapter,
                    heading=current_heading,
                    chunk_index=len(chunks),
                ))
                current_chunk = section
            elif section_tokens > MAX_TOKENS:
                # Section itself is too large, need to split it
                if current_chunk:
                    current_chunk += "\n\n" + section
                else:
                    current_chunk = section

                # Force split the oversized content
                words = current_chunk.split()
                temp_chunk = ""
                for word in words:
                    test_chunk = temp_chunk + " " + word if temp_chunk else word
                    if len(encoder.encode(test_chunk)) > MAX_TOKENS:
                        if len(encoder.encode(temp_chunk)) >= MIN_TOKENS:
                            chunks.append(Chunk(
                                content=temp_chunk.strip(),
                                url=url,
                                title=title,
                                module=module,
                                chapter=chapter,
                                heading=current_heading,
                                chunk_index=len(chunks),
                            ))
                        temp_chunk = word
                    else:
                        temp_chunk = test_chunk
                current_chunk = temp_chunk
            else:
                # Current chunk too small, combine with section
                current_chunk = current_chunk + "\n\n" + section if current_chunk else section
        else:
            # Add section to current chunk
            current_chunk = current_chunk + "\n\n" + section if current_chunk else section

    # Don't forget the last chunk
    if current_chunk:
        final_tokens = len(encoder.encode(current_chunk))
        if final_tokens >= MIN_TOKENS:
            chunks.append(Chunk(
                content=current_chunk.strip(),
                url=url,
                title=title,
                module=module,
                chapter=chapter,
                heading=current_heading,
                chunk_index=len(chunks),
            ))
        elif chunks and final_tokens > 0:
            # Append to last chunk if too small
            last_chunk = chunks[-1]
            combined = last_chunk.content + "\n\n" + current_chunk
            chunks[-1] = Chunk(
                content=combined.strip(),
                url=last_chunk.url,
                title=last_chunk.title,
                module=last_chunk.module,
                chapter=last_chunk.chapter,
                heading=last_chunk.heading,
                chunk_index=last_chunk.chunk_index,
            )
        elif final_tokens > 0:
            # First and only chunk, keep it even if small
            chunks.append(Chunk(
                content=current_chunk.strip(),
                url=url,
                title=title,
                module=module,
                chapter=chapter,
                heading=current_heading,
                chunk_index=len(chunks),
            ))

    return chunks


def generate_point_id(url: str, chunk_index: int) -> str:
    """Generate deterministic UUID from URL and chunk index.

    Args:
        url: Source URL
        chunk_index: Index of chunk within the page

    Returns:
        UUID string for Qdrant point ID
    """
    content = f"{url}::{chunk_index}"
    hash_bytes = hashlib.md5(content.encode()).digest()
    return str(uuid.UUID(bytes=hash_bytes))


async def embed_and_upsert_chunks(
    chunks: list[Chunk],
    embedding_batch_size: int = EMBEDDING_BATCH_SIZE,
    upsert_batch_size: int = UPSERT_BATCH_SIZE,
) -> int:
    """Embed chunks and upsert to Qdrant.

    Args:
        chunks: List of Chunk objects to process
        embedding_batch_size: Number of texts to embed at once
        upsert_batch_size: Number of points to upsert at once

    Returns:
        Number of points successfully upserted
    """
    if not chunks:
        return 0

    embedding_service = get_embedding_service()
    retriever = get_retriever()

    logger.info(f"Embedding and upserting {len(chunks)} chunks")

    points: list[PointStruct] = []
    upserted_count = 0

    # Process chunks in batches for embedding
    for i in range(0, len(chunks), embedding_batch_size):
        batch = chunks[i:i + embedding_batch_size]
        texts = [chunk.content for chunk in batch]

        logger.debug(f"Embedding batch {i // embedding_batch_size + 1}")

        try:
            embeddings = embedding_service.embed_documents(texts)
        except Exception as e:
            logger.error(f"Failed to embed batch: {e}")
            continue

        # Create points for this batch
        for chunk, embedding in zip(batch, embeddings):
            point_id = generate_point_id(chunk.url, chunk.chunk_index)
            points.append(PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "content": chunk.content,
                    "url": chunk.url,
                    "title": chunk.title,
                    "module": chunk.module,
                    "chapter": chunk.chapter,
                    "heading": chunk.heading,
                    "chunk_index": chunk.chunk_index,
                },
            ))

        # Upsert when we have enough points
        if len(points) >= upsert_batch_size:
            try:
                retriever.upsert_points(points[:upsert_batch_size])
                upserted_count += len(points[:upsert_batch_size])
                points = points[upsert_batch_size:]
                logger.info(f"Upserted {upserted_count} points so far")
            except Exception as e:
                logger.error(f"Failed to upsert batch: {e}")

    # Upsert remaining points
    if points:
        try:
            retriever.upsert_points(points)
            upserted_count += len(points)
            logger.info(f"Upserted final batch, total: {upserted_count}")
        except Exception as e:
            logger.error(f"Failed to upsert final batch: {e}")

    return upserted_count


async def run_ingestion(sitemap_url: str = SITEMAP_URL) -> IngestionResult:
    """Run the complete ingestion pipeline.

    Args:
        sitemap_url: URL to the sitemap.xml file

    Returns:
        IngestionResult with statistics and any errors
    """
    result = IngestionResult()
    result.started_at = datetime.now()

    logger.info("Starting textbook ingestion")

    # Fetch sitemap
    try:
        urls = fetch_sitemap_urls(sitemap_url)
    except Exception as e:
        result.errors.append(f"Failed to fetch sitemap: {e}")
        result.completed_at = datetime.now()
        result.duration_seconds = (result.completed_at - result.started_at).total_seconds()
        return result

    all_chunks: list[Chunk] = []

    # Process each page
    with httpx.Client(timeout=30.0) as client:
        for i, url in enumerate(urls):
            logger.info(f"Processing page {i + 1}/{len(urls)}: {url}")

            try:
                page_data = extract_content(url, client)
                if not page_data:
                    result.errors.append(f"Failed to extract content from {url}")
                    continue

                chunks = chunk_content(
                    content=page_data["content"],
                    url=page_data["url"],
                    title=page_data["title"],
                    module=page_data["module"],
                    chapter=page_data["chapter"],
                )

                logger.info(f"  - Created {len(chunks)} chunks")
                all_chunks.extend(chunks)
                result.pages_processed += 1

            except Exception as e:
                error_msg = f"Error processing {url}: {e}"
                logger.error(error_msg)
                result.errors.append(error_msg)

    result.chunks_created = len(all_chunks)
    logger.info(f"Total chunks created: {result.chunks_created}")

    # Embed and upsert all chunks
    if all_chunks:
        try:
            result.chunks_upserted = await embed_and_upsert_chunks(all_chunks)
        except Exception as e:
            error_msg = f"Failed during embedding/upsert: {e}"
            logger.error(error_msg)
            result.errors.append(error_msg)

    result.completed_at = datetime.now()
    result.duration_seconds = (result.completed_at - result.started_at).total_seconds()

    logger.info(
        "Ingestion complete",
        extra={
            "pages_processed": result.pages_processed,
            "chunks_created": result.chunks_created,
            "chunks_upserted": result.chunks_upserted,
            "errors": len(result.errors),
            "duration_seconds": result.duration_seconds,
        }
    )

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Physical AI & Humanoid Robotics Textbook Ingestion")
    print("=" * 60)
    print()

    result = asyncio.run(run_ingestion())

    print()
    print("=" * 60)
    print("Ingestion Complete!")
    print("=" * 60)
    print(f"  Pages processed:  {result.pages_processed}")
    print(f"  Chunks created:   {result.chunks_created}")
    print(f"  Chunks upserted:  {result.chunks_upserted}")
    print(f"  Duration:         {result.duration_seconds:.2f} seconds")

    if result.errors:
        print(f"  Errors:           {len(result.errors)}")
        print()
        print("Errors encountered:")
        for i, error in enumerate(result.errors[:10], 1):
            print(f"  {i}. {error}")
        if len(result.errors) > 10:
            print(f"  ... and {len(result.errors) - 10} more")

    print()

    # Exit with error code if there were significant failures
    if result.chunks_upserted == 0 and result.chunks_created > 0:
        print("ERROR: No chunks were upserted!")
        sys.exit(1)
    elif result.pages_processed == 0:
        print("ERROR: No pages were processed!")
        sys.exit(1)

    sys.exit(0)
