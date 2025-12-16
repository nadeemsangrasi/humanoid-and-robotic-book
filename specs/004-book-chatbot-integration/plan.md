# Implementation Plan: Book & Chatbot Integration

**Branch**: `004-book-chatbot-integration` | **Date**: 2025-12-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-book-chatbot-integration/spec.md`

## Summary

Integrate the existing Docusaurus textbook (GitHub Pages) with the Next.js chatbot frontend using iframe embedding. This creates a unified educational platform with:
- Book iframe page (`/book`) for seamless textbook viewing
- Modern landing page with hero, features, and previews
- Floating chat button (FAB) for instant AI assistance
- Enhanced chatbot UI with conversation history sidebar
- Unified theme with dark/light mode toggle

## Technical Context

**Language/Version**: TypeScript 5.x, React 19.x, Next.js 15.x
**Primary Dependencies**:
- @openai/chatkit-react (existing ChatKit UI)
- better-auth (existing authentication)
- drizzle-orm + @neondatabase/serverless (existing database)
- lucide-react (icons - to be added)
- framer-motion (animations - to be added)
- @radix-ui/react-dialog (modals - to be added)

**Storage**: PostgreSQL Neon DB via Drizzle ORM (existing schema with user, session, account, verification, chatSession, chatMessage tables)

**Testing**: Vitest + @testing-library/react (existing setup)

**Target Platform**: Web (Vercel deployment for frontend, GitHub Pages for book)

**Project Type**: Web application (frontend-only changes for this feature)

**Performance Goals**:
- Book iframe loads within 3 seconds
- Instant chat modal opens within 500ms
- Theme transitions complete within 300ms
- Landing page LCP under 2 seconds

**Constraints**:
- Book remains on GitHub Pages (iframe embedding, no migration)
- Book manages its own theme (no cross-origin sync)
- Frontend-only changes (backend already exists)
- Must work with existing Better Auth setup

**Scale/Scope**: Single-user education platform, ~10 pages, 15+ new components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| Frontend-Backend Separation | PASS | UI changes only, backend RAG unchanged |
| Better Auth Integration | PASS | Leveraging existing auth from 002-auth-frontend-integration |
| RAG Content Scope | PASS | Chat uses existing textbook RAG content |
| Deployment Constraints | PASS | Frontend on Vercel, book on GitHub Pages |
| No Non-Robotics Content | PASS | Book content remains robotics-focused |

## Project Structure

### Documentation (this feature)

```text
specs/004-book-chatbot-integration/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (minimal for frontend-only)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── page.tsx                    # Landing page (NEW - replace redirect)
│   ├── layout.tsx                  # Root layout (UPDATE - add Navbar)
│   ├── globals.css                 # Global styles (UPDATE - theme vars)
│   ├── book/
│   │   └── page.tsx                # Book iframe page (NEW)
│   ├── chat/
│   │   └── page.tsx                # Chat page with sidebar (NEW)
│   ├── (auth)/
│   │   ├── login/page.tsx          # Existing
│   │   └── register/page.tsx       # Existing
│   └── (protected)/
│       └── history/page.tsx        # Existing
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx              # Main navigation (NEW)
│   │   ├── Footer.tsx              # Footer component (NEW)
│   │   └── ThemeToggle.tsx         # Dark/light toggle (NEW)
│   ├── landing/
│   │   ├── Hero.tsx                # Hero section (NEW)
│   │   ├── Features.tsx            # Features grid (NEW)
│   │   ├── BookPreview.tsx         # Book preview (NEW)
│   │   └── ChatbotDemo.tsx         # Chatbot preview (NEW)
│   ├── chat/
│   │   ├── ChatLayout.tsx          # Sidebar + chat layout (NEW)
│   │   ├── ChatSidebar.tsx         # Conversation history (NEW)
│   │   ├── ChatHeader.tsx          # Chat header (NEW)
│   │   ├── ChatMessages.tsx        # Message list (NEW)
│   │   ├── ChatMessage.tsx         # Message bubble (NEW)
│   │   ├── ChatInput.tsx           # Input area (NEW)
│   │   ├── ChatTypingIndicator.tsx # Typing animation (NEW)
│   │   ├── ConversationList.tsx    # Existing (may update)
│   │   ├── NewChatButton.tsx       # Existing
│   │   └── CitationDisplay.tsx     # Existing
│   ├── instant-chat/
│   │   ├── FloatingChatButton.tsx  # FAB (NEW)
│   │   ├── InstantChatModal.tsx    # Modal wrapper (NEW)
│   │   └── LoginPromptModal.tsx    # Auth prompt (NEW)
│   ├── auth/
│   │   └── [existing files]        # No changes
│   ├── ChatKitPanel.tsx            # Existing (may integrate)
│   └── ErrorOverlay.tsx            # Existing
├── hooks/
│   ├── useColorScheme.ts           # Existing
│   ├── useChatHistory.ts           # Existing
│   └── useTheme.ts                 # Theme hook (NEW)
├── lib/
│   ├── constants/
│   │   ├── index.ts                # Existing
│   │   ├── errors.ts               # Existing
│   │   └── theme.ts                # Theme constants (NEW)
│   ├── auth-client.ts              # Existing
│   └── db/                         # Existing
└── middleware.ts                   # Update protected routes

```

**Structure Decision**: Web application using existing Next.js App Router structure. New components organized by domain (layout, landing, chat, instant-chat). Leveraging existing auth and chat infrastructure.

## Complexity Tracking

> No constitution violations requiring justification.

## Implementation Phases Overview

### Phase 1: Infrastructure & Navigation (US-1, US-2)
- Create `/book` route with iframe
- Create Navbar component with Book/Chat links
- Update middleware for route protection
- Add ThemeToggle component

### Phase 2: Floating Chat (US-3)
- Create FloatingChatButton (FAB)
- Create InstantChatModal
- Create LoginPromptModal
- Integrate with root layout

### Phase 3: Landing Page (US-4)
- Create Hero section
- Create Features section
- Create BookPreview and ChatbotDemo
- Create Footer
- Add scroll animations

### Phase 4: Chatbot UI Enhancement (US-5)
- Create ChatLayout with sidebar
- Create ChatSidebar with history
- Redesign message components
- Add typing indicator
- Integrate with existing ChatKitPanel

### Phase 5: Theme Unification (US-6)
- Define CSS custom properties
- Extend Tailwind config
- Update all components for theme support
- Add smooth transitions

## Dependencies to Install

```bash
npm install lucide-react framer-motion @radix-ui/react-dialog clsx tailwind-merge
```

## Key Technical Decisions

1. **Iframe for Book**: Keeps book on GitHub Pages, no migration complexity
2. **Reuse ChatKitPanel**: Leverage existing OpenAI ChatKit integration
3. **CSS Custom Properties**: Enable theme switching without JavaScript re-renders
4. **Framer Motion**: Production-ready animations with good DX
5. **Radix UI**: Accessible modal primitives

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| GitHub Pages X-Frame-Options | Test iframe embedding; fallback to "Open in new tab" |
| Theme sync with book | Accept independent theme controls |
| ChatKit integration complexity | Wrap existing panel, don't replace |
| Mobile FAB/modal UX | Full-screen modal on mobile |
