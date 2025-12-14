# Tasks Prompt: Authentication & Frontend-Backend Integration

Use this prompt with `/sp.tasks` or give it to an AI to generate the detailed task list from the implementation plan.

**IMPORTANT**: All tasks must reference the existing frontend structure and Context7 MCP-verified patterns from the plan.

---

## PROMPT

```
Generate a SpecKit Plus task list for the Authentication & Frontend-Backend Integration feature based on:
- Specification: `specs/002-auth-frontend-integration/spec.md`
- Implementation Plan: `specs/002-auth-frontend-integration/plan.md`
- Data Model: `specs/002-auth-frontend-integration/data-model.md`
- API Contracts: `specs/002-auth-frontend-integration/contracts/api-contracts.md`

## Existing Frontend Structure

The frontend already has Next.js 15 with OpenAI ChatKit initialized:

```text
frontend/
├── app/
│   ├── api/create-session/route.ts    # Existing ChatKit session endpoint
│   ├── App.tsx                        # Main app component (client)
│   ├── layout.tsx                     # Root layout
│   └── page.tsx                       # Home page
├── components/
│   ├── ChatKitPanel.tsx               # Main ChatKit component (419 lines)
│   └── ErrorOverlay.tsx               # Error display
├── hooks/useColorScheme.ts            # Theme hook
├── lib/config.ts                      # ChatKit config
└── package.json                       # Next.js 15.5.4, React 19.2.0
```

## Task Generation Requirements

### Task Format
Each task MUST include:
1. **ID**: Sequential number (T-001, T-002, etc.)
2. **Title**: Short descriptive title
3. **Phase**: Which implementation phase (1-6)
4. **Agent**: Assigned agent from plan
5. **Skill**: Required skill
6. **Dependencies**: List of blocking task IDs
7. **Description**: What to implement
8. **Files**: List of files to create/modify
9. **Acceptance Criteria**: Checkboxes for completion
10. **Test Cases**: Specific tests to verify

### Phase 1: Database & Auth Foundation

Generate tasks for:
- T-001: Create Neon database and configure credentials
- T-002: Install auth and database dependencies
- T-003: Create Drizzle database connection (lib/db/index.ts)
- T-004: Create Drizzle schema for auth tables (lib/db/schema.ts)
- T-005: Create drizzle.config.ts
- T-006: Run initial database migrations
- T-007: Create Better Auth server config (lib/auth.ts)
- T-008: Create Better Auth API route (app/api/auth/[...all]/route.ts)
- T-009: Create Better Auth client (lib/auth-client.ts)
- T-010: Test auth endpoints

### Phase 2: Auth UI Components

Generate tasks for:
- T-011: Create AuthProvider component
- T-012: Create LoginForm component
- T-013: Create RegisterForm component
- T-014: Create LogoutButton component
- T-015: Create login page (app/(auth)/login/page.tsx)
- T-016: Create register page (app/(auth)/register/page.tsx)
- T-017: Create auth layout (app/(auth)/layout.tsx)
- T-018: Modify root layout to add AuthProvider

### Phase 3: Protected Routes

Generate tasks for:
- T-019: Create Next.js middleware for auth
- T-020: Create protected layout (app/(protected)/layout.tsx)
- T-021: Create protected chat page (app/(protected)/chat/page.tsx)
- T-022: Test route protection and redirects

### Phase 4: ChatKit Backend Adapter

Generate tasks for:
- T-023: Create backend adapter service (lib/api/backend-adapter.ts)
- T-024: Create chat proxy endpoint (app/api/chat/route.ts)
- T-025: Modify ChatKitPanel.tsx for backend adapter
- T-026: Update lib/config.ts with BACKEND_URL
- T-027: Create CitationDisplay component
- T-028: Test end-to-end chat flow

### Phase 5: Chat History

Generate tasks for:
- T-029: Add chat tables to schema (chatSession, chatMessage)
- T-030: Run chat history migrations
- T-031: Create chat history service (lib/api/chat-history.ts)
- T-032: Create chat history API routes
- T-033: Create ConversationList component
- T-034: Create NewChatButton component
- T-035: Create history page (app/(protected)/history/page.tsx)
- T-036: Integrate history with chat UI

### Phase 6: Backend Authentication Middleware (US10 - P1 Critical)

Generate tasks for:
- T-058: Install PyJWT dependency in backend
- T-059: Add BETTER_AUTH_SECRET to backend config
- T-060: Update backend .env.example with BETTER_AUTH_SECRET
- T-061: Create JWT validation utilities (backend/app/core/security.py)
- T-062: Create authentication middleware (backend/app/middleware/auth.py)
- T-063: Create get_current_user FastAPI dependency (backend/app/dependencies/auth.py)
- T-064: Modify chat endpoint to require authentication
- T-065: Add authentication failure logging

### Phase 7: Testing & Polish

Generate tasks for:
- T-066: Unit tests for auth components (frontend)
- T-067: Unit tests for chat components (frontend)
- T-068: Unit tests for backend JWT validation
- T-069: Integration tests for frontend auth API routes
- T-070: Integration tests for frontend chat API routes
- T-071: Integration tests for chat history API routes
- T-072: Integration tests for backend auth middleware
- T-073: E2E test for registration flow
- T-074: E2E test for login flow
- T-075: E2E test for chat flow
- T-076: Update frontend .env.example
- T-077: Update backend .env.example
- T-078: Validate quickstart.md setup guide
- T-079: Review and improve error messages
- T-080: Add loading states and retry functionality
- T-081: Final code review and TypeScript/Python error fixes

## Task Dependencies

```
Phase 1 (Foundation):
T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010

Phase 2 (Auth UI) - depends on T-009:
T-011 → T-012, T-013, T-014 (parallel)
T-012, T-013 → T-015, T-016 (parallel)
T-015, T-016 → T-017 → T-018

Phase 3 (Protected Routes) - depends on T-010:
T-019 → T-020 → T-021 → T-022

Phase 4 (ChatKit Adapter) - depends on T-021:
T-023 → T-024 → T-025
T-026 (parallel with T-023)
T-027 (parallel with T-025)
T-028 (depends on T-025, T-027)

Phase 5 (Chat History) - depends on T-024:
T-029 → T-030 → T-031 → T-032
T-033, T-034 (parallel, depend on T-032)
T-035 (depends on T-033)
T-036 (depends on T-034, T-035)

Phase 6 (Backend Auth Middleware - US10) - can start after T-002, runs parallel with frontend phases:
T-058 → T-059, T-060 (parallel)
T-059 → T-061 → T-062 → T-063 → T-064
T-062 → T-065

Phase 7 (Testing) - depends on T-036 and T-065:
T-066, T-067, T-068 (parallel - unit tests)
T-069, T-070, T-071, T-072 (parallel - integration tests)
T-073 → T-074 → T-075 (E2E tests - sequential)
T-076, T-077, T-078 (parallel - docs)
T-079, T-080, T-081 (sequential - polish)
```

## Critical Implementation Notes

### ChatKitPanel.tsx Modification (T-025)

The existing `ChatKitPanel.tsx` has:
- `getClientSecret` callback for OpenAI workflow session
- `useChatKit` hook with theme, prompts, composer config
- Error handling with `ErrorState` type
- Widget actions for `switch_theme` and `record_fact`

Modification strategy:
1. Keep all existing UI, theme, and error handling
2. Replace `getClientSecret` with backend adapter call
3. Add session token from auth to requests
4. Parse citations from backend response

### Schema Table Names

Better Auth requires specific table names:
- `user` (not `users`)
- `session` (not `sessions`)
- `account` (not `accounts`)

### Environment Variables

Required in frontend `.env.local`:
```env
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secure-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BACKEND_URL=https://...
```

Required in backend `.env`:
```env
# MUST match frontend BETTER_AUTH_SECRET
BETTER_AUTH_SECRET=your-secure-secret-key-min-32-chars
```

### Backend Auth Middleware Implementation (T-061 to T-065)

Key implementation details for US10:
1. Use PyJWT for token validation
2. Extract token from `Authorization: Bearer <token>` header
3. Validate signature using `BETTER_AUTH_SECRET`
4. Check token expiration with reasonable clock skew tolerance (60 seconds)
5. Return 401 Unauthorized for all auth failures (don't reveal specific reason)
6. Log failures with request metadata but no sensitive data

## Output Format

Generate `specs/002-auth-frontend-integration/tasks.md` with:

1. **Summary table** of all 67 tasks with status columns
2. **Detailed task definitions** following the format above (including Phase 6 for US10)
3. **Dependency graph** in mermaid or ASCII format (showing backend tasks can run in parallel)
4. **Agent workload summary** showing tasks per agent (Auth-Integration: 25, UI-ChatKit: 16, backend-architect: 23)
5. **File creation summary** (27 frontend files, 5 backend files, 8 test files, 6 modified files)
```

---

## EXPECTED OUTPUT

After running `/sp.tasks`, this file should be created:

```
specs/002-auth-frontend-integration/
└── tasks.md                    # Detailed task list with 67 tasks (including 8 for US10 backend auth middleware)
```

---

## USAGE

1. Ensure plan exists at `specs/002-auth-frontend-integration/plan.md`
2. Run `/sp.tasks` in Claude Code
3. Review generated tasks for completeness
4. Adjust dependencies if needed

---

## RELATED ARTIFACTS

- Specification: `specs/002-auth-frontend-integration/spec.md`
- Implementation Plan: `specs/002-auth-frontend-integration/plan.md`
- Data Model: `specs/002-auth-frontend-integration/data-model.md`
- API Contracts: `specs/002-auth-frontend-integration/contracts/api-contracts.md`
- Research: `specs/002-auth-frontend-integration/research.md`
