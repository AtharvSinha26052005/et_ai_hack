"""Pydantic schemas for knowledge graph API."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class KGNode(BaseModel):
    """A node in the knowledge graph."""
    id: str
    label: str  # Node type (Equipment, Document, etc.)
    properties: Dict[str, Any] = {}


class KGRelationship(BaseModel):
    """A relationship in the knowledge graph."""
    id: str
    type: str  # Relationship type (HAS_DOCUMENT, GOVERNED_BY, etc.)
    source_id: str
    target_id: str
    properties: Dict[str, Any] = {}


class KGStatsResponse(BaseModel):
    """Knowledge graph statistics."""
    total_nodes: int = 0
    total_relationships: int = 0
    nodes_by_type: Dict[str, int] = {}
    relationships_by_type: Dict[str, int] = {}


class KGSubgraphResponse(BaseModel):
    """A subgraph of the knowledge graph for visualization."""
    nodes: List[KGNode] = []
    relationships: List[KGRelationship] = []
    center_node_id: Optional[str] = None


class KGSearchRequest(BaseModel):
    """Search request for the knowledge graph."""
    query: str = Field(..., min_length=1, max_length=500)
    node_types: Optional[List[str]] = None
    limit: int = Field(default=20, ge=1, le=100)


class KGSearchResult(BaseModel):
    """Search result from the knowledge graph."""
    node: KGNode
    score: float = 0.0
    matched_field: str = ""


class KGSearchResponse(BaseModel):
    """Response from knowledge graph search."""
    results: List[KGSearchResult] = []
    total: int = 0
    query: str = ""


class KGNodeDetailResponse(BaseModel):
    """Detailed view of a single node with its relationships."""
    node: KGNode
    connected_nodes: List[KGNode] = []
    relationships: List[KGRelationship] = []
