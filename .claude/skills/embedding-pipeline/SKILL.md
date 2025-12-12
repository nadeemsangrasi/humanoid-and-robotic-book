---
name: Embedding Pipeline
description: Implement reusable embedding functions using Gemini embedding models via LangChain with proper error handling and batching.
---

# Embedding Pipeline

## Instructions

1. Create embedding module at `app/services/embedding/embedding.py`:
   - Provide embed_text(text: str) -> list[float] function
   - Include batch embedding utility for multiple texts
   - Implement retry logic for API failures
   - Add proper error handling and logging

2. Configure Gemini embeddings via LangChain:
   - Use GoogleGenerativeAIEmbeddings from langchain.embeddings
   - Handle API key authentication securely
   - Set appropriate model parameters
   - Include rate limiting if needed

3. Implement batching functionality:
   - Process multiple texts efficiently
   - Handle large batches appropriately
   - Include memory management for large inputs
   - Add progress tracking for long operations

4. Add utility functions:
   - Similarity calculation between embeddings
   - Normalization functions if needed
   - Caching mechanism for repeated embeddings
   - Validation for input text length

5. Follow Context7 MCP standards:
   - Use Gemini embeddings only (no OpenAI)
   - Follow deterministic output patterns
   - Include proper error handling
   - Document all configuration options

## Examples

Input: "Create embedding pipeline with Gemini"
Output: Creates embedding.py with:
```python
from langchain.embeddings import GoogleGenerativeAIEmbeddings
import os
from typing import List, Union

class EmbeddingService:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            # Handle error appropriately
            raise e

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        try:
            return self.embeddings.embed_documents(texts)
        except Exception as e:
            # Handle error appropriately
            raise e
```