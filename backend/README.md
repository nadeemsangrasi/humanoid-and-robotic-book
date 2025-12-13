---
title: Physical AI Textbook Chatbot
emoji: "R"
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Physical AI & Humanoid Robotics Textbook Chatbot

RAG-powered Q&A API for the Physical AI & Humanoid Robotics textbook.

## Overview

This backend provides a conversational interface to query the Physical AI & Humanoid Robotics textbook using Retrieval-Augmented Generation (RAG). Questions are answered based on the textbook content with source citations.

## Architecture

- **Framework**: FastAPI + Uvicorn
- **LLM**: Google Gemini (gemini-2.0-flash) via OpenAI Agent SDK
- **Embeddings**: Google text-embedding-004 via LangChain
- **Vector DB**: Qdrant Cloud (free tier)
- **Deployment**: Hugging Face Spaces (Docker mode)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and documentation links |
| `/health` | GET | Health check endpoint |
| `/api/v1/chat` | POST | Ask a question about the textbook |
| `/docs` | GET | Swagger UI documentation |
| `/redoc` | GET | ReDoc documentation |

## Usage

### Chat Endpoint

Ask a question about the textbook:

```bash
curl -X POST "https://YOUR-SPACE.hf.space/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS2?"}'
```

**Request Body:**
```json
{
  "query": "What is ROS2?"
}
```

**Response:**
```json
{
  "answer": "ROS2 (Robot Operating System 2) is...",
  "citations": [
    {
      "url": "https://humanoid-book.example.com/chapter-5#ros2-overview",
      "title": "ROS2 Overview",
      "snippet": "ROS2 is the next generation of..."
    }
  ],
  "metadata": {
    "model": "gemini-2.0-flash",
    "latency_ms": 1234,
    "chunks_retrieved": 5
  }
}
```

### Health Check

Verify the service is running:

```bash
curl "https://YOUR-SPACE.hf.space/health"
```

## Environment Variables

The application uses environment variables for configuration. All variables are validated on startup with clear error messages if validation fails.

### Required Variables

These must be set for the application to start:

| Variable | Default | Description | How to Obtain |
|----------|---------|-------------|---------------|
| `GOOGLE_API_KEY` | - | Google AI API key for Gemini models (embedding and LLM inference) | [Google AI Studio](https://aistudio.google.com/app/apikey) - Create a new API key |
| `QDRANT_URL` | - | Qdrant Cloud cluster URL (e.g., `https://xxx.aws.cloud.qdrant.io`) | [Qdrant Cloud](https://cloud.qdrant.io/) - Create a free cluster, copy the cluster URL |
| `QDRANT_API_KEY` | - | Qdrant Cloud API key for authentication | [Qdrant Cloud](https://cloud.qdrant.io/) - Navigate to API Keys section, create a new key |

### Optional Variables

These have sensible defaults but can be customized:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Application logging level. Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `COLLECTION_NAME` | `book_chunks` | Name of the Qdrant collection storing book chunk embeddings |
| `EMBEDDING_MODEL` | `models/text-embedding-004` | Google embedding model for vector similarity search |
| `LLM_MODEL` | `gemini-2.0-flash` | Google Gemini LLM model for chat responses |
| `SCORE_THRESHOLD` | `0.7` | Minimum similarity score threshold for retrieved chunks (0.0 to 1.0) |
| `HOST` | `0.0.0.0` | Host address for the FastAPI server |
| `PORT` | `7860` | Port for the FastAPI server (7860 required for Hugging Face Spaces) |

### Validation Rules

The application validates environment variables on startup:

- **Required variables**: Must be set and non-empty
- **API keys**: Must not contain placeholder values (e.g., `your_api_key`, `xxx`, `placeholder`)
- **QDRANT_URL**: Must be a valid URL starting with `https://` or `http://`
- **SCORE_THRESHOLD**: Must be a float between 0.0 and 1.0
- **PORT**: Must be a valid port number between 1 and 65535
- **LOG_LEVEL**: Must be one of the valid logging levels

If validation fails, the application will exit with a clear error message indicating which variable failed and why.

### Setting Secrets on Hugging Face Spaces

1. Go to your Space Settings
2. Navigate to "Repository secrets"
3. Add each required variable:
   - `GOOGLE_API_KEY`: Your Google AI API key
   - `QDRANT_URL`: Your Qdrant Cloud cluster URL (full URL including https://)
   - `QDRANT_API_KEY`: Your Qdrant Cloud API key

### Local Development Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your actual values:
   ```bash
   # Required - Get from https://aistudio.google.com/app/apikey
   GOOGLE_API_KEY=your_actual_google_api_key

   # Required - Get from https://cloud.qdrant.io/
   QDRANT_URL=https://your-cluster-id.aws.cloud.qdrant.io
   QDRANT_API_KEY=your_actual_qdrant_api_key

   # Optional - Customize as needed
   LOG_LEVEL=DEBUG
   ```

3. The application will automatically load from `.env` on startup

## Local Development

### Prerequisites

- Docker installed
- `.env` file with required variables (copy from `.env.example`)

### Build and Run

```bash
# Build the Docker image
./scripts/build.sh

# Run the container
./scripts/run.sh

# Access the API
curl http://localhost:7860/health
```

### Development without Docker

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the server
uvicorn app.main:app --reload --port 7860
```

## Deployment to Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/new-space)
2. Select "Docker" as the SDK
3. Push this repository to the Space
4. Configure environment secrets in Space settings
5. The Space will automatically build and deploy

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment configuration
│   ├── routers/
│   │   ├── chat.py          # Chat endpoint
│   │   └── health.py        # Health endpoint (future)
│   ├── schemas/
│   │   ├── chat.py          # Request/response models
│   │   └── health.py        # Health models
│   ├── services/
│   │   ├── agent/           # OpenAI Agent SDK + Gemini
│   │   ├── embedding/       # Gemini embeddings
│   │   └── retrieval/       # Qdrant vector search
│   └── utils/
│       └── logging.py       # Structured logging
├── scripts/
│   ├── ingest-book.py       # Book ingestion script
│   ├── build.sh             # Docker build script
│   └── run.sh               # Docker run script
├── tests/                   # Test suite
├── Dockerfile               # Multi-stage production build
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── .env.example             # Environment template
└── README.md                # This file
```

## License

This project is part of the Physical AI & Humanoid Robotics textbook.
