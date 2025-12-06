"""
RAG (Retrieval Augmented Generation) system for CoachX.

Uses ChromaDB to store and query sports knowledge base documents.
Provides context-aware information for AI-generated responses.
"""

from typing import List, Dict, Optional
import logging
from pathlib import Path

import chromadb
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
        logger.info("Embedding model loaded")
    return _embedding_model


def get_chroma_client() -> chromadb.PersistentClient:
    """
    Get or create ChromaDB client (singleton pattern).

    Returns:
        ChromaDB client with persistent storage
    """
    global _chroma_client
    if _chroma_client is None:
        logger.info("Initializing ChromaDB client...")
        _chroma_client = chromadb.PersistentClient(
            path=CHROMA_DB_DIR
        )
        logger.info(f"ChromaDB initialized at {CHROMA_DB_DIR}")
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
            logger.info(f"Collection exists with {count} documents. Skipping reload.")
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

    logger.info(f"Knowledge base loaded: {len(documents)} chunks from {doc_id} documents")


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

    logger.info(f"Query: '{query}' (sport={sport}) - {len(formatted_results)} results")
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
