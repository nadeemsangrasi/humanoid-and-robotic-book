# Specification Prompt: Backend RAG Chatbot + Deployment

Use this prompt with `/sp.specify` or give it to an AI to write a SpecKit Plus compliant specification.

---

## PROMPT

```
Write a SpecKit Plus specification for a RAG (Retrieval-Augmented Generation) chatbot backend with deployment for the "Physical AI & Humanoid Robotics" textbook project.

## Project Context

This is a textbook deployed at: https://nadeemsangrasi.github.io/humanoid-and-robotic-book/
The sitemap is at: https://nadeemsangrasi.github.io/humanoid-and-robotic-book/sitemap.xml (23 pages)

The chatbot allows users to ask questions about the textbook content and receive answers with source citations (URLs back to the textbook).

## What This Specification Must Cover

### 1. RAG Ingestion Pipeline
- Crawl textbook from sitemap.xml
- Extract HTML content, clean it (remove nav/footer/sidebar)
- Chunk content by sections (500-1000 tokens)
- Extract metadata: url, module, chapter, title, chunk_index, heading
- Generate embeddings using Google Gemini (models/gemini-embedding-001, 768 dimensions)
- Upload to Qdrant vector database collection "book_chunks"

### 2. Backend API Service
- FastAPI + Uvicorn backend
- POST /chat endpoint for RAG-based Q&A
- POST /health endpoint for health checks
- OpenAI Agent SDK with Google Gemini models (gemini-2.5-flash or gemini-1.5-flash)
- Retrieval tool that searches Qdrant and returns passages with source URLs
- Response format includes answer text + citations (URLs to source pages)

### 3. Deployment & Infrastructure
- Docker container (multi-stage build, Python slim base)
- Deploy to Hugging Face Spaces (Docker mode, free tier)
- Expose port 7860
- Environment variables: GOOGLE_API_KEY, QDRANT_URL, QDRANT_API_KEY
- Local development environment with Docker
- Health monitoring and logging
- Secure secrets management (no exposed credentials)

## Constraints (MUST Follow)

- NO OpenAI models for inference - only Google Gemini
- NO deployment to Vercel, Render, AWS - only Hugging Face Spaces
- MUST use Qdrant free tier for vector storage
- MUST use Google Gemini embeddings (NOT OpenAI embeddings)
- MUST return source URLs in responses for citations
- MUST be idempotent (re-running ingestion doesn't create duplicates)
- MUST NOT expose secrets in logs, errors, or responses

## Specification Requirements

Follow SpecKit Plus format with these mandatory sections:

### User Scenarios & Testing
Write 8 user stories with priorities (P1, P2, P3):

**P1 - Critical (Must Have for MVP):**
- User asks a question and gets an answer with citations
- System ingests textbook content from sitemap
- Deploy backend to production (cloud platform)
- Configure environment securely for production

**P2 - Important (Enhances Value):**
- User asks about specific module/chapter
- System handles questions with no relevant content gracefully
- Run backend locally for development and testing

**P3 - Nice to Have:**
- Admin re-indexes content after textbook updates

Each story must include:
- Plain language description
- Why this priority
- Independent test statement
- Acceptance scenarios (Given/When/Then format)

### Functional Requirements
List FR-001 through FR-022 minimum covering:

**Ingestion (FR-001 to FR-005):**
- Crawling sitemap and extracting URLs
- HTML content extraction and cleaning
- Chunking with metadata preservation
- Embedding generation
- Vector database upload

**API Endpoints (FR-006 to FR-010):**
- Chat endpoint for Q&A
- Health check endpoint
- Request/response formatting
- Error handling
- Citation inclusion

**Retrieval (FR-011 to FR-013):**
- Vector search functionality
- Metadata filtering (by module)
- Relevance scoring

**Deployment (FR-014 to FR-022):**
- Containerization
- Cloud deployment
- Health monitoring
- Environment configuration
- Secrets management (no exposure)
- Startup time requirements
- HTTPS accessibility
- Graceful restart handling
- Local development support

### Key Entities
Define these without implementation details:
- TextbookChunk: embedded content unit with metadata
- ChatRequest: user question input
- ChatResponse: answer with citations
- Citation: source reference with URL and context
- HealthStatus: system health information
- DeploymentConfig: environment and runtime settings

### Success Criteria
Measurable, technology-agnostic outcomes:

**Performance:**
- SC-001: Users receive relevant answers within 5 seconds
- SC-002: 95% of answers include at least one source citation
- SC-003: System handles 10 concurrent users without degradation

**Ingestion:**
- SC-004: Ingestion completes for all 23 pages without errors
- SC-005: Re-indexing is idempotent (no duplicates created)

**Deployment:**
- SC-006: Backend deploys and passes health check within 2 minutes
- SC-007: System maintains 99% uptime during normal operation
- SC-008: Local development environment setup completes in under 5 minutes
- SC-009: Zero secrets exposed in any logs or error responses

### Edge Cases
Document at least 8:

**Ingestion:**
- Page removed from sitemap between indexes
- Sitemap URL returns error or is unavailable
- Page content is empty or malformed HTML

**Chat:**
- Question with no relevant content in textbook
- Malformed or empty user question
- Very long user questions exceeding token limits

**Deployment:**
- Container runs out of memory
- External services (vector DB, LLM API) temporarily unavailable
- Requests in-flight during rolling deployment
- System crash or unexpected restart

## Output Format

The specification must be:
- Technology-agnostic in language (describe WHAT not HOW)
- User-focused (not developer-focused)
- Testable (every requirement has clear pass/fail criteria)
- Measurable (success criteria have numbers)
- Complete (no [NEEDS CLARIFICATION] markers unless truly ambiguous)

Do NOT include:
- Code snippets
- Framework names in requirements (FastAPI, Qdrant, etc.)
- Database schemas
- API endpoint details
- Implementation decisions

Focus on:
- User value and outcomes
- Business requirements
- Testable acceptance criteria
- Measurable success metrics
```

---

## EXPECTED OUTPUT STRUCTURE

```markdown
# Feature Specification: RAG Textbook Chatbot Backend

**Feature Branch**: `002-rag-chatbot-backend`
**Created**: [DATE]
**Status**: Draft
**Input**: RAG chatbot for Physical AI textbook with sitemap ingestion and HF Spaces deployment

## User Scenarios & Testing

### User Story 1 - Ask Question About Textbook (Priority: P1)
...

### User Story 2 - Ingest Textbook Content (Priority: P1)
...

### User Story 3 - Deploy Backend to Production (Priority: P1)
...

### User Story 4 - Configure Environment Securely (Priority: P1)
...

### User Story 5 - Filter by Module (Priority: P2)
...

### User Story 6 - Handle Unknown Topics (Priority: P2)
...

### User Story 7 - Run Backend Locally (Priority: P2)
...

### User Story 8 - Re-index After Updates (Priority: P3)
...

### Edge Cases
...

## Requirements

### Functional Requirements
- FR-001: ... (Ingestion)
- ...
- FR-014: ... (Deployment)
- ...
- FR-022: ...

### Key Entities
- TextbookChunk: ...
- ChatRequest: ...
- DeploymentConfig: ...
...

## Success Criteria

### Measurable Outcomes
- SC-001: ... (Performance)
- ...
- SC-006: ... (Deployment)
- ...
- SC-009: ...
```

---

## USAGE

1. Copy the PROMPT section above
2. Run `/sp.specify` in Claude Code
3. Paste the prompt when asked for feature description
4. Or give the prompt directly to any AI for spec generation
