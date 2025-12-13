#!/bin/bash
# =============================================================================
# RAG Textbook Chatbot Backend - Development Server Script
# =============================================================================
# Usage: ./scripts/dev.sh [--port PORT]
#
# Options:
#   --port, -p PORT    Port to run on (default: 7860)
#
# This script runs the FastAPI application in development mode with hot reload.
# Changes to Python files will automatically trigger a server restart.
#
# Prerequisites:
#   - Python virtual environment activated (or dependencies installed globally)
#   - .env file configured with API keys
# =============================================================================

set -e  # Exit on any error

# Configuration
DEFAULT_PORT=7860
PORT=$DEFAULT_PORT
HOST="0.0.0.0"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --port|-p)
            PORT="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [--port PORT]"
            echo ""
            echo "Options:"
            echo "  --port, -p PORT    Port to run on (default: 7860)"
            echo "  --help, -h         Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Change to backend directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
cd "$BACKEND_DIR"

# Check if .env file exists
if [[ ! -f ".env" ]]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo ""
    echo "Create one from the example:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your API keys"
    echo ""
    echo -e "${YELLOW}Continuing without .env (some features may not work)...${NC}"
fi

# Load environment variables if .env exists
if [[ -f ".env" ]]; then
    set -a
    source .env
    set +a
fi

# Check if uvicorn is available
if ! command -v uvicorn &> /dev/null; then
    echo -e "${RED}Error: uvicorn not found${NC}"
    echo ""
    echo "Install dependencies:"
    echo "  pip install -r requirements.txt"
    echo ""
    echo "Or create a virtual environment first:"
    echo "  python -m venv .venv"
    echo "  source .venv/bin/activate  # Linux/Mac"
    echo "  .venv\\Scripts\\activate   # Windows"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo -e "${GREEN}=== Starting Development Server ===${NC}"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo "  Host:      ${HOST}"
echo "  Port:      ${PORT}"
echo "  Reload:    enabled"
echo ""
echo -e "${BLUE}Endpoints:${NC}"
echo "  API:       http://localhost:${PORT}"
echo "  Health:    http://localhost:${PORT}/health"
echo "  Docs:      http://localhost:${PORT}/docs"
echo "  ReDoc:     http://localhost:${PORT}/redoc"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Run uvicorn with hot reload
exec uvicorn app.main:app \
    --host "$HOST" \
    --port "$PORT" \
    --reload \
    --reload-dir app \
    --log-level "${LOG_LEVEL:-info}"
