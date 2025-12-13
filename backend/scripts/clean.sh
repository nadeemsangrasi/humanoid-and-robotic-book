#!/bin/bash
# =============================================================================
# RAG Textbook Chatbot Backend - Docker Cleanup Script
# =============================================================================
# Usage: ./scripts/clean.sh [--all]
#
# Options:
#   --all, -a    Also remove the Docker image
#
# This script removes the container and optionally the image.
# =============================================================================

# Configuration
IMAGE_NAME="rag-textbook-chatbot"
CONTAINER_NAME="rag-chatbot"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
REMOVE_IMAGE=false
for arg in "$@"; do
    case $arg in
        --all|-a)
            REMOVE_IMAGE=true
            ;;
    esac
done

echo -e "${GREEN}=== Docker Cleanup ===${NC}"

# Stop and remove container
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping container '${CONTAINER_NAME}'..."
    docker stop "${CONTAINER_NAME}" 2>/dev/null || true
    echo "Removing container '${CONTAINER_NAME}'..."
    docker rm "${CONTAINER_NAME}" 2>/dev/null || true
else
    echo -e "${YELLOW}Container '${CONTAINER_NAME}' not found${NC}"
fi

# Remove image if requested
if [[ "$REMOVE_IMAGE" == true ]]; then
    if docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "^${IMAGE_NAME}:"; then
        echo "Removing image '${IMAGE_NAME}'..."
        docker rmi "${IMAGE_NAME}:latest" 2>/dev/null || true
    else
        echo -e "${YELLOW}Image '${IMAGE_NAME}' not found${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Cleanup complete${NC}"
