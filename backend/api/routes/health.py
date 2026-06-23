"""Health check endpoint."""

from fastapi import APIRouter
from database.neo4j_client import Neo4jClient
from database.chroma_client import ChromaClient
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check():
    """Check health of all services."""
    neo4j_status = "connected" if Neo4jClient.is_connected() else "disconnected"
    chroma_status = "connected" if ChromaClient.is_connected() else "disconnected"

    # Try to get Neo4j stats
    neo4j_details = {}
    if Neo4jClient.is_connected():
        try:
            result = await Neo4jClient.execute_query(
                "CALL db.labels() YIELD label RETURN count(label) as count"
            )
            neo4j_details["label_count"] = result[0]["count"] if result else 0
        except Exception as e:
            neo4j_status = f"error: {str(e)}"

    # ChromaDB stats
    chroma_details = {}
    if ChromaClient.is_connected():
        try:
            collection = ChromaClient.get_collection()
            chroma_details["document_count"] = collection.count()
        except Exception as e:
            chroma_status = f"error: {str(e)}"

    overall = "healthy" if neo4j_status == "connected" and chroma_status == "connected" else "degraded"

    return {
        "status": overall,
        "services": {
            "neo4j": {"status": neo4j_status, **neo4j_details},
            "chromadb": {"status": chroma_status, **chroma_details},
            "sqlite": {"status": "connected"},  # Always available
        },
        "version": "1.0.0",
        "app": "IntelliPlant",
    }
