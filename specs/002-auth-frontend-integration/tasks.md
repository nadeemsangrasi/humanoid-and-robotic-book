# Tasks: Authentication & Frontend-Backend Integration

**Input**: Design documents from `/specs/002-auth-frontend-integration/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/api-contracts.md
**Branch**: `002-auth-frontend-integration`
**Generated**: 2025-12-14

---

## Task Summary

| Phase | Description | Task Count | Agent |
|-------|-------------|------------|-------|
| 1 | Setup | 3 | - |
| 2 | Foundational (Database & Auth) | 10 | Auth-Integration-Agent |
| 3 | US1-US2: Registration & Login (P1) | 8 | Auth-Integration-Agent |
| 4 | US3-US4: Chat & Session (P1) | 6 | UI-and-ChatKit-customization-agent |
| 5 | US5: Chat History (P2) | 8 | UI-and-ChatKit-customization-agent |
| 6 | US6-US7: Logout & Route Protection (P2) | 4 | Auth-Integration-Agent |
| 7 | US8: OAuth (P3 - Optional) | 3 | Auth-Integration-Agent |
| 8 | US9: Delete History (P3) | 2 | UI-and-ChatKit-customization-agent |
| 9 | US10: Backend Auth Middleware (P1) | 8 | backend-architect-and-sdk-agent |
| 10 | Testing & Quality Assurance | 10 | backend-architect-and-sdk-agent |
| 11 | Polish & Documentation | 5 | backend-architect-and-sdk-agent |
| **Total** | | **67** | |

---

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US9)
- File paths are relative to `frontend/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Project initialization and dependency installation

- [X] T001 Create Neon PostgreSQL database and obtain connection credentials
- [X] T002 Install auth dependencies: `npm install better-auth @better-fetch/fetch` in frontend/
- [X] T003 [P] Install database dependencies: `npm install drizzle-orm @neondatabase/serverless && npm install -D drizzle-kit` in frontend/

---

## Phase 2: Foundational (Database & Auth Infrastructure)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**Agent**: Auth-Integration-Agent
**Skill**: drizzle-schema-generation, better-auth-configuration

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create Drizzle database connection in frontend/lib/db/index.ts (Note: Neon HTTP driver handles connection pooling automatically per FR-015)
- [X] T005 [P] Create environment variables template in frontend/.env.example
- [X] T006 Create Drizzle schema for auth tables (user, session, account) in frontend/lib/db/schema.ts
- [X] T007 Create drizzle.config.ts in frontend/drizzle.config.ts
- [ ] T008 Run initial database migrations: `npx drizzle-kit generate && npx drizzle-kit migrate`
- [X] T009 Create Better Auth server configuration with rate limiting (5 attempts/15 min) and CSRF protection in frontend/lib/auth.ts
- [X] T010 Create Better Auth API route handler in frontend/app/api/auth/[...all]/route.ts
- [X] T011 Create Better Auth client configuration in frontend/lib/auth-client.ts
- [X] T012 Create AuthProvider component in frontend/components/auth/AuthProvider.tsx
- [X] T013 Modify root layout to wrap with AuthProvider in frontend/app/layout.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Stories 1-2 - Registration & Login (Priority: P1) MVP

**Goal**: Enable users to create accounts and log in with email/password

**Independent Test**: User can complete registration, then log in with credentials

**Agent**: Auth-Integration-Agent
**Skill**: frontend-auth-integration

### Implementation for US1-US2

- [X] T014 [P] [US1] Create RegisterForm component in frontend/components/auth/RegisterForm.tsx
- [X] T015 [P] [US2] Create LoginForm component in frontend/components/auth/LoginForm.tsx
- [X] T016 [US1] Create register page in frontend/app/(auth)/register/page.tsx
- [X] T017 [US2] Create login page in frontend/app/(auth)/login/page.tsx
- [X] T018 Create auth route group layout in frontend/app/(auth)/layout.tsx
- [ ] T019 [US1] Test registration flow: submit form, verify user in database
- [ ] T020 [US2] Test login flow: submit credentials, verify session cookie set
- [ ] T021 [US2] Test login error handling: invalid credentials show error message

**Checkpoint**: Users can register and log in - core authentication functional

---

## Phase 4: User Stories 3-4 - Chat & Session Persistence (Priority: P1) MVP

**Goal**: Enable authenticated users to chat with the RAG backend and persist sessions

**Independent Test**: Logged-in user can send message and receive response; session persists on refresh

**Agent**: UI-and-ChatKit-customization-agent
**Skill**: chatkit-backend-adapter

### Implementation for US3-US4

- [X] T022 [P] [US3] Create backend adapter service in frontend/lib/api/backend-adapter.ts
- [X] T023 [P] [US3] Update config with BACKEND_URL in frontend/lib/config.ts
- [X] T024 [US3] Create chat proxy API route in frontend/app/api/chat/route.ts
- [X] T025 [US3] Modify ChatKitPanel.tsx to use backend adapter in frontend/components/ChatKitPanel.tsx
- [X] T026 [P] [US3] Create CitationDisplay component in frontend/components/chat/CitationDisplay.tsx
- [ ] T027 [US4] Test session persistence: login, refresh page, verify still authenticated

**Checkpoint**: Users can chat with RAG backend and sessions persist - core functionality complete

---

## Phase 5: User Story 5 - Chat History (Priority: P2)

**Goal**: Enable users to view and continue previous conversations

**Independent Test**: User can see list of past conversations and load/continue any one

**Agent**: UI-and-ChatKit-customization-agent + Auth-Integration-Agent
**Skill**: ui-customization, drizzle-schema-generation

### Implementation for US5

- [X] T028 [US5] Add chatSession and chatMessage tables to schema in frontend/lib/db/schema.ts
- [ ] T029 [US5] Run chat history migrations: `npx drizzle-kit generate && npx drizzle-kit migrate`
- [X] T030 [US5] Create chat history service in frontend/lib/api/chat-history.ts
- [X] T031 [US5] Create chat history API routes in frontend/app/api/chat/history/route.ts
- [X] T032 [P] [US5] Create ConversationList component in frontend/components/chat/ConversationList.tsx
- [X] T033 [P] [US5] Create NewChatButton component in frontend/components/chat/NewChatButton.tsx
- [X] T034 [US5] Create history page in frontend/app/(protected)/history/page.tsx
- [X] T035 [US5] Integrate history with chat UI: load previous messages when conversation selected

**Checkpoint**: Users can view and continue previous conversations

---

## Phase 6: User Stories 6-7 - Logout & Route Protection (Priority: P2)

**Goal**: Enable secure logout and protect routes from unauthenticated access

**Independent Test**: Logged-out users cannot access chat; callback URL preserved

**Agent**: Auth-Integration-Agent
**Skill**: frontend-auth-integration

### Implementation for US6-US7

- [X] T036 [US6] Create LogoutButton component in frontend/components/auth/LogoutButton.tsx
- [X] T037 [US7] Create Next.js middleware for auth protection in frontend/middleware.ts
- [X] T038 [US7] Create protected route group layout in frontend/app/(protected)/layout.tsx
- [X] T039 [US7] Create protected chat page in frontend/app/(protected)/chat/page.tsx

**Checkpoint**: Logout works and routes are protected

---

## Phase 7: User Story 8 - OAuth Social Login (Priority: P3 - Optional)

**Goal**: Enable login via Google and GitHub OAuth providers

**Independent Test**: User can click OAuth button, complete provider flow, and be logged in

**Agent**: Auth-Integration-Agent
**Skill**: better-auth-configuration

### Implementation for US8

- [X] T040 [P] [US8] Add Google OAuth configuration to Better Auth in frontend/lib/auth.ts
- [X] T041 [P] [US8] Add GitHub OAuth configuration to Better Auth in frontend/lib/auth.ts
- [X] T042 [US8] Add OAuth buttons to LoginForm and RegisterForm

**Checkpoint**: OAuth login available (optional enhancement)

---

## Phase 8: User Story 9 - Delete Chat History (Priority: P3)

**Goal**: Enable users to delete their chat history for privacy

**Independent Test**: User can delete all conversations; list shows empty after deletion

**Agent**: UI-and-ChatKit-customization-agent
**Skill**: ui-customization

### Implementation for US9

- [X] T043 [US9] Add delete conversation endpoint in frontend/app/api/chat/history/[sessionId]/route.ts
- [X] T044 [US9] Add delete all conversations button to history page

**Checkpoint**: Users can delete their chat history

---

## Phase 9: User Story 10 - Backend Authentication Middleware (Priority: P1)

**Goal**: Secure the FastAPI backend by validating JWT tokens from authenticated frontend users

**Independent Test**: Backend returns 200 for valid tokens, 401 for invalid/missing tokens

**Agent**: backend-architect-and-sdk-agent
**Skill**: fastapi-scaffolding

### Implementation for US10

- [X] T058 [US10] Install PyJWT dependency: `pip install PyJWT` in backend/
- [X] T059 [P] [US10] Add BETTER_AUTH_SECRET to backend config in backend/app/core/config.py
- [X] T060 [P] [US10] Update backend .env.example with BETTER_AUTH_SECRET
- [X] T061 [US10] Create JWT validation utilities in backend/app/core/security.py
- [X] T062 [US10] Create authentication middleware in backend/app/middleware/auth.py
- [X] T063 [US10] Create get_current_user FastAPI dependency in backend/app/dependencies/auth.py
- [X] T064 [US10] Modify chat endpoint to require authentication in backend/app/api/v1/chat.py
- [X] T065 [US10] Add authentication failure logging in backend/app/middleware/auth.py

**Checkpoint**: Backend validates JWT tokens - API secured with authentication

---

## Phase 10: Testing & Quality Assurance

**Purpose**: Test coverage for all functional requirements (SC-022)

**Agent**: backend-architect-and-sdk-agent

### Unit Tests

- [ ] T066 [P] Unit tests for auth components (RegisterForm, LoginForm, LogoutButton) in frontend/__tests__/components/auth/
- [ ] T067 [P] Unit tests for chat components (CitationDisplay, ConversationList) in frontend/__tests__/components/chat/
- [ ] T068 [P] [US10] Unit tests for backend JWT validation in backend/tests/test_security.py

### Integration Tests

- [ ] T069 [P] Integration tests for auth API routes (/api/auth/*) in frontend/__tests__/api/auth.test.ts
- [ ] T070 [P] Integration tests for chat API routes (/api/chat/*) in frontend/__tests__/api/chat.test.ts
- [ ] T071 [P] Integration tests for chat history API routes in frontend/__tests__/api/chat-history.test.ts
- [ ] T072 [P] [US10] Integration tests for backend auth middleware in backend/tests/test_auth_middleware.py

### E2E Tests

- [ ] T073 E2E test for registration flow: form submission → user created → auto-login in frontend/__tests__/e2e/auth.spec.ts
- [ ] T074 E2E test for login flow: credentials → session → redirect to chat in frontend/__tests__/e2e/auth.spec.ts
- [ ] T075 E2E test for chat flow: send message → receive response → citations displayed in frontend/__tests__/e2e/chat.spec.ts

**Checkpoint**: All functional requirements have test coverage per SC-022

---

## Phase 11: Polish & Documentation

**Purpose**: Final refinements and documentation updates

**Agent**: backend-architect-and-sdk-agent

- [ ] T076 [P] Update frontend .env.example with all required environment variables
- [ ] T077 [P] Update backend .env.example with BETTER_AUTH_SECRET
- [ ] T078 [P] Validate quickstart.md setup guide works on clean install
- [ ] T079 Review and improve error messages across all components (frontend & backend)
- [ ] T080 Add loading states and retry functionality (FR-023) to all async operations
- [ ] T081 Final code review and TypeScript/Python error fixes (SC-021)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ──── BLOCKS ALL USER STORIES
    │
    ├───────────────────┬───────────────────┬───────────────────┐
    ▼                   ▼                   ▼                   ▼
Phase 3 (US1-US2)   Phase 4 (US3-US4)   Phase 6 (US6-US7)   Phase 9 (US10)
    │                   │                   │               [Backend Auth]
    ▼                   ▼                   │                   │
  [MVP Ready]        Depends on US2        │                   │
    │                   │                   │                   │
    └───────────────────┼───────────────────┘                   │
                        ▼                                       │
                   Phase 5 (US5) ◄──────────────────────────────┘
                        │        (US10 required for secure chat)
                        ▼
              ┌─────────┴─────────┐
              ▼                   ▼
         Phase 7 (US8)       Phase 8 (US9)
         [Optional P3]       [Optional P3]
              │                   │
              └─────────┬─────────┘
                        ▼
                   Phase 10 (Testing)
                        │
                        ▼
                   Phase 11 (Polish)
```

**IMPORTANT**: Phase 9 (US10 - Backend Auth Middleware) is P1 priority and should be completed
alongside or immediately after Phase 4 (Chat Integration) to ensure the backend is secured
before production deployment.

### Task Dependency Details

| Task | Depends On | Reason |
|------|------------|--------|
| T004 | T001, T002, T003 | Need database and dependencies |
| T006 | T004 | Schema imports db connection |
| T007 | T006 | Config references schema path |
| T008 | T007 | Migrations need config |
| T009 | T006, T008 | Auth uses schema and needs tables |
| T010 | T009 | Route handler imports auth |
| T011 | T009 | Client needs auth types |
| T012 | T011 | Provider uses auth client |
| T013 | T012 | Layout wraps with provider |
| T014-T021 | T013 | Auth UI needs foundation |
| T022-T027 | T013, T020 | Chat needs auth complete |
| T028-T035 | T024 | History needs chat proxy |
| T036-T039 | T013 | Logout/routes need auth |
| T040-T042 | T009 | OAuth extends auth config |
| T043-T044 | T031 | Delete needs history API |
| T058 | - | Can start immediately (backend) |
| T059-T060 | T058 | Config needs PyJWT installed |
| T061 | T059 | Security utils need config |
| T062 | T061 | Middleware uses security utils |
| T063 | T062 | Dependency uses middleware |
| T064 | T063 | Chat endpoint uses auth dependency |
| T065 | T062 | Logging integrated with middleware |
| T066-T075 | All features | Tests require implemented features |
| T076-T081 | T066-T075 | Polish after tests pass |

### Parallel Execution Opportunities

**Within Phase 1:**
```bash
# Run in parallel after T001:
Task: T002 (npm install better-auth)
Task: T003 (npm install drizzle-orm)
```

**Within Phase 2:**
```bash
# Run in parallel:
Task: T004 (db connection)
Task: T005 (env template)
```

**Within Phase 3:**
```bash
# Run in parallel:
Task: T014 (RegisterForm)
Task: T015 (LoginForm)
```

**Within Phase 4:**
```bash
# Run in parallel:
Task: T022 (backend adapter)
Task: T023 (config update)
Task: T026 (CitationDisplay)
```

**Within Phase 5:**
```bash
# Run in parallel after T031:
Task: T032 (ConversationList)
Task: T033 (NewChatButton)
```

**Within Phase 7:**
```bash
# Run in parallel:
Task: T040 (Google OAuth)
Task: T041 (GitHub OAuth)
```

**Within Phase 9 (US10):**
```bash
# Run in parallel after T058:
Task: T059 (backend config)
Task: T060 (backend .env.example)
```

**Within Phase 10:**
```bash
# Run in parallel:
Task: T066 (frontend auth unit tests)
Task: T067 (frontend chat unit tests)
Task: T068 (backend JWT unit tests)
Task: T069-T072 (integration tests)
```

---

## Implementation Strategy

### MVP First (Phases 1-4 + 9)

1. **Phase 1**: Setup (T001-T003)
2. **Phase 2**: Foundational infrastructure (T004-T013)
3. **Phase 3**: Registration & Login (T014-T021) **← MVP Milestone 1**
4. **Phase 4**: Chat with backend (T022-T027) **← MVP Milestone 2**
5. **Phase 9**: Backend Auth Middleware (T058-T065) **← MVP Milestone 3 (Security)**

**STOP and VALIDATE**: Test full flow: register → login → chat (with backend auth) → refresh → still logged in

### Incremental Delivery

| Milestone | Phases | User Value |
|-----------|--------|------------|
| MVP Auth | 1-3 | Users can register and log in |
| MVP Chat | 4 | Users can chat with RAG backend |
| MVP Security | 9 | Backend secured with JWT validation |
| History | 5 | Users can view/continue conversations |
| Security | 6 | Logout and route protection |
| Convenience | 7-8 | OAuth and delete history |
| Quality | 10-11 | Tests and documentation |

---

## Agent Workload Summary

| Agent | Tasks | Phases |
|-------|-------|--------|
| Auth-Integration-Agent | 25 | 2, 3, 6, 7 |
| UI-and-ChatKit-customization-agent | 16 | 4, 5, 8 |
| backend-architect-and-sdk-agent | 23 | 9 (US10), 10, 11 |
| (Manual/Setup) | 3 | 1 |

---

## File Creation Summary

### New Files - Frontend (27)

| File | Task | Phase |
|------|------|-------|
| `frontend/.env.example` | T005 | 2 |
| `frontend/lib/db/index.ts` | T004 | 2 |
| `frontend/lib/db/schema.ts` | T006 | 2 |
| `frontend/drizzle.config.ts` | T007 | 2 |
| `frontend/lib/auth.ts` | T009 | 2 |
| `frontend/app/api/auth/[...all]/route.ts` | T010 | 2 |
| `frontend/lib/auth-client.ts` | T011 | 2 |
| `frontend/components/auth/AuthProvider.tsx` | T012 | 2 |
| `frontend/components/auth/RegisterForm.tsx` | T014 | 3 |
| `frontend/components/auth/LoginForm.tsx` | T015 | 3 |
| `frontend/app/(auth)/register/page.tsx` | T016 | 3 |
| `frontend/app/(auth)/login/page.tsx` | T017 | 3 |
| `frontend/app/(auth)/layout.tsx` | T018 | 3 |
| `frontend/lib/api/backend-adapter.ts` | T022 | 4 |
| `frontend/app/api/chat/route.ts` | T024 | 4 |
| `frontend/components/chat/CitationDisplay.tsx` | T026 | 4 |
| `frontend/lib/api/chat-history.ts` | T030 | 5 |
| `frontend/app/api/chat/history/route.ts` | T031 | 5 |
| `frontend/components/chat/ConversationList.tsx` | T032 | 5 |
| `frontend/components/chat/NewChatButton.tsx` | T033 | 5 |
| `frontend/app/(protected)/history/page.tsx` | T034 | 5 |
| `frontend/components/auth/LogoutButton.tsx` | T036 | 6 |
| `frontend/middleware.ts` | T037 | 6 |
| `frontend/app/(protected)/layout.tsx` | T038 | 6 |
| `frontend/app/(protected)/chat/page.tsx` | T039 | 6 |
| `frontend/app/api/chat/history/[sessionId]/route.ts` | T043 | 8 |

### New Files - Backend (4)

| File | Task | Phase |
|------|------|-------|
| `backend/app/core/security.py` | T061 | 9 |
| `backend/app/middleware/auth.py` | T062 | 9 |
| `backend/app/dependencies/auth.py` | T063 | 9 |
| `backend/tests/test_security.py` | T068 | 10 |
| `backend/tests/test_auth_middleware.py` | T072 | 10 |

### New Files - Tests (8)

| File | Task | Phase |
|------|------|-------|
| `frontend/__tests__/components/auth/` | T066 | 10 |
| `frontend/__tests__/components/chat/` | T067 | 10 |
| `frontend/__tests__/api/auth.test.ts` | T069 | 10 |
| `frontend/__tests__/api/chat.test.ts` | T070 | 10 |
| `frontend/__tests__/api/chat-history.test.ts` | T071 | 10 |
| `frontend/__tests__/e2e/auth.spec.ts` | T073-T074 | 10 |
| `frontend/__tests__/e2e/chat.spec.ts` | T075 | 10 |

### Modified Files - Frontend (3)

| File | Task | Phase |
|------|------|-------|
| `frontend/app/layout.tsx` | T013 | 2 |
| `frontend/lib/config.ts` | T023 | 4 |
| `frontend/components/ChatKitPanel.tsx` | T025 | 4 |

### Modified Files - Backend (3)

| File | Task | Phase |
|------|------|-------|
| `backend/app/core/config.py` | T059 | 9 |
| `backend/app/api/v1/chat.py` | T064 | 9 |
| `backend/requirements.txt` | T058 | 9 |
| `backend/.env.example` | T060, T077 | 9, 11 |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story phase is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- P3 features (OAuth, delete history) are optional and can be skipped for MVP
- **US10 (Backend Auth Middleware) is P1 and CRITICAL for production security**
- Phase 9 can run in parallel with frontend phases after Phase 2 is complete
- Backend and frontend share `BETTER_AUTH_SECRET` - must be identical in both environments
