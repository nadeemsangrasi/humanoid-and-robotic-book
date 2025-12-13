#!/bin/bash
# =============================================================================
# RAG Textbook Chatbot Backend - Docker Build Script
# =============================================================================
# Usage: ./scripts/build.sh [--no-cache]
#
# Options:
#   --no-cache    Build without using Docker cache (clean build)
#
# This script builds the production Docker image for the RAG chatbot backend.
# =============================================================================

set -e  # Exit on any error

# Configuration
IMAGE_NAME="rag-textbook-chatbot"
IMAGE_TAG="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
NO_CACHE=""
if [[ "$1" == "--no-cache" ]]; then
    NO_CACHE="--no-cache"
    echo -e "${YELLOW}Building without cache...${NC}"
fi

# Change to backend directory (script can be run from any location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
cd "$BACKEND_DIR"

echo -e "${GREEN}=== Building Docker Image ===${NC}"
echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "Context: ${BACKEND_DIR}"
echo ""

# Build the image
docker build ${NO_CACHE} -t "${IMAGE_NAME}:${IMAGE_TAG}" .

# Check if build succeeded
if [[ $? -eq 0 ]]; then
    echo ""
    echo -e "${GREEN}=== Build Successful ===${NC}"
    echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
    echo ""
    echo "To run the container:"
    echo "  ./scripts/run.sh"
    echo ""
    echo "Or manually:"
    echo "  docker run -p 7860:7860 --env-file .env ${IMAGE_NAME}:${IMAGE_TAG}"
else
    echo ""
    echo -e "${RED}=== Build Failed ===${NC}"
    exit 1
fi
