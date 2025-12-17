# Implementation Plan: RAG Textbook Chatbot Backend

**Branch**: `001-rag-chatbot-backend` | **Date**: 2025-12-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot-backend/spec.md`

---

## Summary

Build a RAG (Retrieval-Augmented Generation) chatbot backend for the Physical AI & Humanoid Robotics textbook. The system will:

1. **Ingest** textbook content from the published sitemap (23 pages)
2. **Chunk** content into 500-1000 token segments with metadata
3. **Embed** chunks using Google Gemini embeddings (768 dimensions)
4. **Store** vectors in Qdrant Cloud (free tier)
5. **Serve** a FastAPI endpoint that uses OpenAI Agent SDK with Gemini to answer questions with citations
6. **Deploy** as a Docker container on Hugging Face Spaces

**MVP User Stories (5 total):**
| US | Name | Priority |
|----|------|----------|
| US1 | Ask a question and receive a cited answer | P1 |
| US2 | Ingest textbook content from published website | P1 |
| US3 | Deploy backend to production | P1 |
| US4 | Configure environment for production | P1 |
| US5 | Run backend locally for development | P2 |

---

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**:
- FastAPI 0.109+ (web framework)
- Uvicorn 0.27+ (ASGI server)
- openai-agents 0.0.3+ (agent orchestration)
- langchain-google-genai 2.0+ (embeddings)
- qdrant-client 1.12+ (vector database)
- BeautifulSoup4 4.12+ (HTML parsing)
- httpx 0.27+ (async HTTP client)
- pydantic 2.5+ (data validation)
- tenacity 8.2+ (retry logic)

**Storage**: Qdrant Cloud (free tier) - collection `book_chunks`
**Testing**: pytest 8.0+ with httpx for async API testing
**Target Platform**: Hugging Face Spaces (Docker mode, port 7860)
**Project Type**: Backend service (single project)
**Performance Goals**: <5s response time (p95), 10 concurrent users
**Constraints**: Free tier only (Qdrant, HF Spaces, Gemini API)
**Scale/Scope**: 23 textbook pages, ~350-500 chunks, ~2.5MB storage

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Evidence |
|------|--------|----------|
| Uses Google Gemini models only (NO OpenAI for inference) | ✅ PASS | Using `gemini-2.0-flash` via OpenAI compatibility layer |
| Deploys to Hugging Face Spaces only (NO Vercel/Render/AWS) | ✅ PASS | Docker deployment to HF Spaces specified |
| Uses Qdrant free tier | ✅ PASS | Qdrant Cloud free tier (1GB) |
| Returns source URLs for citations | ✅ PASS | Citation schema includes URL field |
| Follows Context7 MCP for documentation | ✅ PASS | MCP mandatory in implementation |
| Backend uses FastAPI + Uvicorn + OpenAI Agent SDK | ✅ PASS | All specified in dependencies |
| Content suitable for RAG indexing | ✅ PASS | Chunking preserves semantic coherence |

**Result**: All gates PASS. Proceeding with implementation.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot-backend/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0: Technical research
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Developer setup guide
├── contracts/
│   └── api-contracts.md # Phase 1: API specifications
├── checklists/
│   └── requirements.md  # Specification quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Environment configuration (pydantic-settings)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py                # POST /chat endpoint
│   │   └── health.py              # GET /health endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py    # OpenAI Agent SDK + Gemini config
│   │   │   └── tools.py           # search_textbook function tool
│   │   ├── embedding/
│   │   │   ├── __init__.py
│   │   │   └── embedding.py       # GoogleGenerativeAIEmbeddings wrapper
│   │   └── retrieval/
│   │       ├── __init__.py
│   │       └── qdrant_client.py   # Qdrant search with threshold
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chat.py                # ChatRequest, ChatResponse, Citation
│   │   └── health.py              # HealthStatus, ServiceStatus
│   └── utils/
│       ├── __init__.py
│       └── logging.py             # Structured logging config
├── scripts/
│   └── ingest-book.py             # CLI: sitemap → chunks → Qdrant
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures (mock clients)
│   ├── test_chat.py               # Chat endpoint tests
│   ├── test_health.py             # Health endpoint tests
│   └── test_ingestion.py          # Ingestion script tests
├── Dockerfile                      # Multi-stage production build
├── docker-compose.yml              # Local development
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
├── pyproject.toml                  # Project metadata + tool config
├── .env.example                    # Environment template
└── README.md                       # HF Spaces metadata + docs
```

**Structure Decision**: Single backend project. Frontend (ChatKit UI) is a separate feature branch and will connect to this API.

---

## Agent/Skill Assignment

| Component | Agent | Skill | Priority |
|-----------|-------|-------|----------|
| FastAPI scaffolding | backend-architect-and-sdk-agent | fastapi-scaffolding | P1 |
| Agent SDK + Gemini | backend-architect-and-sdk-agent | gemini-agent-sdk-setup | P1 |
| Chat endpoint | backend-architect-and-sdk-agent | rag-chat-endpoint | P1 |
| Sitemap ingestion | RAG-pipeline-and-retrieval-agent | book-ingestion | P1 |
| Embeddings | RAG-pipeline-and-retrieval-agent | embedding-pipeline | P1 |
| Qdrant retrieval | RAG-pipeline-and-retrieval-agent | qdrant-retrieval-tool | P1 |
| Dockerfile | deployment-agent | dockerfile-builder | P1 |
| HF Spaces config | deployment-agent | huggingface-config | P1 |
| Local dev scripts | deployment-agent | local-dev-runner | P2 |

---

## Implementation Phases

### Phase 1: Core Infrastructure (P1)

**Goal**: Deployable backend with health check

1. Create `backend/` directory structure
2. Implement `app/config.py` with pydantic-settings
3. Implement `app/main.py` with FastAPI app, CORS, routers
4. Implement `app/routers/health.py` with service checks
5. Implement `app/schemas/health.py`
6. Create Dockerfile (multi-stage)
7. Create docker-compose.yml
8. Create .env.example and README.md

**Deliverables**: Health check endpoint working locally

### Phase 2: Vector Database (P1)

**Goal**: Qdrant collection ready for ingestion

1. Implement `app/services/retrieval/qdrant_client.py`
2. Collection creation with 768 dims, cosine similarity
3. Search method with score_threshold (0.7)
4. Deterministic ID generation for upserts

**Deliverables**: Qdrant client with create/search/upsert

### Phase 3: Embeddings (P1)

**Goal**: Embedding service for queries and documents

1. Implement `app/services/embedding/embedding.py`
2. GoogleGenerativeAIEmbeddings configuration
3. Single text and batch embedding methods
4. Error handling for rate limits

**Deliverables**: Embedding service tested

### Phase 4: Content Ingestion (P1)

**Goal**: CLI script to populate Qdrant

1. Implement `scripts/ingest-book.py`
2. Sitemap parsing
3. HTML content extraction (Docusaurus selectors)
4. Token-based chunking (500-1000 tokens)
5. Metadata extraction (URL, title, module, chapter)
6. Batch embedding and upsert

**Deliverables**: Ingestion script populates Qdrant

### Phase 5: Agent Orchestration (P1)

**Goal**: Agent that answers questions with citations

1. Implement `app/services/agent/tools.py` (search_textbook)
2. Implement `app/services/agent/orchestrator.py`
3. Configure Gemini via OpenAI compatibility
4. Tool registration and agent creation
5. Response formatting with citations

**Deliverables**: Agent answers questions correctly

### Phase 6: Chat Endpoint (P1)

**Goal**: Complete /chat API

1. Implement `app/schemas/chat.py`
2. Implement `app/routers/chat.py`
3. Request validation
4. Response formatting
5. Error handling (validation, service unavailable)

**Deliverables**: Chat endpoint returns answers with citations

### Phase 7: Testing (P1)

**Goal**: Test coverage for critical paths

1. Create `tests/conftest.py` with fixtures
2. Implement `tests/test_health.py`
3. Implement `tests/test_chat.py`
4. Implement `tests/test_ingestion.py`

**Deliverables**: All tests passing

### Phase 8: Deployment (P1)

**Goal**: Running on Hugging Face Spaces

1. Finalize Dockerfile
2. Configure HF Spaces README metadata
3. Push to HF Spaces
4. Run ingestion script
5. Verify production health check

**Deliverables**: Live API on HF Spaces

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Gemini rate limits | Fail-fast approach (no retries at app level), monitor free tier usage |
| Qdrant free tier limits | ~2.5MB storage well within 1GB limit |
| HF Spaces cold starts | 60s startup timeout in health check |
| HTML structure changes | Robust selectors with fallbacks |

---

## Dependencies Between Phases

```
Phase 1 (Infrastructure)
    │
    ├──► Phase 2 (Qdrant) ──► Phase 4 (Ingestion)
    │                              │
    └──► Phase 3 (Embeddings) ─────┤
                                   │
                                   ▼
                            Phase 5 (Agent)
                                   │
                                   ▼
                            Phase 6 (Chat)
                                   │
                                   ▼
                            Phase 7 (Testing)
                                   │
                                   ▼
                            Phase 8 (Deployment)
```

---

## Complexity Tracking

No constitution violations requiring justification.

---

## Related Artifacts

- [spec.md](./spec.md) - Feature specification
- [research.md](./research.md) - Technical research findings
- [data-model.md](./data-model.md) - Entity definitions
- [contracts/api-contracts.md](./contracts/api-contracts.md) - API specifications
- [quickstart.md](./quickstart.md) - Developer setup guide

---

## Next Steps

Run `/sp.tasks` to generate the detailed task breakdown from this plan.
