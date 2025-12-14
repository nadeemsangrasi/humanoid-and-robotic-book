# Plan Prompt: Authentication & Frontend-Backend Integration

Use this prompt with `/sp.plan` or give it to an AI to create an implementation plan from the specification.

**IMPORTANT**: This prompt contains Context7 MCP-verified code patterns. All technical details have been validated against official documentation.

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

## Verified Code Patterns (from Context7 MCP)

### 1. Better Auth Server Configuration (lib/auth.ts)

```typescript
// Verified from: /better-auth/better-auth - drizzle adapter postgres
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/lib/db";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg", // PostgreSQL provider
  }),
  // Additional configuration...
});
```

### 2. Better Auth API Route Handler (app/api/auth/[...all]/route.ts)

```typescript
// Verified from: /better-auth/better-auth - nextjs app router api route handler
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

### 3. Better Auth Client (lib/auth-client.ts)

```typescript
// Verified from: /better-auth/better-auth - client react nextjs
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  // baseURL is optional if auth server is on same domain
});

// Export hooks for components
export const { useSession, signIn, signUp, signOut } = authClient;
```

### 4. Drizzle + Neon Connection (lib/db/index.ts)

```typescript
// Verified from: /drizzle-team/drizzle-orm-docs - neon serverless connection
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";
import { config } from "dotenv";

config({ path: ".env.local" });

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle({ client: sql });
```

### 5. Drizzle Schema for Users (lib/db/schema.ts)

```typescript
// Verified from: /better-auth/better-auth - Define User Table with Drizzle ORM PostgreSQL
import { pgTable, text, timestamp, boolean } from "drizzle-orm/pg-core";

export const user = pgTable("user", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  emailVerified: boolean("email_verified").default(false).notNull(),
  image: text("image"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at")
    .defaultNow()
    .$onUpdate(() => new Date())
    .notNull(),
});

export const session = pgTable("session", {
  id: text("id").primaryKey(),
  expiresAt: timestamp("expires_at").notNull(),
  token: text("token").notNull().unique(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at")
    .defaultNow()
    .$onUpdate(() => new Date())
    .notNull(),
  ipAddress: text("ip_address"),
  userAgent: text("user_agent"),
  userId: text("user_id")
    .notNull()
    .references(() => user.id, { onDelete: "cascade" }),
});

export const account = pgTable("account", {
  id: text("id").primaryKey(),
  accountId: text("account_id").notNull(),
  providerId: text("provider_id").notNull(),
  userId: text("user_id")
    .notNull()
    .references(() => user.id, { onDelete: "cascade" }),
  accessToken: text("access_token"),
  refreshToken: text("refresh_token"),
  idToken: text("id_token"),
  accessTokenExpiresAt: timestamp("access_token_expires_at"),
  refreshTokenExpiresAt: timestamp("refresh_token_expires_at"),
  scope: text("scope"),
  password: text("password"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at")
    .defaultNow()
    .$onUpdate(() => new Date())
    .notNull(),
});
```

### 6. Drizzle Kit Configuration (drizzle.config.ts)

```typescript
// Verified from: /drizzle-team/drizzle-orm-docs - Configure Drizzle Kit for Migrations
import { config } from "dotenv";
import { defineConfig } from "drizzle-kit";

config({ path: ".env.local" });

export default defineConfig({
  schema: "./lib/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

### 7. Protected Server Component Pattern

```typescript
// Verified from: /better-auth/better-auth - Access Session in Next.js App Router Server Component
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

export default async function ProtectedPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect("/login");
  }

  return (
    <div>
      <h1>Protected Content</h1>
      <p>Welcome, {session.user.name}!</p>
    </div>
  );
}
```

### 8. Next.js Middleware for Auth (middleware.ts)

```typescript
// Verified from: /better-auth/better-auth - Next.js 13-15.1.x Middleware
import { betterFetch } from "@better-fetch/fetch";
import type { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

type Session = typeof auth.$Infer.Session;

export async function middleware(request: NextRequest) {
  const { data: session } = await betterFetch<Session>(
    "/api/auth/get-session",
    {
      baseURL: request.nextUrl.origin,
      headers: {
        cookie: request.headers.get("cookie") || "",
      },
    }
  );

  if (!session) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/chat/:path*", "/history/:path*"],
};
```

### 9. useSession Hook Usage

```tsx
// Verified from: /better-auth/better-auth - useSession Hook - React Implementation
import { createAuthClient } from "better-auth/react";

const { useSession } = createAuthClient();

export function UserProfile() {
  const { data: session, isPending, error, refetch } = useSession();

  if (isPending) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!session) return <div>Not logged in</div>;

  return <div>Welcome, {session.user.name}!</div>;
}
```

## Next.js App Router Directory Structure (Context7 Verified)

```text
frontend/
├── app/
│   ├── (auth)/                       # Route group for auth pages (public)
│   │   ├── login/
│   │   │   └── page.tsx              # Login page
│   │   ├── register/
│   │   │   └── page.tsx              # Registration page
│   │   └── layout.tsx                # Auth layout (no sidebar)
│   ├── (protected)/                  # Route group for protected pages
│   │   ├── chat/
│   │   │   └── page.tsx              # Main chat interface
│   │   ├── history/
│   │   │   └── page.tsx              # Conversation history
│   │   └── layout.tsx                # Protected layout with auth check
│   ├── api/
│   │   ├── auth/
│   │   │   └── [...all]/
│   │   │       └── route.ts          # Better Auth catch-all handler
│   │   └── chat/
│   │       ├── route.ts              # Chat proxy to FastAPI
│   │       └── history/
│   │           └── route.ts          # Chat history CRUD
│   ├── layout.tsx                    # Root layout
│   ├── page.tsx                      # Landing/redirect
│   ├── loading.tsx                   # Global loading UI
│   ├── error.tsx                     # Global error boundary
│   └── not-found.tsx                 # 404 page
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   ├── LogoutButton.tsx
│   │   └── AuthProvider.tsx
│   ├── chat/
│   │   ├── ChatKitAdapter.tsx
│   │   ├── CitationDisplay.tsx
│   │   ├── ConversationList.tsx
│   │   └── NewChatButton.tsx
│   └── ui/
│       └── ProtectedRoute.tsx
├── lib/
│   ├── auth.ts                       # Better Auth server config
│   ├── auth-client.ts                # Better Auth client config
│   ├── db/
│   │   ├── index.ts                  # Drizzle + Neon connection
│   │   └── schema.ts                 # Drizzle schema definitions
│   ├── api/
│   │   ├── backend-adapter.ts        # FastAPI adapter
│   │   └── chat-history.ts           # Chat history service
│   └── utils/
│       └── jwt.ts                    # JWT utilities
├── drizzle/                          # Migration files (generated)
├── middleware.ts                     # Next.js auth middleware
├── drizzle.config.ts                 # Drizzle Kit config
├── .env.example
└── .env.local                        # (gitignored)
```

### Key File Conventions (Next.js App Router)

| File | Purpose |
|------|---------|
| `page.tsx` | Route UI component |
| `layout.tsx` | Shared UI wrapper for route segment |
| `loading.tsx` | Loading UI (Suspense boundary) |
| `error.tsx` | Error UI (error boundary) |
| `not-found.tsx` | 404 UI |
| `route.ts` | API endpoint handler |
| `middleware.ts` | Request middleware (root level) |

### Route Groups

- `(auth)` - Groups auth pages without affecting URL path
- `(protected)` - Groups protected pages, allows shared layout with auth check

## Plan Phases

### Phase 0: Documentation Fetch (MANDATORY)

Before ANY implementation, fetch Context7 MCP docs:

```bash
# These have been pre-fetched and verified above
# Implementation must reference these patterns
```

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
2. Create `app/api/chat/route.ts` as proxy
3. Modify `components/ChatKitPanel.tsx` to use adapter
4. Create `components/chat/CitationDisplay.tsx`
5. Test chat flow end-to-end

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
4. **research.md** - Context7 MCP documentation findings (pre-verified above)
5. **data-model.md** - Drizzle schema definitions (verified patterns above)
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
├── research.md                # Context7 MCP findings (verified)
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
4. The verified code patterns above should be used directly - they are MCP-verified
5. Verify all outputs are created

---

## VERIFIED SOURCES (Context7 MCP)

| Technology | Library ID | Topics Fetched |
|------------|-----------|----------------|
| Better Auth | `/better-auth/better-auth` | nextjs, drizzle adapter, client, api route |
| Drizzle ORM | `/drizzle-team/drizzle-orm-docs` | postgres schema, neon connection, migrations |
| Next.js App Router | `/websites/nextjs_app` | directory structure, file conventions |
| Neon Serverless | `/neondatabase/serverless` | connection setup, drizzle integration |

All code patterns in this prompt have been verified against official documentation via Context7 MCP.

---

## RELATED ARTIFACTS

- Specification: `specs/002-auth-frontend-integration/spec.md`
- Existing Frontend: `frontend/`
- Backend Spec (reference): `specs/001-rag-chatbot-backend/`
- Constitution: `.specify/memory/constitution.md`
