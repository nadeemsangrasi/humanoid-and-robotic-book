# Plan Prompt: Authentication & Frontend-Backend Integration

Use this prompt with `/sp.plan` or give it to an AI to create an implementation plan from the specification.

---

## PROMPT

```
Create a SpecKit Plus implementation plan for the Authentication & Frontend-Backend Integration feature based on the specification at `specs/002-auth-frontend-integration/spec.md`.

## Input Specification Summary

The specification covers:
- User Authentication: Registration, login, JWT sessions, logout (Better Auth + Neon + Drizzle)
- ChatKit Backend Adapter: Customizing ChatKit UI to connect to FastAPI RAG backend
- Chat History Persistence: Storing and retrieving user conversations
- Protected Routes: Authenticated access to chat interface

## Clarified Decisions (from /sp.clarify)

These decisions were made during clarification and MUST be followed:

1. **Session Storage**: JWT tokens (stateless, validated via backend middleware)
2. **Auth Header Format**: `Authorization: Bearer <jwt>` (standard OAuth2 pattern)
3. **Backend URL Config**: Environment variable `NEXT_PUBLIC_BACKEND_URL`
4. **Token Storage**: httpOnly cookie (XSS-immune, with cookie-to-header extraction)
5. **Password Hashing**: bcrypt algorithm (Better Auth default)

## Technical Context

**Framework/Version**: Next.js 15 (App Router)
**Language**: TypeScript
**Primary Dependencies**:
- Better Auth (authentication library)
- Drizzle ORM (database ORM)
- @neondatabase/serverless (Neon PostgreSQL driver)
- @openai/chatkit-react (existing chat UI)
- jose (JWT handling if needed)

**Database**: PostgreSQL on Neon (free tier)
**Authentication**: Better Auth with email/password + JWT
**Existing Backend**: FastAPI on Hugging Face Spaces
  - POST /api/v1/chat - RAG Q&A endpoint
  - GET /health - Health check
**Testing**: Jest + React Testing Library
**Project Type**: Frontend (Next.js) in `frontend/` folder
**Performance Goals**:
  - Registration/login < 30s/15s
  - Chat history load < 2s
  - < 500ms added latency for chat

## Constitution Check

Verify against project constitution before implementation:
- [ ] Uses Better Auth library (C-001)
- [ ] Uses PostgreSQL Neon DB free tier (C-002)
- [ ] Uses Drizzle ORM only (C-003)
- [ ] Uses existing ChatKit React components (C-004)
- [ ] Backend calls include auth context (C-005)
- [ ] All secrets in environment variables (C-006)
- [ ] HTTPS for production API calls (C-007)
- [ ] Context7 MCP used for all documentation (C-008)

## Context7 MCP Documentation Requirements (CRITICAL)

Before implementing ANY component, MUST fetch documentation:

1. **Better Auth**: `resolve-library-id` → "better-auth" → `get-library-docs`
   - Topics: installation, nextjs-integration, email-password, jwt, session

2. **Drizzle ORM**: `resolve-library-id` → "drizzle-orm" → `get-library-docs`
   - Topics: postgres, schema, migrations, queries

3. **Neon PostgreSQL**: `resolve-library-id` → "neon" → `get-library-docs`
   - Topics: serverless-driver, connection-pooling

4. **Next.js App Router**: `resolve-library-id` → "nextjs" → `get-library-docs`
   - Topics: app-router, middleware, api-routes, cookies

This is MANDATORY. No implementation without MCP-verified documentation.

## Project Structure

Generate/modify this structure in `frontend/`:

```text
frontend/
├── app/
│   ├── (auth)/                       # Auth route group (public)
│   │   ├── login/
│   │   │   └── page.tsx              # Login page
│   │   ├── register/
│   │   │   └── page.tsx              # Registration page
│   │   └── layout.tsx                # Auth layout (no sidebar)
│   ├── (protected)/                  # Protected route group
│   │   ├── chat/
│   │   │   └── page.tsx              # Main chat interface
│   │   ├── history/
│   │   │   └── page.tsx              # Conversation history list
│   │   └── layout.tsx                # Protected layout with auth check
│   ├── api/
│   │   ├── auth/
│   │   │   └── [...all]/
│   │   │       └── route.ts          # Better Auth API handler
│   │   └── chat/
│   │       ├── route.ts              # Chat proxy to FastAPI
│   │       └── history/
│   │           └── route.ts          # Chat history CRUD
│   ├── layout.tsx                    # Root layout
│   └── page.tsx                      # Landing/redirect page
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx             # Login form component
│   │   ├── RegisterForm.tsx          # Registration form component
│   │   ├── LogoutButton.tsx          # Logout button
│   │   └── AuthProvider.tsx          # Auth context provider
│   ├── chat/
│   │   ├── ChatKitAdapter.tsx        # Adapted ChatKit for FastAPI
│   │   ├── CitationDisplay.tsx       # Citation rendering component
│   │   ├── ConversationList.tsx      # Sidebar conversation list
│   │   └── NewChatButton.tsx         # New conversation button
│   └── ui/
│       └── ProtectedRoute.tsx        # Auth guard wrapper
├── lib/
│   ├── auth.ts                       # Better Auth client config
│   ├── auth-server.ts                # Better Auth server config
│   ├── db/
│   │   ├── index.ts                  # Drizzle client instance
│   │   ├── schema.ts                 # Drizzle schema definitions
│   │   └── migrations/               # Drizzle migrations folder
│   ├── api/
│   │   ├── backend-adapter.ts        # FastAPI request/response adapter
│   │   └── chat-history.ts           # Chat history service
│   └── utils/
│       └── jwt.ts                    # JWT extraction utilities
├── middleware.ts                     # Next.js middleware for auth
├── drizzle.config.ts                 # Drizzle configuration
├── .env.example                      # Environment variables template
└── .env.local                        # Local environment (gitignored)
```

## Plan Phases

### Phase 0: Research & Context7 Documentation

Fetch and document official patterns for:

1. **Better Auth + Next.js App Router**
   - Installation and configuration
   - Email/password authentication setup
   - JWT token configuration
   - Session handling with httpOnly cookies
   - API route handler setup

2. **Drizzle ORM + Neon**
   - Neon serverless driver setup
   - Schema definition patterns
   - Migration workflow
   - Connection pooling best practices

3. **ChatKit Customization**
   - How to replace getClientSecret with custom API
   - Response format transformation
   - Citation display patterns

4. **Next.js Middleware**
   - Auth middleware patterns
   - Protected route implementation
   - Cookie handling

**Output**: `specs/002-auth-frontend-integration/research.md`

### Phase 1: Design & Contracts

1. **Data Model** (`data-model.md`):
   - User (id, email, name, passwordHash, createdAt, updatedAt)
   - Account (id, userId, provider, providerAccountId, accessToken, refreshToken)
   - ChatSession (id, userId, title, createdAt, updatedAt)
   - ChatMessage (id, sessionId, role, content, citations, createdAt)

2. **API Contracts** (`contracts/api-contracts.md`):
   - POST /api/auth/* - Better Auth endpoints (handled by library)
   - POST /api/chat - Proxy to FastAPI with auth
   - GET /api/chat/history - List user conversations
   - GET /api/chat/history/[id] - Get conversation messages
   - POST /api/chat/history - Create new conversation
   - DELETE /api/chat/history/[id] - Delete conversation

3. **Quickstart** (`quickstart.md`):
   - Environment setup (Neon DB, env vars)
   - Running migrations
   - Local development
   - Testing authentication

**Output**: `data-model.md`, `contracts/api-contracts.md`, `quickstart.md`

### Phase 2: Database & Auth Foundation (BLOCKING)

This phase BLOCKS all others. Must complete first.

1. Set up Neon PostgreSQL database
2. Create Drizzle schema for users and accounts (Better Auth tables)
3. Run initial migrations
4. Configure Better Auth server and client
5. Create API route handler for Better Auth

**Agent**: Auth-Integration-Agent
**Skills**: drizzle-schema-generation, better-auth-configuration

### Phase 3: Frontend Auth UI

1. Create AuthProvider context
2. Build LoginForm component
3. Build RegisterForm component
4. Build LogoutButton component
5. Create login and register pages
6. Implement protected route wrapper

**Agent**: Auth-Integration-Agent
**Skills**: frontend-auth-integration

### Phase 4: ChatKit Backend Adapter

1. Create backend-adapter.ts for FastAPI communication
2. Implement request transformation (ChatKit → FastAPI format)
3. Implement response transformation (FastAPI → ChatKit format with citations)
4. Create ChatKitAdapter component replacing getClientSecret
5. Add JWT token to Authorization header
6. Implement error handling and retry logic

**Agent**: UI-and-ChatKit-customization-agent
**Skills**: chatkit-backend-adapter

### Phase 5: Chat History Persistence

1. Add ChatSession and ChatMessage schemas to Drizzle
2. Run migrations for new tables
3. Create chat-history.ts service layer
4. Implement API routes for history CRUD
5. Build ConversationList component
6. Integrate history loading on login
7. Implement new chat and continue chat functionality

**Agent**: Auth-Integration-Agent + UI-and-ChatKit-customization-agent
**Skills**: drizzle-schema-generation, frontend-auth-integration, ui-customization

### Phase 6: Protected Routes & Middleware

1. Create Next.js middleware for auth checks
2. Implement route protection logic
3. Add return URL preservation
4. Handle session expiry gracefully

**Agent**: Auth-Integration-Agent
**Skills**: frontend-auth-integration

### Phase 7: Testing & Polish

1. Unit tests for auth components
2. Integration tests for API routes
3. E2E tests for auth flow
4. Error handling refinement
5. Documentation updates

**Agent**: backend-architect-and-sdk-agent
**Skills**: fastapi-scaffolding (for test patterns)

## Agent Assignment Summary

| Component | Agent | Skill |
|-----------|-------|-------|
| Drizzle schema | Auth-Integration-Agent | drizzle-schema-generation |
| Better Auth config | Auth-Integration-Agent | better-auth-configuration |
| Auth UI components | Auth-Integration-Agent | frontend-auth-integration |
| ChatKit adapter | UI-and-ChatKit-customization-agent | chatkit-backend-adapter |
| Citation display | UI-and-ChatKit-customization-agent | ui-customization |
| Conversation list UI | UI-and-ChatKit-customization-agent | ui-customization |
| Next.js middleware | Auth-Integration-Agent | frontend-auth-integration |
| API routes | Auth-Integration-Agent | better-auth-configuration |

## Environment Variables

Document these in `.env.example`:

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Backend API
NEXT_PUBLIC_BACKEND_URL=https://your-space.hf.space

# Optional: OAuth (P3)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

## Output Format

The plan must include:

1. **Technical Context** - All fields filled (no NEEDS CLARIFICATION)
2. **Constitution Check** - All gates passed with checkmarks
3. **Project Structure** - Concrete file paths for frontend/
4. **research.md** - Context7 MCP documentation findings
5. **data-model.md** - Drizzle schema entity definitions
6. **contracts/api-contracts.md** - API specifications
7. **quickstart.md** - Developer setup instructions
8. **Agent assignments** - Which agent/skill handles each task

## Key Rules

- MUST use Context7 MCP to fetch official documentation BEFORE any implementation
- All paths must be relative to frontend/ folder
- ERROR if constitution gates fail
- ERROR if NEEDS CLARIFICATION items remain after Phase 0
- Include agent/skill assignment for every implementation task
- JWT tokens stored in httpOnly cookies (clarified decision)
- Bearer token format for backend API calls (clarified decision)
```

---

## EXPECTED OUTPUT FILES

After running `/sp.plan`, these files should be created:

```
specs/002-auth-frontend-integration/
├── plan.md                    # Main implementation plan
├── research.md                # Phase 0 Context7 MCP findings
├── data-model.md              # Drizzle schema definitions
├── contracts/
│   └── api-contracts.md       # API specifications
└── quickstart.md              # Developer setup guide
```

---

## USAGE

1. Ensure specification exists at `specs/002-auth-frontend-integration/spec.md`
2. Ensure clarifications have been completed (`## Clarifications` section exists)
3. Run `/sp.plan` in Claude Code
4. Or give this prompt to an AI along with the specification
5. Verify Context7 MCP is called for all technology documentation
6. Verify all outputs are created and no NEEDS CLARIFICATION remains

---

## CONTEXT7 MCP COMMANDS TO RUN

Before planning, run these MCP commands:

```
1. mcp__context7__resolve-library-id("better-auth")
   → mcp__context7__get-library-docs(id, topic="nextjs")
   → mcp__context7__get-library-docs(id, topic="email-password")
   → mcp__context7__get-library-docs(id, topic="jwt")

2. mcp__context7__resolve-library-id("drizzle-orm")
   → mcp__context7__get-library-docs(id, topic="postgres")
   → mcp__context7__get-library-docs(id, topic="schema")
   → mcp__context7__get-library-docs(id, topic="migrations")

3. mcp__context7__resolve-library-id("neon")
   → mcp__context7__get-library-docs(id, topic="serverless")

4. mcp__context7__resolve-library-id("nextjs")
   → mcp__context7__get-library-docs(id, topic="middleware")
   → mcp__context7__get-library-docs(id, topic="app-router")
```

---

## RELATED ARTIFACTS

- Specification: `specs/002-auth-frontend-integration/spec.md`
- Existing Frontend: `frontend/`
- Backend Spec (reference): `specs/001-rag-chatbot-backend/`
- Constitution: `.specify/memory/constitution.md`
- Clarification PHR: `history/prompts/002-auth-frontend-integration/0002-spec-clarification-session-auth-frontend.spec.prompt.md`
