# Quickstart: RAG Textbook Chatbot Backend

**Feature Branch**: `001-rag-chatbot-backend`
**Date**: 2025-12-12

---

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Google AI API key (free tier)
- Qdrant Cloud account (free tier)

---

## 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/nadeemsangrasi/humanoid-and-robotic-book.git
cd humanoid-and-robotic-book

# Checkout the feature branch
git checkout 001-rag-chatbot-backend

# Navigate to backend directory
cd backend
```

---

## 2. Environment Configuration

### Create `.env` file

```bash
cp .env.example .env
```

### Edit `.env` with your credentials

```env
# Google AI API (required)
GOOGLE_API_KEY=your_google_ai_api_key_here

# Qdrant Cloud (required)
QDRANT_URL=https://your-cluster-id.us-east4-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here

# Application settings (optional)
LOG_LEVEL=INFO
```

### Getting API Keys

#### Google AI API Key
1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key to `.env`

#### Qdrant Cloud
1. Go to https://cloud.qdrant.io/
2. Create a free cluster
3. Copy the cluster URL and API key to `.env`

---

## 3. Local Development (Docker)

### Build and run with Docker Compose

```bash
# Build the container
docker compose build

# Start the service
docker compose up

# Or run in background
docker compose up -d
```

### Verify the service is running

```bash
# Check health endpoint
curl http://localhost:7860/health

# Expected response:
# {"status":"healthy","timestamp":"...","version":"1.0.0","services":{...}}
```

---

## 4. Run Content Ingestion

Before asking questions, you need to ingest the textbook content.

### Run the ingestion script

```bash
# From the backend directory
python scripts/ingest-book.py

# Or with Docker
docker compose exec backend python scripts/ingest-book.py
```

### Expected output

```
Starting textbook ingestion...
Fetching sitemap from: https://nadeemsangrasi.github.io/humanoid-and-robotic-book/sitemap.xml
Found 23 pages to process
Processing: https://nadeemsangrasi.github.io/humanoid-and-robotic-book/
  - Created 12 chunks
Processing: https://nadeemsangrasi.github.io/humanoid-and-robotic-book/docs/module-1-ros2/
  - Created 18 chunks
...
Ingestion complete!
  Pages processed: 23
  Chunks created: 387
  Chunks upserted: 387
  Duration: 45.2 seconds
```

---

## 5. Test the API

### Ask a question

```bash
curl -X POST "http://localhost:7860/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS2?"}'
```

### Expected response

```json
{
  "answer": "ROS2 (Robot Operating System 2) is a flexible framework for writing robot software...",
  "citations": [
    {
      "url": "https://nadeemsangrasi.github.io/humanoid-and-robotic-book/docs/module-1-ros2/",
      "title": "Introduction to ROS2",
      "snippet": "ROS2 is the second generation of the Robot Operating System...",
      "score": 0.91
    }
  ],
  "metadata": {
    "chunks_retrieved": 3,
    "processing_time_ms": 1850,
    "model": "gemini-2.0-flash"
  }
}
```

---

## 6. Development Workflow

### Running tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_chat.py -v
```

### Code formatting

```bash
# Format code
ruff format app/ tests/

# Check linting
ruff check app/ tests/
```

### Hot reload (development)

```bash
# Run with auto-reload
uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload
```

---

## 7. Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Environment configuration
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py                # POST /chat endpoint
│   │   └── health.py              # GET /health endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py    # OpenAI Agent SDK + Gemini
│   │   │   └── tools.py           # Retrieval tool definitions
│   │   ├── embedding/
│   │   │   ├── __init__.py
│   │   │   └── embedding.py       # Gemini embeddings via LangChain
│   │   └── retrieval/
│   │       ├── __init__.py
│   │       └── qdrant_client.py   # Qdrant vector search
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chat.py                # ChatRequest, ChatResponse, Citation
│   │   └── health.py              # HealthStatus
│   └── utils/
│       ├── __init__.py
│       └── logging.py             # Logging configuration
├── scripts/
│   └── ingest-book.py             # Sitemap crawler + chunker + uploader
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── test_chat.py
│   ├── test_health.py
│   └── test_ingestion.py
├── Dockerfile                      # Multi-stage production build
├── docker-compose.yml              # Local development
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

---

## 8. Deployment to Hugging Face Spaces

### Create a new Space

1. Go to https://huggingface.co/new-space
2. Choose "Docker" SDK
3. Set visibility (public/private)
4. Create the Space

### Configure secrets

In Space Settings → Repository secrets:
- `GOOGLE_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`

### Push code

```bash
# Add HF remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Push to HF
git push hf 001-rag-chatbot-backend:main
```

### Verify deployment

Wait 2-3 minutes for the container to build, then:

```bash
curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/health
```

---

## 9. Troubleshooting

### Common Issues

#### "Connection refused" on localhost:7860
- Ensure Docker container is running: `docker compose ps`
- Check logs: `docker compose logs -f`

#### "No content found" in responses
- Run the ingestion script first
- Verify Qdrant has data: check collection in Qdrant Cloud dashboard

#### "Rate limit exceeded" errors
- Wait 60 seconds and retry
- Check Gemini API quota at https://aistudio.google.com/

#### Health check shows "unhealthy"
- Verify environment variables are set correctly
- Check Qdrant Cloud cluster is running
- Test API keys individually

### Debug mode

```bash
# Enable debug logging
LOG_LEVEL=DEBUG docker compose up
```

---

## 10. API Documentation

Once running, interactive API docs are available at:
- **Swagger UI**: http://localhost:7860/docs
- **ReDoc**: http://localhost:7860/redoc
- **OpenAPI JSON**: http://localhost:7860/openapi.json
