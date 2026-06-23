"""SQLAlchemy ORM models for document metadata and audit logging."""

from sqlalchemy import Column, String, Integer, DateTime, Text, Float, JSON, Enum as SAEnum
from sqlalchemy.sql import func
from database.sqlite_client import Base
import enum
import uuid


class DocumentStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class DocumentType(str, enum.Enum):
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


class Document(Base):
    """Document metadata stored in SQLite."""

    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=True)

    # Classification
    doc_type = Column(SAEnum(DocumentType), default=DocumentType.OTHER)
    status = Column(SAEnum(DocumentStatus), default=DocumentStatus.UPLOADED)

    # Processing results
    page_count = Column(Integer, default=0)
    chunk_count = Column(Integer, default=0)
    entity_count = Column(Integer, default=0)
    text_preview = Column(Text, nullable=True)  # First 500 chars

    # Processing metadata
    processing_time_seconds = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    metadata_json = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AuditLog(Base):
    """Audit trail for all system actions."""

    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    action = Column(String, nullable=False)  # e.g., "document_upload", "query", "kg_update"
    entity_type = Column(String, nullable=True)  # e.g., "document", "equipment"
    entity_id = Column(String, nullable=True)
    details = Column(JSON, nullable=True)
    user = Column(String, default="system")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ChatMessage(Base):
    """Stores chat conversation history."""

    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    sources = Column(JSON, nullable=True)  # Source citations
    confidence = Column(Float, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
