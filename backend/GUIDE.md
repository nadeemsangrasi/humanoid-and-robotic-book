# RAG Textbook Chatbot Backend - Developer Guide

Complete guide for running the Physical AI & Humanoid Robotics Textbook Chatbot backend.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Environment Setup](#environment-setup)
- [Running Locally](#running-locally)
- [Content Ingestion](#content-ingestion)
- [Testing](#testing)
- [Deployment](#deployment)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Runtime |
| Docker | 20.10+ | Containerization |
| Docker Compose | 2.0+ | Local orchestration |

### Required Accounts (Free Tier)

1. **Google AI Studio** - For Gemini API
   - Sign up: https://aistudio.google.com/
   - Get API key: https://aistudio.google.com/apikey

2. **Qdrant Cloud** - For vector database
   - Sign up: https://cloud.qdrant.io/
   - Create a free cluster
   - Get cluster URL and API key from dashboard

---

## Quick Start

```bash
# 1. Navigate to backend directory
cd backend

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env with your API keys (see Environment Setup)

# 4. Run with Docker
docker compose up --build

# 5. Verify it's running
curl http://localhost:7860/health
```

---

## Environment Setup

### Step 1: Create .env File

```bash
cp .env.example .env
```

### Step 2: Configure Required Variables

Edit `.env` with your credentials:

```env
# Required - Google AI API Key
# Get from: https://aistudio.google.com/apikey
GOOGLE_API_KEY=your_google_api_key_here

# Required - Qdrant Cloud Configuration
# Get from: https://cloud.qdrant.io/ (create free cluster)
QDRANT_URL=https://your-cluster-id.us-east4-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
```

### Step 3: Optional Configuration

```env
# Logging (DEBUG for development, INFO for production)
LOG_LEVEL=INFO

# Vector database collection name
COLLECTION_NAME=book_chunks

# Embedding model (768 dimensions)
EMBEDDING_MODEL=models/text-embedding-004

# LLM model for chat
LLM_MODEL=gemini-2.0-flash

# Similarity threshold for search (0.0-1.0)
SCORE_THRESHOLD=0.7

# Server configuration
HOST=0.0.0.0
PORT=7860
```

---

## Running Locally

### Option 1: Docker Compose (Recommended)

```bash
# Start the service
docker compose up

# Start in detached mode
docker compose up -d

# Rebuild and start
docker compose up --build

# View logs
docker compose logs -f

# Stop
docker compose down
```

### Option 2: Native Python

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server with hot reload
./scripts/dev.sh
# Or directly:
uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload
```

### Option 3: Using Scripts

```bash
# Build Docker image
./scripts/build.sh

# Run container
./scripts/run.sh

# Stop container
./scripts/stop.sh

# Clean up
./scripts/clean.sh
```

### Verify Running

```bash
# Health check
curl http://localhost:7860/health

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2025-12-13T10:30:00Z",
#   "version": "1.0.0",
#   "services": {
#     "qdrant": {"status": "healthy", "latency_ms": 45},
#     "gemini": {"status": "healthy", "latency_ms": null}
#   }
# }
```

---

## Content Ingestion

Before the chatbot can answer questions, you need to ingest the textbook content into Qdrant.

### Run Ingestion Script

```bash
# With Docker
docker compose exec backend python scripts/ingest_book.py

# Or natively (with venv activated)
python scripts/ingest_book.py
```

### Expected Output

```
============================================================
Physical AI & Humanoid Robotics Textbook Ingestion
============================================================

Fetching sitemap from: https://nadeemsangrasi.github.io/humanoid-and-robotic-book/sitemap.xml
Found 23 pages in sitemap
Processing page 1/23: https://nadeemsangrasi.github.io/...
  - Created 12 chunks
Processing page 2/23: ...
...

============================================================
Ingestion Complete!
============================================================
  Pages processed:  23
  Chunks created:   387
  Chunks upserted:  387
  Duration:         45.2 seconds
```

### Verify Ingestion

```bash
# Ask a test question
curl -X POST "http://localhost:7860/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS2?"}'
```

---

## Testing

### Run All Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_chat.py -v
```

### Test Files

| File | Description |
|------|-------------|
| `tests/conftest.py` | Shared fixtures and mocks |
| `tests/test_health.py` | Health endpoint tests |
| `tests/test_chat.py` | Chat endpoint tests |
| `tests/test_ingestion.py` | Ingestion script tests |

---

## Deployment

### Deploy to Hugging Face Spaces

1. **Create a new Space**
   - Go to https://huggingface.co/new-space
   - Choose **Docker** as the SDK
   - Set visibility (public/private)

2. **Configure Secrets**

   In Space Settings → Repository secrets, add:
   - `GOOGLE_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`

3. **Push Code**

   ```bash
   # Add HF remote
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

   # Push backend directory
   cd backend
   git subtree push --prefix=backend hf main
   ```

4. **Verify Deployment**

   Wait 2-3 minutes for build, then:
   ```bash
   curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/health
   ```

5. **Run Ingestion on Production**

   Use the HF Spaces terminal or run locally pointing to production Qdrant.

---

## API Reference

### POST /api/v1/chat

Ask a question about the textbook.

**Request:**
```json
{
  "query": "What is inverse kinematics?",
  "k": 5
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | - | Question (1-2000 chars) |
| `k` | integer | No | 5 | Max results (1-10) |

**Response:**
```json
{
  "answer": "Inverse kinematics (IK) is the mathematical process...",
  "citations": [
    {
      "url": "https://...",
      "title": "Inverse Kinematics",
      "snippet": "IK computes joint angles from...",
      "score": 0.92
    }
  ],
  "metadata": {
    "chunks_retrieved": 3,
    "processing_time_ms": 1250,
    "model": "gemini-2.0-flash"
  }
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-13T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "qdrant": {"status": "healthy", "latency_ms": 45},
    "gemini": {"status": "healthy", "latency_ms": null}
  }
}
```

### Interactive Documentation

- **Swagger UI**: http://localhost:7860/docs
- **ReDoc**: http://localhost:7860/redoc
- **OpenAPI JSON**: http://localhost:7860/openapi.json

---

## Troubleshooting

### Connection Refused on localhost:7860

```bash
# Check if container is running
docker compose ps

# Check container logs
docker compose logs -f

# Restart the service
docker compose restart
```

### "No content found" in Responses

The textbook hasn't been ingested yet.

```bash
# Run ingestion
python scripts/ingest_book.py

# Verify Qdrant has data
# Check collection in Qdrant Cloud dashboard
```

### Rate Limit Exceeded

Gemini API has rate limits on the free tier.

```bash
# Wait 60 seconds and retry
# Check quota at https://aistudio.google.com/
```

### Health Check Shows "unhealthy"

```bash
# Check environment variables
cat .env

# Verify Qdrant connection
curl $QDRANT_URL/collections -H "api-key: $QDRANT_API_KEY"

# Enable debug logging
LOG_LEVEL=DEBUG docker compose up
```

### Import Errors When Running Natively

```bash
# Ensure you're in the backend directory
cd backend

# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Docker Build Fails

```bash
# Clean build cache
docker compose build --no-cache

# Remove old images
./scripts/clean.sh --all
```

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Package init with version
│   ├── config.py            # Environment configuration
│   ├── main.py              # FastAPI application
│   ├── routers/
│   │   ├── chat.py          # POST /api/v1/chat
│   │   └── health.py        # GET /health
│   ├── schemas/
│   │   ├── chat.py          # Request/response models
│   │   └── health.py        # Health check models
│   ├── services/
│   │   ├── agent/
│   │   │   ├── orchestrator.py  # Gemini agent
│   │   │   └── tools.py         # Search tool
│   │   ├── embedding/
│   │   │   └── embedding.py     # Gemini embeddings
│   │   └── retrieval/
│   │       └── qdrant_client.py # Vector search
│   └── utils/
│       └── logging.py       # Structured logging
├── scripts/
│   ├── ingest_book.py       # Content ingestion
│   ├── build.sh             # Docker build
│   ├── run.sh               # Docker run
│   ├── dev.sh               # Development server
│   ├── stop.sh              # Stop container
│   └── clean.sh             # Cleanup
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_chat.py
│   ├── test_health.py
│   └── test_ingestion.py
├── Dockerfile               # Production image
├── docker-compose.yml       # Local development
├── requirements.txt         # Production deps
├── requirements-dev.txt     # Dev deps
├── pyproject.toml           # Project config
├── .env.example             # Environment template
├── README.md                # HF Spaces metadata
└── GUIDE.md                 # This file
```

---

## Support

- **Issues**: https://github.com/nadeemsangrasi/humanoid-and-robotic-book/issues
- **Documentation**: See `specs/001-rag-chatbot-backend/` for detailed specifications
