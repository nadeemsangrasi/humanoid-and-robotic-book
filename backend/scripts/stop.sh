#!/bin/bash
# =============================================================================
# RAG Textbook Chatbot Backend - Docker Stop Script
# =============================================================================
# Usage: ./scripts/stop.sh [--remove]
#
# Options:
#   --remove, -r    Remove the container after stopping
#
# This script stops the running Docker container.
# =============================================================================

# Configuration
CONTAINER_NAME="rag-chatbot"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
REMOVE=false
for arg in "$@"; do
    case $arg in
        --remove|-r)
            REMOVE=true
            ;;
    esac
done

# Check if container exists
if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${YELLOW}Container '${CONTAINER_NAME}' not found${NC}"
    exit 0
fi

# Stop container
echo -e "${GREEN}Stopping container '${CONTAINER_NAME}'...${NC}"
docker stop "${CONTAINER_NAME}"

# Remove if requested
if [[ "$REMOVE" == true ]]; then
    echo -e "${GREEN}Removing container '${CONTAINER_NAME}'...${NC}"
    docker rm "${CONTAINER_NAME}"
fi

echo -e "${GREEN}Done${NC}"
