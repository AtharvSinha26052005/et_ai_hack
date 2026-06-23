"""ChromaDB vector store client — persistent client singleton."""

import chromadb
from chromadb.config import Settings as ChromaSettings
from config.settings import settings
import logging
import os

logger = logging.getLogger(__name__)


class ChromaClient:
    """Manages ChromaDB persistent client lifecycle."""

    _client: chromadb.ClientAPI | None = None
    _collection: chromadb.Collection | None = None

    COLLECTION_NAME = "intelliplant_documents"

    @classmethod
    def connect(cls) -> None:
        """Initialize the ChromaDB persistent client."""
        try:
            # Ensure directory exists
            os.makedirs(settings.chroma_persist_dir, exist_ok=True)

            cls._client = chromadb.PersistentClient(
                path=settings.chroma_persist_dir,
            )

            # Get or create the main collection
            cls._collection = cls._client.get_or_create_collection(
                name=cls.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )

            count = cls._collection.count()
            logger.info(
                f"ChromaDB initialized at {settings.chroma_persist_dir} "
                f"({count} existing documents)"
            )
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            cls._client = None
            cls._collection = None

    @classmethod
    def get_client(cls) -> chromadb.ClientAPI:
        """Get the ChromaDB client."""
        if cls._client is None:
            raise RuntimeError("ChromaDB not initialized. Call connect() first.")
        return cls._client

    @classmethod
    def get_collection(cls) -> chromadb.Collection:
        """Get the main document collection."""
        if cls._collection is None:
            raise RuntimeError("ChromaDB collection not initialized.")
        return cls._collection

    @classmethod
    def is_connected(cls) -> bool:
        """Check if ChromaDB is initialized."""
        return cls._client is not None

    @classmethod
    def close(cls) -> None:
        """Cleanup ChromaDB client."""
        cls._client = None
        cls._collection = None
        logger.info("ChromaDB client closed")
