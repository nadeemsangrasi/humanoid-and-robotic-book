# Data Model: RAG Textbook Chatbot Backend

**Feature Branch**: `001-rag-chatbot-backend`
**Date**: 2025-12-12
**Status**: Complete

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         TextbookChunk                            │
│─────────────────────────────────────────────────────────────────│
│ id: UUID (deterministic from url + chunk_index)                  │
│ content: str                                                     │
│ embedding: vector[768]                                           │
│ url: str                                                         │
│ title: str                                                       │
│ module: str | null                                               │
│ chapter: str | null                                              │
│ heading: str                                                     │
│ chunk_index: int                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ retrieved by
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         ChatRequest                              │
│─────────────────────────────────────────────────────────────────│
│ query: str (required, 1-2000 chars)                              │
│ k: int (optional, default=5, 1-10)                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ produces
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         ChatResponse                             │
│─────────────────────────────────────────────────────────────────│
│ answer: str                                                      │
│ citations: list[Citation]                                        │
│ metadata: ResponseMetadata                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ contains
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Citation                                │
│─────────────────────────────────────────────────────────────────│
│ url: str                                                         │
│ title: str                                                       │
│ snippet: str (excerpt from content, max 200 chars)               │
│ score: float (0.0-1.0)                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Entity Definitions

### TextbookChunk

A searchable unit of textbook content stored in the vector database.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary key, deterministic | Generated from `md5(url::chunk_index)` |
| `content` | string | 500-1000 tokens | The text content of the chunk |
| `embedding` | float[768] | Required | Vector representation for similarity search |
| `url` | string | Valid URL | Source page URL in the textbook |
| `title` | string | Non-empty | Page title |
| `module` | string | Nullable | Module identifier (e.g., "module-1-ros2") |
| `chapter` | string | Nullable | Chapter identifier (e.g., "02-nodes-and-topics") |
| `heading` | string | Non-empty | Section heading this chunk belongs to |
| `chunk_index` | integer | >= 0 | Position of chunk within the page |

**Storage**: Qdrant collection `book_chunks`

**ID Generation**:
```python
id = uuid.UUID(bytes=hashlib.md5(f"{url}::{chunk_index}".encode()).digest())
```

---

### ChatRequest

User's question submission to the chat endpoint.

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `query` | string | 1-2000 chars, required | - | The user's question |
| `k` | integer | 1-10, optional | 5 | Maximum results to retrieve |

**Validation Rules**:
- `query` must not be empty or whitespace-only
- `query` must not exceed 2000 characters
- `k` must be between 1 and 10 inclusive

**Pydantic Schema**:
```python
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    k: int = Field(default=5, ge=1, le=10)

    @field_validator("query")
    @classmethod
    def query_not_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace")
        return v.strip()
```

---

### ChatResponse

The system's response to a user question.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `answer` | string | Non-empty | Synthesized answer from retrieved content |
| `citations` | Citation[] | 0-5 items | Source citations for the answer |
| `metadata` | ResponseMetadata | Required | Response metadata |

**Pydantic Schema**:
```python
class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    metadata: ResponseMetadata
```

---

### Citation

A reference to a source passage used in an answer.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `url` | string | Valid URL | Source page URL |
| `title` | string | Non-empty | Page title |
| `snippet` | string | Max 200 chars | Excerpt from the relevant passage |
| `score` | float | 0.0-1.0 | Similarity score from vector search |

**Pydantic Schema**:
```python
class Citation(BaseModel):
    url: str
    title: str
    snippet: str = Field(max_length=200)
    score: float = Field(ge=0.0, le=1.0)
```

---

### ResponseMetadata

Metadata about the response generation.

| Field | Type | Description |
|-------|------|-------------|
| `chunks_retrieved` | integer | Number of chunks found above threshold |
| `processing_time_ms` | integer | Total processing time in milliseconds |
| `model` | string | LLM model used for answer generation |

**Pydantic Schema**:
```python
class ResponseMetadata(BaseModel):
    chunks_retrieved: int
    processing_time_ms: int
    model: str
```

---

### HealthStatus

Health check response for monitoring.

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "healthy" or "unhealthy" |
| `timestamp` | datetime | Current server time (ISO 8601) |
| `version` | string | Application version |
| `services` | dict | Status of dependent services |

**Pydantic Schema**:
```python
class ServiceStatus(BaseModel):
    status: Literal["healthy", "unhealthy", "unknown"]
    latency_ms: int | None = None

class HealthStatus(BaseModel):
    status: Literal["healthy", "unhealthy"]
    timestamp: datetime
    version: str
    services: dict[str, ServiceStatus]
```

---

### IngestionResult

Outcome of a content ingestion run (for CLI script output).

| Field | Type | Description |
|-------|------|-------------|
| `pages_processed` | integer | Number of pages crawled |
| `chunks_created` | integer | Total chunks generated |
| `chunks_upserted` | integer | Chunks written to Qdrant |
| `errors` | list[str] | Any errors encountered |
| `started_at` | datetime | Ingestion start time |
| `completed_at` | datetime | Ingestion end time |
| `duration_seconds` | float | Total processing time |

**Pydantic Schema**:
```python
class IngestionResult(BaseModel):
    pages_processed: int
    chunks_created: int
    chunks_upserted: int
    errors: list[str] = Field(default_factory=list)
    started_at: datetime
    completed_at: datetime
    duration_seconds: float
```

---

### ErrorResponse

Standard error response format.

| Field | Type | Description |
|-------|------|-------------|
| `error` | string | Error type/code |
| `message` | string | Human-readable error message |
| `details` | dict | Additional error context (optional) |

**Pydantic Schema**:
```python
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: dict[str, Any] | None = None
```

**Error Types**:
- `validation_error`: Invalid input (400)
- `not_found`: No relevant content found (200 with empty citations)
- `service_unavailable`: External service down (503)
- `rate_limited`: API rate limit exceeded (429)
- `internal_error`: Unexpected server error (500)

---

## State Transitions

### ChatRequest Lifecycle

```
                    ┌─────────────┐
                    │  Received   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Validated  │──────────────► ValidationError (400)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Embedded   │──────────────► ServiceUnavailable (503)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Retrieved  │──────────────► ServiceUnavailable (503)
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
       ┌──────▼──────┐          ┌───────▼──────┐
       │  No Results │          │ Has Results  │
       └──────┬──────┘          └───────┬──────┘
              │                         │
       ┌──────▼──────┐          ┌───────▼──────┐
       │  No Answer  │          │  Synthesized │──► ServiceUnavailable (503)
       │  Response   │          └───────┬──────┘
       └─────────────┘                  │
                                 ┌──────▼──────┐
                                 │  Response   │
                                 │  with Cites │
                                 └─────────────┘
```

---

## Indexes and Constraints

### Qdrant Collection Configuration

```python
VectorParams(
    size=768,
    distance=Distance.COSINE
)
```

### Payload Indexes (Qdrant)

| Field | Index Type | Purpose |
|-------|------------|---------|
| `module` | Keyword | Filter by module |
| `chapter` | Keyword | Filter by chapter |
| `url` | Keyword | Deduplication check |

---

## Data Volume Estimates

| Metric | Estimate | Calculation |
|--------|----------|-------------|
| Pages | 23 | From sitemap |
| Avg chunks/page | 15-20 | ~3000 words/page ÷ 750 tokens/chunk |
| Total chunks | 350-500 | 23 × 17.5 |
| Vector size | 768 × 4 bytes | 3 KB per vector |
| Payload size | ~2 KB | Content + metadata |
| Total storage | ~2.5 MB | Well within Qdrant free tier (1 GB) |
