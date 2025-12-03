"""
FastAPI application entry point for CoachX backend.

This file initializes the FastAPI app, sets up middleware, includes routers,
and defines startup/shutdown events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging

from app.config import settings
from app.database.connection import create_tables
from app.ai.rag import load_knowledge_base, get_collection_stats, query_knowledge

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered personal training assistant",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware - Allow frontend (localhost:3000) to make requests
# Without this, browser will block requests from different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


@app.on_event("startup")
async def startup_event() -> None:
    """
    Startup event handler.

    Creates database tables and loads knowledge base on application startup.
    """
    logger.info(f"Starting {settings.APP_NAME}...")
    create_tables()

    # Load knowledge base into RAG system
    try:
        load_knowledge_base(force_reload=False)
        stats = get_collection_stats()
        logger.info(f"RAG System: {stats['document_count']} chunks loaded")
    except Exception as e:
        logger.error(f"RAG System failed to load: {e}")
        logger.warning("Application will continue without RAG system")

    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Shutdown event handler."""
    logger.info("Shutting down application...")


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        Dictionary with status: healthy
    """
    return {"status": "healthy"}


@app.get("/")
async def root() -> dict:
    """
    Root endpoint.

    Returns:
        Welcome message with API info
    """
    return {
        "message": "Welcome to CoachX API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/rag/stats")
async def rag_stats() -> dict:
    """
    Get RAG system statistics.

    Returns:
        Dictionary with collection stats
    """
    return get_collection_stats()


@app.get("/rag/query")
async def rag_query(q: str, sport: Optional[str] = None, top_k: int = 3) -> dict:
    """
    Test RAG query endpoint.

    Args:
        q: Query string
        sport: Optional sport filter (boxing, crossfit, gym)
        top_k: Number of results to return (default: 3)

    Returns:
        Query results with metadata

    Example:
        GET /rag/query?q=boxing%20jab&sport=boxing&top_k=2
    """
    results = query_knowledge(query=q, sport=sport, top_k=top_k)
    return {
        "query": q,
        "sport": sport,
        "top_k": top_k,
        "results_count": len(results),
        "results": results
    }


# Future: Include API routers here
# from app.api import onboarding, training, chat
# app.include_router(onboarding.router)
# app.include_router(training.router)
# app.include_router(chat.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
