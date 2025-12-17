# API Contracts: Frontend Bug Fixes & Enhancements

**Feature**: 005-frontend-bugfixes-enhancements
**Date**: 2025-12-17
**Status**: Complete

## Overview

This feature primarily involves frontend bug fixes and UI enhancements. No new API endpoints are required. The feature leverages existing API contracts.

## Existing APIs Used

### Chat History API (No Changes)

#### Create Chat Session
```
POST /api/chat/sessions
Authorization: Better Auth Session Cookie

Request Body:
{
  "title": string (optional, auto-generated if not provided)
}

Response (201):
{
  "id": string,
  "userId": string,
  "title": string,
  "createdAt": string (ISO 8601),
  "updatedAt": string (ISO 8601)
}
```

#### Add Message to Session
```
POST /api/chat/sessions/{sessionId}/messages
Authorization: Better Auth Session Cookie

Request Body:
{
  "role": "user" | "assistant",
  "content": string,
  "citations": [
    {
      "title": string,
      "url": string,
      "excerpt": string (optional),
      "score": number (optional)
    }
  ] (optional)
}

Response (201):
{
  "id": string,
  "sessionId": string,
  "role": string,
  "content": string,
  "citations": array,
  "createdAt": string (ISO 8601)
}
```

#### Get User Sessions
```
GET /api/chat/sessions
Authorization: Better Auth Session Cookie

Response (200):
{
  "sessions": [
    {
      "id": string,
      "title": string,
      "createdAt": string,
      "updatedAt": string,
      "messageCount": number
    }
  ]
}
```

#### Get Session with Messages
```
GET /api/chat/sessions/{sessionId}
Authorization: Better Auth Session Cookie

Response (200):
{
  "id": string,
  "title": string,
  "createdAt": string,
  "updatedAt": string,
  "messages": [
    {
      "id": string,
      "role": string,
      "content": string,
      "citations": array,
      "createdAt": string
    }
  ]
}
```

## Frontend-Only Contracts

### Theme URL Parameter Contract
**Consumer**: Book page (`/book`)
**Provider**: Docusaurus book site

```
URL Format: {BOOK_URL}?theme={mode}

Parameters:
  - theme: "light" | "dark"

Expected Behavior:
  - Docusaurus book reads `theme` query parameter
  - Applies corresponding theme (light/dark mode)
  - Falls back to default theme if parameter missing
```

### Theme State Contract
**Storage**: localStorage
**Key**: `theme`

```
Stored Value: "light" | "dark" | "system"

Behavior:
  - "light": Force light theme
  - "dark": Force dark theme
  - "system": Follow OS preference

Application:
  - CSS class added to <html> element: "light" or "dark"
  - All components use CSS custom properties
```

### CSS Custom Properties Contract
**Provider**: `globals.css`
**Consumer**: All components

```css
/* Light theme (default) */
:root {
  --background: #ffffff;
  --foreground: #171717;
  --primary: #667eea;
  --hover-bg: rgba(0, 0, 0, 0.05);
  /* ... additional variables */
}

/* Dark theme */
.dark {
  --background: #0a0a0a;
  --foreground: #ededed;
  --primary: #818cf8;
  --hover-bg: rgba(255, 255, 255, 0.05);
  /* ... additional variables */
}
```

## Error Handling

### Chat Session Creation Failure
```
Response (401): Unauthorized
{
  "error": "Authentication required"
}

Response (500): Server Error
{
  "error": "Failed to create session"
}
```

### Message Save Failure
```
Response (404): Session Not Found
{
  "error": "Session not found"
}

Response (500): Server Error
{
  "error": "Failed to save message"
}
```

## Integration Notes

1. **Instant Chat Modal**: Will use the same Chat History API as the main chat page
2. **Theme Sync**: Frontend-only, no API calls needed
3. **Bug Fixes**: All fixes are frontend-only, no API changes required
