#!/bin/bash
# =============================================================================
# RAG Textbook Chatbot Backend - Docker Run Script
# =============================================================================
# Usage: ./scripts/run.sh [--detach] [--build]
#
# Options:
#   --detach, -d    Run container in detached mode (background)
#   --build, -b     Rebuild image before running
#
# This script runs the Docker container for local development testing.
# Requires a .env file with the required environment variables.
# =============================================================================

set -e  # Exit on any error

# Configuration
IMAGE_NAME="rag-textbook-chatbot"
IMAGE_TAG="latest"
CONTAINER_NAME="rag-chatbot"
PORT=7860

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
DETACH=""
BUILD=false

for arg in "$@"; do
    case $arg in
        --detach|-d)
            DETACH="-d"
            ;;
        --build|-b)
            BUILD=true
            ;;
    esac
done

# Change to backend directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
cd "$BACKEND_DIR"

# Check if .env file exists
if [[ ! -f ".env" ]]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo ""
    echo "Please create a .env file with your configuration:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your API keys"
    exit 1
fi

# Build if requested
if [[ "$BUILD" == true ]]; then
    echo -e "${GREEN}=== Building Image ===${NC}"
    ./scripts/build.sh
    echo ""
fi

# Stop and remove existing container if running
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${YELLOW}Stopping existing container...${NC}"
    docker stop "${CONTAINER_NAME}" 2>/dev/null || true
    docker rm "${CONTAINER_NAME}" 2>/dev/null || true
fi

echo -e "${GREEN}=== Starting Container ===${NC}"
echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "Container: ${CONTAINER_NAME}"
echo "Port: ${PORT}"
echo ""

# Run the container
docker run ${DETACH} \
    --name "${CONTAINER_NAME}" \
    -p "${PORT}:7860" \
    --env-file .env \
    "${IMAGE_NAME}:${IMAGE_TAG}"

if [[ -n "$DETACH" ]]; then
    echo ""
    echo -e "${GREEN}=== Container Started (Detached) ===${NC}"
    echo ""
    echo "API available at: http://localhost:${PORT}"
    echo "Health check:     http://localhost:${PORT}/health"
    echo "Documentation:    http://localhost:${PORT}/docs"
    echo ""
    echo "View logs:    docker logs -f ${CONTAINER_NAME}"
    echo "Stop:         docker stop ${CONTAINER_NAME}"
    echo "Remove:       docker rm ${CONTAINER_NAME}"
fi
