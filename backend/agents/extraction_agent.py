"""Extraction Agent — Entity and relationship extraction from document text."""

from agents.state import AgentState
from services.entity_extractor import EntityExtractor
from langchain_core.messages import AIMessage
import logging

logger = logging.getLogger(__name__)


async def extraction_agent(state: AgentState) -> AgentState:
    """Extract entities and relationships from document text."""
    logger.info(f"Extraction Agent: Processing document {state.get('document_id')}")

    try:
        extractor = EntityExtractor()
        text = state.get("document_text", "")

        if not text:
            return {
                **state,
                "error": "No document text to extract from",
                "current_agent": "extraction",
                "messages": [AIMessage(content="Error: No text available for extraction")],
            }

        # Extract entities
        entities = await extractor.extract_entities(text)

        # Resolve/deduplicate
        entities = extractor.resolve_entities(entities)

        # Extract relationships
        relationships = await extractor.extract_relationships(text, entities)

        logger.info(
            f"Extracted {len(entities)} entities and {len(relationships)} relationships"
        )

        return {
            **state,
            "extracted_entities": entities,
            "extracted_relationships": relationships,
            "current_agent": "extraction",
            "messages": [
                AIMessage(
                    content=f"Extracted {len(entities)} entities and {len(relationships)} relationships"
                )
            ],
        }

    except Exception as e:
        logger.error(f"Extraction agent failed: {e}")
        return {
            **state,
            "error": str(e),
            "current_agent": "extraction",
            "extracted_entities": [],
            "extracted_relationships": [],
            "messages": [AIMessage(content=f"Extraction failed: {str(e)}")],
        }
