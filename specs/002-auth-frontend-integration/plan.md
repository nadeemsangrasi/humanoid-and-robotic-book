# Implementation Plan: Authentication & Frontend-Backend Integration

**Branch**: `002-auth-frontend-integration` | **Date**: 2025-12-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-auth-frontend-integration/spec.md`

---

## Summary

Implement user authentication and frontend-backend integration for the Physical AI & Humanoid Robotics textbook chatbot. This includes:

1. **User Authentication**: Better Auth with Drizzle ORM + Neon PostgreSQL for registration, login, session management
2. **ChatKit Backend Adapter**: Transform ChatKit UI to communicate with FastAPI RAG backend instead of OpenAI
3. **Chat History Persistence**: Store and retrieve user conversations across sessions
4. **Protected Routes**: Next.js middleware for authenticated access to chat interface
5. **Backend Authentication Middleware**: FastAPI middleware to verify JWT tokens and secure API endpoints

**Technical Approach**: Use Better Auth's native Drizzle adapter with JWT sessions stored in httpOnly cookies. Create an API adapter layer to transform requests/responses between ChatKit format and FastAPI backend. Store chat history in Neon PostgreSQL with cascade deletion on user removal. Implement JWT token verification on FastAPI backend using PyJWT with shared secret configuration.

---

## Technical Context

**Language/Version**: TypeScript 5.x, Node.js 18+
**Framework/Version**: Next.js 15 (App Router)
**Primary Dependencies**:
- `better-auth` (authentication)
- `better-auth/adapters/drizzle` (Drizzle adapter)
- `drizzle-orm` (ORM)
- `@neondatabase/serverless` (database driver)
- `@openai/chatkit-react` (existing chat UI)
- `PyJWT` (backend JWT validation)
- `python-jose[cryptography]` (optional: backend JWT with crypto support)

**Storage**: PostgreSQL on Neon (free tier)
**Testing**: Jest + React Testing Library
**Target Platform**: Web (modern browsers)
**Project Type**: Frontend (Next.js in `frontend/` folder)
**Performance Goals**:
- Registration/login < 30 seconds
- Chat response latency < 500ms additional vs direct API
- Chat history load < 2 seconds

**Constraints**:
- Must use Better Auth (C-001)
- Must use Neon PostgreSQL (C-002)
- Must use Drizzle ORM (C-003)
- Must use existing ChatKit components (C-004)
- All secrets in environment variables (C-006)
- HTTPS in production (C-007)
- Context7 MCP for all documentation (C-008)

**Scale/Scope**: < 1000 initial users, free tier limits

---

## Constitution Check

*GATE: All items must pass before implementation.*

| Gate | Status | Evidence |
|------|--------|----------|
| C-001: Uses Better Auth | ✅ PASS | `better-auth` library with `drizzleAdapter` |
| C-002: Uses PostgreSQL Neon DB | ✅ PASS | `@neondatabase/serverless` driver |
| C-003: Uses Drizzle ORM only | ✅ PASS | `drizzle-orm/neon-http` with schema in `lib/db/schema.ts` |
| C-004: Uses ChatKit React | ✅ PASS | Modifying existing `ChatKitPanel.tsx`, not replacing |
| C-005: Backend calls include auth | ✅ PASS | JWT in `Authorization: Bearer` header |
| C-006: Secrets in env vars | ✅ PASS | `DATABASE_URL`, `BETTER_AUTH_SECRET` in `.env.local` |
| C-007: HTTPS in production | ✅ PASS | Neon requires SSL, backend on HF Spaces uses HTTPS |
| C-008: Context7 MCP used | ✅ PASS | All patterns verified via Context7 (see research.md) |

**Result**: All gates passed. Proceeding with implementation.

---

## Project Structure

### Documentation (this feature)

```text
specs/002-auth-frontend-integration/
├── spec.md                    # Feature specification
├── plan.md                    # This implementation plan
├── research.md                # Context7 MCP findings
├── data-model.md              # Drizzle schema definitions
├── quickstart.md              # Developer setup guide
├── contracts/
│   └── api-contracts.md       # API specifications
└── checklists/
    └── requirements.md        # Spec quality checklist
```

### Source Code (frontend/)

```text
frontend/
├── app/
│   ├── (auth)/                         # NEW: Public auth route group
│   │   ├── login/
│   │   │   └── page.tsx                # Login page
│   │   ├── register/
│   │   │   └── page.tsx                # Register page
│   │   └── layout.tsx                  # Auth layout
│   ├── (protected)/                    # NEW: Protected route group
│   │   ├── chat/
│   │   │   └── page.tsx                # Chat interface
│   │   ├── history/
│   │   │   └── page.tsx                # Chat history
│   │   └── layout.tsx                  # Protected layout
│   ├── api/
│   │   ├── auth/
│   │   │   └── [...all]/
│   │   │       └── route.ts            # NEW: Better Auth handler
│   │   ├── chat/
│   │   │   ├── route.ts                # NEW: Backend proxy
│   │   │   └── history/
│   │   │       └── route.ts            # NEW: Chat history API
│   │   └── create-session/
│   │       └── route.ts                # EXISTING (may remove)
│   ├── App.tsx                         # EXISTING
│   ├── layout.tsx                      # MODIFY: Add AuthProvider
│   └── page.tsx                        # EXISTING
├── components/
│   ├── auth/                           # NEW: Auth components
│   │   ├── AuthProvider.tsx
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── LogoutButton.tsx
│   ├── chat/                           # NEW: Chat components
│   │   ├── CitationDisplay.tsx
│   │   ├── ConversationList.tsx
│   │   └── NewChatButton.tsx
│   ├── ChatKitPanel.tsx                # MODIFY: Backend adapter
│   └── ErrorOverlay.tsx                # EXISTING
├── hooks/
│   └── useColorScheme.ts               # EXISTING
├── lib/
│   ├── auth.ts                         # NEW: Better Auth server config
│   ├── auth-client.ts                  # NEW: Better Auth client
│   ├── config.ts                       # MODIFY: Add BACKEND_URL
│   ├── db/
│   │   ├── index.ts                    # NEW: Drizzle connection
│   │   └── schema.ts                   # NEW: Schema definitions
│   └── api/
│       ├── backend-adapter.ts          # NEW: FastAPI adapter
│       └── chat-history.ts             # NEW: History service
├── drizzle/                            # NEW: Migrations (generated)
├── middleware.ts                       # NEW: Auth middleware
├── drizzle.config.ts                   # NEW: Drizzle Kit config
├── .env.local                          # NEW: Environment variables
└── package.json                        # MODIFY: Add dependencies
```

**Structure Decision**: Using Next.js App Router with route groups (`(auth)` for public routes, `(protected)` for authenticated routes). This follows Next.js 15 conventions and enables shared layouts per route group.

### Backend Code (backend/)

```text
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── chat.py                    # MODIFY: Add auth dependency
│   │       └── health.py                  # EXISTING (no auth needed)
│   ├── core/
│   │   ├── config.py                      # MODIFY: Add BETTER_AUTH_SECRET
│   │   └── security.py                    # NEW: JWT validation utilities
│   ├── middleware/
│   │   └── auth.py                        # NEW: Authentication middleware
│   └── main.py                            # MODIFY: Register middleware
├── requirements.txt                       # MODIFY: Add PyJWT
└── .env.example                           # MODIFY: Add BETTER_AUTH_SECRET
```

---

## Implementation Phases

### Phase 1: Database & Auth Foundation

**Agent**: Auth-Integration-Agent
**Skill**: drizzle-schema-generation, better-auth-configuration
**Blocking**: Yes (all other phases depend on this)

**Tasks**:
1. Create Neon PostgreSQL database and obtain credentials
2. Install dependencies: `better-auth`, `drizzle-orm`, `@neondatabase/serverless`
3. Create `lib/db/index.ts` with Neon connection
4. Create `lib/db/schema.ts` with Better Auth tables (user, session, account)
5. Create `drizzle.config.ts`
6. Run `npx drizzle-kit generate` and `npx drizzle-kit migrate`
7. Create `lib/auth.ts` with `drizzleAdapter`
8. Create `app/api/auth/[...all]/route.ts` with `toNextJsHandler`
9. Create `lib/auth-client.ts` with `createAuthClient`
10. Test auth endpoints: `/api/auth/sign-up`, `/api/auth/sign-in`

**Acceptance Criteria**:
- [ ] Database tables created in Neon
- [ ] Migrations applied successfully
- [ ] Sign-up creates user in database
- [ ] Sign-in returns session token
- [ ] Session stored in httpOnly cookie

---

### Phase 2: Auth UI Components

**Agent**: Auth-Integration-Agent
**Skill**: frontend-auth-integration

**Tasks**:
1. Create `components/auth/AuthProvider.tsx` (React context)
2. Create `components/auth/LoginForm.tsx`
3. Create `components/auth/RegisterForm.tsx`
4. Create `components/auth/LogoutButton.tsx`
5. Create `app/(auth)/login/page.tsx`
6. Create `app/(auth)/register/page.tsx`
7. Create `app/(auth)/layout.tsx`
8. Modify `app/layout.tsx` to wrap with AuthProvider

**Acceptance Criteria**:
- [ ] Login form validates input
- [ ] Login form handles errors gracefully
- [ ] Registration form enforces password requirements
- [ ] Logout button clears session
- [ ] Auth state available via `useSession` hook

---

### Phase 3: Protected Routes

**Agent**: Auth-Integration-Agent
**Skill**: frontend-auth-integration

**Tasks**:
1. Create `middleware.ts` with auth check
2. Create `app/(protected)/layout.tsx` with server-side session validation
3. Create `app/(protected)/chat/page.tsx` (move chat interface)
4. Test route protection (redirect unauthenticated users)
5. Implement callback URL preservation

**Acceptance Criteria**:
- [ ] Unauthenticated users redirected to `/login`
- [ ] Callback URL preserved in query parameter
- [ ] After login, user redirected to original destination
- [ ] Expired sessions handled gracefully

---

### Phase 4: ChatKit Backend Adapter

**Agent**: UI-and-ChatKit-customization-agent
**Skill**: chatkit-backend-adapter

**Tasks**:
1. Create `lib/api/backend-adapter.ts`
   - Transform ChatKit request → FastAPI format
   - Transform FastAPI response → ChatKit format
   - Parse citations from response
2. Create `app/api/chat/route.ts` as proxy to FastAPI
   - Validate session
   - Add `Authorization: Bearer` header
   - Forward to `${NEXT_PUBLIC_BACKEND_URL}/api/v1/chat`
3. Modify `components/ChatKitPanel.tsx`
   - Replace `getClientSecret` with backend adapter call
   - Keep existing theme, error handling, widget actions
4. Create `components/chat/CitationDisplay.tsx`
5. Update `lib/config.ts` to add `BACKEND_URL`
6. Test end-to-end chat flow

**Acceptance Criteria**:
- [ ] Chat messages sent to FastAPI backend
- [ ] Responses displayed in ChatKit UI
- [ ] Citations rendered with clickable links
- [ ] Errors displayed in user-friendly format
- [ ] Loading state shown during API calls

---

### Phase 5: Chat History

**Agent**: UI-and-ChatKit-customization-agent + Auth-Integration-Agent
**Skill**: ui-customization, drizzle-schema-generation

**Tasks**:
1. Add `chatSession` and `chatMessage` tables to schema
2. Run migrations
3. Create `lib/api/chat-history.ts` service
4. Create `app/api/chat/history/route.ts`
5. Create `components/chat/ConversationList.tsx`
6. Create `components/chat/NewChatButton.tsx`
7. Create `app/(protected)/history/page.tsx`
8. Integrate history with chat UI

**Acceptance Criteria**:
- [ ] Messages saved to database after each exchange
- [ ] Conversation list loads on login
- [ ] User can continue previous conversations
- [ ] User can start new conversation
- [ ] User can delete conversations

---

### Phase 5.5: Backend Authentication Middleware (US10 - P1)

**Agent**: backend-architect-and-sdk-agent
**Skill**: fastapi-scaffolding

**Purpose**: Secure the FastAPI backend by validating JWT tokens from authenticated frontend users

**Tasks**:
1. Install PyJWT dependency in backend (`pip install PyJWT`)
2. Add `BETTER_AUTH_SECRET` to backend config and `.env.example`
3. Create `backend/app/core/security.py` with JWT validation utilities
4. Create `backend/app/middleware/auth.py` with authentication middleware
5. Create `get_current_user` dependency for FastAPI routes
6. Modify `backend/app/api/v1/chat.py` to require authentication
7. Add authentication failure logging
8. Update backend `.env.example` with new environment variables

**Acceptance Criteria**:
- [ ] Valid JWT tokens are accepted and user ID extracted
- [ ] Invalid/expired tokens return 401 Unauthorized
- [ ] Missing Authorization header returns 401 Unauthorized
- [ ] User context available in route handlers via dependency injection
- [ ] Authentication failures logged (without sensitive data)
- [ ] Shared secret configured via `BETTER_AUTH_SECRET` environment variable

---

### Phase 6: Testing & Polish

**Agent**: backend-architect-and-sdk-agent

**Tasks**:
1. Unit tests for auth components
2. Integration tests for API routes
3. E2E tests for auth flow
4. Error handling refinement
5. Update `.env.example` with all required variables
6. Documentation updates

**Acceptance Criteria**:
- [ ] All tests pass
- [ ] No TypeScript errors
- [ ] Setup guide tested on clean install
- [ ] Error messages are user-friendly

---

## Agent Assignment Summary

| Phase | Component | Agent | Skill |
|-------|-----------|-------|-------|
| 1 | Database & Auth | Auth-Integration-Agent | drizzle-schema-generation |
| 1 | Better Auth Config | Auth-Integration-Agent | better-auth-configuration |
| 2 | Auth UI | Auth-Integration-Agent | frontend-auth-integration |
| 3 | Protected Routes | Auth-Integration-Agent | frontend-auth-integration |
| 4 | ChatKit Adapter | UI-and-ChatKit-customization-agent | chatkit-backend-adapter |
| 4 | Citation Display | UI-and-ChatKit-customization-agent | ui-customization |
| 5 | Chat History | Auth-Integration-Agent | drizzle-schema-generation |
| 5 | History UI | UI-and-ChatKit-customization-agent | ui-customization |
| 5.5 | Backend Auth Middleware | backend-architect-and-sdk-agent | fastapi-scaffolding |
| 6 | Testing | backend-architect-and-sdk-agent | - |

---

## Dependencies

### NPM Packages to Add (Frontend)

```bash
# Authentication
npm install better-auth @better-fetch/fetch

# Database ORM
npm install drizzle-orm @neondatabase/serverless

# Development
npm install -D drizzle-kit
```

### Python Packages to Add (Backend)

```bash
# JWT Token Validation
pip install PyJWT

# Or with cryptographic support (optional)
pip install python-jose[cryptography]
```

### Environment Variables

**Frontend (.env.local)**
```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://...

# Better Auth
BETTER_AUTH_SECRET=your-secure-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Backend API
NEXT_PUBLIC_BACKEND_URL=https://your-space.hf.space

# Optional: OAuth (P3)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

**Backend (.env)**
```env
# JWT Secret (MUST match frontend BETTER_AUTH_SECRET)
BETTER_AUTH_SECRET=your-secure-secret-key-min-32-chars

# Existing backend config
GOOGLE_API_KEY=...
QDRANT_URL=...
```

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Neon free tier limits | Low | High | Monitor usage, implement rate limiting |
| Better Auth breaking changes | Low | Medium | Pin version, use Context7 for docs |
| ChatKit API changes | Low | Medium | Adapter layer isolates changes |
| Backend unavailability | Medium | High | Implement retry logic, graceful errors |
| Session expiry during chat | Medium | Medium | Refresh session on activity |
| JWT secret mismatch frontend/backend | Medium | High | Document shared secret requirement, validate on startup |
| Clock skew causing token validation failures | Low | Medium | Add reasonable time tolerance (e.g., 60 seconds leeway) |

---

## Related Artifacts

- **Specification**: [spec.md](./spec.md)
- **Research**: [research.md](./research.md)
- **Data Model**: [data-model.md](./data-model.md)
- **API Contracts**: [contracts/api-contracts.md](./contracts/api-contracts.md)
- **Quickstart**: [quickstart.md](./quickstart.md)
- **Constitution**: [../../.specify/memory/constitution.md](../../.specify/memory/constitution.md)

---

## Next Steps

Run `/sp.tasks` to generate the detailed task list with:
- Individual task definitions
- Acceptance criteria per task
- Test cases
- Agent assignments
