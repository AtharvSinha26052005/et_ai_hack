"""Knowledge Graph Builder Agent — Upserts entities and relationships into Neo4j."""

from agents.state import AgentState
from services.knowledge_graph_service import KnowledgeGraphService
from langchain_core.messages import AIMessage
import logging

logger = logging.getLogger(__name__)


async def kg_builder_agent(state: AgentState) -> AgentState:
    """Take extracted entities/relationships and upsert into Neo4j."""
    logger.info(f"KG Builder Agent: Building graph for document {state.get('document_id')}")

    try:
        kg_service = KnowledgeGraphService()

        document_id = state.get("document_id", "")
        entities = state.get("extracted_entities", [])
        relationships = state.get("extracted_relationships", [])

        if not entities:
            return {
                **state,
                "kg_update_status": "no_entities",
                "current_agent": "kg_builder",
                "messages": [AIMessage(content="No entities to add to knowledge graph")],
            }

        # Add entities and relationships to KG
        result = await kg_service.add_document_entities(
            document_id=document_id,
            entities=entities,
            relationships=relationships,
        )

        logger.info(
            f"KG updated: {result['nodes_created']} nodes, "
            f"{result['relationships_created']} relationships"
        )

        return {
            **state,
            "kg_update_status": "success",
            "kg_nodes_created": result["nodes_created"],
            "kg_relationships_created": result["relationships_created"],
            "current_agent": "kg_builder",
            "messages": [
                AIMessage(
                    content=f"Knowledge graph updated: {result['nodes_created']} nodes, "
                    f"{result['relationships_created']} relationships created"
                )
            ],
        }

    except Exception as e:
        logger.error(f"KG builder agent failed: {e}")
        return {
            **state,
            "kg_update_status": f"error: {str(e)}",
            "current_agent": "kg_builder",
            "messages": [AIMessage(content=f"KG build failed: {str(e)}")],
        }
