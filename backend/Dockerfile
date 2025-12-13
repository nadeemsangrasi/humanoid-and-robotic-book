# =============================================================================
# RAG Textbook Chatbot Backend - Multi-Stage Production Dockerfile
# =============================================================================
# Target: Hugging Face Spaces (Docker mode, port 7860)
# Base: Python 3.11-slim
# Application: FastAPI + Uvicorn + OpenAI Agent SDK + Qdrant
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder
# -----------------------------------------------------------------------------
# Builds Python wheels for all dependencies to minimize runtime image size
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies required for compiling Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Runtime
# -----------------------------------------------------------------------------
# Minimal production image with only runtime dependencies
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install runtime dependencies only
# - curl: Required for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy pre-built wheels from builder stage and install
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

# Copy application code
COPY app/ ./app/
COPY scripts/ ./scripts/

# Create non-root user for security
# HF Spaces requirement: user must have UID 1000
RUN useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

# -----------------------------------------------------------------------------
# Port Configuration (T030)
# -----------------------------------------------------------------------------
# Hugging Face Spaces REQUIRES port 7860
EXPOSE 7860

# -----------------------------------------------------------------------------
# Health Check
# -----------------------------------------------------------------------------
# Ensures the container is healthy before receiving traffic
# - interval: Check every 30 seconds
# - timeout: Allow 10 seconds for response
# - start-period: Wait 60 seconds for app startup before checking
# - retries: Mark unhealthy after 3 consecutive failures
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# -----------------------------------------------------------------------------
# Runtime Command (T030)
# -----------------------------------------------------------------------------
# Start uvicorn with:
# - Host 0.0.0.0: Accept connections from all interfaces
# - Port 7860: HF Spaces requirement
# - Workers: Single worker for free tier resource constraints
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
