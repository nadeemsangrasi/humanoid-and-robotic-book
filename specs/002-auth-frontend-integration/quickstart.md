# Quickstart: Authentication & Frontend-Backend Integration

**Feature Branch**: `002-auth-frontend-integration`
**Date**: 2025-12-14
**Estimated Setup Time**: 10 minutes

---

## Prerequisites

- Node.js 18+ installed
- npm or pnpm package manager
- Neon PostgreSQL account (free tier): https://neon.tech
- Existing frontend in `frontend/` folder

---

## Step 1: Create Neon Database

1. Go to https://console.neon.tech
2. Create a new project (free tier)
3. Copy the connection string from the dashboard

**Connection String Format**:
```
postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

---

## Step 2: Environment Setup

Create `.env.local` in the `frontend/` directory:

```bash
cd frontend
```

Create the file with these variables:

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-at-least-32-characters-long
BETTER_AUTH_URL=http://localhost:3000

# Backend API (Hugging Face Spaces)
NEXT_PUBLIC_BACKEND_URL=https://your-space.hf.space

# Optional: OAuth Providers (P3)
# GOOGLE_CLIENT_ID=
# GOOGLE_CLIENT_SECRET=
# GITHUB_CLIENT_ID=
# GITHUB_CLIENT_SECRET=
```

**Generate a secure secret**:
```bash
openssl rand -base64 32
```

---

## Step 3: Install Dependencies

```bash
cd frontend

# Core dependencies
npm install better-auth @better-fetch/fetch
npm install drizzle-orm @neondatabase/serverless

# Development dependencies
npm install -D drizzle-kit
```

---

## Step 4: Database Schema & Migrations

**4.1 Create schema file** (`lib/db/schema.ts`):

```typescript
import { pgTable, text, timestamp, boolean } from 'drizzle-orm/pg-core';

// Better Auth Core Tables
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

// Application Tables (Phase 4)
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
  role: text('role').notNull(),
  content: text('content').notNull(),
  citations: text('citations'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});
```

**4.2 Create database connection** (`lib/db/index.ts`):

```typescript
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";
import * as schema from "./schema";

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle({ client: sql, schema });
```

**4.3 Create Drizzle config** (`drizzle.config.ts`):

```typescript
import { config } from 'dotenv';
import { defineConfig } from "drizzle-kit";

config({ path: '.env.local' });

export default defineConfig({
  schema: "./lib/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

**4.4 Generate and apply migrations**:

```bash
# Generate migration files
npx drizzle-kit generate

# Apply migrations to database
npx drizzle-kit migrate
```

---

## Step 5: Better Auth Configuration

**5.1 Server config** (`lib/auth.ts`):

```typescript
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "./db";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
  }),
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 minutes
    },
  },
});
```

**5.2 API route handler** (`app/api/auth/[...all]/route.ts`):

```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

**5.3 Client config** (`lib/auth-client.ts`):

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient();

export const { useSession, signIn, signUp, signOut } = authClient;
```

---

## Step 6: Verify Setup

**6.1 Start development server**:

```bash
npm run dev
```

**6.2 Test authentication endpoints**:

```bash
# Test sign-up
curl -X POST http://localhost:3000/api/auth/sign-up/email \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"Password123"}'

# Test sign-in
curl -X POST http://localhost:3000/api/auth/sign-in/email \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Password123"}'
```

**6.3 Verify database**:

Check your Neon dashboard to see the created tables:
- `user`
- `session`
- `account`
- `chat_session`
- `chat_message`

---

## Troubleshooting

### Database Connection Errors

```
Error: connection refused
```

**Solution**: Verify `DATABASE_URL` is correct and Neon project is active.

### Migration Errors

```
Error: relation "user" already exists
```

**Solution**: Run `npx drizzle-kit drop` to clear migrations, then regenerate.

### Auth Cookie Not Set

**Solution**: Ensure `BETTER_AUTH_URL` matches your development URL (http://localhost:3000).

### CORS Errors

**Solution**: Add the backend URL to Next.js config if needed:

```typescript
// next.config.ts
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/backend/:path*',
        destination: `${process.env.NEXT_PUBLIC_BACKEND_URL}/:path*`,
      },
    ];
  },
};
```

---

## Project Structure After Setup

```
frontend/
├── app/
│   ├── api/
│   │   └── auth/
│   │       └── [...all]/
│   │           └── route.ts          # Better Auth handler
│   └── ...
├── lib/
│   ├── auth.ts                       # Better Auth server config
│   ├── auth-client.ts                # Better Auth client
│   └── db/
│       ├── index.ts                  # Drizzle connection
│       └── schema.ts                 # Database schema
├── drizzle/                          # Migration files
├── drizzle.config.ts                 # Drizzle Kit config
├── .env.local                        # Environment variables
└── ...
```

---

## Next Steps

After completing this quickstart:

1. **Phase 3**: Build auth UI components (LoginForm, RegisterForm)
2. **Phase 4**: Add middleware for route protection
3. **Phase 5**: Create ChatKit backend adapter
4. **Phase 6**: Implement chat history

See `plan.md` for the full implementation roadmap.
