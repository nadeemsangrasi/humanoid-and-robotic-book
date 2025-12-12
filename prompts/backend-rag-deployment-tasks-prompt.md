# Tasks Prompt: Backend RAG Chatbot + Deployment

Use this prompt with `/sp.tasks` or give it to an AI to generate actionable tasks from the specification and plan.

---

## PROMPT

```
Generate a SpecKit Plus tasks.md file for the RAG Textbook Chatbot Backend feature based on the specification and plan.

## Input Documents

- **spec.md**: 8 user stories (4 P1, 3 P2, 1 P3) with acceptance criteria
- **plan.md**: Technical context, project structure, agent assignments
- **data-model.md**: Entity definitions (TextbookChunk, ChatRequest, ChatResponse, Citation, etc.)
- **contracts/**: API specifications (POST /chat, GET /health)

## Task Format (STRICT)

Every task MUST follow this exact format:

```
- [ ] T### [P?] [US#?] Description with exact file path
```

- **Checkbox**: Always `- [ ]`
- **Task ID**: T001, T002, T003... (sequential)
- **[P]**: Include ONLY if parallelizable (different files, no dependencies)
- **[US#]**: Include ONLY in user story phases (US1, US2, etc.)
- **Description**: Clear action with exact file path

## Phase Structure

### Phase 1: Setup (No [US#] labels)
Project initialization tasks - can start immediately.

### Phase 2: Foundational (No [US#] labels)
Blocking prerequisites - MUST complete before ANY user story.

### Phase 3-10: User Stories (MUST have [US#] labels)
One phase per user story in priority order (P1 → P2 → P3).

### Final Phase: Polish (No [US#] labels)
Cross-cutting concerns after all stories complete.

## User Stories from Spec (Map to Phases)

| Phase | User Story | Priority | Agent Assignment |
|-------|------------|----------|------------------|
| Phase 3 | US1 - Ask Question About Textbook | P1 | backend-architect-and-sdk-agent |
| Phase 4 | US2 - Ingest Textbook Content | P1 | RAG-pipeline-and-retrieval-agent |
| Phase 5 | US3 - Deploy Backend to Production | P1 | deployment-agent |
| Phase 6 | US4 - Configure Environment Securely | P1 | deployment-agent |
| Phase 7 | US5 - Filter by Module | P2 | RAG-pipeline-and-retrieval-agent |
| Phase 8 | US6 - Handle Unknown Topics | P2 | backend-architect-and-sdk-agent |
| Phase 9 | US7 - Run Backend Locally | P2 | deployment-agent |
| Phase 10 | US8 - Re-index After Updates | P3 | RAG-pipeline-and-retrieval-agent |

## Agent/Skill Assignment Per Task

Include agent and skill for each implementation task:

| Component | Agent | Skill |
|-----------|-------|-------|
| FastAPI app structure | backend-architect-and-sdk-agent | fastapi-scaffolding |
| Agent SDK + Gemini config | backend-architect-and-sdk-agent | gemini-agent-sdk-setup |
| POST /chat endpoint | backend-architect-and-sdk-agent | rag-chat-endpoint |
| Sitemap crawler + chunker | RAG-pipeline-and-retrieval-agent | book-ingestion |
| Embedding service | RAG-pipeline-and-retrieval-agent | embedding-pipeline |
| Qdrant retrieval tools | RAG-pipeline-and-retrieval-agent | qdrant-retrieval-tool |
| Dockerfile | deployment-agent | dockerfile-builder |
| HF Spaces config | deployment-agent | huggingface-config |
| Local dev scripts | deployment-agent | local-dev-runner |

## Project Structure (From Plan)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   │   ├── chat.py
│   │   └── health.py
│   ├── services/
│   │   ├── agent/
│   │   │   ├── orchestrator.py
│   │   │   └── tools.py
│   │   ├── embedding/
│   │   │   └── embedding.py
│   │   └── retrieval/
│   │       └── qdrant_client.py
│   ├── schemas/
│   │   ├── chat.py
│   │   └── health.py
│   └── utils/
│       └── logging.py
├── scripts/
│   └── ingest-book.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Generate Tasks

### Phase 1: Setup

- [ ] T001 Create backend/ directory structure per plan
- [ ] T002 Initialize Python project with requirements.txt
- [ ] T003 [P] Create .env.example with all required variables
- [ ] T004 [P] Setup logging configuration in backend/app/utils/logging.py

### Phase 2: Foundational (BLOCKS all user stories)

- [ ] T005 Create config.py with environment variable management
- [ ] T006 [P] Create base schemas in backend/app/schemas/
- [ ] T007 [P] Setup Qdrant client connection in backend/app/services/retrieval/qdrant_client.py
- [ ] T008 [P] Setup Gemini embeddings in backend/app/services/embedding/embedding.py
- [ ] T009 Create FastAPI app in backend/app/main.py with CORS middleware

**Checkpoint**: Foundation ready - user story implementation can begin

### Phase 3: User Story 1 - Ask Question About Textbook (P1) 🎯 MVP

**Goal**: User can ask a question and receive an answer with source citations
**Agent**: backend-architect-and-sdk-agent
**Skills**: fastapi-scaffolding, gemini-agent-sdk-setup, rag-chat-endpoint
**Independent Test**: Send POST /chat with question, receive answer + citations

- [ ] T010 [US1] Create ChatRequest/ChatResponse/Citation schemas in backend/app/schemas/chat.py
- [ ] T011 [US1] Implement retrieval tool in backend/app/services/agent/tools.py
- [ ] T012 [US1] Configure OpenAI Agent SDK with Gemini in backend/app/services/agent/orchestrator.py
- [ ] T013 [US1] Implement POST /chat endpoint in backend/app/routers/chat.py
- [ ] T014 [US1] Wire up agent orchestration with retrieval tool
- [ ] T015 [US1] Add citation formatting to response

**Checkpoint**: US1 complete - can ask questions and get cited answers

### Phase 4: User Story 2 - Ingest Textbook Content (P1)

**Goal**: System crawls sitemap, chunks content, embeds, uploads to Qdrant
**Agent**: RAG-pipeline-and-retrieval-agent
**Skills**: book-ingestion, embedding-pipeline, qdrant-retrieval-tool
**Independent Test**: Run ingest script, verify chunks in Qdrant

- [ ] T016 [US2] Create sitemap parser in backend/scripts/ingest-book.py
- [ ] T017 [US2] Implement HTML content extractor (strip nav/footer)
- [ ] T018 [US2] Implement text chunker (500-1000 tokens)
- [ ] T019 [US2] Add metadata extraction (url, module, chapter, title, heading)
- [ ] T020 [US2] Implement batch embedding with Gemini
- [ ] T021 [US2] Implement Qdrant upsert with deterministic IDs
- [ ] T022 [US2] Add progress tracking and error handling

**Checkpoint**: US2 complete - textbook indexed in Qdrant

### Phase 5: User Story 3 - Deploy Backend to Production (P1)

**Goal**: Backend runs on Hugging Face Spaces via Docker
**Agent**: deployment-agent
**Skills**: dockerfile-builder, huggingface-config
**Independent Test**: Access deployed /health endpoint

- [ ] T023 [US3] Create multi-stage Dockerfile in backend/Dockerfile
- [ ] T024 [US3] Configure port 7860 exposure and CMD
- [ ] T025 [US3] Create README.md for HF Spaces
- [ ] T026 [US3] Create hf-space.yaml configuration (if needed)
- [ ] T027 [US3] Test Docker build locally

**Checkpoint**: US3 complete - backend deployable to HF Spaces

### Phase 6: User Story 4 - Configure Environment Securely (P1)

**Goal**: Secrets managed securely, no exposure in logs/responses
**Agent**: deployment-agent
**Skills**: huggingface-config
**Independent Test**: Verify no secrets in logs after requests

- [ ] T028 [US4] Implement secrets masking in logging
- [ ] T029 [US4] Add environment variable validation on startup
- [ ] T030 [US4] Document HF Spaces secret configuration
- [ ] T031 [US4] Add error response sanitization

**Checkpoint**: US4 complete - secrets secure

### Phase 7: User Story 5 - Filter by Module (P2)

**Goal**: User can filter questions to specific module
**Agent**: RAG-pipeline-and-retrieval-agent
**Skills**: qdrant-retrieval-tool
**Independent Test**: Query with module_filter returns only that module's content

- [ ] T032 [US5] Add module_filter parameter to ChatRequest schema
- [ ] T033 [US5] Implement Qdrant filter by module metadata
- [ ] T034 [US5] Update retrieval tool to use filter

**Checkpoint**: US5 complete - filtering works

### Phase 8: User Story 6 - Handle Unknown Topics (P2)

**Goal**: Graceful response when no relevant content found
**Agent**: backend-architect-and-sdk-agent
**Skills**: rag-chat-endpoint
**Independent Test**: Ask off-topic question, get graceful response

- [ ] T035 [US6] Add relevance score threshold check
- [ ] T036 [US6] Implement "no relevant content" response format
- [ ] T037 [US6] Add helpful suggestions in response

**Checkpoint**: US6 complete - handles unknown topics gracefully

### Phase 9: User Story 7 - Run Backend Locally (P2)

**Goal**: Developer can run backend locally with Docker
**Agent**: deployment-agent
**Skills**: local-dev-runner
**Independent Test**: Run scripts, backend accessible on localhost

- [ ] T038 [US7] Create docker-compose.yml for local development
- [ ] T039 [US7] Create build.sh script
- [ ] T040 [US7] Create run.sh script
- [ ] T041 [US7] Create stop.sh script
- [ ] T042 [US7] Update README with local dev instructions

**Checkpoint**: US7 complete - local dev works

### Phase 10: User Story 8 - Re-index After Updates (P3)

**Goal**: Admin can re-run ingestion idempotently
**Agent**: RAG-pipeline-and-retrieval-agent
**Skills**: book-ingestion
**Independent Test**: Run ingestion twice, no duplicate chunks

- [ ] T043 [US8] Add --force flag to ingest script
- [ ] T044 [US8] Implement chunk diff detection
- [ ] T045 [US8] Add logging for updated vs unchanged chunks

**Checkpoint**: US8 complete - re-indexing is idempotent

### Phase 11: Polish & Cross-Cutting

- [ ] T046 [P] Add GET /health endpoint in backend/app/routers/health.py
- [ ] T047 [P] Add comprehensive error handling middleware
- [ ] T048 [P] Add request logging middleware
- [ ] T049 Run quickstart.md validation
- [ ] T050 Final documentation updates

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → [Phase 3-10 User Stories] → Phase 11 (Polish)
                         ↓
              BLOCKS all user stories
```

### User Story Dependencies

- **US1 (Chat)**: Needs Foundational complete (Qdrant client, embeddings)
- **US2 (Ingest)**: Needs Foundational complete, can parallel with US1
- **US3 (Deploy)**: Needs US1 and US2 complete (need working app to deploy)
- **US4 (Secrets)**: Can parallel with US3
- **US5 (Filter)**: Needs US1 complete
- **US6 (Unknown)**: Needs US1 complete
- **US7 (Local Dev)**: Needs US3 complete
- **US8 (Re-index)**: Needs US2 complete

### Parallel Opportunities

```
After Phase 2 completes:
├── US1 (Chat) ─────────────┐
├── US2 (Ingest) ───────────┼── Can run in parallel
                            ↓
                    US3 (Deploy) + US4 (Secrets) in parallel
                            ↓
              US5, US6, US7 can parallel after dependencies
                            ↓
                    US8 after US2
```

## Implementation Strategy

### MVP (Minimum Viable Product)
1. Complete Phase 1 + Phase 2 (Setup + Foundational)
2. Complete US1 (Ask Questions) - working chat
3. Complete US2 (Ingest) - content indexed
4. Complete US3 (Deploy) - live on HF Spaces
5. **STOP**: You have a working, deployed chatbot!

### Full Feature
Continue with US4-US8 for enhanced functionality.

## Summary

- **Total Tasks**: 50
- **Setup**: 4 tasks
- **Foundational**: 5 tasks
- **User Stories**: 37 tasks across 8 stories
- **Polish**: 4 tasks
- **MVP Scope**: T001-T027 (27 tasks for US1-US3)
```

---

## EXPECTED OUTPUT

After running `/sp.tasks`, you should have:

```
specs/002-rag-chatbot-backend/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/
├── quickstart.md
└── tasks.md          ← Generated by this prompt
```

---

## USAGE

1. Ensure spec.md and plan.md exist in `specs/002-rag-chatbot-backend/`
2. Run `/sp.tasks` in Claude Code
3. Or give this prompt to an AI along with spec.md and plan.md
4. Execute tasks in order, respecting dependencies
5. Stop at MVP (US1-US3) or continue for full feature
