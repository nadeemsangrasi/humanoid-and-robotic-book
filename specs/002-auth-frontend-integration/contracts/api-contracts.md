# API Contracts: Authentication & Frontend-Backend Integration

**Feature Branch**: `002-auth-frontend-integration`
**Date**: 2025-12-14
**Base URL**: `/api`

---

## Table of Contents

1. [Authentication Endpoints (Better Auth)](#1-authentication-endpoints-better-auth)
2. [Chat Proxy Endpoint](#2-chat-proxy-endpoint)
3. [Chat History Endpoints](#3-chat-history-endpoints)
4. [Error Responses](#4-error-responses)

---

## 1. Authentication Endpoints (Better Auth)

Better Auth handles all authentication endpoints automatically via the catch-all route at `/api/auth/[...all]`.

### 1.1 Sign Up

**Endpoint**: `POST /api/auth/sign-up/email`

**Request Body**:
```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "string",
    "name": "string",
    "email": "string",
    "emailVerified": false,
    "image": null,
    "createdAt": "2025-12-14T00:00:00.000Z",
    "updatedAt": "2025-12-14T00:00:00.000Z"
  },
  "session": {
    "id": "string",
    "userId": "string",
    "token": "string",
    "expiresAt": "2025-12-21T00:00:00.000Z"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid email format or password requirements not met
- `409 Conflict`: Email already registered

---

### 1.2 Sign In

**Endpoint**: `POST /api/auth/sign-in/email`

**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "string",
    "name": "string",
    "email": "string",
    "emailVerified": false,
    "image": null
  },
  "session": {
    "id": "string",
    "userId": "string",
    "token": "string",
    "expiresAt": "2025-12-21T00:00:00.000Z"
  }
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid credentials
- `429 Too Many Requests`: Rate limit exceeded (5 attempts per 15 minutes)

**Cookies Set**:
- `better-auth.session_token`: httpOnly, Secure, SameSite=Lax

---

### 1.3 Sign Out

**Endpoint**: `POST /api/auth/sign-out`

**Headers**:
```
Cookie: better-auth.session_token=<token>
```

**Response** (200 OK):
```json
{
  "success": true
}
```

**Cookies Cleared**:
- `better-auth.session_token`

---

### 1.4 Get Session

**Endpoint**: `GET /api/auth/get-session`

**Headers**:
```
Cookie: better-auth.session_token=<token>
```

**Response** (200 OK - Authenticated):
```json
{
  "user": {
    "id": "string",
    "name": "string",
    "email": "string",
    "emailVerified": false,
    "image": null
  },
  "session": {
    "id": "string",
    "userId": "string",
    "expiresAt": "2025-12-21T00:00:00.000Z",
    "ipAddress": "string",
    "userAgent": "string"
  }
}
```

**Response** (200 OK - Not Authenticated):
```json
null
```

---

### 1.5 OAuth Sign In (P3 - Optional)

**Endpoint**: `GET /api/auth/sign-in/social`

**Query Parameters**:
- `provider`: `google` | `github`
- `callbackURL`: Redirect URL after OAuth

**Response**: Redirect to OAuth provider

---

## 2. Chat Proxy Endpoint

### 2.1 Send Chat Message

**Endpoint**: `POST /api/chat`

**Description**: Proxies chat messages to the FastAPI backend, adding authentication context.

**Headers**:
```
Cookie: better-auth.session_token=<token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "string",
  "sessionId": "string | null",
  "context": {
    "previousMessages": [
      {
        "role": "user" | "assistant",
        "content": "string"
      }
    ]
  }
}
```

**Response** (200 OK):
```json
{
  "response": "string",
  "citations": [
    {
      "title": "string",
      "url": "string",
      "excerpt": "string",
      "score": 0.95
    }
  ],
  "sessionId": "string"
}
```

**Error Responses**:
- `401 Unauthorized`: Not authenticated
- `502 Bad Gateway`: Backend unavailable
- `504 Gateway Timeout`: Backend timeout

**Internal Flow**:
1. Validate session from cookie
2. Extract user ID from session
3. Transform request to FastAPI format
4. Add `Authorization: Bearer <jwt>` header
5. Forward to `${NEXT_PUBLIC_BACKEND_URL}/api/v1/chat`
6. Transform response to frontend format
7. Save message to chat history (if sessionId provided)

---

## 3. Chat History Endpoints

### 3.1 List Conversations

**Endpoint**: `GET /api/chat/history`

**Headers**:
```
Cookie: better-auth.session_token=<token>
```

**Query Parameters**:
- `limit`: number (default: 20, max: 100)
- `offset`: number (default: 0)

**Response** (200 OK):
```json
{
  "conversations": [
    {
      "id": "string",
      "title": "string",
      "createdAt": "2025-12-14T00:00:00.000Z",
      "updatedAt": "2025-12-14T00:00:00.000Z",
      "messageCount": 10
    }
  ],
  "total": 50,
  "limit": 20,
  "offset": 0
}
```

**Error Responses**:
- `401 Unauthorized`: Not authenticated

---

### 3.2 Get Conversation

**Endpoint**: `GET /api/chat/history/:sessionId`

**Headers**:
```
Cookie: better-auth.session_token=<token>
```

**Response** (200 OK):
```json
{
  "id": "string",
  "title": "string",
  "createdAt": "2025-12-14T00:00:00.000Z",
  "updatedAt": "2025-12-14T00:00:00.000Z",
  "messages": [
    {
      "id": "string",
      "role": "user",
      "content": "string",
      "citations": null,
      "createdAt": "2025-12-14T00:00:00.000Z"
    },
    {
      "id": "string",
      "role": "assistant",
      "content": "string",
      "citations": [
        {
          "title": "string",
          "url": "string",
          "excerpt": "string"
        }
      ],
      "createdAt": "2025-12-14T00:00:01.000Z"
    }
  ]
}
```

**Error Responses**:
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Conversation not found or doesn't belong to user

---

### 3.3 Create New Conversation

**Endpoint**: `POST /api/chat/history`

**Headers**:
```
Cookie: better-auth.session_token=<token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "string | null"
}
```

**Response** (201 Created):
```json
{
  "id": "string",
  "title": null,
  "createdAt": "2025-12-14T00:00:00.000Z",
  "updatedAt": "2025-12-14T00:00:00.000Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Not authenticated

---

### 3.4 Delete Conversation

**Endpoint**: `DELETE /api/chat/history/:sessionId`

**Headers**:
```
Cookie: better-auth.session_token=<token>
```

**Response** (204 No Content)

**Error Responses**:
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Conversation not found or doesn't belong to user

---

### 3.5 Delete All Conversations

**Endpoint**: `DELETE /api/chat/history`

**Headers**:
```
Cookie: better-auth.session_token=<token>
```

**Response** (204 No Content):

**Error Responses**:
- `401 Unauthorized`: Not authenticated

---

## 4. Error Responses

### Standard Error Format

All error responses follow this structure:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

### Error Codes

| HTTP Status | Code | Description |
|-------------|------|-------------|
| 400 | `BAD_REQUEST` | Invalid request body or parameters |
| 401 | `UNAUTHORIZED` | Missing or invalid authentication |
| 403 | `FORBIDDEN` | Access denied to resource |
| 404 | `NOT_FOUND` | Resource not found |
| 409 | `CONFLICT` | Resource conflict (e.g., email exists) |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error |
| 502 | `BAD_GATEWAY` | Backend service unavailable |
| 504 | `GATEWAY_TIMEOUT` | Backend service timeout |

---

## Backend API Contract (FastAPI)

The frontend proxies to the existing FastAPI backend. Here's the expected backend contract:

### POST /api/v1/chat

**Request**:
```json
{
  "query": "string",
  "user_id": "string",
  "conversation_history": [
    {
      "role": "user" | "assistant",
      "content": "string"
    }
  ]
}
```

**Response**:
```json
{
  "response": "string",
  "sources": [
    {
      "title": "string",
      "url": "string",
      "content": "string",
      "score": 0.95
    }
  ]
}
```

### GET /health

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-14T00:00:00.000Z"
}
```

---

## Request/Response Transformation

### Frontend → Backend

```typescript
// Frontend format (ChatKit)
{
  message: "What is ROS2?",
  sessionId: "abc123",
  context: {
    previousMessages: [...]
  }
}

// Transformed to Backend format (FastAPI)
{
  query: "What is ROS2?",
  user_id: "user_xyz",  // From session
  conversation_history: [...]
}
```

### Backend → Frontend

```typescript
// Backend format (FastAPI)
{
  response: "ROS2 is...",
  sources: [
    { title: "...", url: "...", content: "...", score: 0.95 }
  ]
}

// Transformed to Frontend format (ChatKit)
{
  response: "ROS2 is...",
  citations: [
    { title: "...", url: "...", excerpt: "...", score: 0.95 }
  ],
  sessionId: "abc123"
}
```
