"""Compliance Agent — Regulatory gap analysis and evidence generation."""

from agents.state import AgentState
from services.knowledge_graph_service import KnowledgeGraphService
from services.llm_service import LLMService
from utils.prompts import COMPLIANCE_ANALYSIS_PROMPT
from langchain_core.messages import AIMessage
import logging

logger = logging.getLogger(__name__)


async def compliance_agent(state: AgentState) -> AgentState:
    """Analyze regulatory compliance gaps using KG traversal + LLM analysis."""
    logger.info("Compliance Agent: Running gap analysis")

    try:
        kg_service = KnowledgeGraphService()
        llm = LLMService()

        # Get compliance gaps from KG
        gaps = await kg_service.find_compliance_gaps()

        # Get failure patterns for context
        from database.neo4j_client import Neo4jClient

        equipment_data = await Neo4jClient.execute_query(
            "MATCH (e:Equipment) RETURN e.tag as tag, e.name as name, e.type as type LIMIT 50"
        )
        regulation_data = await Neo4jClient.execute_query(
            "MATCH (r:Regulation) RETURN r.standard_id as id, r.title as title LIMIT 20"
        )
        procedure_data = await Neo4jClient.execute_query(
            "MATCH (p:Procedure) RETURN p.procedure_id as id, p.title as title LIMIT 20"
        )

        compliance_gaps = []
        for gap in gaps:
            compliance_gaps.append({
                "equipment": gap.get("tag", ""),
                "name": gap.get("name", ""),
                "type": gap.get("type", ""),
                "issue": "No regulatory coverage",
                "severity": "high",
            })

        return {
            **state,
            "compliance_gaps": compliance_gaps,
            "compliance_score": max(0, 100 - len(compliance_gaps) * 5),
            "current_agent": "compliance",
            "messages": [
                AIMessage(
                    content=f"Compliance analysis complete. Found {len(compliance_gaps)} gaps. "
                    f"Compliance score: {max(0, 100 - len(compliance_gaps) * 5)}%"
                )
            ],
        }

    except Exception as e:
        logger.error(f"Compliance agent failed: {e}")
        return {
            **state,
            "current_agent": "compliance",
            "compliance_gaps": [],
            "messages": [AIMessage(content=f"Compliance analysis failed: {str(e)}")],
        }
