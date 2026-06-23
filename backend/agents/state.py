"""Shared agent state definitions for LangGraph workflows."""

from typing import TypedDict, Optional, Annotated
from langgraph.graph import add_messages


class AgentState(TypedDict):
    """Shared state across all agents in the LangGraph workflow."""

    # Message history (LangGraph managed)
    messages: Annotated[list, add_messages]

    # Document processing
    document_id: Optional[str]
    document_path: Optional[str]
    document_text: Optional[str]

    # Entity extraction results
    extracted_entities: list[dict]
    extracted_relationships: list[dict]

    # Knowledge graph update status
    kg_update_status: Optional[str]
    kg_nodes_created: int
    kg_relationships_created: int

    # Retrieval results (for RAG)
    retrieval_results: list[dict]
    retrieval_context: Optional[str]

    # Compliance analysis
    compliance_gaps: list[dict]
    compliance_score: Optional[float]

    # Maintenance intelligence
    maintenance_recommendations: list[dict]
    failure_patterns: list[dict]

    # Routing
    current_agent: str
    next_agent: Optional[str]

    # Error handling
    error: Optional[str]
