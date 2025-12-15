# Research: Authentication & Frontend-Backend Integration

**Feature Branch**: `002-auth-frontend-integration`
**Date**: 2025-12-14
**Sources**: Context7 MCP Server (verified documentation)

---

## 1. Better Auth + Drizzle ORM Integration

### Decision
Use `betterAuth()` with `drizzleAdapter(db, { provider: "pg" })` for authentication with PostgreSQL/Neon.

### Rationale
- Better Auth provides native Drizzle adapter support
- The adapter handles schema mapping automatically for user, session, and account tables
- Supports bcrypt password hashing by default
- JWT sessions with httpOnly cookies are supported out-of-box

### Context7 Verified Patterns

**Server Configuration** (`lib/auth.ts`):
```typescript
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/lib/db";

export const auth = betterAuth({
    database: drizzleAdapter(db, {
        provider: "pg",
    }),
});
```

**API Route Handler** (`app/api/auth/[...all]/route.ts`):
```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

**Client Configuration** (`lib/auth-client.ts`):
```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
    // client configuration
});

export const { useSession, signIn, signUp, signOut } = authClient;
```

### Alternatives Considered
- **NextAuth.js**: More complex configuration, requires additional adapters
- **Clerk**: Third-party service, not self-hosted
- **Custom JWT**: More work, less secure without proper implementation

---

## 2. Drizzle ORM + Neon PostgreSQL Connection

### Decision
Use `drizzle-orm/neon-http` driver with `@neondatabase/serverless` for serverless-optimized database connections.

### Rationale
- Neon HTTP driver is optimized for serverless environments (Next.js Edge/Serverless)
- Connection pooling handled automatically
- Low-latency connections to Neon PostgreSQL
- Compatible with Drizzle Kit for migrations

### Context7 Verified Patterns

**Database Connection** (`lib/db/index.ts`):
```typescript
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";
import { config } from "dotenv";

config({ path: ".env" });

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle({ client: sql });
```

**Drizzle Kit Configuration** (`drizzle.config.ts`):
```typescript
import { config } from 'dotenv';
import { defineConfig } from "drizzle-kit";

config({ path: '.env' });

export default defineConfig({
  schema: "./lib/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

**Schema Definition** (`lib/db/schema.ts`):
```typescript
import { pgTable, text, timestamp, boolean } from 'drizzle-orm/pg-core';

export const user = pgTable('user', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  emailVerified: boolean('email_verified').notNull().default(false),
  image: text('image'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});

export const session = pgTable('session', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
  token: text('token').notNull().unique(),
  expiresAt: timestamp('expires_at').notNull(),
  ipAddress: text('ip_address'),
  userAgent: text('user_agent'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});

export const account = pgTable('account', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
  accountId: text('account_id').notNull(),
  providerId: text('provider_id').notNull(),
  accessToken: text('access_token'),
  refreshToken: text('refresh_token'),
  accessTokenExpiresAt: timestamp('access_token_expires_at'),
  refreshTokenExpiresAt: timestamp('refresh_token_expires_at'),
  scope: text('scope'),
  idToken: text('id_token'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});
```

### Alternatives Considered
- **Prisma**: Heavier, different migration approach
- **pg/node-postgres**: Not optimized for serverless
- **Drizzle with WebSocket**: More complex, not needed for this use case

---

## 3. Next.js Middleware for Route Protection

### Decision
Use Next.js middleware with `auth.api.getSession()` for server-side session validation in protected routes.

### Rationale
- Middleware runs before requests reach pages
- Can validate session and redirect unauthenticated users
- Next.js 15.2.0+ supports Node.js runtime in middleware
- Cookie forwarding handled automatically

### Context7 Verified Patterns

**Middleware** (`middleware.ts`):
```typescript
import { NextRequest, NextResponse } from "next/server";
import { headers } from "next/headers";
import { auth } from "@/lib/auth";

const protectedRoutes = ['/chat', '/history'];
const publicRoutes = ['/login', '/register', '/'];

export async function middleware(request: NextRequest) {
    const path = request.nextUrl.pathname;
    const isProtectedRoute = protectedRoutes.some(route => path.startsWith(route));
    const isPublicRoute = publicRoutes.includes(path);

    const session = await auth.api.getSession({
        headers: await headers()
    });

    if (isProtectedRoute && !session) {
        const loginUrl = new URL("/login", request.url);
        loginUrl.searchParams.set("callbackUrl", path);
        return NextResponse.redirect(loginUrl);
    }

    if (isPublicRoute && session && !path.startsWith('/chat')) {
        return NextResponse.redirect(new URL("/chat", request.url));
    }

    return NextResponse.next();
}

export const config = {
    runtime: "nodejs",
    matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
};
```

**Alternative: Edge Runtime with HTTP fetch** (for Next.js < 15.2.0):
```typescript
import { betterFetch } from "@better-fetch/fetch";
import type { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

type Session = typeof auth.$Infer.Session;

export async function middleware(request: NextRequest) {
    const { data: session } = await betterFetch<Session>("/api/auth/get-session", {
        baseURL: request.nextUrl.origin,
        headers: {
            cookie: request.headers.get("cookie") || "",
        },
    });

    if (!session) {
        return NextResponse.redirect(new URL("/login", request.url));
    }

    return NextResponse.next();
}
```

---

## 4. Better Auth Client Hooks

### Decision
Use `createAuthClient()` from `better-auth/react` with `useSession`, `signIn.email`, `signUp.email`, and `signOut` methods.

### Rationale
- Native React integration with reactive state management
- Built-in loading states, error handling, and refetch capabilities
- Type-safe session data
- Supports callbacks for request lifecycle (onRequest, onSuccess, onError)

### Context7 Verified Patterns

**useSession Hook**:
```typescript
import { createAuthClient } from "better-auth/react";

const { useSession } = createAuthClient();

export function UserProfile() {
    const { data: session, isPending, error, refetch } = useSession();

    if (isPending) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;
    if (!session) return <div>Not authenticated</div>;

    return (
        <div>
            <h1>Welcome, {session.user.name}!</h1>
            <p>Email: {session.user.email}</p>
        </div>
    );
}
```

**Sign In**:
```typescript
const signIn = async () => {
    await authClient.signIn.email(
        { email, password },
        {
            onRequest: () => setLoading(true),
            onSuccess: () => router.push('/chat'),
            onError: (ctx) => setError(ctx.error.message),
        }
    );
};
```

**Sign Up**:
```typescript
const signUp = async () => {
    await authClient.signUp.email(
        { email, password, name },
        {
            onRequest: () => setLoading(true),
            onSuccess: () => router.push('/chat'),
            onError: (ctx) => setError(ctx.error.message),
        }
    );
};
```

---

## 5. Session/Token Strategy

### Decision
Use JWT tokens stored in httpOnly cookies, validated via backend middleware.

### Rationale (from /sp.clarify)
- **httpOnly cookies**: Immune to XSS attacks, automatically sent with requests
- **JWT (stateless)**: No database lookup required for session validation, better performance
- **bcrypt**: Industry standard password hashing, built into Better Auth

### Implementation Details
- JWT token generated on login, stored in httpOnly cookie
- Token extracted from cookie for API calls using `Authorization: Bearer <jwt>` header
- Backend validates JWT cryptographically without database lookup
- Session expiry: 7 days of inactivity (configurable in Better Auth)

---

## 6. Backend URL Configuration

### Decision
Use environment variable `NEXT_PUBLIC_BACKEND_URL` for configuring the FastAPI backend endpoint.

### Rationale
- Environment-variable-based configuration allows different URLs per deployment
- `NEXT_PUBLIC_` prefix makes it available in client-side code
- Easy to switch between development, staging, and production backends

### Implementation
```env
# .env.local (development)
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# .env.production
NEXT_PUBLIC_BACKEND_URL=https://your-space.hf.space
```

---

## 7. Chat History Schema

### Decision
Add `chatSession` and `chatMessage` tables to Drizzle schema for conversation persistence.

### Schema Design
```typescript
export const chatSession = pgTable('chat_session', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
  title: text('title'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});

export const chatMessage = pgTable('chat_message', {
  id: text('id').primaryKey(),
  sessionId: text('session_id').notNull().references(() => chatSession.id, { onDelete: 'cascade' }),
  role: text('role').notNull(), // 'user' | 'assistant'
  content: text('content').notNull(),
  citations: text('citations'), // JSON string of citation objects
  createdAt: timestamp('created_at').notNull().defaultNow(),
});
```

---

## 8. Dependencies Summary

### Required Packages
```bash
# Authentication
npm install better-auth @better-fetch/fetch

# Database ORM
npm install drizzle-orm @neondatabase/serverless

# Development
npm install -D drizzle-kit
```

### Package Versions (verified compatible)
- `better-auth`: latest (v1.x)
- `drizzle-orm`: latest
- `@neondatabase/serverless`: latest
- `drizzle-kit`: latest (dev dependency)

---

## Sources

All patterns verified via Context7 MCP Server:

| Library | Context7 ID | Topics Verified |
|---------|-------------|-----------------|
| Better Auth | `/better-auth/better-auth` | drizzle adapter, nextjs integration, client hooks, middleware |
| Drizzle ORM | `/drizzle-team/drizzle-orm-docs` | neon connection, schema definition, migrations |
| Neon Serverless | `/neondatabase/serverless` | connection setup, serverless patterns |
| Next.js App Router | `/websites/nextjs_app` | middleware, route protection, API routes |
