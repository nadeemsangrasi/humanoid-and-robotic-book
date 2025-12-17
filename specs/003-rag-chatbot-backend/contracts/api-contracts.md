# API Contracts: RAG Textbook Chatbot Backend

**Feature Branch**: `001-rag-chatbot-backend`
**Date**: 2025-12-12
**Base URL**: `https://<space-name>.hf.space` (production) | `http://localhost:7860` (local)

---

## Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Ask a question about the textbook |
| `/health` | GET | Health check endpoint |

---

## POST /chat

Ask a question about the Physical AI & Humanoid Robotics textbook and receive an answer with source citations.

### Request

**Content-Type**: `application/json`

```json
{
  "query": "What is inverse kinematics?",
  "k": 5
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | - | Question to ask (1-2000 characters) |
| `k` | integer | No | 5 | Max results to retrieve (1-10) |

### Response (Success - 200 OK)

```json
{
  "answer": "Inverse kinematics (IK) is the mathematical process of calculating the joint angles needed to position an end-effector at a desired location. Unlike forward kinematics which computes end-effector position from joint angles, IK works backwards from the desired position to find the required joint configurations.",
  "citations": [
    {
      "url": "https://nadeemsangrasi.github.io/humanoid-and-robotic-book/docs/module-2-gazebo-unity/inverse-kinematics",
      "title": "Inverse Kinematics",
      "snippet": "Inverse kinematics (IK) is the mathematical process of calculating the joint angles...",
      "score": 0.92
    },
    {
      "url": "https://nadeemsangrasi.github.io/humanoid-and-robotic-book/docs/module-2-gazebo-unity/kinematics-overview",
      "title": "Kinematics Overview",
      "snippet": "Forward kinematics computes end-effector position from joint angles, while inverse kinematics...",
      "score": 0.85
    }
  ],
  "metadata": {
    "chunks_retrieved": 2,
    "processing_time_ms": 1250,
    "model": "gemini-2.0-flash"
  }
}
```

### Response (No Relevant Content - 200 OK)

When the question cannot be answered from textbook content:

```json
{
  "answer": "I couldn't find relevant information about this topic in the Physical AI & Humanoid Robotics textbook. This topic may not be covered in the available materials.",
  "citations": [],
  "metadata": {
    "chunks_retrieved": 0,
    "processing_time_ms": 850,
    "model": "gemini-2.0-flash"
  }
}
```

### Response (Validation Error - 400 Bad Request)

```json
{
  "error": "validation_error",
  "message": "Query cannot be empty or whitespace",
  "details": {
    "field": "query",
    "constraint": "min_length"
  }
}
```

### Response (Service Unavailable - 503)

```json
{
  "error": "service_unavailable",
  "message": "Vector database is temporarily unavailable. Please try again later.",
  "details": {
    "service": "qdrant",
    "retry_after": 30
  }
}
```

### Response (Rate Limited - 429)

```json
{
  "error": "rate_limited",
  "message": "API rate limit exceeded. Please try again later.",
  "details": {
    "service": "gemini",
    "retry_after": 60
  }
}
```

### cURL Example

```bash
curl -X POST "http://localhost:7860/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is inverse kinematics?", "k": 5}'
```

### Python Example

```python
import httpx

async def ask_question(query: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:7860/chat",
            json={"query": query, "k": 5}
        )
        response.raise_for_status()
        return response.json()
```

---

## GET /health

Health check endpoint for monitoring and orchestration.

### Request

No request body required.

### Response (Healthy - 200 OK)

```json
{
  "status": "healthy",
  "timestamp": "2025-12-12T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "qdrant": {
      "status": "healthy",
      "latency_ms": 45
    },
    "gemini": {
      "status": "healthy",
      "latency_ms": null
    }
  }
}
```

### Response (Unhealthy - 503)

```json
{
  "status": "unhealthy",
  "timestamp": "2025-12-12T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "qdrant": {
      "status": "unhealthy",
      "latency_ms": null
    },
    "gemini": {
      "status": "unknown",
      "latency_ms": null
    }
  }
}
```

### cURL Example

```bash
curl "http://localhost:7860/health"
```

---

## Error Response Format

All error responses follow this standard format:

```json
{
  "error": "<error_type>",
  "message": "<human_readable_message>",
  "details": {
    // Optional additional context
  }
}
```

### Error Types

| Error Type | HTTP Status | Description |
|------------|-------------|-------------|
| `validation_error` | 400 | Invalid request parameters |
| `service_unavailable` | 503 | External service (Qdrant/Gemini) unavailable |
| `rate_limited` | 429 | API rate limit exceeded |
| `internal_error` | 500 | Unexpected server error |

---

## Rate Limits

The API does not implement rate limiting at the application level. Rate limits are determined by:

1. **Gemini API**: ~1500 requests/minute (free tier)
2. **Qdrant Cloud**: No explicit rate limit on free tier

When external service rate limits are hit, the API returns a 429 response with fail-fast behavior (no retries).

---

## CORS Configuration

For local development and cross-origin requests:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## OpenAPI Specification

The full OpenAPI spec is available at `/docs` (Swagger UI) and `/openapi.json` when running the server.

```yaml
openapi: 3.1.0
info:
  title: Physical AI Textbook Chatbot API
  version: 1.0.0
  description: RAG-powered Q&A API for the Physical AI & Humanoid Robotics textbook

servers:
  - url: http://localhost:7860
    description: Local development
  - url: https://{space}.hf.space
    description: Hugging Face Spaces production

paths:
  /chat:
    post:
      summary: Ask a question
      operationId: chat
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ChatRequest'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ChatResponse'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '429':
          description: Rate limited
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '503':
          description: Service unavailable
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

  /health:
    get:
      summary: Health check
      operationId: health
      responses:
        '200':
          description: Service healthy
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthStatus'
        '503':
          description: Service unhealthy
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthStatus'

components:
  schemas:
    ChatRequest:
      type: object
      required:
        - query
      properties:
        query:
          type: string
          minLength: 1
          maxLength: 2000
        k:
          type: integer
          minimum: 1
          maximum: 10
          default: 5

    ChatResponse:
      type: object
      required:
        - answer
        - citations
        - metadata
      properties:
        answer:
          type: string
        citations:
          type: array
          items:
            $ref: '#/components/schemas/Citation'
        metadata:
          $ref: '#/components/schemas/ResponseMetadata'

    Citation:
      type: object
      required:
        - url
        - title
        - snippet
        - score
      properties:
        url:
          type: string
          format: uri
        title:
          type: string
        snippet:
          type: string
          maxLength: 200
        score:
          type: number
          minimum: 0
          maximum: 1

    ResponseMetadata:
      type: object
      required:
        - chunks_retrieved
        - processing_time_ms
        - model
      properties:
        chunks_retrieved:
          type: integer
        processing_time_ms:
          type: integer
        model:
          type: string

    HealthStatus:
      type: object
      required:
        - status
        - timestamp
        - version
        - services
      properties:
        status:
          type: string
          enum: [healthy, unhealthy]
        timestamp:
          type: string
          format: date-time
        version:
          type: string
        services:
          type: object
          additionalProperties:
            $ref: '#/components/schemas/ServiceStatus'

    ServiceStatus:
      type: object
      required:
        - status
      properties:
        status:
          type: string
          enum: [healthy, unhealthy, unknown]
        latency_ms:
          type: integer
          nullable: true

    ErrorResponse:
      type: object
      required:
        - error
        - message
      properties:
        error:
          type: string
        message:
          type: string
        details:
          type: object
          nullable: true
```
