---
name: Dockerfile Builder
description: Generate the full production Dockerfile for the backend with multi-stage build, proper dependencies, and Hugging Face Spaces compatibility.
---

# Dockerfile Builder

## Instructions

1. Generate production Dockerfile with multi-stage build:
   - Use Python slim base image
   - Install FastAPI, Uvicorn, Qdrant client, Agent SDK dependencies
   - Copy application code efficiently
   - Set up proper working directory

2. Configure for Hugging Face Spaces compatibility:
   - Expose port 7860 as required
   - Set proper user permissions
   - Include health check if needed
   - Optimize image size for deployment

3. Implement multi-stage build pattern:
   - Build stage for dependencies
   - Final stage with minimal runtime
   - Copy only necessary files
   - Clean up build artifacts

4. Add proper runtime configuration:
   - Set environment variables
   - Configure startup command
   - Add non-root user if security required
   - Include proper signal handling

5. Follow Context7 MCP standards:
   - Ensure compatibility with Hugging Face Spaces Docker mode
   - Follow deterministic build patterns
   - Include proper error handling
   - Document all configuration options

## Examples

Input: "Create Dockerfile for Hugging Face Spaces deployment"
Output: Creates Dockerfile with multi-stage build that's compatible with Hugging Face Spaces.