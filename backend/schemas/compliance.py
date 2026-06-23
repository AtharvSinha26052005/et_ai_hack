"""Pydantic schemas for compliance API."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class GapSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ComplianceGap(BaseModel):
    """A single compliance gap identified."""
    id: str
    regulation_id: str
    regulation_title: str
    requirement: str
    gap_description: str
    severity: GapSeverity
    affected_equipment: List[str] = []
    evidence: List[str] = []  # Document references
    recommendation: str = ""


class ComplianceAnalyzeRequest(BaseModel):
    """Request to analyze compliance against a regulation."""
    regulation_id: Optional[str] = None  # Specific regulation or all
    equipment_tags: Optional[List[str]] = None  # Filter by equipment
    include_evidence: bool = True


class ComplianceAnalyzeResponse(BaseModel):
    """Response from compliance analysis."""
    total_gaps: int = 0
    gaps_by_severity: dict = {}
    gaps: List[ComplianceGap] = []
    compliance_score: float = Field(default=0.0, ge=0.0, le=100.0)
    analysis_timestamp: datetime
    processing_time_seconds: float = 0.0


class RegulationSummary(BaseModel):
    """Summary of a regulation in the knowledge graph."""
    standard_id: str
    title: str
    body: Optional[str] = None
    version: Optional[str] = None
    status: Optional[str] = None
    equipment_count: int = 0  # How many equipment items are governed
    gap_count: int = 0


class ComplianceReportResponse(BaseModel):
    """Full compliance report."""
    report_id: str
    generated_at: datetime
    total_regulations: int
    total_gaps: int
    overall_score: float
    gaps: List[ComplianceGap] = []
    regulations: List[RegulationSummary] = []
