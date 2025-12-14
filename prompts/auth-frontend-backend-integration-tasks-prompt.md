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

### Phase 6: Testing & Polish

Generate tasks for:
- T-037: Unit tests for auth components
- T-038: Integration tests for API routes
- T-039: E2E tests for auth flow
- T-040: Update .env.example
- T-041: Final documentation updates

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

Phase 6 (Testing) - depends on T-036:
T-037, T-038, T-039 (parallel)
T-040 (depends on all tests)
T-041 (depends on T-040)
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

Required in `.env.local`:
```env
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BACKEND_URL=https://...
```

## Output Format

Generate `specs/002-auth-frontend-integration/tasks.md` with:

1. **Summary table** of all tasks with status columns
2. **Detailed task definitions** following the format above
3. **Dependency graph** in mermaid or ASCII format
4. **Agent workload summary** showing tasks per agent
```

---

## EXPECTED OUTPUT

After running `/sp.tasks`, this file should be created:

```
specs/002-auth-frontend-integration/
└── tasks.md                    # Detailed task list with 41 tasks
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
