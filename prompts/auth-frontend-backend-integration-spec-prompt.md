# Specification Prompt: Authentication + Frontend-Backend Integration

Use this prompt with `/sp.specify` or give it to an AI to write a SpecKit Plus compliant specification.

---

## PROMPT

```
Write a SpecKit Plus specification for Authentication and Frontend-Backend Integration for the "Physical AI & Humanoid Robotics" textbook chatbot project.

## Project Context

This project has:
- **Frontend**: Next.js app with OpenAI ChatKit starter UI (`frontend/` folder)
- **Backend**: FastAPI RAG chatbot API already deployed on Hugging Face Spaces
  - POST /api/v1/chat - RAG-based Q&A endpoint
  - GET /health - Health check endpoint
  - Deployed at: (Hugging Face Spaces URL)
- **Textbook**: Docusaurus static site at https://nadeemsangrasi.github.io/humanoid-and-robotic-book/

### Current State
The ChatKit frontend currently uses OpenAI's workflow-based sessions (NEXT_PUBLIC_CHATKIT_WORKFLOW_ID). We need to:
1. Add user authentication (Better Auth + PostgreSQL Neon DB + Drizzle ORM)
2. Customize ChatKit to connect to our FastAPI backend instead of OpenAI
3. Add chat history persistence and protected routes
4. Add backend authentication middleware (FastAPI middleware to verify JWT tokens)

### Technology Stack (MANDATORY)
- **Authentication**: Better Auth (https://better-auth.com/)
- **Database**: PostgreSQL Neon DB (free tier) - https://neon.tech/
- **ORM**: Drizzle ORM - https://orm.drizzle.team/
- **Frontend Framework**: Next.js 15 (already in place)
- **UI Components**: OpenAI ChatKit React - https://github.com/openai/chatkit
- **Backend JWT Validation**: PyJWT (shared BETTER_AUTH_SECRET with frontend)

## What This Specification Must Cover

### 1. Authentication System (Better Auth + Neon + Drizzle)

**Database Schema (Drizzle ORM):**
- Users table: id, email, name, passwordHash, emailVerified, createdAt, updatedAt
- Sessions table: id, userId, token, expiresAt, createdAt
- Accounts table (OAuth): id, userId, provider, providerAccountId, accessToken, refreshToken
- ChatHistory table: id, userId, sessionId, messages (JSON), createdAt, updatedAt

**Better Auth Configuration:**
- Email/password authentication
- OAuth providers (Google, GitHub - optional but define interface)
- Session management with JWT or database sessions
- Password hashing and security best practices
- CSRF protection

**Frontend Auth Components:**
- Login page/modal
- Register page/modal
- Logout functionality
- Protected route wrapper
- Auth context provider
- User profile display in UI

### 2. ChatKit Customization (Connect to FastAPI Backend)

**Adapter Layer:**
- Create custom API adapter to replace OpenAI workflow calls
- Map ChatKit's expected request/response format to FastAPI /api/v1/chat
- Handle streaming responses if supported
- Format citations from backend into ChatKit's message format

**UI Customization:**
- Remove/hide OpenAI-specific workflow configuration
- Add custom starter prompts relevant to the textbook
- Style customization for textbook branding (optional)
- Error handling for backend unavailability
- Loading states during API calls

**Integration Points:**
- Replace `getClientSecret` with direct FastAPI calls
- Handle authentication tokens in API requests
- Display citations from RAG responses properly

### 3. Chat History & Protected Routes

**Chat History Persistence:**
- Store chat conversations per user in database
- Load previous conversations on login
- Allow users to view/continue past conversations
- Optional: Delete conversation history

**Protected Routes:**
- Chat interface requires authentication
- Redirect unauthenticated users to login
- Preserve intended destination after login
- Session expiry handling

**User Experience:**
- Show user name/email in chat interface
- "New Chat" functionality
- Conversation list sidebar (optional for MVP)

### 4. Backend Authentication Middleware (US10 - P1 Critical)

**JWT Token Validation:**
- FastAPI middleware to intercept all protected routes
- Extract JWT token from `Authorization: Bearer <token>` header
- Validate token signature using shared `BETTER_AUTH_SECRET`
- Verify token expiration and reject expired tokens

**User Context:**
- Extract user ID from validated token payload
- Make user context available to route handlers via dependency injection
- Log authentication failures (without sensitive data) for security monitoring

**Error Handling:**
- Return 401 Unauthorized for missing, invalid, or expired tokens
- Do not reveal specific validation failure reasons (security best practice)

**Configuration:**
- Share `BETTER_AUTH_SECRET` between frontend and backend via environment variable
- Add PyJWT dependency to backend requirements

## Constraints (MUST Follow)

### Technical Constraints
- **C-001**: Authentication MUST use Better Auth - no custom auth or other auth libraries
- **C-002**: Database MUST be PostgreSQL Neon DB (free tier) - no other databases
- **C-003**: ORM MUST be Drizzle ORM - no Prisma, TypeORM, or raw SQL
- **C-004**: Frontend MUST keep ChatKit React components - no building chat UI from scratch
- **C-005**: Backend API calls MUST include user authentication context (user ID or session)
- **C-006**: All secrets MUST be in environment variables - never hardcoded
- **C-007**: HTTPS MUST be used for all API calls in production

### Documentation Constraint (CRITICAL)
- **C-008**: Before implementing ANY technology (Better Auth, Drizzle, Neon, ChatKit customization), developers MUST use Context7 MCP server to retrieve up-to-date official documentation. NO implementation without MCP-verified documentation first.

### Agent Assignment Constraint
- **C-009**: ChatKit UI customization tasks MUST use `UI-and-ChatKit-customization-agent`
- **C-010**: Authentication configuration MUST use `Auth-Integration-Agent`
- **C-011**: Database schema and Drizzle setup MUST reference Context7 documentation for Drizzle ORM
- **C-012**: Better Auth setup MUST reference Context7 documentation for Better Auth

## Specification Requirements

Follow SpecKit Plus format with these mandatory sections:

### User Scenarios & Testing
Write 10 user stories with priorities (P1, P2, P3):

**P1 - Critical (Must Have for MVP):**
- User registers and logs into the chatbot
- User asks questions through authenticated chat interface
- Chat interface connects to custom FastAPI backend (not OpenAI)
- User session persists across page refreshes
- **Backend validates JWT tokens and secures API endpoints (US10)**

**P2 - Important (Enhances Value):**
- User views and continues previous chat conversations
- User logs out and session is invalidated
- Protected routes redirect unauthenticated users

**P3 - Nice to Have:**
- User authenticates via OAuth (Google/GitHub)
- User deletes their chat history

Each story must include:
- Plain language description
- Why this priority
- Independent test statement
- Acceptance scenarios (Given/When/Then format)

### Functional Requirements
List FR-001 through FR-044+ covering:

**Authentication (FR-001 to FR-010):**
- User registration with email/password
- User login with email/password
- Password hashing (bcrypt or argon2)
- Session creation and management
- Session validation on protected routes
- Logout and session invalidation
- Password requirements (min length, complexity)
- Email uniqueness validation
- CSRF protection
- Rate limiting on auth endpoints

**Database (FR-011 to FR-015):**
- Drizzle schema definition for all entities
- Database migrations
- Connection pooling for Neon
- Data validation before persistence
- Cascade delete for user data

**ChatKit Customization (FR-016 to FR-022):**
- Custom API adapter for FastAPI backend
- Request transformation (ChatKit format -> FastAPI format)
- Response transformation (FastAPI format -> ChatKit format)
- Citation display in chat messages
- Error handling for API failures
- Authentication header injection
- Loading/streaming state management

**Chat History (FR-023 to FR-027):**
- Save chat messages to database
- Load chat history on login
- Create new chat sessions
- Continue previous conversations
- Delete chat history (optional)

**Protected Routes (FR-028 to FR-030):**
- Auth guard component/middleware
- Redirect to login for unauthenticated users
- Preserve return URL after login
- Handle session expiry gracefully

**Backend Authentication Middleware (FR-037 to FR-044):**
- FastAPI middleware to intercept all protected routes
- Extract JWT token from Authorization header
- Validate JWT token signature using shared BETTER_AUTH_SECRET
- Verify token expiration and reject expired tokens
- Extract user ID from token payload
- Make user context available to route handlers
- Return 401 Unauthorized for invalid tokens
- Log authentication failures for security monitoring

### Key Entities
Define these without implementation details:

- **User**: Authenticated user account with profile information
- **Session**: Active login session with expiry
- **Account**: OAuth provider connection (for social login)
- **ChatSession**: A conversation thread between user and chatbot
- **ChatMessage**: Individual message in a conversation (user or assistant)
- **Citation**: Source reference returned by RAG backend
- **AuthConfig**: Authentication provider configuration
- **APIAdapter**: Interface for backend communication

### Success Criteria
Measurable, technology-agnostic outcomes:

**Authentication:**
- SC-001: Users can register and log in within 30 seconds
- SC-002: 100% of protected routes correctly redirect unauthenticated users
- SC-003: Sessions expire correctly after configured timeout
- SC-004: Zero credentials or tokens exposed in client-side code or logs

**Chat Integration:**
- SC-005: Chat messages reach FastAPI backend with <500ms additional latency vs direct API
- SC-006: 100% of RAG citations display correctly in chat UI
- SC-007: Chat works seamlessly after ChatKit->FastAPI adapter integration

**Chat History:**
- SC-008: Users see their previous conversations within 2 seconds of login
- SC-009: Chat history persists correctly across browser sessions

**Backend Authentication Middleware:**
- SC-014: Backend middleware validates tokens in under 10ms average latency
- SC-015: 100% of requests without valid tokens return 401 Unauthorized
- SC-016: 100% of requests with valid tokens include user context in route handlers
- SC-017: Authentication failures are logged with request metadata (no sensitive data)
- SC-018: Backend shares JWT secret with frontend via environment variable configuration

**Development:**
- SC-019: Local development setup completes in under 10 minutes
- SC-020: All Context7 MCP documentation fetched before implementation begins
- SC-021: Zero TypeScript/Python errors in final implementation
- SC-022: All functional requirements have corresponding test coverage

### Edge Cases
Document at least 17:

**Authentication:**
- User tries to register with existing email
- User enters wrong password multiple times (rate limiting)
- Session expires while user is actively chatting
- User tries to access protected route with expired session
- OAuth provider is unavailable (if implemented)

**Chat Integration:**
- FastAPI backend is unavailable during chat
- Backend returns error response
- Long response causes timeout
- User sends message while previous response is streaming

**Chat History:**
- User has no previous chat history
- Database is temporarily unavailable
- User deletes account (cascade delete history)
- Very long chat history causes slow load

**Backend Authentication Middleware:**
- Token is valid but user has been deleted from the database
- Token signature is valid but payload is malformed
- Clock skew between frontend and backend causes valid tokens to appear expired
- Concurrent requests with same token during token refresh window
- Token contains unexpected or additional claims
- Backend receives token in wrong format (e.g., Basic auth instead of Bearer)
- Token is truncated or corrupted during transmission

## Implementation Phases (for Plan Generation)

### Phase 1: Database & Auth Foundation (BLOCKING)
1. Set up Neon PostgreSQL database
2. Create Drizzle schema (users, sessions, accounts)
3. Configure Drizzle migrations
4. Set up Better Auth with email/password

### Phase 2: Frontend Auth Integration
1. Create auth context provider
2. Build login/register pages
3. Add protected route wrapper
4. Integrate auth state with UI

### Phase 3: ChatKit Backend Adapter
1. Create API adapter for FastAPI
2. Transform request/response formats
3. Handle citations display
4. Add auth headers to requests

### Phase 4: Chat History
1. Add ChatHistory schema to Drizzle
2. Implement save/load chat history
3. Add conversation list UI
4. Implement new chat/continue chat

### Phase 5: Backend Authentication Middleware (P1 Critical)
1. Install PyJWT dependency in backend
2. Add BETTER_AUTH_SECRET to backend config
3. Create JWT validation utilities (backend/app/core/security.py)
4. Create authentication middleware (backend/app/middleware/auth.py)
5. Create get_current_user FastAPI dependency
6. Modify chat endpoint to require authentication
7. Add authentication failure logging

### Phase 6: Testing & Polish
1. Integration tests for auth flow
2. E2E tests for chat functionality
3. Backend middleware unit tests
4. Error handling polish
5. Documentation

## Agent Usage for Implementation

When generating tasks, assign agents as follows:

| Task Area | Agent | Skill |
|-----------|-------|-------|
| Drizzle schema | backend-architect-and-sdk-agent | drizzle-schema-generation |
| Better Auth config | Auth-Integration-Agent | better-auth-configuration |
| Frontend auth UI | Auth-Integration-Agent | frontend-auth-integration |
| ChatKit customization | UI-and-ChatKit-customization-agent | chatkit-backend-adapter |
| UI theming | UI-and-ChatKit-customization-agent | ui-customization |
| Selection Q&A | UI-and-ChatKit-customization-agent | selection-qa |
| Backend auth middleware | backend-architect-and-sdk-agent | fastapi-scaffolding |

## Output Format

The specification must be:
- Technology-agnostic in language (describe WHAT not HOW)
- User-focused (not developer-focused)
- Testable (every requirement has clear pass/fail criteria)
- Measurable (success criteria have numbers)
- Complete (no [NEEDS CLARIFICATION] markers unless truly ambiguous)

Do NOT include:
- Code snippets
- Detailed database schemas
- API endpoint implementations
- Framework-specific implementation details

Focus on:
- User value and outcomes
- Business requirements
- Testable acceptance criteria
- Measurable success metrics
- Agent and skill assignments for implementation
```

---

## EXPECTED OUTPUT STRUCTURE

```markdown
# Feature Specification: Authentication & Frontend-Backend Integration

**Feature Branch**: `002-auth-frontend-backend-integration`
**Created**: [DATE]
**Status**: Draft
**Input**: Authentication (Better Auth + Neon + Drizzle) and ChatKit-FastAPI integration with chat history

---

## Overview

This specification defines the authentication system and frontend-backend integration for the Physical AI & Humanoid Robotics textbook chatbot. It covers user registration/login, session management, ChatKit customization to connect to the custom FastAPI backend, and chat history persistence.

---

## User Scenarios & Testing

### User Story 1 - Register and Login (Priority: P1)
...

### User Story 2 - Chat via Authenticated Interface (Priority: P1)
...

### User Story 3 - ChatKit Connects to FastAPI Backend (Priority: P1)
...

### User Story 4 - Session Persistence (Priority: P1)
...

### User Story 5 - View Previous Conversations (Priority: P2)
...

### User Story 6 - Logout (Priority: P2)
...

### User Story 7 - Protected Routes (Priority: P2)
...

### User Story 8 - OAuth Login (Priority: P3)
...

### User Story 9 - Delete Chat History (Priority: P3)
...

### Edge Cases
...

---

## Requirements

### Functional Requirements - Authentication
- FR-001: ... (Registration)
- FR-002: ... (Login)
...

### Functional Requirements - Database
- FR-011: ... (Schema)
...

### Functional Requirements - ChatKit Customization
- FR-016: ... (API Adapter)
...

### Functional Requirements - Chat History
- FR-023: ... (Persistence)
...

### Functional Requirements - Protected Routes
- FR-028: ...
...

### Key Entities
- User: ...
- Session: ...
- ChatSession: ...
- ChatMessage: ...
...

---

## Success Criteria

### Measurable Outcomes
- SC-001: ... (Auth performance)
- SC-005: ... (Chat latency)
- SC-008: ... (History load time)
...

---

## Constraints

### Technical Constraints
- C-001: MUST use Better Auth
- C-002: MUST use PostgreSQL Neon DB
- C-003: MUST use Drizzle ORM
- C-004: MUST use ChatKit React components
...

### Documentation Constraint
- C-008: MUST use Context7 MCP for all technology documentation before implementation

### Agent Constraints
- C-009: UI-and-ChatKit-customization-agent for ChatKit work
- C-010: Auth-Integration-Agent for authentication work
...

---

## Dependencies

- FastAPI backend (already deployed)
- Neon PostgreSQL account
- Better Auth library
- Drizzle ORM
- OpenAI ChatKit React
- Context7 MCP server for documentation

---

## Assumptions

- FastAPI backend is stable and accessible
- Neon free tier has sufficient capacity
- User base will not exceed free tier limits initially
- Better Auth supports all required features
...

---

## Out of Scope

- Multi-factor authentication
- Admin dashboard for user management
- Real-time collaboration features
- Mobile app authentication
- Payment/subscription features
...
```

---

## USAGE

1. Copy the PROMPT section above
2. Run `/sp.specify` in Claude Code
3. Paste the prompt when asked for feature description
4. Or give the prompt directly to any AI for spec generation

---

## CONTEXT7 MCP DOCUMENTATION REQUIREMENTS

Before implementing any task, fetch documentation for:

1. **Better Auth**: `mcp__context7__resolve-library-id` with "better-auth"
2. **Drizzle ORM**: `mcp__context7__resolve-library-id` with "drizzle-orm"
3. **Neon PostgreSQL**: `mcp__context7__resolve-library-id` with "neon postgres"
4. **OpenAI ChatKit**: `mcp__context7__resolve-library-id` with "openai chatkit"
5. **Next.js App Router**: `mcp__context7__resolve-library-id` with "nextjs"
6. **FastAPI Security**: `mcp__context7__resolve-library-id` with "fastapi" (for middleware/dependencies)
7. **PyJWT**: `mcp__context7__resolve-library-id` with "pyjwt" (for JWT validation on backend)

This is MANDATORY per project constitution. No implementation without MCP-verified documentation.

---

## RELATED ARTIFACTS

- Constitution: `.specify/memory/constitution.md`
- Previous RAG Backend Spec: `specs/001-rag-chatbot-backend/spec.md`
- Frontend Code: `frontend/`
- Backend Code: `backend/`
