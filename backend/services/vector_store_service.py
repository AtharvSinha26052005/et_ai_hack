"""Vector store service — ChromaDB operations."""

from database.chroma_client import ChromaClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class VectorStoreService:
    """High-level service for ChromaDB vector store operations."""

    def __init__(self):
        self._embedding_model = None

    def _get_embedding_model(self):
        """Lazy-load the sentence-transformers model."""
        if self._embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("Embedding model loaded: all-MiniLM-L6-v2")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise
        return self._embedding_model

    async def add_documents(
        self,
        texts: list[str],
        metadatas: list[dict],
        ids: list[str],
    ) -> int:
        """Store document chunks with embeddings in ChromaDB."""
        if not texts:
            return 0

        model = self._get_embedding_model()
        embeddings = model.encode(texts).tolist()

        collection = ChromaClient.get_collection()
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

        logger.info(f"Added {len(texts)} documents to vector store")
        return len(texts)

    async def similarity_search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[dict] = None,
    ) -> list[dict]:
        """Semantic search — Top-K similar chunks."""
        model = self._get_embedding_model()
        query_embedding = model.encode([query]).tolist()

        collection = ChromaClient.get_collection()

        kwargs = {
            "query_embeddings": query_embedding,
            "n_results": top_k,
        }
        if filter_metadata:
            kwargs["where"] = filter_metadata

        results = collection.query(**kwargs)

        # Format results
        formatted = []
        if results and results["ids"]:
            for i in range(len(results["ids"][0])):
                formatted.append({
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0,
                    "relevance_score": 1 - (results["distances"][0][i] if results["distances"] else 0),
                })

        return formatted

    async def delete_by_document(self, document_id: str) -> int:
        """Remove all chunks for a document."""
        try:
            collection = ChromaClient.get_collection()
            collection.delete(where={"document_id": document_id})
            logger.info(f"Deleted chunks for document {document_id}")
            return 1
        except Exception as e:
            logger.error(f"Failed to delete chunks: {e}")
            return 0

    async def get_document_count(self) -> int:
        """Get total number of chunks in the vector store."""
        try:
            collection = ChromaClient.get_collection()
            return collection.count()
        except Exception:
            return 0
