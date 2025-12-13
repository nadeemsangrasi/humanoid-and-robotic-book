---
id: 0007
title: MVP Simplification - Remove Deferrable Tasks
stage: tasks
date: 2025-12-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-rag-chatbot-backend
branch: 001-rag-chatbot-backend
user: developer
command: manual
labels: ["simplification", "mvp", "scope-reduction", "tasks"]
links:
  spec: specs/001-rag-chatbot-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot-backend/tasks.md
tests:
  - Task count validation (53 → 28 tasks)
  - MVP completeness check (all essential tasks retained)
---

## Prompt

Remove deferrable tasks from entire project and create PHR for it. User identified these as unnecessary for core MVP:
- T031-T034: Secrets masking, error sanitization
- T035-T037: Module filtering
- T041-T045: Local dev scripts (build.sh, run.sh)
- T051-T052: Logging middleware
- T026a: Special chars validation

## Response snapshot

Simplified tasks.md from 53 tasks to 28 tasks by removing deferrable items:

**Removed (25 tasks)**:
| Removed | Original Tasks | Reason |
|---------|---------------|--------|
| US4 - Secrets masking | T031-T034 (4) | Low risk - can patch if needed |
| US5 - Module filtering | T035-T037 (3) | Zero impact - general Q&A works |
| US6 - Unknown topics | T038-T040 (3) | Gemini handles natively |
| US7 - Local dev scripts | T041-T045 (5) | Use manual docker commands |
| US8 - Re-indexing | T046-T048a (4) | Textbook is static |
| Special chars validation | T026a (1) | BeautifulSoup handles |
| Logging middleware | T051-T053 (5) | Use container logs |

**Retained MVP (28 tasks)**:
- Phase 1: Setup (4 tasks)
- Phase 2: Foundation (5 tasks)
- Phase 3: Chat US1 (9 tasks)
- Phase 4: Ingest US2 (8 tasks)
- Phase 5: Health (2 tasks)
- Phase 6: Deploy US3 (4 tasks)

**Renumbered task IDs**:
- Health endpoint: T049-T050 → T027-T028
- Deploy tasks: T027-T030 → T029-T032

**Execution simplified to 6 phases** with clear parallel opportunity between Chat and Ingest.

## Outcome

- ✅ Impact: 47% task reduction (53 → 28) while preserving all core value
- 🧪 Tests: MVP completeness verified - all essential tasks retained
- 📁 Files: 1 file modified (tasks.md)
- 🔁 Next prompts: /sp.implement to begin Phase 1 setup
- 🧠 Reflection: Aggressive scope cut focuses on core value: user asks → gets answer with citations. Deferred items are documented for Phase 2 post-MVP. No constitution violations - all MUST requirements preserved.

## Evaluation notes (flywheel)

- Failure modes observed: None - clean scope reduction
- Graders run and results (PASS/FAIL): MVP completeness PASS, constitution PASS
- Prompt variant (if applicable): User-directed simplification based on analysis
- Next experiment (smallest change to try): Begin implementation with lean MVP
