# Data Model: Frontend Bug Fixes & Enhancements

**Feature**: 005-frontend-bugfixes-enhancements
**Date**: 2025-12-17
**Status**: Complete

## Overview

This feature is primarily frontend bug fixes and UI enhancements. No new database tables or entities are required. The existing data model supports all required functionality.

## Existing Entities (No Changes Required)

### User (existing)
Already supports authentication and session management via Better Auth.

### ChatSession (existing)
Already supports conversation history with the following fields:
- `id`: Primary key
- `userId`: Foreign key to user
- `title`: Conversation title
- `createdAt`: Timestamp
- `updatedAt`: Timestamp

### ChatMessage (existing)
Already supports message persistence:
- `id`: Primary key
- `sessionId`: Foreign key to chat session
- `role`: "user" | "assistant"
- `content`: Message text
- `citations`: JSON array of citation objects
- `createdAt`: Timestamp

## Frontend State Changes

### Theme State
**Location**: `localStorage` + CSS class on `<html>`
**Key**: `theme`
**Values**: `"light"` | `"dark"` | `"system"`

No database persistence needed - localStorage is sufficient for user preference.

### Instant Chat Sessions
**Change Required**: Instant chat modal will now create sessions in the existing `ChatSession` table.

Currently, instant chat does not persist. After this feature:
- Each instant chat conversation creates a new `ChatSession`
- Messages are saved to `ChatMessage` table
- Sessions appear in conversation history sidebar

## URL Parameters

### Book Page Theme Parameter
**Parameter**: `?theme=light` or `?theme=dark`
**Applied to**: Book iframe URL
**Purpose**: Pass frontend theme preference to Docusaurus book

Example:
```
BOOK_URL?theme=dark
```

## Schema Compatibility

All existing schemas remain unchanged:
- `drizzle/schema.ts` - No modifications needed
- `user`, `session`, `account`, `verification` tables - No changes
- `chatSession`, `chatMessage` tables - No changes (already support the required functionality)

## Migration Requirements

**None** - No database migrations required for this feature.
