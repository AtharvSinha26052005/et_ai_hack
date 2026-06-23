"""LangGraph Orchestrator — Supervisor-Worker pattern for multi-agent coordination."""

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from agents.state import AgentState
from agents.ingestion_agent import ingestion_agent
from agents.extraction_agent import extraction_agent
from agents.kg_builder_agent import kg_builder_agent
from agents.query_agent import query_agent
from agents.compliance_agent import compliance_agent
from agents.maintenance_agent import maintenance_agent
from services.llm_service import LLMService
from utils.prompts import SUPERVISOR_ROUTING_PROMPT
import logging

logger = logging.getLogger(__name__)


async def supervisor_agent(state: AgentState) -> AgentState:
    """Supervisor agent — routes requests to appropriate worker agents."""
    messages = state.get("messages", [])

    # Get the latest user message
    user_message = ""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            user_message = msg.content
            break

    if not user_message:
        return {**state, "next_agent": "FINISH", "current_agent": "supervisor"}

    # Route based on content analysis
    try:
        llm = LLMService()
        prompt = SUPERVISOR_ROUTING_PROMPT.format(request=user_message)
        route = await llm.generate(prompt)
        route = route.strip().lower()

        # Validate route
        valid_routes = {"ingestion", "query", "compliance", "maintenance", "finish"}
        if route not in valid_routes:
            route = "query"  # Default to query agent

        logger.info(f"Supervisor routing to: {route}")

    except Exception as e:
        logger.warning(f"Supervisor routing failed, defaulting to query: {e}")
        route = "query"

    return {**state, "next_agent": route, "current_agent": "supervisor"}


def route_to_agent(state: AgentState) -> str:
    """Conditional routing function for LangGraph."""
    next_agent = state.get("next_agent", "FINISH")
    if next_agent == "finish":
        return "FINISH"
    return next_agent


def create_workflow():
    """Build and compile the LangGraph workflow."""
    workflow = StateGraph(AgentState)

    # Add nodes (agents)
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("ingestion", ingestion_agent)
    workflow.add_node("extraction", extraction_agent)
    workflow.add_node("kg_builder", kg_builder_agent)
    workflow.add_node("query", query_agent)
    workflow.add_node("compliance", compliance_agent)
    workflow.add_node("maintenance", maintenance_agent)

    # Entry point
    workflow.set_entry_point("supervisor")

    # Conditional routing from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "ingestion": "ingestion",
            "query": "query",
            "compliance": "compliance",
            "maintenance": "maintenance",
            "FINISH": END,
        },
    )

    # Ingestion pipeline: sequential chain
    workflow.add_edge("ingestion", "extraction")
    workflow.add_edge("extraction", "kg_builder")
    workflow.add_edge("kg_builder", END)

    # Other agents return directly
    workflow.add_edge("query", END)
    workflow.add_edge("compliance", END)
    workflow.add_edge("maintenance", END)

    # Compile
    compiled = workflow.compile()
    logger.info("LangGraph workflow compiled successfully")

    return compiled


# Export compiled workflow
try:
    agent_workflow = create_workflow()
except Exception as e:
    logger.error(f"Failed to compile LangGraph workflow: {e}")
    agent_workflow = None
