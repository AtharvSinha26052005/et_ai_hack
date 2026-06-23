"""Pydantic schemas for document API requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class DocumentType(str, Enum):
    EQUIPMENT_MANUAL = "equipment_manual"
    MAINTENANCE_RECORD = "maintenance_record"
    INSPECTION_REPORT = "inspection_report"
    SAFETY_PROCEDURE = "safety_procedure"
    REGULATORY = "regulatory"
    PID_DRAWING = "pid_drawing"
    WORK_ORDER = "work_order"
    SOP = "sop"
    INCIDENT_REPORT = "incident_report"
    OTHER = "other"


class DocumentResponse(BaseModel):
    """Response schema for a single document."""
    id: str
    filename: str
    original_filename: str
    file_size: int
    mime_type: Optional[str] = None
    doc_type: DocumentType = DocumentType.OTHER
    status: DocumentStatus = DocumentStatus.UPLOADED
    page_count: int = 0
    chunk_count: int = 0
    entity_count: int = 0
    text_preview: Optional[str] = None
    processing_time_seconds: Optional[float] = None
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class DocumentListResponse(BaseModel):
    """Response schema for listing documents."""
    documents: List[DocumentResponse]
    total: int
    page: int = 1
    page_size: int = 20


class DocumentUploadResponse(BaseModel):
    """Response after uploading a document."""
    id: str
    filename: str
    status: DocumentStatus
    message: str


class DocumentEntityResponse(BaseModel):
    """Entities extracted from a document."""
    document_id: str
    entities: List[dict]
    relationships: List[dict]
    total_entities: int
    total_relationships: int
