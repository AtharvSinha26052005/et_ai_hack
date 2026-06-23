"""Document upload and management API routes."""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from database.sqlite_client import get_session
from models.database import Document, DocumentStatus, DocumentType
from schemas.document import (
    DocumentResponse,
    DocumentListResponse,
    DocumentUploadResponse,
    DocumentEntityResponse,
)
from config.settings import settings
import os
import uuid
import logging
import time
import aiofiles

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])


async def _save_upload_file(upload_file: UploadFile, doc_id: str) -> tuple[str, int]:
    """Save uploaded file to disk. Returns (file_path, file_size)."""
    upload_dir = os.path.abspath(settings.upload_dir)
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    ext = os.path.splitext(upload_file.filename)[1] if upload_file.filename else ""
    filename = f"{doc_id}{ext}"
    file_path = os.path.join(upload_dir, filename)

    # Stream write
    file_size = 0
    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await upload_file.read(1024 * 1024):  # 1MB chunks
            await f.write(chunk)
            file_size += len(chunk)

    return file_path, file_size, filename


async def _process_document_background(doc_id: str):
    """Background task to process an uploaded document through the ingestion pipeline."""
    # This will be wired to the LangGraph ingestion pipeline in Phase 5
    # For now, just mark as processed
    from database.sqlite_client import async_session_factory

    async with async_session_factory() as session:
        result = await session.execute(select(Document).where(Document.id == doc_id))
        doc = result.scalar_one_or_none()
        if doc:
            try:
                # Import and run the ingestion pipeline
                from services.document_processor import DocumentProcessor

                processor = DocumentProcessor()
                start_time = time.time()

                # Process the document
                process_result = await processor.process_file(doc.file_path)

                doc.status = DocumentStatus.PROCESSED
                doc.page_count = process_result.get("page_count", 0)
                doc.chunk_count = process_result.get("chunk_count", 0)
                doc.entity_count = process_result.get("entity_count", 0)
                doc.text_preview = process_result.get("text_preview", "")[:500]
                doc.doc_type = process_result.get("doc_type", DocumentType.OTHER)
                doc.processing_time_seconds = time.time() - start_time

                await session.commit()
                logger.info(f"Document {doc_id} processed successfully")

            except Exception as e:
                doc.status = DocumentStatus.FAILED
                doc.error_message = str(e)
                await session.commit()
                logger.error(f"Failed to process document {doc_id}: {e}")


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    """Upload a document and trigger background processing."""
    # Validate file type
    allowed_types = {
        ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".csv",
        ".txt", ".png", ".jpg", ".jpeg", ".tiff", ".bmp",
    }
    ext = os.path.splitext(file.filename)[1].lower() if file.filename else ""
    if ext not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' not supported. Allowed: {', '.join(sorted(allowed_types))}",
        )

    doc_id = str(uuid.uuid4())

    # Save file
    file_path, file_size, filename = await _save_upload_file(file, doc_id)

    # Create document record
    doc = Document(
        id=doc_id,
        filename=filename,
        original_filename=file.filename or "unknown",
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type,
        status=DocumentStatus.PROCESSING,
    )

    session.add(doc)
    await session.commit()

    # Trigger background processing
    background_tasks.add_task(_process_document_background, doc_id)

    return DocumentUploadResponse(
        id=doc_id,
        filename=file.filename or "unknown",
        status=DocumentStatus.PROCESSING,
        message="Document uploaded and processing started",
    )


@router.post("/batch-upload", response_model=List[DocumentUploadResponse])
async def batch_upload_documents(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session),
):
    """Upload multiple documents at once."""
    results = []
    for file in files:
        try:
            doc_id = str(uuid.uuid4())
            ext = os.path.splitext(file.filename)[1].lower() if file.filename else ""

            file_path, file_size, filename = await _save_upload_file(file, doc_id)

            doc = Document(
                id=doc_id,
                filename=filename,
                original_filename=file.filename or "unknown",
                file_path=file_path,
                file_size=file_size,
                mime_type=file.content_type,
                status=DocumentStatus.PROCESSING,
            )
            session.add(doc)

            background_tasks.add_task(_process_document_background, doc_id)

            results.append(DocumentUploadResponse(
                id=doc_id,
                filename=file.filename or "unknown",
                status=DocumentStatus.PROCESSING,
                message="Document uploaded and processing started",
            ))
        except Exception as e:
            results.append(DocumentUploadResponse(
                id="",
                filename=file.filename or "unknown",
                status=DocumentStatus.FAILED,
                message=f"Upload failed: {str(e)}",
            ))

    await session.commit()
    return results


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    page: int = 1,
    page_size: int = 20,
    doc_type: Optional[str] = None,
    status: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    """List all uploaded documents with pagination and filters."""
    query = select(Document).order_by(Document.created_at.desc())

    if doc_type:
        query = query.where(Document.doc_type == doc_type)
    if status:
        query = query.where(Document.status == status)

    # Count total
    count_query = select(func.count()).select_from(Document)
    if doc_type:
        count_query = count_query.where(Document.doc_type == doc_type)
    if status:
        count_query = count_query.where(Document.status == status)

    total_result = await session.execute(count_query)
    total = total_result.scalar() or 0

    # Paginate
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await session.execute(query)
    documents = result.scalars().all()

    return DocumentListResponse(
        documents=[DocumentResponse.model_validate(doc) for doc in documents],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{doc_id}", response_model=DocumentResponse)
async def get_document(
    doc_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get document details by ID."""
    result = await session.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentResponse.model_validate(doc)


@router.delete("/{doc_id}")
async def delete_document(
    doc_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Delete a document and its associated KG entities."""
    result = await session.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete file from disk
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    # Delete from ChromaDB
    try:
        from database.chroma_client import ChromaClient
        collection = ChromaClient.get_collection()
        collection.delete(where={"document_id": doc_id})
    except Exception as e:
        logger.warning(f"Failed to clean up ChromaDB for {doc_id}: {e}")

    # Delete from Neo4j
    try:
        from database.neo4j_client import Neo4jClient
        await Neo4jClient.execute_write(
            "MATCH (d:Document {doc_id: $doc_id}) DETACH DELETE d",
            {"doc_id": doc_id},
        )
    except Exception as e:
        logger.warning(f"Failed to clean up Neo4j for {doc_id}: {e}")

    # Delete from SQLite
    await session.delete(doc)
    await session.commit()

    return {"message": f"Document {doc_id} deleted successfully"}


@router.get("/{doc_id}/entities", response_model=DocumentEntityResponse)
async def get_document_entities(doc_id: str):
    """Get entities extracted from a document."""
    try:
        from database.neo4j_client import Neo4jClient

        # Query entities linked to this document
        entities = await Neo4jClient.execute_query(
            """
            MATCH (d:Document {doc_id: $doc_id})-[r]-(n)
            RETURN labels(n)[0] as label, properties(n) as props,
                   type(r) as rel_type, properties(r) as rel_props
            """,
            {"doc_id": doc_id},
        )

        entity_list = []
        rel_list = []
        seen = set()

        for record in entities:
            node_key = f"{record['label']}:{record['props'].get('tag', record['props'].get('name', ''))}"
            if node_key not in seen:
                entity_list.append({
                    "type": record["label"],
                    "properties": record["props"],
                })
                seen.add(node_key)

            rel_list.append({
                "type": record["rel_type"],
                "properties": record["rel_props"],
            })

        return DocumentEntityResponse(
            document_id=doc_id,
            entities=entity_list,
            relationships=rel_list,
            total_entities=len(entity_list),
            total_relationships=len(rel_list),
        )
    except Exception as e:
        logger.error(f"Failed to get entities for {doc_id}: {e}")
        return DocumentEntityResponse(
            document_id=doc_id,
            entities=[],
            relationships=[],
            total_entities=0,
            total_relationships=0,
        )
