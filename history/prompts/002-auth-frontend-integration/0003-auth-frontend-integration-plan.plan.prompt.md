---
id: 0003
title: Authentication & Frontend-Backend Integration Implementation Plan
stage: plan
date: 2025-12-14
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-auth-frontend-integration
branch: 002-auth-frontend-integration
user: nadeemsangrasi
command: /sp.plan
labels: ["authentication", "better-auth", "drizzle", "chatkit", "implementation-plan", "context7", "backend-middleware", "jwt", "fastapi", "pyjwt"]
links:
  spec: specs/002-auth-frontend-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-auth-frontend-integration/plan.md
  - specs/002-auth-frontend-integration/research.md
  - specs/002-auth-frontend-integration/data-model.md
  - specs/002-auth-frontend-integration/quickstart.md
  - specs/002-auth-frontend-integration/contracts/api-contracts.md
tests:
  - Constitution Check (8/8 gates passed)
  - Context7 MCP documentation verified for all technologies
---

## Prompt

Create a SpecKit Plus implementation plan for the Authentication & Frontend-Backend Integration feature based on the specification at `specs/002-auth-frontend-integration/spec.md`.

Key requirements:
- User Authentication with Better Auth + Neon PostgreSQL + Drizzle ORM
- ChatKit Backend Adapter to connect to FastAPI RAG backend
- Chat History Persistence with user conversations
- Protected Routes with Next.js middleware
- Backend Authentication Middleware (US10) - FastAPI middleware to verify JWT tokens using PyJWT

Clarified decisions from /sp.clarify:
1. Session Storage: JWT tokens (stateless)
2. Auth Header Format: `Authorization: Bearer <jwt>`
3. Backend URL Config: `NEXT_PUBLIC_BACKEND_URL`
4. Token Storage: httpOnly cookie
5. Password Hashing: bcrypt
6. Backend JWT Secret: Shared `BETTER_AUTH_SECRET` between frontend and backend

Technical Context:
- Framework: Next.js 15 (App Router)
- Language: TypeScript (frontend), Python (backend)
- Database: PostgreSQL on Neon (free tier)
- Authentication: Better Auth with Drizzle adapter
- Chat UI: OpenAI ChatKit React (existing)
- Backend: FastAPI with PyJWT for JWT validation

## Response snapshot

Generated comprehensive implementation plan with the following artifacts:

**1. research.md** - Context7 MCP findings including:
- Better Auth + Drizzle integration patterns
- Drizzle ORM + Neon connection setup
- Next.js middleware for route protection
- Better Auth client hooks (useSession, signIn, signUp)
- Session/token strategy (JWT in httpOnly cookies)

**2. data-model.md** - Drizzle schema definitions:
- User table (Better Auth core)
- Session table (Better Auth core)
- Account table (OAuth, Better Auth core)
- ChatSession table (application-specific)
- ChatMessage table (application-specific with citations)

**3. contracts/api-contracts.md** - API specifications:
- Better Auth endpoints (sign-up, sign-in, sign-out, get-session)
- Chat proxy endpoint (POST /api/chat)
- Chat history endpoints (list, get, create, delete)
- Request/response transformation formats

**4. quickstart.md** - Developer setup guide:
- Environment setup with Neon PostgreSQL
- Dependency installation
- Schema and migrations
- Better Auth configuration
- Verification steps

**5. plan.md** - Main implementation plan:
- 7 implementation phases (including Phase 5.5 for Backend Auth Middleware)
- Constitution check (8/8 gates passed)
- Project structure (new and modified files for both frontend and backend)
- Agent assignments per phase (including backend-architect-and-sdk-agent for US10)
- Risks and mitigations (including JWT secret mismatch and clock skew)
- Backend project structure with new files (security.py, auth.py middleware, auth.py dependency)

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation (including backend auth middleware for US10)
- 🧪 Tests: Constitution check passed all 8 gates; Context7 documentation verified for Better Auth, Drizzle ORM, Neon, Next.js, FastAPI, PyJWT
- 📁 Files: 5 plan artifacts created (plan.md, research.md, data-model.md, quickstart.md, contracts/api-contracts.md)
- 🔁 Next prompts: /sp.tasks to generate detailed task list with acceptance criteria
- 🧠 Reflection: Plan follows mandatory technology stack per constitution. All patterns verified via Context7 MCP ensuring up-to-date implementation guidance. Backend auth middleware (US10) uses shared JWT secret for stateless token validation.

## Evaluation notes (flywheel)

- Failure modes observed: None - all constitution gates passed
- Graders run and results (PASS/FAIL): Constitution Check PASS, Context7 Verification PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with /sp.tasks for detailed task generation
