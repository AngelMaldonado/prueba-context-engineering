# INITIAL.md - RAG System with ChromaDB

## FEATURE:

Implement a Retrieval Augmented Generation (RAG) system using ChromaDB for CoachX to provide context-aware responses based on the sports knowledge base.

**Requirements:**

1. **ChromaDB Setup**
   - Install and configure ChromaDB for local persistence
   - Create collection: "coachx_knowledge"
   - Persist to directory: `backend/chroma_db/`
   - Support for adding, querying, and updating documents

2. **Document Loading**
   - Load all markdown files from `knowledge_base/`
   - Process documents by sport categories:
     - boxing/ → official-boxing.md
     - crossfit/ → official-crossfit.md
     - gym/ → official-gym-and-strength.md
   - Split documents into chunks (500 tokens, 50 overlap)
   - Preserve metadata (sport, source, section)

3. **Embeddings**
   - Use sentence-transformers (local, free, no API)
   - Model: "all-MiniLM-L6-v2" (fast, effective, 384 dimensions)
   - Embed document chunks on load
   - Store embeddings in ChromaDB

4. **Query Functionality**
   - `query_knowledge(query: str, sport: str, top_k: int = 3)`
   - Return top-k most relevant chunks
   - Include metadata and similarity scores
   - Filter by sport if specified

5. **Integration with Backend**
   - Create `app/ai/rag.py` module
   - Startup event: Load knowledge base into ChromaDB
   - Function to query RAG system
   - Helper to format context for LLM prompts

6. **Directory Structure**
   ```
   backend/
   ├── app/
   │   ├── ai/
   │   │   ├── __init__.py
   │   │   └── rag.py              # RAG implementation
   │   └── main.py                  # Add startup event
   ├── chroma_db/                   # ChromaDB persistence (gitignored)
   └── requirements.txt             # Add chromadb, sentence-transformers
   ```

**Success Criteria:**
- ChromaDB collection created with knowledge base
- Can query "boxing techniques" and get relevant chunks
- Can query "crossfit warmup" and get relevant chunks
- Embeddings are fast (< 1 second for query)
- Database persists between restarts
- Integration with backend startup
- No external API calls needed

## EXAMPLES:

Reference these patterns:

1. **Backend Integration**
   - Follow `backend/app/database/connection.py` pattern
   - Singleton pattern for ChromaDB client
   - Startup event in `main.py`

2. **Module Structure**
   - Similar to `app/database/` module
   - Clean separation of concerns
   - Type hints and docstrings

3. **CLAUDE.md Guidelines**
   - Functions under 50 lines
   - Type hints everywhere
   - Google-style docstrings
   - Proper error handling

## DOCUMENTATION:

Essential documentation:

1. **ChromaDB:**
   - Docs: https://docs.trychroma.com/
   - Getting Started: https://docs.trychroma.com/getting-started
   - Collections: https://docs.trychroma.com/usage-guide#using-collections
   - Persistence: https://docs.trychroma.com/usage-guide#changing-the-distance-function

2. **LangChain:**
   - ChromaDB integration: https://python.langchain.com/docs/integrations/vectorstores/chroma
   - Text Splitters: https://python.langchain.com/docs/modules/data_connection/document_transformers/
   - RecursiveCharacterTextSplitter: https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/recursive_text_splitter

3. **Sentence Transformers:**
   - Docs: https://www.sbert.net/
   - Models: https://www.sbert.net/docs/pretrained_models.html
   - all-MiniLM-L6-v2: Fast and effective for semantic search

## OTHER CONSIDERATIONS:

**Critical Gotchas:**

1. **ChromaDB Persistence**
   - Must specify `persist_directory` when creating client
   - Call `client.persist()` after adding documents
   - Add `chroma_db/` to `.gitignore`

2. **Document Chunking**
   - Too large: Poor retrieval accuracy
   - Too small: Loss of context
   - Recommended: 500 tokens with 50 token overlap
   - Use RecursiveCharacterTextSplitter from LangChain

3. **Embeddings Model**
   - all-MiniLM-L6-v2: 384 dimensions, fast, good quality
   - Downloaded once, cached locally
   - No API calls needed (runs on CPU)
   - First run will download model (~90MB)

4. **Knowledge Base Loading**
   - Load on startup (one-time operation)
   - Check if collection exists before reloading
   - Option to force reload for updates

5. **Metadata Importance**
   - Store sport type for filtering
   - Store source document for citations
   - Store section/heading for context

6. **Query Optimization**
   - Use sport filter to narrow results
   - top_k = 3 is usually sufficient
   - Can adjust based on query complexity

7. **Error Handling**
   - Handle missing knowledge base files
   - Handle ChromaDB connection errors
   - Graceful degradation if RAG fails

8. **Testing**
   - Test with each sport type
   - Test with various query types
   - Verify metadata is preserved
   - Check persistence works

**File Organization:**
- Keep RAG logic in `app/ai/` module
- Knowledge base stays in `knowledge_base/`
- ChromaDB data in `chroma_db/` (gitignored)
- No file over 500 lines

**Performance Considerations:**
- Initial load: ~5-10 seconds (one time)
- Query time: < 1 second
- Embedding is CPU-based (no GPU needed)
- ChromaDB is fast for small collections

**Security:**
- No API keys needed
- All processing local
- No data sent externally

**Dependencies to Add:**
```txt
chromadb==0.4.18
langchain==0.0.350
sentence-transformers==2.2.2
```

**Validation:**
After implementation, verify:

1. ChromaDB collection created:
   ```python
   from app.ai.rag import get_rag_client
   client = get_rag_client()
   collection = client.get_collection("coachx_knowledge")
   print(f"Documents: {collection.count()}")  # Should be > 0
   ```

2. Query works:
   ```python
   from app.ai.rag import query_knowledge
   results = query_knowledge("boxing jab technique", sport="boxing")
   print(results)  # Should return relevant chunks
   ```

3. Persistence works:
   - Restart server
   - Query again
   - Should still work without reloading

4. Metadata preserved:
   ```python
   results = query_knowledge("warmup exercises")
   print(results[0]['metadata'])  # Should have sport, source, etc.
   ```

**Integration Example:**
```python
# In future endpoints, use like this:
from app.ai.rag import query_knowledge

def generate_workout_plan(user_data):
    # Get relevant knowledge
    context = query_knowledge(
        query=f"{user_data.sport} workout for {user_data.experience_level}",
        sport=user_data.sport,
        top_k=3
    )

    # Format context for LLM
    context_str = "\n\n".join([chunk['text'] for chunk in context])

    # Pass to Gemini (Feature 3)
    prompt = f"Context:\n{context_str}\n\nGenerate a workout plan for..."
    # ...
```

---

## Tips for Implementation:

1. **Start Simple**
   - First: Load one document, test embedding
   - Then: Load all documents
   - Finally: Add query functionality

2. **Test as You Go**
   - Print collection count after loading
   - Test query with simple examples
   - Verify metadata is correct

3. **Handle Edge Cases**
   - Empty query
   - Sport not found
   - No results returned

4. **Follow Patterns**
   - Similar to database connection setup
   - Singleton for ChromaDB client
   - Clean module structure

---

**Ready to generate PRP!**

This INITIAL.md provides everything needed to implement a robust RAG system for CoachX.
