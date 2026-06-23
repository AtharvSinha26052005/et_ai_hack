"""IntelliPlant — FastAPI Application Entry Point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from config.settings import settings
from database.neo4j_client import Neo4jClient
from database.chroma_client import ChromaClient
from database.sqlite_client import init_db, close_db
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — initialize and cleanup resources."""
    logger.info(f"Starting {settings.app_name} ({settings.app_env})")

    # Initialize SQLite
    await init_db()
    logger.info("SQLite initialized")

    # Initialize ChromaDB
    ChromaClient.connect()
    logger.info("ChromaDB initialized")

    # Initialize Neo4j
    await Neo4jClient.connect()

    # Ensure upload directory exists
    os.makedirs(settings.upload_dir, exist_ok=True)

    logger.info(f"{settings.app_name} is ready!")

    yield  # App is running

    # Cleanup
    logger.info("Shutting down...")
    await Neo4jClient.close()
    ChromaClient.close()
    await close_db()
    logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="IntelliPlant API",
    description="AI-Powered Industrial Knowledge Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded documents
upload_dir = os.path.abspath(settings.upload_dir)
os.makedirs(upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# Register API routes
from api.routes.health import router as health_router
from api.routes.documents import router as documents_router
from api.routes.knowledge_graph import router as kg_router
from api.routes.chat import router as chat_router
from api.routes.compliance import router as compliance_router
from api.routes.maintenance import router as maintenance_router

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(kg_router)
app.include_router(chat_router)
app.include_router(compliance_router)
app.include_router(maintenance_router)


@app.get("/")
async def root():
    """Root endpoint — redirect to docs."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "description": "AI-Powered Industrial Knowledge Intelligence Platform",
        "docs": "/docs",
        "health": "/api/health",
    }
