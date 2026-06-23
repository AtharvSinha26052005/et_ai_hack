"""Ingestion Agent — Document parsing, chunking, and vector storage."""

from agents.state import AgentState
from services.document_processor import DocumentProcessor
from langchain_core.messages import AIMessage
import logging

logger = logging.getLogger(__name__)


async def ingestion_agent(state: AgentState) -> AgentState:
    """Parse and chunk an uploaded document, store in ChromaDB."""
    logger.info(f"Ingestion Agent: Processing document {state.get('document_id')}")

    try:
        processor = DocumentProcessor()
        doc_path = state.get("document_path", "")

        if not doc_path:
            return {
                **state,
                "error": "No document path provided",
                "current_agent": "ingestion",
                "messages": [AIMessage(content="Error: No document path provided")],
            }

        result = await processor.process_file(doc_path)

        return {
            **state,
            "document_text": result.get("text", ""),
            "current_agent": "ingestion",
            "messages": [
                AIMessage(
                    content=f"Document processed: {result.get('page_count', 0)} pages, "
                    f"{result.get('chunk_count', 0)} chunks created"
                )
            ],
        }

    except Exception as e:
        logger.error(f"Ingestion agent failed: {e}")
        return {
            **state,
            "error": str(e),
            "current_agent": "ingestion",
            "messages": [AIMessage(content=f"Ingestion failed: {str(e)}")],
        }
