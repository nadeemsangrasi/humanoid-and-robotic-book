# Implementation Tasks: Book & Chatbot Integration

**Feature**: 004-book-chatbot-integration
**Branch**: `004-book-chatbot-integration`
**Created**: 2025-12-16
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## User Story Summary

| Story | Priority | Description | Tasks |
|-------|----------|-------------|-------|
| US1 | P1 | Seamless Book Access | T006-T010 |
| US2 | P1 | Navigation Between Book and Chat | T011-T017 |
| US3 | P2 | Modern Landing Page | T018-T027 |
| US4 | P2 | Instant Chat Floating Button | T028-T034 |
| US5 | P2 | Modern Chatbot UI with Sidebar | T035-T045 |
| US6 | P3 | Unified Modern Theme | T046-T052 |

---

## Phase 1: Setup

**Goal**: Initialize project dependencies and foundational infrastructure.

- [ ] T001 Install new dependencies: `npm install lucide-react framer-motion @radix-ui/react-dialog clsx tailwind-merge` in `frontend/`
- [ ] T002 [P] Create theme constants file at `frontend/lib/constants/theme.ts` with color palette and gradient definitions
- [ ] T003 [P] Create useTheme hook at `frontend/hooks/useTheme.ts` with localStorage persistence and system preference detection
- [ ] T004 [P] Create utility function file at `frontend/lib/utils.ts` with cn() helper using clsx and tailwind-merge
- [ ] T005 Update `frontend/app/globals.css` with CSS custom properties for theme colors (light and dark mode variables)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Create shared components required by multiple user stories.

- [ ] T006 Create ThemeToggle component at `frontend/components/layout/ThemeToggle.tsx` with sun/moon icons and smooth transition
- [ ] T007 Update `frontend/middleware.ts` to make `/` and `/book` public routes, keep `/chat` protected

---

## Phase 3: User Story 1 - Seamless Book Access (P1)

**Story Goal**: Users can click "Book" in navbar and see textbook loaded seamlessly in iframe.

**Independent Test**: Navigate to `/book` route, verify Docusaurus site loads in iframe without borders, responsive on all devices.

### Implementation Tasks

- [ ] T008 [US1] Create book page directory at `frontend/app/book/`
- [ ] T009 [US1] Create book iframe page at `frontend/app/book/page.tsx` with loading spinner, error fallback, and responsive iframe
- [ ] T010 [US1] Add BOOK_URL constant to `frontend/lib/constants/index.ts` for GitHub Pages URL

---

## Phase 4: User Story 2 - Navigation Between Book and Chat (P1)

**Story Goal**: Users can easily switch between Book and Chat sections with proper auth protection.

**Independent Test**: Verify navbar shows Book/Chat links, navigation works, Chat redirects to login for unauthenticated users.

### Implementation Tasks

- [ ] T011 [US2] Create Navbar component at `frontend/components/layout/Navbar.tsx` with logo, Book link, Chat link, auth buttons
- [ ] T012 [US2] Add mobile hamburger menu to Navbar with responsive breakpoints
- [ ] T013 [US2] Add active link highlighting to Navbar using usePathname hook
- [ ] T014 [US2] Integrate ThemeToggle into Navbar component
- [ ] T015 [US2] Update `frontend/app/layout.tsx` to include Navbar component in root layout
- [ ] T016 [US2] Create chat page directory at `frontend/app/chat/`
- [ ] T017 [US2] Create basic chat page at `frontend/app/chat/page.tsx` that renders existing ChatKitPanel (placeholder for US5 enhancement)

---

## Phase 5: User Story 3 - Modern Landing Page (P2)

**Story Goal**: Visitors see a modern, cohesive landing page with hero, features, and previews.

**Independent Test**: Visit root URL, verify hero section, features grid, preview sections, and footer render correctly with CTAs.

### Implementation Tasks

- [ ] T018 [US3] Create landing components directory at `frontend/components/landing/`
- [ ] T019 [P] [US3] Create Hero component at `frontend/components/landing/Hero.tsx` with headline, subheadline, and two CTA buttons
- [ ] T020 [P] [US3] Create Features component at `frontend/components/landing/Features.tsx` with 4 feature cards (Curriculum, AI Assistant, Code Examples, Capstone)
- [ ] T021 [P] [US3] Create BookPreview component at `frontend/components/landing/BookPreview.tsx` with screenshot/mockup
- [ ] T022 [P] [US3] Create ChatbotDemo component at `frontend/components/landing/ChatbotDemo.tsx` with screenshot/animation
- [ ] T023 [US3] Create Footer component at `frontend/components/layout/Footer.tsx` with links and copyright
- [ ] T024 [US3] Add scroll animations to landing components using framer-motion useInView hook
- [ ] T025 [US3] Create landing page index at `frontend/components/landing/index.ts` exporting all components
- [ ] T026 [US3] Update `frontend/app/page.tsx` to render landing page with all sections (Hero, Features, BookPreview, ChatbotDemo, Footer)
- [ ] T027 [US3] Update `frontend/app/layout.tsx` to include Footer conditionally (not on /chat page)

---

## Phase 6: User Story 4 - Instant Chat Floating Button (P2)

**Story Goal**: Users see a floating chat button that opens instant chat modal or login prompt.

**Independent Test**: Verify FAB appears on all pages except /chat, opens modal on click, shows login prompt for unauthenticated users.

### Implementation Tasks

- [ ] T028 [US4] Create instant-chat components directory at `frontend/components/instant-chat/`
- [ ] T029 [US4] Create FloatingChatButton component at `frontend/components/instant-chat/FloatingChatButton.tsx` with gradient styling, pulse animation, and pathname check
- [ ] T030 [US4] Create LoginPromptModal component at `frontend/components/instant-chat/LoginPromptModal.tsx` with Radix Dialog, login/signup buttons
- [ ] T031 [US4] Create InstantChatModal component at `frontend/components/instant-chat/InstantChatModal.tsx` with slide-up animation, close/minimize buttons, ChatKitPanel integration
- [ ] T032 [US4] Create instant-chat index at `frontend/components/instant-chat/index.ts` exporting all components
- [ ] T033 [US4] Add InstantChatProvider wrapper at `frontend/components/instant-chat/InstantChatProvider.tsx` to manage modal state and context preservation
- [ ] T034 [US4] Update `frontend/app/layout.tsx` to include FloatingChatButton component globally

---

## Phase 7: User Story 5 - Modern Chatbot UI with Sidebar (P2)

**Story Goal**: Authenticated users see modern chat interface with conversation history sidebar.

**Independent Test**: Login, start conversations, verify sidebar shows history with new chat, delete, and date grouping.

### Implementation Tasks

- [ ] T035 [US5] Create ChatLayout component at `frontend/components/chat/ChatLayout.tsx` with flexbox sidebar + main area structure
- [ ] T036 [US5] Create ChatSidebar component at `frontend/components/chat/ChatSidebar.tsx` with collapsible panel, date grouping, conversation list
- [ ] T037 [US5] Create ChatHeader component at `frontend/components/chat/ChatHeader.tsx` with title, theme toggle, mobile sidebar toggle
- [ ] T038 [US5] Create ChatMessage component at `frontend/components/chat/ChatMessage.tsx` with user/bot styling, gradient backgrounds, markdown rendering
- [ ] T039 [US5] Create ChatMessages component at `frontend/components/chat/ChatMessages.tsx` as container with scroll-to-bottom functionality
- [ ] T040 [US5] Create ChatInput component at `frontend/components/chat/ChatInput.tsx` with auto-expanding textarea, send button, keyboard shortcuts
- [ ] T041 [US5] Create ChatTypingIndicator component at `frontend/components/chat/ChatTypingIndicator.tsx` with animated dots
- [ ] T042 [US5] Update existing ConversationList at `frontend/components/chat/ConversationList.tsx` to support date grouping (Today, Yesterday, Last 7 days)
- [ ] T043 [US5] Create chat components index at `frontend/components/chat/index.ts` exporting all new components
- [ ] T044 [US5] Update `frontend/app/chat/page.tsx` to use ChatLayout wrapping ChatKitPanel with sidebar integration
- [ ] T045 [US5] Add sidebar collapse state persistence to localStorage in ChatSidebar

---

## Phase 8: User Story 6 - Unified Modern Theme (P3)

**Story Goal**: Consistent theme across all pages with working dark/light mode toggle.

**Independent Test**: Verify color scheme consistency, theme toggle works, preference persists across sessions.

### Implementation Tasks

- [ ] T046 [US6] Update `frontend/app/globals.css` with complete light and dark theme CSS custom properties
- [ ] T047 [US6] Add theme transition CSS with smooth color transitions (300ms)
- [ ] T048 [P] [US6] Update Navbar component styling for theme consistency
- [ ] T049 [P] [US6] Update all landing components (Hero, Features, BookPreview, ChatbotDemo, Footer) for dark mode support
- [ ] T050 [P] [US6] Update chat components for theme consistency (ChatLayout, ChatSidebar, ChatMessage, ChatInput)
- [ ] T051 [P] [US6] Update instant-chat components for theme consistency (FAB, modals)
- [ ] T052 [US6] Update book page iframe container for theme-aware loading state

---

## Phase 9: Polish & Integration

**Goal**: Final integration, edge case handling, and verification.

- [ ] T053 Add iframe error handling with "Open in new tab" fallback link to `frontend/app/book/page.tsx`
- [ ] T054 Add session expiry handling to InstantChatModal with re-login prompt
- [ ] T055 Test and verify responsive behavior on mobile for all new components
- [ ] T056 Run `npm run build` and fix any TypeScript/build errors
- [ ] T057 Run `npm run lint` and fix any linting issues
- [ ] T058 Verify all navigation flows work correctly (landing → book → chat → landing)
- [ ] T059 Test theme toggle persistence across page refreshes
- [ ] T060 Create PR with summary of all changes

---

## Dependencies & Execution Order

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ──────────────────────────────┐
    │                                                 │
    ▼                                                 │
Phase 3 (US1: Book Access) ◄─────────────────────────┤
    │                                                 │
    ▼                                                 │
Phase 4 (US2: Navigation) ◄──────────────────────────┤
    │                                                 │
    ├──────────────┬──────────────┬──────────────────┤
    ▼              ▼              ▼                   │
Phase 5        Phase 6        Phase 7                 │
(US3: Landing) (US4: FAB)    (US5: Chat UI)          │
    │              │              │                   │
    └──────────────┴──────────────┴───────────────────┤
                                                      │
                   ▼                                  │
              Phase 8 (US6: Theme) ◄──────────────────┘
                   │
                   ▼
              Phase 9 (Polish)
```

### Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|------------|-------------------|
| US1 (Book) | Setup, Foundational | - |
| US2 (Nav) | Setup, Foundational, US1 | - |
| US3 (Landing) | Setup, Foundational, US2 | US4, US5 |
| US4 (FAB) | Setup, Foundational, US2 | US3, US5 |
| US5 (Chat UI) | Setup, Foundational, US2 | US3, US4 |
| US6 (Theme) | All above | - |

---

## Parallel Execution Examples

### After Phase 4 (US2 complete), these can run in parallel:

**Parallel Set A** (3 agents):
- Agent 1: T018-T027 (US3: Landing Page)
- Agent 2: T028-T034 (US4: Instant Chat FAB)
- Agent 3: T035-T045 (US5: Chatbot UI)

### Within US3 (Landing Page), parallel tasks:
- T019, T020, T021, T022 can all run in parallel (independent components)

### Within US6 (Theme), parallel tasks:
- T048, T049, T050, T051 can all run in parallel (independent component updates)

---

## MVP Scope

**Minimum Viable Product**: Complete Phase 1-4 (US1 + US2)

This delivers:
- Book accessible via iframe at `/book`
- Navigation between Book and Chat
- Auth-protected chat access
- Basic theme toggle

**Recommended MVP+**: Add Phase 5 (US3) for landing page

This adds:
- Professional landing page for first impressions
- Clear CTAs for book and chat access

---

## Implementation Strategy

1. **MVP First**: Complete US1 + US2 for core navigation functionality
2. **Incremental Delivery**: Each user story is independently deployable
3. **Parallel Where Possible**: After US2, parallelize US3/US4/US5
4. **Theme Last**: US6 touches all components, do after features complete
5. **Polish Integration**: Final phase ensures everything works together

---

## Task Count Summary

| Phase | Tasks | Parallelizable |
|-------|-------|----------------|
| Setup | 5 | 3 |
| Foundational | 2 | 0 |
| US1 (Book) | 3 | 0 |
| US2 (Navigation) | 7 | 0 |
| US3 (Landing) | 10 | 4 |
| US4 (FAB) | 7 | 0 |
| US5 (Chat UI) | 11 | 0 |
| US6 (Theme) | 7 | 4 |
| Polish | 8 | 0 |
| **Total** | **60** | **11** |

---

## Verification Checklist

After all tasks complete, verify:

- [ ] Landing page renders at `/` with all sections
- [ ] Book iframe loads at `/book` without borders
- [ ] Navbar shows on all pages with active link highlighting
- [ ] Chat page requires authentication
- [ ] FAB appears on landing and book pages, hidden on chat
- [ ] FAB shows login prompt for unauthenticated users
- [ ] Chat sidebar shows conversation history with date grouping
- [ ] Theme toggle works and persists across sessions
- [ ] Mobile navigation works with hamburger menu
- [ ] Build succeeds without errors
- [ ] Deployment to Vercel succeeds
