"""Maintenance Intelligence Agent — RCA and predictive recommendations."""

from agents.state import AgentState
from services.knowledge_graph_service import KnowledgeGraphService
from langchain_core.messages import AIMessage
import logging

logger = logging.getLogger(__name__)


async def maintenance_agent(state: AgentState) -> AgentState:
    """Analyze maintenance patterns, perform RCA, and generate recommendations."""
    logger.info("Maintenance Agent: Analyzing maintenance intelligence")

    try:
        kg_service = KnowledgeGraphService()

        # Get failure patterns across equipment
        patterns = await kg_service.get_failure_patterns()

        # Get compliance gaps (equipment needing attention)
        gaps = await kg_service.find_compliance_gaps()

        recommendations = []
        for pattern in patterns:
            recommendations.append({
                "failure_code": pattern.get("code", ""),
                "description": pattern.get("description", ""),
                "severity": pattern.get("severity", "medium"),
                "affected_equipment": pattern.get("equipment", []),
                "recommendation": f"Investigate recurring failure: {pattern.get('description', '')}",
            })

        return {
            **state,
            "maintenance_recommendations": recommendations,
            "failure_patterns": patterns,
            "current_agent": "maintenance",
            "messages": [
                AIMessage(
                    content=f"Maintenance analysis complete. "
                    f"Found {len(patterns)} failure patterns, "
                    f"generated {len(recommendations)} recommendations."
                )
            ],
        }

    except Exception as e:
        logger.error(f"Maintenance agent failed: {e}")
        return {
            **state,
            "current_agent": "maintenance",
            "maintenance_recommendations": [],
            "failure_patterns": [],
            "messages": [AIMessage(content=f"Maintenance analysis failed: {str(e)}")],
        }
