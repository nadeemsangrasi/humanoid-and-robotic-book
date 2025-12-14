# Data Model: Authentication & Frontend-Backend Integration

**Feature Branch**: `002-auth-frontend-integration`
**Date**: 2025-12-14
**ORM**: Drizzle ORM
**Database**: PostgreSQL (Neon)

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    user     │───1:N─│   session   │       │   account   │
│             │       │             │       │   (OAuth)   │
│  id (PK)    │       │  id (PK)    │       │  id (PK)    │
│  name       │       │  userId(FK) │       │  userId(FK) │
│  email      │       │  token      │       │  providerId │
│  image      │       │  expiresAt  │       │  accountId  │
│  ...        │       │  ...        │       │  ...        │
└─────────────┘       └─────────────┘       └─────────────┘
       │
       │ 1:N
       ▼
┌─────────────┐       ┌─────────────┐
│ chatSession │───1:N─│ chatMessage │
│             │       │             │
│  id (PK)    │       │  id (PK)    │
│  userId(FK) │       │ sessionId(FK)
│  title      │       │  role       │
│  ...        │       │  content    │
└─────────────┘       │  citations  │
                      └─────────────┘
```

---

## Schema Definitions

### User Table (Better Auth Core)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | text | PK | Unique identifier (UUID) |
| `name` | text | NOT NULL | User's display name |
| `email` | text | NOT NULL, UNIQUE | User's email address |
| `emailVerified` | boolean | DEFAULT false | Email verification status |
| `image` | text | NULLABLE | Profile image URL |
| `createdAt` | timestamp | NOT NULL, DEFAULT NOW | Account creation time |
| `updatedAt` | timestamp | NOT NULL, DEFAULT NOW | Last update time |

**Drizzle Schema:**
```typescript
export const user = pgTable('user', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  emailVerified: boolean('email_verified').notNull().default(false),
  image: text('image'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});
```

---

### Session Table (Better Auth Core)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | text | PK | Unique identifier |
| `userId` | text | FK -> user.id, NOT NULL | Associated user |
| `token` | text | NOT NULL, UNIQUE | Session token (JWT) |
| `expiresAt` | timestamp | NOT NULL | Session expiry time |
| `ipAddress` | text | NULLABLE | Client IP address |
| `userAgent` | text | NULLABLE | Client user agent |
| `createdAt` | timestamp | NOT NULL, DEFAULT NOW | Session creation time |
| `updatedAt` | timestamp | NOT NULL, DEFAULT NOW | Last activity time |

**Drizzle Schema:**
```typescript
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
```

---

### Account Table (OAuth - Better Auth Core)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | text | PK | Unique identifier |
| `userId` | text | FK -> user.id, NOT NULL | Associated user |
| `accountId` | text | NOT NULL | Provider's account ID |
| `providerId` | text | NOT NULL | OAuth provider (google, github) |
| `accessToken` | text | NULLABLE | OAuth access token |
| `refreshToken` | text | NULLABLE | OAuth refresh token |
| `accessTokenExpiresAt` | timestamp | NULLABLE | Access token expiry |
| `refreshTokenExpiresAt` | timestamp | NULLABLE | Refresh token expiry |
| `scope` | text | NULLABLE | OAuth scopes |
| `idToken` | text | NULLABLE | OIDC ID token |
| `createdAt` | timestamp | NOT NULL, DEFAULT NOW | Account link time |
| `updatedAt` | timestamp | NOT NULL, DEFAULT NOW | Last update time |

**Drizzle Schema:**
```typescript
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

---

### Chat Session Table (Application-Specific)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | text | PK | Unique identifier (UUID) |
| `userId` | text | FK -> user.id, NOT NULL | Conversation owner |
| `title` | text | NULLABLE | Conversation title (auto-generated) |
| `createdAt` | timestamp | NOT NULL, DEFAULT NOW | Conversation start time |
| `updatedAt` | timestamp | NOT NULL, DEFAULT NOW | Last message time |

**Drizzle Schema:**
```typescript
export const chatSession = pgTable('chat_session', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
  title: text('title'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});
```

---

### Chat Message Table (Application-Specific)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | text | PK | Unique identifier (UUID) |
| `sessionId` | text | FK -> chatSession.id, NOT NULL | Parent conversation |
| `role` | text | NOT NULL | 'user' or 'assistant' |
| `content` | text | NOT NULL | Message content |
| `citations` | text | NULLABLE | JSON array of citations |
| `createdAt` | timestamp | NOT NULL, DEFAULT NOW | Message timestamp |

**Drizzle Schema:**
```typescript
export const chatMessage = pgTable('chat_message', {
  id: text('id').primaryKey(),
  sessionId: text('session_id').notNull().references(() => chatSession.id, { onDelete: 'cascade' }),
  role: text('role').notNull(), // 'user' | 'assistant'
  content: text('content').notNull(),
  citations: text('citations'), // JSON string
  createdAt: timestamp('created_at').notNull().defaultNow(),
});
```

---

## Citation JSON Structure

The `citations` column stores a JSON string with the following structure:

```typescript
interface Citation {
  title: string;        // Source document/section title
  url: string;          // Link to textbook section
  excerpt?: string;     // Relevant text excerpt
  score?: number;       // Relevance score (0-1)
}

// Example stored value:
// '[{"title":"Chapter 2: ROS2 Basics","url":"/docs/02-module-1-ros2/01-ros2-basics","excerpt":"ROS 2 is the second generation of the Robot Operating System...","score":0.92}]'
```

---

## Relationships

| Relationship | Type | Cascade | Description |
|--------------|------|---------|-------------|
| user → session | 1:N | DELETE | User deletion removes all sessions |
| user → account | 1:N | DELETE | User deletion removes OAuth accounts |
| user → chatSession | 1:N | DELETE | User deletion removes all conversations |
| chatSession → chatMessage | 1:N | DELETE | Conversation deletion removes all messages |

---

## Indexes (Recommended)

```sql
-- Performance indexes
CREATE INDEX idx_session_user_id ON session(user_id);
CREATE INDEX idx_session_token ON session(token);
CREATE INDEX idx_account_user_id ON account(user_id);
CREATE INDEX idx_chat_session_user_id ON chat_session(user_id);
CREATE INDEX idx_chat_message_session_id ON chat_message(session_id);
CREATE INDEX idx_chat_message_created_at ON chat_message(created_at);
```

---

## Type Definitions

```typescript
// Inferred types from Drizzle schema
export type User = typeof user.$inferSelect;
export type NewUser = typeof user.$inferInsert;

export type Session = typeof session.$inferSelect;
export type NewSession = typeof session.$inferInsert;

export type Account = typeof account.$inferSelect;
export type NewAccount = typeof account.$inferInsert;

export type ChatSession = typeof chatSession.$inferSelect;
export type NewChatSession = typeof chatSession.$inferInsert;

export type ChatMessage = typeof chatMessage.$inferSelect;
export type NewChatMessage = typeof chatMessage.$inferInsert;

// Application types
export type MessageRole = 'user' | 'assistant';

export interface Citation {
  title: string;
  url: string;
  excerpt?: string;
  score?: number;
}
```

---

## Migration Strategy

1. **Initial Migration**: Create user, session, account tables (Better Auth core)
2. **Phase 4 Migration**: Add chatSession and chatMessage tables

```bash
# Generate migration
npx drizzle-kit generate

# Apply migration
npx drizzle-kit migrate
```

---

## Validation Rules

### User
- **email**: Valid email format, max 255 characters
- **name**: Min 1 character, max 100 characters
- **password** (handled by Better Auth): Min 8 characters, 1 uppercase, 1 lowercase, 1 number

### ChatSession
- **title**: Auto-generated from first user message, max 100 characters

### ChatMessage
- **role**: Must be 'user' or 'assistant'
- **content**: Max 50,000 characters
- **citations**: Valid JSON array or null
