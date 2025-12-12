# Plan Prompt: Backend RAG Chatbot + Deployment

Use this prompt with `/sp.plan` or give it to an AI to create an implementation plan from the specification.

---

## PROMPT

```
Create a SpecKit Plus implementation plan for the RAG Textbook Chatbot Backend feature based on the specification.

## Input Specification

The specification covers:
- RAG ingestion pipeline (sitemap crawling, chunking, embedding, Qdrant upload)
- Backend API service (chat endpoint, health check, agent orchestration)
- Deployment (Docker, Hugging Face Spaces, environment configuration)

## Technical Context (Fill These)

**Language/Version**: Python 3.11
**Primary Dependencies**:
- FastAPI + Uvicorn (web framework)
- OpenAI Agent SDK (agent orchestration)
- LangChain + langchain-google-genai (embeddings)
- qdrant-client (vector database)
- BeautifulSoup4 + requests (web scraping)
- tenacity (retry logic)

**LLM**: Google Gemini (gemini-2.5-flash or gemini-1.5-flash) via OpenAI Agent SDK compatibility layer
**Embeddings**: Google Gemini (models/gemini-embedding-001, 768 dimensions) via LangChain
**Storage**: Qdrant Cloud (free tier) - collection "book_chunks"
**Testing**: pytest + httpx (for async API testing)
**Target Platform**: Hugging Face Spaces (Docker mode, port 7860)
**Project Type**: Backend service (single project)
**Performance Goals**: <5s response time, 10 concurrent users
**Constraints**: Free tier only (Qdrant, HF Spaces, Gemini API)
**Scale/Scope**: 23 textbook pages, ~200-500 chunks

## Constitution Check

Verify against project constitution:
- [ ] Uses Google Gemini models only (NO OpenAI for inference)
- [ ] Deploys to Hugging Face Spaces only (NO Vercel/Render/AWS)
- [ ] Uses Qdrant free tier
- [ ] Returns source URLs for citations
- [ ] Follows Context7 MCP for documentation

## Project Structure

Generate this structure:

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Environment configuration
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py                # POST /chat endpoint
│   │   └── health.py              # GET /health endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py    # OpenAI Agent SDK + Gemini
│   │   │   └── tools.py           # Retrieval tool definitions
│   │   ├── embedding/
│   │   │   ├── __init__.py
│   │   │   └── embedding.py       # Gemini embeddings via LangChain
│   │   └── retrieval/
│   │       ├── __init__.py
│   │       └── qdrant_client.py   # Qdrant vector search
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chat.py                # ChatRequest, ChatResponse, Citation
│   │   └── health.py              # HealthStatus
│   └── utils/
│       ├── __init__.py
│       └── logging.py             # Logging configuration
├── scripts/
│   └── ingest-book.py             # Sitemap crawler + chunker + uploader
├── tests/
│   ├── __init__.py
│   ├── test_chat.py
│   ├── test_health.py
│   └── test_ingestion.py
├── Dockerfile                      # Multi-stage production build
├── docker-compose.yml              # Local development
├── requirements.txt
├── .env.example
└── README.md
```

## Plan Phases

### Phase 0: Research & Resolve Unknowns

Research and document decisions for:

1. **OpenAI Agent SDK + Gemini Integration**
   - How to configure base_url for Gemini compatibility
   - Tool registration pattern
   - Response streaming (if needed)

2. **LangChain Gemini Embeddings**
   - GoogleGenerativeAIEmbeddings configuration
   - Batch size limits
   - Error handling patterns

3. **Qdrant Client Setup**
   - Cloud vs local configuration
   - Collection creation with 768 dimensions
   - Upsert with deterministic IDs

4. **Sitemap Crawling**
   - Rate limiting strategy
   - HTML content extraction (main content only)
   - Chunking algorithm (500-1000 tokens)

5. **Docker + HF Spaces**
   - Multi-stage build pattern
   - Port 7860 exposure
   - Environment variable injection

**Output**: `specs/002-rag-chatbot-backend/research.md`

### Phase 1: Design & Contracts

1. **Data Model** (`data-model.md`):
   - TextbookChunk (id, content, vector, url, module, chapter, title, chunk_index, heading)
   - ChatRequest (query, k, module_filter)
   - ChatResponse (answer, citations, metadata)
   - Citation (url, title, snippet, score)
   - HealthStatus (status, timestamp, version)

2. **API Contracts** (`contracts/`):
   - `openapi.yaml` or `api-contracts.md`
   - POST /chat - request/response schemas
   - GET /health - response schema
   - Error response format (4xx, 5xx)

3. **Quickstart** (`quickstart.md`):
   - Local development setup
   - Environment variables
   - Running ingestion script
   - Testing the API

**Output**: `data-model.md`, `contracts/`, `quickstart.md`

## Agent Assignment

Specify which agent handles each component:

| Component | Agent | Skills |
|-----------|-------|--------|
| FastAPI structure | backend-architect-and-sdk-agent | fastapi-scaffolding |
| Agent SDK + Gemini | backend-architect-and-sdk-agent | gemini-agent-sdk-setup |
| Chat endpoint | backend-architect-and-sdk-agent | rag-chat-endpoint |
| Sitemap ingestion | RAG-pipeline-and-retrieval-agent | book-ingestion |
| Embeddings | RAG-pipeline-and-retrieval-agent | embedding-pipeline |
| Qdrant retrieval | RAG-pipeline-and-retrieval-agent | qdrant-retrieval-tool |
| Dockerfile | deployment-agent | dockerfile-builder |
| HF Spaces config | deployment-agent | huggingface-config |
| Local dev scripts | deployment-agent | local-dev-runner |

## Output Format

The plan must include:

1. **Technical Context** - All fields filled (no NEEDS CLARIFICATION remaining)
2. **Constitution Check** - All gates passed with checkmarks
3. **Project Structure** - Concrete file paths (no Option labels)
4. **research.md** - Decisions with rationale for each unknown
5. **data-model.md** - Entity definitions with fields and relationships
6. **contracts/** - API specifications (OpenAPI or markdown)
7. **quickstart.md** - Developer setup instructions
8. **Agent assignments** - Which agent/skill handles each task

## Key Rules

- Use Context7 MCP to fetch official documentation for all technologies
- All paths must be absolute
- ERROR if constitution gates fail
- ERROR if NEEDS CLARIFICATION items remain after Phase 0
- Include agent/skill assignment for implementation phase
```

---

## EXPECTED OUTPUT FILES

After running `/sp.plan`, these files should be created:

```
specs/002-rag-chatbot-backend/
├── plan.md              # Main implementation plan
├── research.md          # Phase 0 research findings
├── data-model.md        # Entity definitions
├── contracts/
│   └── api-contracts.md # API specifications
└── quickstart.md        # Developer setup guide
```

---

## USAGE

1. Ensure specification exists at `specs/002-rag-chatbot-backend/spec.md`
2. Run `/sp.plan` in Claude Code
3. Or give this prompt to an AI along with the specification
4. Verify all outputs are created and no NEEDS CLARIFICATION remains
