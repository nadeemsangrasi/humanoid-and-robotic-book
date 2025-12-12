# Tasks: RAG Textbook Chatbot Backend

**Feature Branch**: `001-rag-chatbot-backend`
**Generated**: 2025-12-12 | **Simplified**: 2025-12-12
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 40 |
| Setup Phase | 4 |
| Foundational Phase | 5 |
| Chat (US1) | 9 |
| Ingest (US2) | 8 |
| Health | 2 |
| Deploy (US3) | 4 |
| Environment (US4) | 2 |
| Local Dev (US5) | 2 |
| Testing | 4 |

**MVP = All 40 tasks → Working deployed chatbot**

**User Stories:**
- US1: Ask a question and receive a cited answer (P1)
- US2: Ingest textbook content from published website (P1)
- US3: Deploy backend to production (P1)
- US4: Configure environment for production (P1)
- US5: Run backend locally for development (P2)

---

## Task Format

```
- [ ] T### [P?] [US#?] Description with file path
      Agent: <agent-name> | Skill: <skill-name>
```

- **[P]**: Parallelizable (different files, no dependencies)
- **[US#]**: User story reference (only in story phases)

---

## Phase 1: Setup

**Goal**: Project scaffolding ready for development

- [ ] T001 Create backend/ directory structure per plan
      Agent: backend-architect-and-sdk-agent | Skill: fastapi-scaffolding

- [ ] T002 Initialize Python project with requirements.txt and pyproject.toml
      Agent: backend-architect-and-sdk-agent | Skill: fastapi-scaffolding

- [ ] T003 [P] Create .env.example with all required variables (GOOGLE_API_KEY, QDRANT_URL, QDRANT_API_KEY, LOG_LEVEL)
      Agent: deployment-agent | Skill: huggingface-config

- [ ] T004 [P] Setup logging configuration in backend/app/utils/logging.py
      Agent: backend-architect-and-sdk-agent | Skill: fastapi-scaffolding

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational

**Goal**: Core infrastructure ready - BLOCKS all user stories

- [ ] T005 Create config.py with pydantic-settings for environment variable management in backend/app/config.py
      Agent: backend-architect-and-sdk-agent | Skill: fastapi-scaffolding

- [ ] T006 [P] Create base Pydantic schemas in backend/app/schemas/__init__.py (export all schemas)
      Agent: backend-architect-and-sdk-agent | Skill: rag-chat-endpoint

- [ ] T007 [P] Setup Qdrant client connection with collection creation in backend/app/services/retrieval/qdrant_client.py
      Agent: RAG-pipeline-and-retrieval-agent | Skill: qdrant-retrieval-tool

- [ ] T008 [P] Setup Gemini embeddings service in backend/app/services/embedding/embedding.py
      Agent: RAG-pipeline-and-retrieval-agent | Skill: embedding-pipeline

- [ ] T009 Create FastAPI app in backend/app/main.py with CORS middleware and router registration
      Agent: backend-architect-and-sdk-agent | Skill: fastapi-scaffolding

**Checkpoint**: Foundation complete - user story implementation can begin

---

## Phase 3: User Story 1 - Ask Question About Textbook (P1)

**User Story**: As a reader, I want to ask questions about textbook content and receive cited answers
**Agent**: backend-architect-and-sdk-agent
**Skills**: fastapi-scaffolding, gemini-agent-sdk-setup, rag-chat-endpoint
**Independent Test**: Send POST /chat with question, receive answer + citations

- [ ] T010 [US1] Create ChatRequest schema with query validation (1-2000 chars) in backend/app/schemas/chat.py
      Agent: backend-architect-and-sdk-agent | Skill: rag-chat-endpoint

- [ ] T011 [US1] Create ChatResponse and Citation schemas in backend/app/schemas/chat.py
      Agent: backend-architect-and-sdk-agent | Skill: rag-chat-endpoint

- [ ] T012 [US1] Create ResponseMetadata and ErrorResponse schemas in backend/app/schemas/chat.py
      Agent: backend-architect-and-sdk-agent | Skill: rag-chat-endpoint

- [ ] T013 [US1] Implement search_textbook function tool in backend/app/services/agent/tools.py
      Agent: RAG-pipeline-and-retrieval-agent | Skill: qdrant-retrieval-tool

- [ ] T014 [US1] Configure OpenAI Agent SDK with Gemini (gemini-2.0-flash) in backend/app/services/agent/orchestrator.py
      Agent: backend-architect-and-sdk-agent | Skill: gemini-agent-sdk-setup

- [ ] T015 [US1] Register search_textbook tool with agent in backend/app/services/agent/orchestrator.py
      Agent: backend-architect-and-sdk-agent | Skill: gemini-agent-sdk-setup

- [ ] T016 [US1] Implement POST /chat endpoint in backend/app/routers/chat.py
      Agent: backend-architect-and-sdk-agent | Skill: rag-chat-endpoint

- [ ] T017 [US1] Wire agent orchestration to return ChatResponse with citations
      Agent: backend-architect-and-sdk-agent | Skill: rag-chat-endpoint

- [ ] T018 [US1] Add citation URL formatting and snippet extraction (max 200 chars)
      Agent: backend-architect-and-sdk-agent | Skill: rag-chat-endpoint

**Checkpoint**: US1 complete - can ask questions and get cited answers

---

## Phase 4: User Story 2 - Ingest Textbook Content (P1)

**User Story**: As an administrator, I want to ingest textbook content so users can ask questions
**Agent**: RAG-pipeline-and-retrieval-agent
**Skills**: book-ingestion, embedding-pipeline, qdrant-retrieval-tool
**Independent Test**: Run ingest script, verify chunks in Qdrant

- [ ] T019 [US2] Create sitemap parser to extract page URLs in backend/scripts/ingest-book.py
      Agent: RAG-pipeline-and-retrieval-agent | Skill: book-ingestion

- [ ] T020 [US2] Implement HTML content extractor with Docusaurus selectors (strip nav/footer/sidebar)
      Agent: RAG-pipeline-and-retrieval-agent | Skill: book-ingestion

- [ ] T021 [US2] Implement token-based text chunker (500-1000 tokens) preserving headings
      Agent: RAG-pipeline-and-retrieval-agent | Skill: book-ingestion

- [ ] T022 [US2] Add metadata extraction (url, module, chapter, title, heading, chunk_index)
      Agent: RAG-pipeline-and-retrieval-agent | Skill: book-ingestion

- [ ] T023 [US2] Implement batch embedding with GoogleGenerativeAIEmbeddings (text-embedding-004)
      Agent: RAG-pipeline-and-retrieval-agent | Skill: embedding-pipeline

- [ ] T024 [US2] Implement Qdrant upsert with deterministic IDs (md5 of url::chunk_index)
      Agent: RAG-pipeline-and-retrieval-agent | Skill: qdrant-retrieval-tool

- [ ] T025 [US2] Add progress tracking, logging, and IngestionResult output
      Agent: RAG-pipeline-and-retrieval-agent | Skill: book-ingestion

- [ ] T026 [US2] Add error handling for network failures and partial ingestion recovery
      Agent: RAG-pipeline-and-retrieval-agent | Skill: book-ingestion

**Checkpoint**: US2 complete - textbook indexed in Qdrant (350-500 chunks)

---

## Phase 5: Health Endpoint (Required for Deploy)

**Goal**: Health check for HF Spaces deployment verification

- [ ] T027 [P] Implement GET /health endpoint in backend/app/routers/health.py
      Agent: backend-architect-and-sdk-agent | Skill: fastapi-scaffolding

- [ ] T028 [P] Create HealthStatus and ServiceStatus schemas in backend/app/schemas/health.py
      Agent: backend-architect-and-sdk-agent | Skill: fastapi-scaffolding

**Checkpoint**: Health endpoint ready for deployment

---

## Phase 6: User Story 3 - Deploy Backend to Production (P1)

**User Story**: As a developer, I want to deploy the backend to Hugging Face Spaces
**Agent**: deployment-agent
**Skills**: dockerfile-builder, huggingface-config
**Independent Test**: Access deployed /health endpoint

- [ ] T029 [US3] Create multi-stage Dockerfile in backend/Dockerfile (Python 3.11-slim)
      Agent: deployment-agent | Skill: dockerfile-builder

- [ ] T030 [US3] Configure port 7860 exposure and uvicorn CMD
      Agent: deployment-agent | Skill: dockerfile-builder

- [ ] T031 [US3] Create README.md with HF Spaces metadata (title, emoji, sdk, app_port)
      Agent: deployment-agent | Skill: huggingface-config

- [ ] T032 [US3] Test Docker build and run locally
      Agent: deployment-agent | Skill: local-dev-runner

**Checkpoint**: US3 complete - backend deployable to HF Spaces

---

## Phase 7: User Story 4 - Configure Environment for Production (P1)

**User Story**: As a developer, I want to configure environment variables securely
**Agent**: deployment-agent
**Skills**: huggingface-config
**Independent Test**: Backend connects to Qdrant and Gemini API without exposing secrets

- [ ] T033 [US4] Document all required environment variables in backend/README.md
      Agent: deployment-agent | Skill: huggingface-config

- [ ] T034 [US4] Add environment variable validation on startup in backend/app/config.py
      Agent: backend-architect-and-sdk-agent | Skill: fastapi-scaffolding

**Checkpoint**: US4 complete - environment configuration documented and validated

---

## Phase 8: User Story 5 - Run Backend Locally for Development (P2)

**User Story**: As a developer, I want to run the backend locally using containers
**Agent**: deployment-agent
**Skills**: local-dev-runner
**Independent Test**: Run docker-compose up, access localhost:7860/health

- [ ] T035 [US5] Create docker-compose.yml for local development in backend/docker-compose.yml
      Agent: deployment-agent | Skill: local-dev-runner

- [ ] T036 [US5] Create local development scripts (run.sh, build.sh) in backend/scripts/
      Agent: deployment-agent | Skill: local-dev-runner

**Checkpoint**: US5 complete - local development environment ready

---

## Phase 9: Testing

**Goal**: Test coverage for critical paths

- [ ] T037 Create tests/conftest.py with pytest fixtures (mock Qdrant, mock Gemini)
      Agent: backend-architect-and-sdk-agent | Skill: fastapi-scaffolding

- [ ] T038 [P] Implement tests/test_health.py for health endpoint
      Agent: backend-architect-and-sdk-agent | Skill: fastapi-scaffolding

- [ ] T039 [P] Implement tests/test_chat.py for chat endpoint
      Agent: backend-architect-and-sdk-agent | Skill: rag-chat-endpoint

- [ ] T040 [P] Implement tests/test_ingestion.py for ingestion script
      Agent: RAG-pipeline-and-retrieval-agent | Skill: book-ingestion

**Checkpoint**: All tests passing

---

## Summary Notes

This MVP focuses on 5 user stories:
- **US1**: Ask a question and receive a cited answer (P1)
- **US2**: Ingest textbook content from published website (P1)
- **US3**: Deploy backend to production (P1)
- **US4**: Configure environment for production (P1)
- **US5**: Run backend locally for development (P2)

---

## Execution Order

```
Phase 1: Setup (4 tasks)
    │
    ▼
Phase 2: Foundation (5 tasks) [BLOCKS EVERYTHING]
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 3: Chat (9)  ←── PARALLEL ──→ Phase 4: Ingest (8)
└─────────────────────────────────────┘
    │
    ▼
Phase 5: Health (2 tasks)
    │
    ▼
Phase 6: Deploy (4 tasks) [US3]
    │
    ▼
Phase 7: Environment (2 tasks) [US4]
    │
    ▼
Phase 8: Local Dev (2 tasks) [US5]
    │
    ▼
Phase 9: Testing (4 tasks)
    │
    ▼
✅ MVP COMPLETE = Working deployed chatbot
```

---

## Agent Assignment Summary

| Agent | Tasks | Primary Responsibility |
|-------|-------|------------------------|
| backend-architect-and-sdk-agent | 21 | FastAPI, schemas, endpoints, agent SDK, tests |
| RAG-pipeline-and-retrieval-agent | 11 | Ingestion, embeddings, Qdrant |
| deployment-agent | 8 | Docker, HF Spaces, environment, local dev |

---

## Skill Usage Summary

| Skill | Tasks | Description |
|-------|-------|-------------|
| fastapi-scaffolding | 11 | Project structure, config, main app, health, tests |
| rag-chat-endpoint | 7 | Chat endpoint, schemas, chat tests |
| gemini-agent-sdk-setup | 2 | Agent SDK + Gemini configuration |
| book-ingestion | 6 | Sitemap crawling, chunking, ingestion, tests |
| embedding-pipeline | 2 | Gemini embeddings via LangChain |
| qdrant-retrieval-tool | 3 | Vector search, upsert |
| dockerfile-builder | 2 | Multi-stage Docker build |
| huggingface-config | 3 | HF Spaces config, env documentation |
| local-dev-runner | 4 | Local Docker test, docker-compose, scripts |

---

## Related Artifacts

- [spec.md](./spec.md) - Feature specification
- [plan.md](./plan.md) - Implementation plan
- [research.md](./research.md) - Technical research findings
- [data-model.md](./data-model.md) - Entity definitions
- [contracts/api-contracts.md](./contracts/api-contracts.md) - API specifications
- [quickstart.md](./quickstart.md) - Developer setup guide
