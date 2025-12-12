# Claude Skills for Physical AI & Humanoid Robotics Project (MVP)

## Overview
This directory contains **15 essential Claude Skills** for the MVP development of the Physical AI & Humanoid Robotics textbook with RAG chatbot and authentication.

## Architecture: 5 Agents × 3 Skills Each

| Agent | Skills | Purpose |
|-------|--------|---------|
| Backend Architect | 3 | FastAPI + Agent SDK + RAG endpoint |
| RAG Pipeline | 3 | Ingestion + Embedding + Retrieval |
| Deployment | 3 | Docker + HF Spaces + Local dev |
| UI & ChatKit | 3 | Backend adapter + UI + Selection QA |
| Auth Integration | 3 | Better Auth + Drizzle + Frontend auth |

---

## Skills by Agent

### 1. Backend Architect Agent (3 skills)
| Skill | Purpose |
|-------|---------|
| `fastapi-scaffolding` | Generate FastAPI backend structure |
| `gemini-agent-sdk-setup` | Configure OpenAI Agent SDK with Gemini |
| `rag-chat-endpoint` | Implement RAG reasoning chat endpoint |

### 2. RAG Pipeline Agent (3 skills)
| Skill | Purpose |
|-------|---------|
| `book-ingestion` | Chunk and ingest textbook content |
| `embedding-pipeline` | Generate embeddings with Gemini |
| `qdrant-retrieval-tool` | Vector search and retrieval |

### 3. Deployment Agent (3 skills)
| Skill | Purpose |
|-------|---------|
| `dockerfile-builder` | Multi-stage production Dockerfile |
| `huggingface-config` | HF Spaces configuration |
| `local-dev-runner` | Local Docker development scripts |

### 4. UI & ChatKit Agent (3 skills)
| Skill | Purpose |
|-------|---------|
| `chatkit-backend-adapter` | Connect ChatKit to FastAPI backend |
| `ui-customization` | Theme and layout customization |
| `selection-qa` | Selection-based Q&A feature |

### 5. Auth Integration Agent (3 skills)
| Skill | Purpose |
|-------|---------|
| `better-auth-configuration` | Better Auth setup |
| `drizzle-schema-generation` | Database schemas with Drizzle |
| `frontend-auth-integration` | Auth UI integration |

---

## Technology Stack Alignment

| Requirement | Covered By |
|-------------|-----------|
| FastAPI + Uvicorn | `fastapi-scaffolding` |
| OpenAI Agent SDK + Gemini | `gemini-agent-sdk-setup` |
| Qdrant Vector DB | `qdrant-retrieval-tool` |
| Google Embeddings | `embedding-pipeline` |
| Docker + HF Spaces | `dockerfile-builder`, `huggingface-config` |
| OpenAI ChatKit UI | `chatkit-backend-adapter`, `ui-customization` |
| Better Auth | `better-auth-configuration` |
| Drizzle ORM | `drizzle-schema-generation` |
| PostgreSQL Neon DB | `drizzle-schema-generation` |

---

## Usage
Each skill directory contains a `SKILL.md` file with:
- YAML frontmatter (name, description)
- Step-by-step instructions
- Concrete examples

Skills are automatically discovered by Claude when working on related tasks.
