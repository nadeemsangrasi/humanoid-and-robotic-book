---
name: Qdrant Retrieval Tool
description: Generate JSON schemas and Python handlers for Qdrant-based retrieval tools used by the RAG agent to search textbook content.
---

# Qdrant Retrieval Tool

## Instructions

1. Create tool definitions for retrieval functionality in app/services/tools/retrieval_tools.py:
   - Define retrieve_passages({ query: string }) tool
   - Define lookup_metadata({ id: string }) tool
   - Create proper JSON schemas following OpenAI Agent SDK specification
   - Include proper parameter validation

2. Implement Qdrant client integration:
   - Initialize Qdrant client with proper configuration
   - Connect to the "book_chunks" collection
   - Implement vector search functionality
   - Handle connection errors and retries

3. Create retrieval handlers:
   - Implement retrieve_passages function that performs semantic search
   - Implement lookup_metadata function for getting document metadata
   - Include proper error handling and logging
   - Return results in the expected format for the agent

4. Follow Context7 MCP conventions:
   - Match OpenAI Agent SDK tool specification exactly
   - Produce deterministic JSON schemas
   - Integrate with RAG Pipeline tools
   - Follow proper error handling patterns

5. Add proper configuration management:
   - Support environment variables for Qdrant connection
   - Include default values and validation
   - Handle both local and cloud Qdrant instances

## Examples

Input: "Create Qdrant retrieval tools"
Output: Creates retrieval_tools.py with:
```python
from qdrant_client import QdrantClient
from typing import List, Dict, Any
import os

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def retrieve_passages(query: str) -> List[Dict[str, Any]]:
    """Retrieve relevant passages from the textbook using semantic search."""
    try:
        # Perform vector search in Qdrant
        search_results = qdrant_client.search(
            collection_name="book_chunks",
            query_text=query,
            limit=5
        )

        passages = []
        for result in search_results:
            passages.append({
                "id": result.id,
                "content": result.payload.get("content", ""),
                "metadata": result.payload.get("metadata", {}),
                "score": result.score
            })

        return passages
    except Exception as e:
        # Handle errors appropriately
        raise e

def lookup_metadata(doc_id: str) -> Dict[str, Any]:
    """Lookup metadata for a specific document."""
    try:
        records = qdrant_client.retrieve(
            collection_name="book_chunks",
            ids=[doc_id]
        )

        if records:
            return records[0].payload.get("metadata", {})
        return {}
    except Exception as e:
        # Handle errors appropriately
        raise e

# Define tool schemas for OpenAI Agent SDK
retrieval_tools = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_passages",
            "description": "Retrieve relevant passages from the textbook based on the query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant passages"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_metadata",
            "description": "Lookup metadata for a specific document by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The document ID to lookup metadata for"
                    }
                },
                "required": ["id"]
            }
        }
    }
]
```