---
id: "0002"
title: "Book Chatbot Integration Plan"
stage: plan
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-book-chatbot-integration
branch: 004-book-chatbot-integration
user: nadeemsangrasi
command: /sp.plan
labels: ["planning", "frontend", "iframe", "chatkit", "theme"]
links:
  spec: specs/004-book-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-book-chatbot-integration/plan.md
  - specs/004-book-chatbot-integration/research.md
  - specs/004-book-chatbot-integration/data-model.md
  - specs/004-book-chatbot-integration/contracts/api-contracts.md
  - specs/004-book-chatbot-integration/quickstart.md
tests:
  - N/A (planning phase)
---

## Prompt

User executed `/sp.plan` to generate the implementation plan for feature 004-book-chatbot-integration (Book & Chatbot Integration).

The feature integrates the existing Docusaurus textbook on GitHub Pages with the Next.js chatbot frontend using iframe embedding strategy. Key components include:
- Book iframe page (`/book`)
- Modern landing page with hero, features, previews
- Floating chat button (FAB) for instant AI assistance
- Enhanced chatbot UI with conversation history sidebar
- Unified theme with dark/light mode toggle

## Response snapshot

Generated complete implementation planning artifacts:

**plan.md**: Technical context filled with:
- TypeScript 5.x, React 19.x, Next.js 15.x
- Existing Better Auth + Drizzle ORM + Neon DB
- New dependencies: lucide-react, framer-motion, @radix-ui/react-dialog, clsx, tailwind-merge
- Project structure with 15+ new components across 5 domains (layout, landing, chat, instant-chat)
- 5 implementation phases mapped to user stories
- Constitution check: All gates PASS

**research.md**: Resolved 8 technical questions:
1. GitHub Pages allows iframe embedding (fallback: new tab)
2. Next.js App Router file-based routing
3. CSS vars + Tailwind dark mode for theming
4. Framer Motion + Radix for FAB/modals
5. Flexbox + date-fns for sidebar grouping
6. Wrap existing ChatKitPanel (don't rewrite)
7. Framer Motion useInView for scroll animations
8. Middleware updates for new public routes

**data-model.md**: No new database tables needed - frontend-only feature using existing schema

**contracts/api-contracts.md**: No new APIs - reuses existing auth and chat history endpoints

**quickstart.md**: Step-by-step implementation guide with code snippets

**Agent context updated**: CLAUDE.md updated with TypeScript/React/Next.js tech stack

## Outcome

- ✅ Impact: Complete planning artifacts ready for task generation
- 🧪 Tests: N/A (planning phase - no code written)
- 📁 Files: 5 planning documents created + CLAUDE.md updated
- 🔁 Next prompts: `/sp.tasks` to generate actionable task list
- 🧠 Reflection: Frontend-only feature simplifies planning - no backend changes needed, leverages existing auth and chat infrastructure

## Evaluation notes (flywheel)

- Failure modes observed: None - existing codebase well-structured
- Graders run and results (PASS/FAIL): Constitution check PASS (all 5 gates)
- Prompt variant (if applicable): Standard /sp.plan flow
- Next experiment (smallest change to try): N/A - proceeding to task generation
