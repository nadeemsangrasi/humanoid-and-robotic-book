# Research: RAG Textbook Chatbot Backend

**Feature Branch**: `001-rag-chatbot-backend`
**Date**: 2025-12-12
**Status**: Complete

---

## 1. OpenAI Agent SDK + Google Gemini Integration

### Decision
Use OpenAI Agent SDK with Google Gemini via the OpenAI compatibility endpoint.

### Configuration

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool

# Google Gemini via OpenAI compatibility layer
client = AsyncOpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Create agent with Gemini model
agent = Agent(
    name="textbook_assistant",
    model="gemini-2.0-flash",  # or gemini-1.5-flash
    instructions="You are a helpful assistant that answers questions about the Physical AI & Humanoid Robotics textbook. Always cite your sources.",
    tools=[search_textbook],  # function tools
    model_settings={"temperature": 0.3}
)
```

### Tool Registration Pattern

```python
from agents import function_tool
from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    query: str = Field(description="The search query to find relevant textbook content")
    k: int = Field(default=5, description="Number of results to return")

@function_tool
async def search_textbook(query: str, k: int = 5) -> str:
    """Search the textbook content for relevant passages."""
    # Implementation calls Qdrant
    results = await qdrant_service.search(query, k=k, threshold=0.7)
    return format_results(results)
```

### Running the Agent

```python
from agents import Runner

async def chat(question: str) -> str:
    result = await Runner.run(agent, question)
    return result.final_output
```

### Rationale
- OpenAI Agent SDK provides clean abstractions for tool-based agents
- Google Gemini supports OpenAI compatibility API with function calling
- `gemini-2.0-flash` offers good performance/cost balance for RAG tasks
- Function tools with Pydantic models provide type safety

### Alternatives Considered
1. **Direct Gemini SDK**: More verbose, no agent abstraction
2. **LangChain Agents**: Heavier dependency, more complex
3. **Custom implementation**: Too much boilerplate

---

## 2. LangChain Gemini Embeddings

### Decision
Use `GoogleGenerativeAIEmbeddings` from `langchain-google-genai` with `text-embedding-004` model.

### Configuration

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=os.environ["GOOGLE_API_KEY"],
    task_type="retrieval_document"  # or "retrieval_query" for queries
)
```

### Model Details
- **Model**: `models/text-embedding-004` (latest, recommended)
- **Dimensions**: 768
- **Task Types**: `retrieval_document`, `retrieval_query`, `semantic_similarity`
- **Rate Limits**: 1500 RPM, 1M tokens/minute (free tier)

### Batch Processing

```python
# Single embedding
vector = embeddings.embed_query("What is inverse kinematics?")

# Batch embeddings (documents)
vectors = embeddings.embed_documents([
    "Inverse kinematics is...",
    "Forward kinematics computes...",
])
```

### Error Handling

```python
from tenacity import retry, stop_after_attempt, wait_exponential
from google.api_core.exceptions import ResourceExhausted

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(ResourceExhausted)
)
async def embed_with_retry(text: str) -> list[float]:
    return embeddings.embed_query(text)
```

### Rationale
- LangChain provides consistent interface for embeddings
- `text-embedding-004` is the latest model with best quality
- 768 dimensions matches Qdrant collection configuration
- Built-in batching support

### Alternatives Considered
1. **Direct Gemini API**: More verbose, manual batching
2. **models/gemini-embedding-001**: Older model, same dimensions
3. **OpenAI embeddings**: Prohibited by constraints

---

## 3. Qdrant Client Setup

### Decision
Use `qdrant-client` with Qdrant Cloud (free tier), cosine similarity, and deterministic UUIDs.

### Client Configuration

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os

client = QdrantClient(
    url=os.environ["QDRANT_URL"],
    api_key=os.environ["QDRANT_API_KEY"],
)
```

### Collection Creation

```python
from qdrant_client.models import Distance, VectorParams

COLLECTION_NAME = "book_chunks"
VECTOR_SIZE = 768

# Create collection (idempotent check)
collections = client.get_collections().collections
if COLLECTION_NAME not in [c.name for c in collections]:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )
```

### Upsert with Deterministic IDs

```python
import hashlib
import uuid

def generate_point_id(url: str, chunk_index: int) -> str:
    """Generate deterministic UUID from URL and chunk index."""
    content = f"{url}::{chunk_index}"
    hash_bytes = hashlib.md5(content.encode()).digest()
    return str(uuid.UUID(bytes=hash_bytes))

# Upsert points
points = [
    PointStruct(
        id=generate_point_id(chunk.url, chunk.index),
        vector=chunk.embedding,
        payload={
            "url": chunk.url,
            "title": chunk.title,
            "module": chunk.module,
            "chapter": chunk.chapter,
            "heading": chunk.heading,
            "content": chunk.content,
            "chunk_index": chunk.index
        }
    )
    for chunk in chunks
]

client.upsert(collection_name=COLLECTION_NAME, points=points)
```

### Search with Threshold

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

async def search(
    query_vector: list[float],
    k: int = 5,
    threshold: float = 0.7,
    module_filter: str | None = None
) -> list[dict]:
    """Search with similarity threshold and optional module filter."""

    filter_conditions = None
    if module_filter:
        filter_conditions = Filter(
            must=[
                FieldCondition(
                    key="module",
                    match=MatchValue(value=module_filter)
                )
            ]
        )

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=k,
        score_threshold=threshold,
        query_filter=filter_conditions
    )

    return [
        {
            "content": hit.payload["content"],
            "url": hit.payload["url"],
            "title": hit.payload["title"],
            "score": hit.score
        }
        for hit in results
    ]
```

### Rationale
- Qdrant Cloud free tier: 1GB storage, sufficient for ~500 chunks
- Cosine similarity standard for text embeddings
- Deterministic UUIDs enable idempotent re-indexing
- `score_threshold` parameter native to Qdrant search

### Alternatives Considered
1. **Pinecone**: No free tier for production
2. **ChromaDB**: Better for local, not ideal for cloud
3. **Milvus**: More complex setup

---

## 4. Sitemap Crawling & Content Extraction

### Decision
Use `requests` + `BeautifulSoup4` with rate limiting and Docusaurus-specific selectors.

### Sitemap Parsing

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    """Extract all page URLs from sitemap.xml."""
    response = requests.get(sitemap_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    return urls
```

### Content Extraction (Docusaurus-specific)

```python
import time

def extract_content(url: str) -> dict:
    """Extract main content from Docusaurus page."""
    time.sleep(0.5)  # Rate limiting: 2 requests/second

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    # Docusaurus main content selector
    main = soup.select_one("article.markdown") or soup.select_one("main")

    # Remove non-content elements
    for selector in ["nav", "footer", "aside", ".sidebar", ".toc", ".pagination"]:
        for elem in main.select(selector):
            elem.decompose()

    # Extract metadata
    title = soup.select_one("h1")?.get_text(strip=True) or ""

    # Extract module/chapter from URL path
    path_parts = url.split("/")
    module = next((p for p in path_parts if p.startswith("module-")), None)
    chapter = next((p for p in path_parts if p[0].isdigit()), None)

    return {
        "url": url,
        "title": title,
        "module": module,
        "chapter": chapter,
        "content": main.get_text(separator="\n", strip=True)
    }
```

### Chunking Algorithm

```python
import tiktoken

def chunk_content(
    content: str,
    url: str,
    title: str,
    module: str,
    chapter: str,
    min_tokens: int = 500,
    max_tokens: int = 1000
) -> list[dict]:
    """Split content into chunks of 500-1000 tokens."""

    encoder = tiktoken.get_encoding("cl100k_base")

    # Split by headings first
    sections = re.split(r'\n(?=#{1,3}\s)', content)

    chunks = []
    current_chunk = ""
    current_heading = title

    for section in sections:
        # Extract heading if present
        heading_match = re.match(r'^(#{1,3})\s+(.+)', section)
        if heading_match:
            current_heading = heading_match.group(2)

        section_tokens = len(encoder.encode(section))
        current_tokens = len(encoder.encode(current_chunk))

        if current_tokens + section_tokens <= max_tokens:
            current_chunk += "\n" + section
        else:
            if current_tokens >= min_tokens:
                chunks.append({
                    "content": current_chunk.strip(),
                    "heading": current_heading,
                    "url": url,
                    "title": title,
                    "module": module,
                    "chapter": chapter,
                    "chunk_index": len(chunks)
                })
            current_chunk = section

    # Don't forget the last chunk
    if len(encoder.encode(current_chunk)) >= min_tokens:
        chunks.append({
            "content": current_chunk.strip(),
            "heading": current_heading,
            "url": url,
            "title": title,
            "module": module,
            "chapter": chapter,
            "chunk_index": len(chunks)
        })

    return chunks
```

### Rationale
- Simple, well-tested libraries (requests, BeautifulSoup)
- Rate limiting prevents overwhelming the textbook server
- Docusaurus-specific selectors for clean extraction
- Token-based chunking ensures consistent chunk sizes

### Alternatives Considered
1. **Scrapy**: Overkill for 23 pages
2. **Playwright**: Unnecessary for static site
3. **LangChain text splitters**: Less control over boundaries

---

## 5. Docker + Hugging Face Spaces Deployment

### Decision
Multi-stage Dockerfile with Python 3.11-slim, port 7860, and HF Spaces README metadata.

### Dockerfile (Multi-stage)

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels and install
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy application code
COPY app/ ./app/

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Expose port (HF Spaces requirement)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### HF Spaces README.md

```yaml
---
title: Physical AI Textbook Chatbot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Physical AI & Humanoid Robotics Textbook Chatbot

Ask questions about the textbook and get answers with source citations.

## API Endpoints

- `POST /chat` - Ask a question
- `GET /health` - Health check
```

### docker-compose.yml (Local Development)

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "7860:7860"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - QDRANT_URL=${QDRANT_URL}
      - QDRANT_API_KEY=${QDRANT_API_KEY}
    volumes:
      - ./app:/app/app:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key for Gemini | Yes |
| `QDRANT_URL` | Qdrant Cloud cluster URL | Yes |
| `QDRANT_API_KEY` | Qdrant Cloud API key | Yes |

### Rationale
- Multi-stage build reduces image size (~200MB vs ~800MB)
- Python 3.11-slim is the standard for production
- Port 7860 is mandatory for HF Spaces
- Non-root user improves security
- Health check enables proper orchestration

### Alternatives Considered
1. **Alpine base**: Compatibility issues with some packages
2. **Single-stage build**: Larger image size
3. **Poetry**: More complex, unnecessary for this project

---

## Summary of Decisions

| Area | Decision | Key Rationale |
|------|----------|---------------|
| Agent Framework | OpenAI Agent SDK | Clean abstractions, tool support |
| LLM | Gemini 2.0 Flash via OpenAI compat | Required by constraints, good performance |
| Embeddings | text-embedding-004 via LangChain | Latest model, 768 dims |
| Vector DB | Qdrant Cloud (free tier) | Native threshold search, generous free tier |
| Ingestion | CLI script with BeautifulSoup | Simple, controllable |
| Chunking | Token-based (500-1000) | Consistent sizes |
| Deployment | Docker + HF Spaces | Required by constraints |
| ID Generation | Deterministic UUID from URL+index | Enables idempotent upserts |

---

## Unresolved Items

None. All technical unknowns have been resolved.
