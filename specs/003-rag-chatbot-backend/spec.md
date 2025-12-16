# Feature Specification: RAG Textbook Chatbot Backend

**Feature Branch**: `001-rag-chatbot-backend`
**Created**: 2025-12-12
**Status**: Draft
**Input**: RAG chatbot backend for Physical AI & Humanoid Robotics textbook with sitemap-based content ingestion, vector-based retrieval, and containerized cloud deployment. Use of Context7 MCP server for documentation retrieval is mandatory during implementation.

---

## Overview

This specification defines a conversational assistant backend that enables users to ask questions about the "Physical AI & Humanoid Robotics" textbook and receive accurate, cited answers. The system ingests textbook content from the published website, stores it in a searchable format, and provides a question-answering service that returns relevant passages with source URLs.

**Textbook URL**: https://nadeemsangrasi.github.io/humanoid-and-robotic-book/
**Sitemap URL**: https://nadeemsangrasi.github.io/humanoid-and-robotic-book/sitemap.xml (23 pages)

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask a Question and Receive a Cited Answer (Priority: P1)

A reader studying the textbook wants to quickly find information about a specific robotics concept. They type their question into the chatbot interface and receive a concise, accurate answer that includes links back to the relevant textbook pages where they can read more.

**Why this priority**: This is the core value proposition of the chatbot. Without the ability to answer questions with citations, the system provides no value. Every other feature depends on this working correctly.

**Independent Test**: Can be fully tested by submitting a question about textbook content (e.g., "What is inverse kinematics?") and verifying the response contains relevant information plus at least one source URL pointing to the textbook.

**Acceptance Scenarios**:

1. **Given** the textbook content has been indexed, **When** a user submits a question about a topic covered in the textbook, **Then** the system returns an answer that addresses the question with at least one citation URL to the source page.

2. **Given** the textbook content has been indexed, **When** a user submits a question, **Then** the response is returned within 10 seconds.

3. **Given** the textbook content has been indexed, **When** a user asks about a specific chapter or module, **Then** the citations in the response point to pages from that chapter/module when the content exists there.

---

### User Story 2 - Ingest Textbook Content from Published Website (Priority: P1)

An administrator needs to populate the system with textbook content so users can ask questions. They run a standalone CLI ingestion script (manually or via CI/CD) that automatically crawls the textbook website, extracts the educational content, and stores it in a searchable format.

**Why this priority**: Without content ingestion, there is nothing to search. This is a prerequisite for the question-answering functionality and must work before any user-facing features can be tested.

**Independent Test**: Can be tested by running the ingestion process and verifying that content from all 23 textbook pages is successfully stored with proper metadata (URL, title, chapter information).

**Acceptance Scenarios**:

1. **Given** the textbook sitemap is accessible, **When** the ingestion process runs, **Then** content from all pages listed in the sitemap is extracted and stored.

2. **Given** a textbook page contains educational content mixed with navigation elements, **When** that page is processed, **Then** only the main educational content is extracted (navigation, footers, and sidebars are excluded).

3. **Given** content is being ingested, **When** a page is processed, **Then** metadata is preserved including: source URL, page title, module/chapter information, and content position.

4. **Given** the ingestion process runs multiple times, **When** processing the same content, **Then** no duplicate entries are created (idempotent operation).

---

### User Story 3 - Deploy Backend to Production (Priority: P1)

As a developer, I want to deploy the RAG chatbot backend to a cloud platform so that users can access the chatbot from the published textbook.

**Why this priority**: Without deployment, the chatbot cannot be accessed by end users. This is essential for the feature to deliver value.

**Independent Test**: Can be fully tested by deploying the container, accessing the health endpoint, and sending a test chat request to verify end-to-end functionality.

**Acceptance Scenarios**:

1. **Given** the backend code is ready, **When** I build and push the container, **Then** it deploys successfully and starts accepting requests.

2. **Given** the backend is deployed, **When** I access the health endpoint, **Then** I receive a successful health response.

3. **Given** the backend is deployed, **When** a user sends a chat request from the textbook UI, **Then** they receive a response with citations.

---

### User Story 4 - Configure Environment for Production (Priority: P1)

As a developer, I want to configure environment variables and secrets securely so that the backend can connect to external services (vector database, LLM API) without exposing credentials.

**Why this priority**: Security is critical. Exposed credentials would compromise the entire system.

**Independent Test**: Can be tested by verifying the deployed service connects to all external services and no secrets are visible in logs or responses.

**Acceptance Scenarios**:

1. **Given** environment variables are configured, **When** the backend starts, **Then** it connects to the vector database successfully.

2. **Given** environment variables are configured, **When** the backend processes a request, **Then** it authenticates with the LLM API successfully.

3. **Given** the backend is running, **When** I inspect logs or error messages, **Then** no secrets or API keys are exposed.

---

### User Story 5 - Run Backend Locally for Development (Priority: P2)

As a developer, I want to run the backend locally using containers so that I can test changes before deploying to production.

**Why this priority**: Local development speeds up iteration and reduces deployment failures.

**Independent Test**: Can be tested by building and running the container locally, then sending requests to verify functionality.

**Acceptance Scenarios**:

1. **Given** I have the source code, **When** I run the local development script, **Then** the backend starts and is accessible on localhost.

2. **Given** the backend is running locally, **When** I make a chat request, **Then** I receive a valid response.

3. **Given** I make code changes, **When** I rebuild and restart, **Then** the changes are reflected.

---

### Edge Cases

- **Empty or malformed question**: User submits a blank message, only whitespace, or a single character. System should return a helpful prompt to ask a proper question.

- **Question exceeds length limits**: User submits an extremely long question (>2000 characters). System should either truncate intelligently or return an error with guidance.

- **External service unavailable**: The embedding service or vector storage is temporarily unavailable. System should return a user-friendly error message rather than a technical error.

- **Page removed between ingestions**: A page exists in the stored content but has been removed from the live sitemap. Citations should still work or gracefully indicate the page is no longer available.

- **Non-English question**: User asks a question in a language other than English. System should respond in the same language if possible or indicate English-only support.

- **Repeated identical questions**: User asks the same question multiple times in succession. System should return consistent answers.

- **HTML content with special characters**: Textbook pages contain code snippets, mathematical notation, or special characters. These should be preserved correctly in the indexed content and responses.

- **Container memory exhaustion**: Container runs out of memory during request processing. System should handle gracefully without crashing the entire service.

- **External services temporarily unavailable**: Vector database or LLM API is temporarily unavailable during deployment or runtime. System should return appropriate error messages and recover when services return.

- **Rolling deployment with in-flight requests**: Requests are in-flight when a new deployment starts. System should complete existing requests before shutting down or handle handoff gracefully.

- **Crash recovery**: System crashes unexpectedly or restarts. System should recover state and resume operation without data corruption or loss.

---

## Requirements *(mandatory)*

### Functional Requirements - Content Ingestion

- **FR-001**: System MUST discover all textbook pages by parsing the sitemap file at the configured URL.

- **FR-002**: System MUST extract main educational content from each page while excluding navigation elements, headers, footers, sidebars, and other non-content elements.

- **FR-003**: System MUST divide extracted content into searchable segments between 500-1000 tokens each, preserving logical boundaries where possible (headings, paragraphs).

- **FR-004**: System MUST preserve metadata for each content segment including: source page URL, page title, module/chapter identifier, segment position, and associated heading.

- **FR-005**: System MUST generate numerical representations (embeddings) of each content segment for similarity search, using 768-dimensional vectors.

- **FR-006**: System MUST store content segments and their embeddings in a vector database collection named "book_chunks".

- **FR-007**: System MUST implement idempotent ingestion - re-running the process with the same content produces no duplicates.

- **FR-007a**: Ingestion MUST be triggered via a standalone CLI script (not an API endpoint), executable manually or via CI/CD pipeline.

### Functional Requirements - Query API

- **FR-008**: System MUST expose a chat endpoint that accepts user questions and returns answers with citations.

- **FR-009**: System MUST expose a health check endpoint that reports service availability status.

- **FR-010**: System MUST search stored content using semantic similarity to find passages relevant to the user's question.

- **FR-011**: System MUST retrieve up to 5 most relevant content segments for each query, filtering out any results below a 0.7 similarity threshold (may return 0-5 results).

- **FR-012**: System MUST use an AI language model to synthesize retrieved passages into a coherent answer.

- **FR-013**: System MUST include source citations (URLs) in every response that contains information from the textbook.

- **FR-014**: System MUST return appropriate error responses for invalid inputs (empty questions, exceeded length limits).

### Functional Requirements - Deployment

- **FR-015**: System MUST be deployable as a containerized service.

- **FR-016**: System MUST expose its service on port 7860.

- **FR-017**: System MUST read configuration from environment variables (API keys, service URLs).

- **FR-018**: System MUST be deployable on free-tier cloud infrastructure.

- **FR-019**: System MUST start and respond to health checks within 60 seconds of container launch.

- **FR-020**: System MUST NOT expose secrets, API keys, or credentials in logs, error messages, or responses.

- **FR-021**: System MUST be accessible via HTTPS in production.

- **FR-022**: System MUST gracefully handle restarts without data loss or corruption.

- **FR-023**: System MUST support local development environment using containers with the same configuration as production.

### Functional Requirements - Error Handling

- **FR-024**: System MUST return user-friendly error messages when external services are unavailable or rate-limited (fail fast, no retry/queue logic).

- **FR-025**: System MUST log errors with sufficient detail for debugging without exposing sensitive information.

- **FR-026**: System MUST validate all user input before processing.

---

### Key Entities

- **TextbookChunk**: A searchable unit of textbook content. Contains the text content, its numerical representation for similarity search, and metadata including source URL, page title, module/chapter identifier, chunk position index, and associated heading.

- **ChatRequest**: A user's question submission. Contains the question text and optional parameter for limiting the number of results to retrieve.

- **ChatResponse**: The system's answer to a user question. Contains the synthesized answer text, a list of citations with source URLs and relevant excerpts, and optional metadata about confidence or relevance scores.

- **Citation**: A reference to a source passage used in an answer. Contains the source page URL, the page title, a brief excerpt from the relevant passage, and optionally the module/chapter information.

- **IngestionResult**: The outcome of a content ingestion run. Contains counts of pages processed, chunks created, any errors encountered, and timestamps.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users receive answers to their questions within 10 seconds for 95% of requests under normal load conditions.

- **SC-002**: At least 90% of answers to questions about textbook topics include at least one source citation with a valid URL.

- **SC-003**: System successfully handles 10 concurrent users without degradation in response time or availability.

- **SC-004**: Content ingestion completes successfully for all 23 textbook pages without errors.

- **SC-005**: Re-running ingestion on unchanged content results in exactly 0 duplicate entries (idempotent operation verified).

- **SC-006**: System achieves 99% uptime during operational hours (excluding scheduled maintenance).

- **SC-007**: Health check endpoint responds within 1 second for 99% of requests.

- **SC-008**: At least 80% of user questions about topics covered in the textbook receive relevant, accurate answers (measured by manual review of sample queries).

- **SC-009**: All citation URLs in responses successfully resolve to live textbook pages (no broken links).

- **SC-010**: Backend deploys and passes health check within 2 minutes of container start.

- **SC-011**: System maintains 99% uptime during normal operation (excluding scheduled maintenance).

- **SC-012**: Local development environment can be set up and running in under 5 minutes from a fresh clone.

- **SC-013**: Zero secrets or API keys exposed in any logs, error responses, or public outputs.

---

## Constraints

### Technical Constraints

- **C-001**: Backend inference MUST use Google Gemini models only - OpenAI models are prohibited for answer generation.

- **C-002**: Embeddings MUST be generated using Google Gemini embedding models only - OpenAI embeddings are prohibited.

- **C-003**: Production deployment MUST be on Hugging Face Spaces (Docker mode, free tier) - Vercel, Render, AWS, and other platforms are prohibited for production backend.

- **C-004**: Vector storage MUST use Qdrant free tier.

- **C-005**: All responses with textbook-sourced information MUST include citation URLs.

### Documentation Constraint

- **C-006**: During implementation, developers MUST use the Context7 MCP server to retrieve up-to-date official documentation for all technologies, tools, libraries, and frameworks before writing code.

---

## Dependencies

- **External Services**:
  - Google AI API (Gemini models for embeddings and text generation)
  - Qdrant Cloud (vector database for content storage and retrieval)
  - Hugging Face Spaces (deployment platform)

- **Content Source**:
  - Published textbook at https://nadeemsangrasi.github.io/humanoid-and-robotic-book/
  - Sitemap at https://nadeemsangrasi.github.io/humanoid-and-robotic-book/sitemap.xml

---

## Assumptions

- The textbook website remains publicly accessible and the sitemap accurately reflects available pages.
- Textbook content is primarily in English.
- The 23-page textbook will not grow to exceed free-tier limits of chosen services.
- Users have reasonable internet connectivity (latency < 500ms to deployment region).
- Question frequency will not exceed free-tier API rate limits during normal usage.
- Textbook HTML structure is consistent enough for reliable content extraction.

---

## Clarifications

### Session 2025-12-12

- Q: Should the system return low-relevance results if they're the "top 5", or filter out results below a minimum similarity score? → A: Filter results below 0.7 similarity threshold (may return 0-5 results)
- Q: How should the system behave when approaching or hitting API rate limits (Gemini, Qdrant)? → A: Fail fast with error message (no rate limit handling)
- Q: How should the content ingestion process be triggered? → A: Standalone CLI script run manually or via CI/CD

---

## Out of Scope

- User authentication or personalization
- Conversation history or multi-turn dialogue memory
- Real-time content updates (content refresh requires manual re-ingestion)
- Analytics dashboard or usage reporting
- Multiple language support beyond English
- Mobile-specific optimizations
- Caching layer for frequently asked questions
- Admin UI for managing content or configuration
