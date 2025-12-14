# Plan Prompt: Authentication & Frontend-Backend Integration

Use this prompt with `/sp.plan` or give it to an AI to create an implementation plan from the specification.

**IMPORTANT**: All technical patterns referenced in this prompt have been verified via Context7 MCP against official documentation.

---

## PROMPT

```
Create a SpecKit Plus implementation plan for the Authentication & Frontend-Backend Integration feature based on the specification at `specs/002-auth-frontend-integration/spec.md`.

## Input Specification Summary

The specification covers:
- User Authentication: Registration, login, JWT sessions, logout (Better Auth + Neon + Drizzle)
- ChatKit Backend Adapter: Customizing ChatKit UI to connect to FastAPI RAG backend
- Chat History Persistence: Storing and retrieving user conversations
- Protected Routes: Authenticated access to chat interface

## Clarified Decisions (from /sp.clarify)

These decisions were made during clarification and MUST be followed:

1. **Session Storage**: JWT tokens (stateless, validated via backend middleware)
2. **Auth Header Format**: `Authorization: Bearer <jwt>` (standard OAuth2 pattern)
3. **Backend URL Config**: Environment variable `NEXT_PUBLIC_BACKEND_URL`
4. **Token Storage**: httpOnly cookie (XSS-immune, with cookie-to-header extraction)
5. **Password Hashing**: bcrypt algorithm (Better Auth default)

## Technical Context (Context7 MCP Verified)

**Framework/Version**: Next.js 15 (App Router)
**Language**: TypeScript
**Primary Dependencies**:
- better-auth (authentication library)
- better-auth/adapters/drizzle (Drizzle adapter)
- drizzle-orm (TypeScript ORM)
- drizzle-orm/neon-http (Neon HTTP driver)
- @neondatabase/serverless (Neon serverless driver)
- @openai/chatkit-react (existing chat UI)

**Database**: PostgreSQL on Neon (free tier)
**Authentication**: Better Auth with email/password + JWT
**Existing Backend**: FastAPI on Hugging Face Spaces
  - POST /api/v1/chat - RAG Q&A endpoint
  - GET /health - Health check
**Testing**: Jest + React Testing Library
**Project Type**: Frontend (Next.js) in `frontend/` folder

## Constitution Check

Verify against project constitution before implementation:
- [ ] Uses Better Auth library (C-001)
- [ ] Uses PostgreSQL Neon DB free tier (C-002)
- [ ] Uses Drizzle ORM only (C-003)
- [ ] Uses existing ChatKit React components (C-004)
- [ ] Backend calls include auth context (C-005)
- [ ] All secrets in environment variables (C-006)
- [ ] HTTPS for production API calls (C-007)
- [ ] Context7 MCP used for all documentation (C-008)

## Context7 MCP Verified Patterns

The following patterns have been verified against official documentation. Use these as reference during implementation:

| Pattern | Source | Key Points |
|---------|--------|------------|
| Better Auth Server Config | `/better-auth/better-auth` | Use `betterAuth()` with `drizzleAdapter(db, { provider: "pg" })` |
| Better Auth API Route | `/better-auth/better-auth` | Use `toNextJsHandler(auth)` in `app/api/auth/[...all]/route.ts` |
| Better Auth Client | `/better-auth/better-auth` | Use `createAuthClient()` from `better-auth/react` |
| Drizzle + Neon Connection | `/drizzle-team/drizzle-orm-docs` | Use `drizzle({ client: neon(DATABASE_URL) })` from `drizzle-orm/neon-http` |
| Drizzle Schema | `/better-auth/better-auth` | Tables: `user`, `session`, `account` with `pgTable()` |
| Drizzle Kit Config | `/drizzle-team/drizzle-orm-docs` | Use `defineConfig()` with `dialect: "postgresql"` |
| Protected Server Component | `/better-auth/better-auth` | Use `auth.api.getSession({ headers: await headers() })` |
| Next.js Middleware | `/better-auth/better-auth` | Use `betterFetch("/api/auth/get-session")` with cookie forwarding |
| useSession Hook | `/better-auth/better-auth` | Returns `{ data, isPending, error, refetch }` |

## Existing Frontend Structure (OpenAI ChatKit Starter)

The frontend already has Next.js 15 with OpenAI ChatKit initialized:

```text
frontend/                            # EXISTING FILES
├── app/
│   ├── api/
│   │   └── create-session/
│   │       └── route.ts             # ChatKit session endpoint (existing)
│   ├── App.tsx                      # Main app component (client)
│   ├── favicon.ico
│   ├── globals.css
│   ├── layout.tsx                   # Root layout
│   └── page.tsx                     # Home page (renders App)
├── components/
│   ├── ChatKitPanel.tsx             # Main ChatKit component (to modify)
│   └── ErrorOverlay.tsx             # Error display component
├── hooks/
│   └── useColorScheme.ts            # Theme hook
├── lib/
│   └── config.ts                    # ChatKit config (workflow ID, prompts)
├── public/
│   └── docs/
│       └── workflow.jpg
├── .env.example                     # Existing: OPENAI_API_KEY, NEXT_PUBLIC_CHATKIT_WORKFLOW_ID
├── next.config.ts
├── package.json                     # Next.js 15.5.4, React 19.2.0, @openai/chatkit-react
├── postcss.config.mjs
├── eslint.config.mjs
└── tsconfig.json
```

## New Files to Add (Auth + Backend Adapter)

```text
frontend/                            # NEW FILES TO CREATE
├── app/
│   ├── (auth)/                      # Route group for auth pages (public)
│   │   ├── login/
│   │   │   └── page.tsx             # NEW: Login page
│   │   ├── register/
│   │   │   └── page.tsx             # NEW: Register page
│   │   └── layout.tsx               # NEW: Auth layout
│   ├── (protected)/                 # Route group for protected pages
│   │   ├── chat/
│   │   │   └── page.tsx             # NEW: Protected chat page
│   │   ├── history/
│   │   │   └── page.tsx             # NEW: Chat history page
│   │   └── layout.tsx               # NEW: Protected layout with auth check
│   └── api/
│       ├── auth/
│       │   └── [...all]/
│       │       └── route.ts         # NEW: Better Auth catch-all handler
│       └── chat/
│           ├── route.ts             # NEW: Backend proxy endpoint
│           └── history/
│               └── route.ts         # NEW: Chat history endpoint
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx            # NEW
│   │   ├── RegisterForm.tsx         # NEW
│   │   ├── LogoutButton.tsx         # NEW
│   │   └── AuthProvider.tsx         # NEW
│   └── chat/
│       ├── CitationDisplay.tsx      # NEW
│       ├── ConversationList.tsx     # NEW
│       └── NewChatButton.tsx        # NEW
├── lib/
│   ├── auth.ts                      # NEW: Better Auth server config
│   ├── auth-client.ts               # NEW: Better Auth client config
│   ├── db/
│   │   ├── index.ts                 # NEW: Drizzle + Neon connection
│   │   └── schema.ts                # NEW: Drizzle schema definitions
│   └── api/
│       ├── backend-adapter.ts       # NEW: FastAPI request/response adapter
│       └── chat-history.ts          # NEW: Chat history service
├── drizzle/                         # NEW: Migration files (generated)
├── middleware.ts                    # NEW: Auth middleware
└── drizzle.config.ts                # NEW: Drizzle Kit config
```

## Files to Modify

| File | Modification |
|------|-------------|
| `components/ChatKitPanel.tsx` | Replace `getClientSecret` with backend adapter, add auth headers |
| `lib/config.ts` | Add `BACKEND_URL` config, update session endpoint |
| `app/layout.tsx` | Wrap with `AuthProvider` |
| `.env.example` | Add `DATABASE_URL`, `BETTER_AUTH_SECRET`, `NEXT_PUBLIC_BACKEND_URL` |
| `package.json` | Add `better-auth`, `drizzle-orm`, `@neondatabase/serverless` |

### Key File Conventions (Next.js App Router)

| File | Purpose |
|------|---------|
| `page.tsx` | Route UI component |
| `layout.tsx` | Shared UI wrapper for route segment |
| `route.ts` | API endpoint handler |
| `middleware.ts` | Request middleware (root level) |

### Route Groups

- `(auth)` - Groups auth pages without affecting URL path (login, register)
- `(protected)` - Groups protected pages with shared auth check layout

## Plan Phases

### Phase 1: Database Setup

1. Create Neon PostgreSQL database (free tier)
2. Obtain connection string
3. Set up `DATABASE_URL` in `.env.local`
4. Install dependencies: `@neondatabase/serverless`, `drizzle-orm`, `drizzle-kit`
5. Create `lib/db/index.ts` with Neon connection
6. Create `lib/db/schema.ts` with Better Auth tables (user, session, account)
7. Create `drizzle.config.ts`
8. Run `npx drizzle-kit generate` and `npx drizzle-kit migrate`

**Agent**: Auth-Integration-Agent
**Skill**: drizzle-schema-generation

### Phase 2: Better Auth Configuration

1. Install: `better-auth`, `@better-fetch/fetch`
2. Create `lib/auth.ts` with drizzleAdapter
3. Create `app/api/auth/[...all]/route.ts` with toNextJsHandler
4. Create `lib/auth-client.ts` with createAuthClient
5. Test auth endpoints: `/api/auth/sign-up`, `/api/auth/sign-in`

**Agent**: Auth-Integration-Agent
**Skill**: better-auth-configuration

### Phase 3: Auth UI Components

1. Create `components/auth/AuthProvider.tsx` (React context)
2. Create `components/auth/LoginForm.tsx`
3. Create `components/auth/RegisterForm.tsx`
4. Create `components/auth/LogoutButton.tsx`
5. Create `app/(auth)/login/page.tsx`
6. Create `app/(auth)/register/page.tsx`
7. Create `app/(auth)/layout.tsx`

**Agent**: Auth-Integration-Agent
**Skill**: frontend-auth-integration

### Phase 4: Protected Routes

1. Create `middleware.ts` with auth check
2. Create `app/(protected)/layout.tsx` with server-side session check
3. Create `components/ui/ProtectedRoute.tsx` for client components
4. Test route protection

**Agent**: Auth-Integration-Agent
**Skill**: frontend-auth-integration

### Phase 5: ChatKit Backend Adapter

1. Create `lib/api/backend-adapter.ts`
   - Transform ChatKit request → FastAPI format
   - Transform FastAPI response → ChatKit format
   - Add Authorization header with JWT
2. Create `app/api/chat/route.ts` as proxy to FastAPI backend
3. Modify existing `components/ChatKitPanel.tsx`:
   - Replace OpenAI workflow session with backend adapter
   - Keep existing theme, error handling, and widget action logic
4. Update `lib/config.ts` to add `BACKEND_URL` config
5. Create `components/chat/CitationDisplay.tsx` for RAG citations
6. Test chat flow end-to-end with FastAPI backend

**Agent**: UI-and-ChatKit-customization-agent
**Skill**: chatkit-backend-adapter

### Phase 6: Chat History

1. Add `chatSession` and `chatMessage` tables to schema
2. Run migrations
3. Create `lib/api/chat-history.ts` service
4. Create `app/api/chat/history/route.ts`
5. Create `components/chat/ConversationList.tsx`
6. Create `components/chat/NewChatButton.tsx`
7. Integrate with chat UI

**Agent**: UI-and-ChatKit-customization-agent + Auth-Integration-Agent
**Skill**: ui-customization, drizzle-schema-generation

### Phase 7: Testing & Polish

1. Unit tests for auth components
2. Integration tests for API routes
3. E2E tests for auth flow
4. Error handling refinement
5. Update `.env.example`
6. Documentation

**Agent**: backend-architect-and-sdk-agent

## Environment Variables

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Backend API
NEXT_PUBLIC_BACKEND_URL=https://your-space.hf.space

# Optional: OAuth (P3)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

## Agent Assignment Summary

| Component | Agent | Skill |
|-----------|-------|-------|
| Drizzle schema | Auth-Integration-Agent | drizzle-schema-generation |
| Better Auth config | Auth-Integration-Agent | better-auth-configuration |
| Auth UI components | Auth-Integration-Agent | frontend-auth-integration |
| ChatKit adapter | UI-and-ChatKit-customization-agent | chatkit-backend-adapter |
| Citation display | UI-and-ChatKit-customization-agent | ui-customization |
| Conversation list UI | UI-and-ChatKit-customization-agent | ui-customization |
| Next.js middleware | Auth-Integration-Agent | frontend-auth-integration |

## Key Installation Commands

```bash
# Core dependencies
npm install better-auth @better-fetch/fetch
npm install drizzle-orm @neondatabase/serverless
npm install -D drizzle-kit

# Generate and apply migrations
npx drizzle-kit generate
npx drizzle-kit migrate
```

## Output Format

The plan must include:

1. **Technical Context** - All fields filled (no NEEDS CLARIFICATION)
2. **Constitution Check** - All gates passed with checkmarks
3. **Project Structure** - Verified against Next.js App Router conventions
4. **research.md** - Context7 MCP documentation findings
5. **data-model.md** - Drizzle schema definitions
6. **contracts/api-contracts.md** - API specifications
7. **quickstart.md** - Developer setup instructions
8. **Agent assignments** - Per phase assignments
```

---

## EXPECTED OUTPUT FILES

After running `/sp.plan`, these files should be created:

```
specs/002-auth-frontend-integration/
├── plan.md                    # Main implementation plan
├── research.md                # Context7 MCP findings
├── data-model.md              # Drizzle schema definitions
├── contracts/
│   └── api-contracts.md       # API specifications
└── quickstart.md              # Developer setup guide
```

---

## USAGE

1. Ensure specification exists at `specs/002-auth-frontend-integration/spec.md`
2. Ensure clarifications have been completed (`## Clarifications` section exists)
3. Run `/sp.plan` in Claude Code
4. Verify all outputs are created

---

## VERIFIED SOURCES (Context7 MCP)

| Technology | Library ID | Topics Verified |
|------------|-----------|-----------------|
| Better Auth | `/better-auth/better-auth` | nextjs, drizzle adapter, client, api route, middleware |
| Drizzle ORM | `/drizzle-team/drizzle-orm-docs` | postgres schema, neon connection, migrations |
| Next.js App Router | `/websites/nextjs_app` | directory structure, file conventions |
| Neon Serverless | `/neondatabase/serverless` | connection setup, drizzle integration |

---

## RELATED ARTIFACTS

- Specification: `specs/002-auth-frontend-integration/spec.md`
- Existing Frontend: `frontend/`
- Backend Spec (reference): `specs/001-rag-chatbot-backend/`
- Constitution: `.specify/memory/constitution.md`
