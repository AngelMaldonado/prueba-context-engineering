"""
FastAPI application entry point for CoachX backend.

This file initializes the FastAPI app, sets up middleware, includes routers,
and defines startup/shutdown events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.database.connection import create_tables

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

    Creates database tables on application startup.
    """
    logger.info(f"=€ Starting {settings.APP_NAME}...")
    create_tables()
    logger.info(" Application startup complete")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Shutdown event handler."""
    logger.info("=K Shutting down application...")


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
