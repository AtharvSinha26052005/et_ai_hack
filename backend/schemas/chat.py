"""Pydantic schemas for chat/RAG API."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SourceCitation(BaseModel):
    """A source reference for a RAG answer."""
    document_id: str
    document_title: str
    page_number: Optional[int] = None
    chunk_text: str = ""
    relevance_score: float = 0.0


class ChatRequest(BaseModel):
    """Request to the RAG chat endpoint."""
    query: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None
    include_graph_context: bool = True
    max_sources: int = Field(default=5, ge=1, le=20)


class ChatResponse(BaseModel):
    """Response from the RAG chat endpoint."""
    answer: str
    sources: List[SourceCitation] = []
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    session_id: str
    graph_context: Optional[dict] = None  # Relevant KG subgraph
    follow_up_questions: List[str] = []
    processing_time_seconds: float = 0.0


class ChatHistoryItem(BaseModel):
    """A single message in chat history."""
    id: str
    role: str
    content: str
    sources: Optional[List[SourceCitation]] = None
    confidence: Optional[float] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatHistoryResponse(BaseModel):
    """Full chat history for a session."""
    session_id: str
    messages: List[ChatHistoryItem]
    total: int


class ChatFeedbackRequest(BaseModel):
    """User feedback on a chat response."""
    message_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
