---
name: Book Ingestion
description: Generate the complete RAG ingestion script to read the textbook, chunk content, embed using Gemini, and push to Qdrant following MCP documentation.
---

# Book Ingestion

## Instructions

1. Generate the complete RAG ingestion script at `scripts/ingest-book.py` that:
   - Loads all Markdown files under /book/ directory
   - Chunks content by sections, code blocks, paragraphs with 500-1000 token sizes
   - Extracts metadata (chapter, section, heading)
   - Generates embeddings using Gemini via LangChain
   - Uploads vectors to Qdrant collection "book_chunks"

2. Follow chunking best practices:
   - Preserve semantic boundaries
   - Maintain document hierarchy in metadata
   - Handle code blocks separately from text
   - Include overlap between chunks if needed

3. Implement Gemini embedding integration:
   - Use LangChain GoogleGenerativeAIEmbeddings
   - Handle API authentication properly
   - Implement batch processing for efficiency
   - Include retry logic for failed embeddings

4. Configure Qdrant upload:
   - Connect to Qdrant collection "book_chunks"
   - Batch upload with proper metadata
   - Handle duplicate detection and updates
   - Include progress tracking and error handling

5. Follow Context7 MCP conventions:
   - Use Gemini embeddings only (no OpenAI)
   - Follow Qdrant best practices for batch uploads
   - Output deterministic Python code
   - Include proper error handling and logging

## Examples

Input: "Create book ingestion pipeline for textbook"
Output: Creates ingest-book.py with complete implementation following MCP documentation for LangChain and Qdrant.