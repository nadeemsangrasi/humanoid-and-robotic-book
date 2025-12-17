# Tasks: Frontend Bug Fixes & Enhancements

**Feature**: 005-frontend-bugfixes-enhancements
**Branch**: `005-frontend-bugfixes-enhancements`
**Created**: 2025-12-17
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

**Input**: Design documents from `/specs/005-frontend-bugfixes-enhancements/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓

**Tests**: Not explicitly requested - test tasks omitted.

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1, US2, US3, US4, US5)
- Exact file paths included

## User Story Summary

| Story | Priority | Description | Tasks |
|-------|----------|-------------|-------|
| US1 | P1 | Frontend Bug Fixes (7 bugs) | T003-T015 |
| US2 | P1 | Theme Synchronization with Book | T016-T019 |
| US3 | P2 | Modern Chat Interface Enhancement | T020-T027 |
| US4 | P2 | Unified Theme System | T028-T033 |
| US5 | P3 | Documentation Updates | T034-T038 |

---

## Phase 1: Setup

**Purpose**: Verify existing infrastructure before making changes

- [ ] T001 Verify all dependencies are installed by running `npm install` in `frontend/`
- [ ] T002 Run `npm run build` to establish baseline and ensure no pre-existing build errors

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core fixes that MUST be complete before user story-specific work

**⚠️ CRITICAL**: These tasks establish the z-index hierarchy and layout structure that all stories depend on

**No tasks in this phase** - All fixes are story-specific in this feature. Proceed to User Story 1.

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Frontend Bug Fixes (Priority: P1) 🎯 MVP

**Goal**: Fix 7 critical bugs affecting user experience: duplicate headers, chat overlap, modal blur, hover states, theme inconsistency, loading states, instant chat history.

**Independent Test**: Each bug can be verified by triggering the specific scenario and confirming the fix.

### Bug Fix 1: Duplicate Headers & Auth Navbar

- [ ] T003 [US1] Modify root layout to conditionally hide navbar on auth routes in `frontend/app/layout.tsx`
- [ ] T004 [US1] Verify auth layout header is standalone (no parent navbar conflict) in `frontend/app/(auth)/layout.tsx`

### Bug Fix 2: Chat Component Overlap

- [ ] T005 [US1] Establish z-index hierarchy (navbar z-40) in `frontend/components/layout/Navbar.tsx`
- [ ] T006 [US1] Verify chat page respects navbar height and doesn't overlap in `frontend/app/(protected)/chat/page.tsx`

### Bug Fix 3: Modal Blur Bug

- [ ] T007 [US1] Fix AnimatePresence blur handling - keep overlay mounted, animate opacity when minimized in `frontend/components/instant-chat/InstantChatModal.tsx`

### Bug Fix 4: Missing Hover States

- [ ] T008 [P] [US1] Add global hover utility classes (hover-bg, hover-text) to `frontend/app/globals.css`
- [ ] T009 [P] [US1] Add hover states to Navbar links and buttons in `frontend/components/layout/Navbar.tsx`
- [ ] T010 [P] [US1] Add hover states to Footer links in `frontend/components/layout/Footer.tsx`
- [ ] T011 [P] [US1] Add hover states to FloatingChatButton in `frontend/components/instant-chat/FloatingChatButton.tsx`
- [ ] T012 [US1] Audit and fix any broken links across all navigation components

### Bug Fix 5: Theme Inconsistency

- [ ] T013 [US1] Verify useTheme hook applies theme class consistently in `frontend/hooks/useTheme.ts`

### Bug Fix 6: History Chat Loading

- [ ] T014 [US1] Enhance loading indicator visibility when loading chat from history in `frontend/app/(protected)/chat/page.tsx`

### Bug Fix 7: Instant Chat History Persistence

- [ ] T015 [US1] Add useChatHistory hook to InstantChatModal for conversation persistence in `frontend/components/instant-chat/InstantChatModal.tsx`

**Checkpoint**: All 7 bugs should be fixed. Verify each acceptance scenario passes.

---

## Phase 4: User Story 2 - Theme Synchronization with Book (Priority: P1)

**Goal**: Synchronize frontend theme with Docusaurus book iframe via URL parameter.

**Independent Test**: Toggle theme in frontend and verify book iframe receives theme parameter and updates accordingly.

### Implementation

- [ ] T016 [US2] Add theme parameter to book iframe URL construction in `frontend/app/book/page.tsx`
- [ ] T017 [US2] Import and use theme from useTheme hook in book page in `frontend/app/book/page.tsx`
- [ ] T018 [US2] Handle iframe reload when theme changes in `frontend/app/book/page.tsx`
- [ ] T019 [US2] Document theme parameter handling requirements for Docusaurus book site in `frontend/GUIDE.md`

**Checkpoint**: Theme toggle on /book page should update iframe URL with ?theme=light or ?theme=dark

---

## Phase 5: User Story 3 - Modern Chat Interface Enhancement (Priority: P2)

**Goal**: Refactor chat page to modern ChatGPT-style layout with sidebar for conversation history.

**Independent Test**: Navigate to /chat, verify sidebar with history appears, vertical scroll works, no duplicate headers.

### Implementation

- [ ] T020 [US3] Remove duplicate header from chat page (keep navbar only) in `frontend/app/(protected)/chat/page.tsx`
- [ ] T021 [US3] Integrate ChatLayout component to wrap chat page content in `frontend/app/(protected)/chat/page.tsx`
- [ ] T022 [US3] Connect ChatSidebar to conversation history data in `frontend/components/chat/ChatSidebar.tsx`
- [ ] T023 [US3] Add date grouping logic (Today, Yesterday, Last 7 days, Older) to ChatSidebar in `frontend/components/chat/ChatSidebar.tsx`
- [ ] T024 [US3] Implement sidebar collapse/expand functionality with localStorage persistence in `frontend/components/chat/ChatSidebar.tsx`
- [ ] T025 [US3] Fix vertical scroll issues in chat message area in `frontend/components/chat/ChatMessages.tsx`
- [ ] T026 [US3] Add prominent "New Chat" button to sidebar in `frontend/components/chat/ChatSidebar.tsx`
- [ ] T027 [US3] Handle conversation selection in sidebar to load in main area in `frontend/app/(protected)/chat/page.tsx`

**Checkpoint**: Chat page should have modern sidebar layout with working history, scroll, and new chat functionality

---

## Phase 6: User Story 4 - Unified Theme System (Priority: P2)

**Goal**: Ensure consistent theming across all frontend components using shared CSS variables.

**Independent Test**: Toggle theme and verify all pages (landing, book, chat) display consistent colors.

### Implementation

- [ ] T028 [P] [US4] Audit and ensure all components use CSS custom properties (not hardcoded colors) in `frontend/components/landing/*.tsx`
- [ ] T029 [P] [US4] Verify chat components use theme variables in `frontend/components/chat/*.tsx`
- [ ] T030 [P] [US4] Verify instant-chat components use theme variables in `frontend/components/instant-chat/*.tsx`
- [ ] T031 [US4] Ensure theme toggle updates all components simultaneously via CSS variables in `frontend/app/globals.css`
- [ ] T032 [US4] Add theme transition CSS (300ms) for smooth color changes in `frontend/app/globals.css`
- [ ] T033 [US4] Test theme persistence across page navigation and browser refresh

**Checkpoint**: Theme should be consistent across all pages with smooth transitions

---

## Phase 7: User Story 5 - Documentation Updates (Priority: P3)

**Goal**: Update documentation to accurately reflect current implementation.

**Independent Test**: Review documentation and verify it matches actual codebase behavior.

### Implementation

- [ ] T034 [US5] Update RAG chatbot specs to document email header auth (not JWT) in `specs/003-rag-chatbot-backend/spec.md`
- [ ] T035 [US5] Update parent README with comprehensive architecture overview in `README.md`
- [ ] T036 [US5] Add frontend setup documentation to README in `README.md`
- [ ] T037 [US5] Add backend setup and deployment documentation to README in `README.md`
- [ ] T038 [US5] Update frontend GUIDE.md with theme parameter handling for book iframe in `frontend/GUIDE.md`

**Checkpoint**: All documentation should accurately describe current implementation

---

## Phase 8: Polish & Verification

**Purpose**: Final verification and cross-cutting improvements

- [ ] T039 Run `npm run build` to verify no TypeScript/build errors in `frontend/`
- [ ] T040 Run `npm run lint` to verify no linting issues in `frontend/`
- [ ] T041 Manual verification: Test all 7 bug fixes from US1 acceptance scenarios
- [ ] T042 Manual verification: Test theme sync with book iframe (US2)
- [ ] T043 Manual verification: Test chat interface sidebar and scroll (US3)
- [ ] T044 Manual verification: Test theme consistency across pages (US4)
- [ ] T045 Documentation review: Verify all docs match implementation (US5)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    │
    ▼
Phase 2: Foundational (empty - proceed directly)
    │
    ├──────────────────────────────────┐
    ▼                                  ▼
Phase 3: US1 (P1)                Phase 4: US2 (P1)
Bug Fixes                        Theme Sync
    │                                  │
    └──────────────┬───────────────────┘
                   │
    ├──────────────┼──────────────┐
    ▼              ▼              ▼
Phase 5: US3   Phase 6: US4   Phase 7: US5
Chat UI        Theme System   Documentation
    │              │              │
    └──────────────┴──────────────┘
                   │
                   ▼
            Phase 8: Polish
```

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|------------|-------------------|
| US1 (Bug Fixes) | Setup | US2 |
| US2 (Theme Sync) | Setup | US1 |
| US3 (Chat UI) | US1 (header fix) | US4, US5 |
| US4 (Theme System) | US1 (theme fix) | US3, US5 |
| US5 (Documentation) | None | US3, US4 |

### Parallel Opportunities

**Within US1 (Hover States)**:
- T008, T009, T010, T011 can all run in parallel (different files)

**Within US4 (Theme Audit)**:
- T028, T029, T030 can all run in parallel (different component directories)

**Cross-Story Parallelism**:
- After US1+US2 complete: US3, US4, US5 can all run in parallel

---

## Parallel Example: User Story 1 Hover States

```bash
# Launch all hover state tasks in parallel:
Task: "Add hover states to Navbar links" → frontend/components/layout/Navbar.tsx
Task: "Add hover states to Footer links" → frontend/components/layout/Footer.tsx
Task: "Add hover states to FloatingChatButton" → frontend/components/instant-chat/FloatingChatButton.tsx
Task: "Add global hover utility classes" → frontend/app/globals.css
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 3: US1 Bug Fixes (T003-T015)
3. **STOP and VALIDATE**: Test all 7 bugs are fixed
4. Deploy if ready - core functionality restored

### MVP+ (US1 + US2)

1. Complete US1 (bug fixes)
2. Complete US2 (theme sync)
3. **VALIDATE**: Theme works across frontend and book
4. Deploy - full theme consistency

### Full Feature

1. Complete US1 + US2 (P1 priority)
2. Add US3 (modern chat UI)
3. Add US4 (unified theme)
4. Add US5 (documentation)
5. Complete Phase 8 (polish)

### Parallel Team Strategy

With 2+ developers:

1. Developer A: US1 (Bug Fixes)
2. Developer B: US2 (Theme Sync)
3. After both complete:
   - Developer A: US3 (Chat UI)
   - Developer B: US4 (Theme System)
4. Either developer: US5 (Documentation)

---

## Task Count Summary

| Phase | Tasks | Parallelizable |
|-------|-------|----------------|
| Setup | 2 | 0 |
| US1 (Bug Fixes) | 13 | 4 |
| US2 (Theme Sync) | 4 | 0 |
| US3 (Chat UI) | 8 | 0 |
| US4 (Theme System) | 6 | 3 |
| US5 (Documentation) | 5 | 0 |
| Polish | 7 | 0 |
| **Total** | **45** | **7** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story is independently testable
- Commit after each task or logical group
- US1 is the MVP - delivers immediate value by fixing bugs
- US3 (Chat UI) depends on US1 header fix being complete
- US4 (Theme) depends on US1 theme consistency fix
- US5 (Docs) can be done anytime but best after implementation complete
