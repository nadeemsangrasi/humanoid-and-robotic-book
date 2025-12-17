# Data Model: Book & Chatbot Integration

**Feature**: 004-book-chatbot-integration
**Date**: 2025-12-16

## Overview

This feature is primarily a **frontend UI enhancement** and does not require new database tables. It leverages the existing Drizzle ORM schema from feature 002-auth-frontend-integration.

## Existing Entities (No Changes)

The following entities from `frontend/lib/db/schema.ts` are used as-is:

### User
```typescript
{
  id: string;           // Primary key
  name: string;         // Display name
  email: string;        // Unique email
  emailVerified: boolean;
  image: string | null;
  createdAt: Date;
  updatedAt: Date;
}
```

### Session
```typescript
{
  id: string;           // Primary key
  userId: string;       // FK to user
  token: string;        // Session token (unique)
  expiresAt: Date;
  ipAddress: string | null;
  userAgent: string | null;
  createdAt: Date;
  updatedAt: Date;
}
```

### ChatSession
```typescript
{
  id: string;           // Primary key
  userId: string;       // FK to user
  title: string | null; // Auto-generated from first message
  createdAt: Date;
  updatedAt: Date;
}
```

### ChatMessage
```typescript
{
  id: string;           // Primary key
  sessionId: string;    // FK to chatSession
  role: string;         // 'user' | 'assistant'
  content: string;      // Message text
  citations: string | null;  // JSON string of Citation[]
  createdAt: Date;
}
```

## Client-Side State Models

These are **not persisted to database** but used for UI state management.

### Theme Preference
```typescript
// Stored in localStorage
interface ThemePreference {
  theme: 'light' | 'dark' | 'system';
}

// Key: 'theme'
// Value: 'light' | 'dark' | 'system'
```

### Sidebar State
```typescript
// Stored in localStorage
interface SidebarState {
  collapsed: boolean;
}

// Key: 'chat-sidebar-collapsed'
// Value: 'true' | 'false'
```

### Instant Chat State
```typescript
// In-memory only (React state)
interface InstantChatState {
  isOpen: boolean;
  messages: Message[];
  isLoading: boolean;
}
```

### Grouped Conversations
```typescript
// Derived from ChatSession[] for UI display
interface GroupedConversations {
  today: ChatSession[];
  yesterday: ChatSession[];
  lastWeek: ChatSession[];
  older: ChatSession[];
}
```

## Entity Relationships

```
┌─────────────┐       ┌─────────────┐
│    User     │───┬───│   Session   │
└─────────────┘   │   └─────────────┘
                  │
                  │   ┌─────────────┐
                  └───│ ChatSession │
                      └──────┬──────┘
                             │
                      ┌──────┴──────┐
                      │ ChatMessage │
                      └─────────────┘
```

## Validation Rules

### Theme Preference
- Must be one of: 'light', 'dark', 'system'
- Default: 'system' (respects OS preference)

### Sidebar State
- Boolean value
- Default: false (expanded)

### Conversation Title
- Auto-generated: First 50 characters of first user message
- Truncated with ellipsis if longer
- Fallback: "New Conversation" if no messages

## State Transitions

### Chat Session Lifecycle
```
[Created] → [Active] → [Archived/Deleted]
     ↓
  Title generated from first message
```

### Theme State
```
[Initial Load]
     ↓
[Check localStorage]
     ↓
[Found?] → Yes → [Apply stored theme]
     ↓
   No
     ↓
[Check system preference]
     ↓
[Apply system theme]
```

### Instant Chat Modal State
```
[Closed] ←→ [Open]
            ↓
      [Auth check]
            ↓
    [Authenticated?]
     ↓           ↓
   Yes          No
     ↓           ↓
[Show Chat]  [Show Login Prompt]
```

## No Schema Migrations Required

This feature does not require database schema changes. All new state is either:
1. Client-side only (React state)
2. Browser storage (localStorage)
3. Using existing database tables

## API Data Contracts

See `/contracts/` directory for API endpoint specifications that use these models.
