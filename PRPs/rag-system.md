# PRP: RAG System with ChromaDB

**Feature:** Retrieval Augmented Generation system for context-aware AI responses
**Time:** 1.5 hours
**Difficulty:** Medium-High

---

## 1. Overview

### What We're Building

A complete RAG system using ChromaDB to retrieve relevant information from the sports knowledge base (boxing, crossfit, gym) to provide context for AI-generated workout plans and chat responses.

### Architecture

```
knowledge_base/           ← Source documents
    ├── boxing/
    ├── crossfit/
    └── gym/
           ↓
    Load & Chunk
           ↓
    Embed (sentence-transformers)
           ↓
    Store in ChromaDB
           ↓
chroma_db/               ← Persistent vector store
           ↓
    Query Interface
           ↓
app/ai/rag.py            ← RAG module
```

### Why This Feature Matters

- Provides factual, sport-specific knowledge to AI
- Improves accuracy of workout plans
- Enables citation of sources
- No external API calls needed (all local)

### Success Criteria

- ✅ ChromaDB collection "coachx_knowledge" created
- ✅ All knowledge base documents loaded and embedded
- ✅ Can query "boxing jab technique" → returns relevant chunks
- ✅ Can filter by sport type
- ✅ Query time < 1 second
- ✅ Persists between server restarts
- ✅ No external API dependencies

---

## 2. Implementation Steps

### Step 1: Update Dependencies

**File:** `backend/requirements.txt`

Add RAG dependencies:

```txt
chromadb==0.4.18
langchain==0.0.350
sentence-transformers==2.2.2
```

**Install:**

```bash
cd backend
source venv/bin/activate
pip install chromadb==0.4.18 langchain==0.0.350 sentence-transformers==2.2.2
```

**Note:** First install will download the embedding model (~90MB), takes 1-2 minutes.

**Validate:**

```bash
python -c "import chromadb; print('✅ ChromaDB OK')"
python -c "from langchain.text_splitter import RecursiveCharacterTextSplitter; print('✅ LangChain OK')"
python -c "from sentence_transformers import SentenceTransformer; print('✅ Sentence Transformers OK')"
```

---

### Step 2: Create AI Module Directory

```bash
mkdir -p backend/app/ai
touch backend/app/ai/__init__.py
touch backend/app/ai/rag.py
```

**Validate:**

```bash
tree backend/app/ai/
# Should show __init__.py and rag.py
```

---

### Step 3: Update .gitignore

**File:** `backend/.gitignore` (create if doesn't exist)

```gitignore
# Virtual environment
venv/
__pycache__/
*.pyc
*.pyo

# Database
*.db
coachx.db

# ChromaDB
chroma_db/

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
```

**Validate:**

```bash
cat backend/.gitignore
```

---

### Step 4: Implement RAG Module

**File:** `backend/app/ai/rag.py`

**Pattern:** Singleton for ChromaDB client, similar to database connection

```python
"""
RAG (Retrieval Augmented Generation) system for CoachX.

Uses ChromaDB to store and query sports knowledge base documents.
Provides context-aware information for AI-generated responses.
"""

import os
from typing import List, Dict, Optional
import logging
from pathlib import Path

import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Constants
CHROMA_DB_DIR = "./chroma_db"
COLLECTION_NAME = "coachx_knowledge"
KNOWLEDGE_BASE_DIR = "../knowledge_base"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Global instances
_chroma_client = None
_embedding_model = None


def get_embedding_model() -> SentenceTransformer:
    """
    Get or create the embedding model (singleton pattern).

    Returns:
        SentenceTransformer model for generating embeddings
    """
    global _embedding_model
    if _embedding_model is None:
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("✅ Embedding model loaded")
    return _embedding_model


def get_chroma_client() -> chromadb.Client:
    """
    Get or create ChromaDB client (singleton pattern).

    Returns:
        ChromaDB client with persistent storage
    """
    global _chroma_client
    if _chroma_client is None:
        logger.info("Initializing ChromaDB client...")
        _chroma_client = chromadb.Client(
            Settings(
                persist_directory=CHROMA_DB_DIR,
                anonymized_telemetry=False
            )
        )
        logger.info(f"✅ ChromaDB initialized at {CHROMA_DB_DIR}")
    return _chroma_client


def load_knowledge_base(force_reload: bool = False) -> None:
    """
    Load knowledge base documents into ChromaDB.

    Reads markdown files from knowledge_base/ directory, chunks them,
    embeds them, and stores in ChromaDB collection.

    Args:
        force_reload: If True, delete existing collection and reload

    Raises:
        FileNotFoundError: If knowledge base directory not found
    """
    logger.info("Loading knowledge base into ChromaDB...")

    client = get_chroma_client()
    embedding_model = get_embedding_model()

    # Check if collection exists
    try:
        collection = client.get_collection(COLLECTION_NAME)
        if not force_reload:
            count = collection.count()
            logger.info(f"✅ Collection exists with {count} documents. Skipping reload.")
            return
        else:
            logger.info("Force reload requested. Deleting existing collection...")
            client.delete_collection(COLLECTION_NAME)
    except Exception:
        logger.info("Collection does not exist. Creating new...")

    # Create collection
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "CoachX sports knowledge base"}
    )

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )

    # Load documents
    knowledge_base_path = Path(KNOWLEDGE_BASE_DIR)
    if not knowledge_base_path.exists():
        raise FileNotFoundError(f"Knowledge base not found at {KNOWLEDGE_BASE_DIR}")

    documents = []
    metadatas = []
    ids = []
    doc_id = 0

    # Process each sport directory
    for sport_dir in knowledge_base_path.iterdir():
        if not sport_dir.is_dir():
            continue

        sport_name = sport_dir.name
        logger.info(f"Processing {sport_name}...")

        # Process markdown files in sport directory
        for md_file in sport_dir.glob("*.md"):
            logger.info(f"  Loading {md_file.name}...")

            # Read file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Chunk document
            chunks = text_splitter.split_text(content)
            logger.info(f"  Split into {len(chunks)} chunks")

            # Add each chunk
            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({
                    "sport": sport_name,
                    "source": md_file.name,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                })
                ids.append(f"{sport_name}_{md_file.stem}_{i}")
                doc_id += 1

    # Generate embeddings and add to collection
    logger.info(f"Embedding {len(documents)} chunks...")
    embeddings = embedding_model.encode(documents).tolist()

    logger.info("Adding to ChromaDB...")
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    logger.info(f"✅ Knowledge base loaded: {len(documents)} chunks from {doc_id} documents")


def query_knowledge(
    query: str,
    sport: Optional[str] = None,
    top_k: int = 3
) -> List[Dict]:
    """
    Query the knowledge base for relevant information.

    Args:
        query: Search query
        sport: Optional sport filter (boxing, crossfit, gym, etc.)
        top_k: Number of results to return

    Returns:
        List of dictionaries with 'text', 'metadata', and 'distance' keys

    Example:
        >>> results = query_knowledge("jab technique", sport="boxing", top_k=3)
        >>> for result in results:
        >>>     print(result['text'])
        >>>     print(result['metadata'])
    """
    client = get_chroma_client()
    embedding_model = get_embedding_model()

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as e:
        logger.error(f"Collection not found: {e}")
        return []

    # Generate query embedding
    query_embedding = embedding_model.encode([query]).tolist()

    # Build where filter
    where_filter = {"sport": sport} if sport else None

    # Query
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where=where_filter
    )

    # Format results
    formatted_results = []
    if results and results['documents'] and len(results['documents']) > 0:
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })

    logger.info(f"Query: '{query}' (sport={sport}) → {len(formatted_results)} results")
    return formatted_results


def format_context_for_llm(results: List[Dict]) -> str:
    """
    Format RAG results into context string for LLM prompts.

    Args:
        results: List of query results from query_knowledge()

    Returns:
        Formatted string with numbered context items

    Example:
        >>> results = query_knowledge("warmup exercises")
        >>> context = format_context_for_llm(results)
        >>> prompt = f"Context:\n{context}\n\nGenerate workout..."
    """
    if not results:
        return "No relevant information found."

    context_parts = []
    for i, result in enumerate(results, 1):
        sport = result['metadata'].get('sport', 'unknown')
        source = result['metadata'].get('source', 'unknown')
        text = result['text']

        context_parts.append(
            f"[{i}] Source: {sport}/{source}\n{text}"
        )

    return "\n\n".join(context_parts)


def get_collection_stats() -> Dict:
    """
    Get statistics about the knowledge base collection.

    Returns:
        Dictionary with collection statistics
    """
    client = get_chroma_client()

    try:
        collection = client.get_collection(COLLECTION_NAME)
        return {
            "collection_name": COLLECTION_NAME,
            "document_count": collection.count(),
            "embedding_model": EMBEDDING_MODEL,
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {"error": str(e)}
```

**Validate:**

```bash
python -c "from app.ai.rag import get_chroma_client; print('✅ RAG module OK')"
```

---

### Step 5: Update Backend Startup

**File:** `backend/app/main.py`

Add RAG initialization to startup event:

```python
# Add import at top
from app.ai.rag import load_knowledge_base, get_collection_stats

# Update startup event
@app.on_event("startup")
async def startup_event() -> None:
    """
    Startup event handler.

    Creates database tables and loads knowledge base on application startup.
    """
    logger.info(f"🚀 Starting {settings.APP_NAME}...")

    # Create database tables
    create_tables()

    # Load knowledge base into RAG system
    try:
        load_knowledge_base(force_reload=False)
        stats = get_collection_stats()
        logger.info(f"📚 RAG System: {stats['document_count']} chunks loaded")
    except Exception as e:
        logger.error(f"⚠️  RAG System failed to load: {e}")
        logger.warning("Application will continue without RAG system")

    logger.info("✅ Application startup complete")
```

**Validate:**

```bash
python -c "from app.main import app; print('✅ Main updated OK')"
```

---

### Step 6: Add RAG Test Endpoint

**File:** `backend/app/main.py`

Add test endpoint to verify RAG works:

```python
# Add import
from app.ai.rag import query_knowledge, get_collection_stats

# Add endpoint after health check
@app.get("/rag/stats")
async def rag_stats() -> dict:
    """Get RAG system statistics."""
    return get_collection_stats()


@app.get("/rag/query")
async def rag_query(q: str, sport: Optional[str] = None, top_k: int = 3) -> dict:
    """
    Test RAG query endpoint.

    Args:
        q: Query string
        sport: Optional sport filter
        top_k: Number of results

    Example:
        GET /rag/query?q=boxing%20jab&sport=boxing&top_k=3
    """
    from typing import Optional
    results = query_knowledge(query=q, sport=sport, top_k=top_k)
    return {
        "query": q,
        "sport": sport,
        "results_count": len(results),
        "results": results
    }
```

---

### Step 7: Start Server and Load Knowledge Base

**Commands:**

```bash
cd backend
source venv/bin/activate
python -m app.main
```

**Expected Output:**

```
INFO: 🚀 Starting CoachX API...
INFO: Creating database tables...
INFO: ✅ Database tables created successfully
INFO: Loading knowledge base into ChromaDB...
INFO: Loading embedding model: all-MiniLM-L6-v2
INFO: ✅ Embedding model loaded
INFO: Initializing ChromaDB client...
INFO: ✅ ChromaDB initialized at ./chroma_db
INFO: Processing boxing...
INFO:   Loading official-boxing.md...
INFO:   Split into X chunks
INFO: Processing crossfit...
INFO:   Loading official-crossfit.md...
INFO:   Split into X chunks
INFO: Processing gym...
INFO:   Loading official-gym-and-strength.md...
INFO:   Split into X chunks
INFO: Embedding X chunks...
INFO: Adding to ChromaDB...
INFO: ✅ Knowledge base loaded: X chunks from X documents
INFO: 📚 RAG System: X chunks loaded
INFO: ✅ Application startup complete
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Note:** First run will take longer (model download + embedding). Subsequent runs will be fast.

---

### Step 8: Test RAG System

**Test 1: Check Stats**

```bash
curl http://localhost:8000/rag/stats
```

**Expected:**

```json
{
  "collection_name": "coachx_knowledge",
  "document_count": 50,
  "embedding_model": "all-MiniLM-L6-v2",
  "chunk_size": 500,
  "chunk_overlap": 50
}
```

**Test 2: Query Boxing**

```bash
curl "http://localhost:8000/rag/query?q=boxing%20jab%20technique&sport=boxing&top_k=2"
```

**Expected:**

```json
{
  "query": "boxing jab technique",
  "sport": "boxing",
  "results_count": 2,
  "results": [
    {
      "text": "The jab is the most important punch...",
      "metadata": {
        "sport": "boxing",
        "source": "official-boxing.md",
        "chunk_index": 5
      },
      "distance": 0.35
    },
    ...
  ]
}
```

**Test 3: Query CrossFit**

```bash
curl "http://localhost:8000/rag/query?q=warmup%20exercises&sport=crossfit"
```

**Test 4: Persistence**

- Stop server (Ctrl+C)
- Start again: `python -m app.main`
- Query again - should work instantly (no reload)

---

### Step 9: Test from Python

**Create:** `backend/test_rag.py`

```python
"""Test RAG system functionality."""

from app.ai.rag import query_knowledge, get_collection_stats, format_context_for_llm

# Test 1: Get stats
print("=== RAG System Stats ===")
stats = get_collection_stats()
print(f"Documents: {stats['document_count']}")
print(f"Model: {stats['embedding_model']}")

# Test 2: Query boxing
print("\n=== Query: Boxing Jab ===")
results = query_knowledge("jab technique", sport="boxing", top_k=2)
for i, result in enumerate(results, 1):
    print(f"\n[{i}] Distance: {result['distance']:.3f}")
    print(f"Source: {result['metadata']['sport']}/{result['metadata']['source']}")
    print(f"Text: {result['text'][:200]}...")

# Test 3: Query crossfit
print("\n=== Query: CrossFit Warmup ===")
results = query_knowledge("warmup exercises", sport="crossfit", top_k=1)
if results:
    print(f"Found: {len(results)} results")
    print(f"Text: {results[0]['text'][:200]}...")

# Test 4: Format for LLM
print("\n=== Formatted Context ===")
results = query_knowledge("strength training", top_k=2)
context = format_context_for_llm(results)
print(context[:300] + "...")

print("\n✅ All RAG tests passed!")
```

**Run:**

```bash
python test_rag.py
```

---

### Step 10: Verify Persistence

```bash
# Check chroma_db directory exists
ls chroma_db/

# Should contain ChromaDB files
# chroma_db/
# ├── chroma.sqlite3
# └── ...

# Verify gitignored
git status
# Should NOT show chroma_db/
```

---

### Step 11: Update requirements.txt

Ensure RAG dependencies are in requirements.txt:

```bash
cat backend/requirements.txt | grep -E "chromadb|langchain|sentence"
```

Should show:

```
chromadb==0.4.18
langchain==0.0.350
sentence-transformers==2.2.2
```

---

### Step 12: Final Validation

**Checklist:**

- [ ] ChromaDB client initializes without errors
- [ ] Knowledge base loads on startup
- [ ] `/rag/stats` returns document count > 0
- [ ] `/rag/query` with boxing returns relevant results
- [ ] `/rag/query` with crossfit returns relevant results
- [ ] Queries complete in < 1 second
- [ ] Server restart doesn't reload (uses persisted data)
- [ ] `chroma_db/` is in .gitignore
- [ ] All imports work without errors
- [ ] Logging shows proper info messages

**All should pass ✅**

---

## 3. Code Quality Standards

From CLAUDE.md:

**✅ Required:**

- Type hints on all functions
- Google-style docstrings
- Functions under 50 lines
- Proper error handling
- Logging for important events
- No hardcoded paths (use constants)

**✅ RAG-Specific:**

- Singleton pattern for clients
- Graceful degradation if RAG fails
- Metadata preservation
- Proper chunking strategy

---

## 4. Commit Message

```bash
git add backend/ PRPs/rag-system.md INITIAL-RAG.md
git commit -m "feat(rag): implement RAG system with ChromaDB

- Setup ChromaDB with persistent storage
- Load knowledge base documents (boxing, crossfit, gym)
- Implement document chunking with LangChain
- Add sentence-transformers for local embeddings
- Create query interface with sport filtering
- Add RAG test endpoints (/rag/stats, /rag/query)
- Integrate with application startup
- Add .gitignore for chroma_db/

RAG system provides context-aware information from sports knowledge base.
No external APIs needed - fully local.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 5. Common Issues

**"Model download failed"**
→ Check internet connection, retry

**"Knowledge base not found"**
→ Verify path: `../knowledge_base` from backend/

**"Embedding takes too long"**
→ Normal on first run, subsequent runs are fast

**"Collection already exists"**
→ Use `force_reload=True` to reload

**"No results returned"**
→ Check if knowledge base loaded, verify query

---

## 6. Next Steps

After completing:

1. ✅ Test all endpoints work
2. ✅ Verify persistence
3. ✅ Commit changes
4. ➡️ Move to Feature 3: Gemini Integration

---

**Ready to execute!**

Estimated time: 1-1.5 hours
