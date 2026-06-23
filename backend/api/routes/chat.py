"""Chat / Interactive RAG API routes."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.sqlite_client import get_session
from models.database import ChatMessage
from schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatHistoryResponse,
    ChatHistoryItem,
    ChatFeedbackRequest,
    SourceCitation,
)
import uuid
import time
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat_query(
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
):
    """Send a query and get a RAG response with citations."""
    start_time = time.time()
    session_id = request.session_id or str(uuid.uuid4())

    try:
        # Import RAG engine
        from services.rag_engine import RAGEngine

        rag = RAGEngine()
        result = await rag.query(
            query=request.query,
            session_id=session_id,
            include_graph_context=request.include_graph_context,
            max_sources=request.max_sources,
        )

        # Save user message
        user_msg = ChatMessage(
            session_id=session_id,
            role="user",
            content=request.query,
        )
        session.add(user_msg)

        # Save assistant response
        assistant_msg = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=result["answer"],
            sources=json.loads(json.dumps([s.model_dump() for s in result.get("sources", [])])) if result.get("sources") else None,
            confidence=result.get("confidence", 0.0),
        )
        session.add(assistant_msg)
        await session.commit()

        return ChatResponse(
            answer=result["answer"],
            sources=result.get("sources", []),
            confidence=result.get("confidence", 0.0),
            session_id=session_id,
            graph_context=result.get("graph_context"),
            follow_up_questions=result.get("follow_up_questions", []),
            processing_time_seconds=time.time() - start_time,
        )

    except ImportError:
        # RAG engine not yet implemented — return placeholder
        processing_time = time.time() - start_time

        # Save messages anyway
        user_msg = ChatMessage(
            session_id=session_id,
            role="user",
            content=request.query,
        )
        session.add(user_msg)

        assistant_msg = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=f"RAG engine is being set up. Your query: '{request.query}' will be processed once the system is fully configured.",
            confidence=0.0,
        )
        session.add(assistant_msg)
        await session.commit()

        return ChatResponse(
            answer=f"RAG engine is being set up. Your query: '{request.query}' will be processed once the system is fully configured.",
            sources=[],
            confidence=0.0,
            session_id=session_id,
            follow_up_questions=[],
            processing_time_seconds=processing_time,
        )
    except Exception as e:
        logger.error(f"Chat query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket):
    """WebSocket endpoint for streaming chat responses."""
    await websocket.accept()
    session_id = str(uuid.uuid4())

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            query = message.get("query", "")

            if not query:
                await websocket.send_json({"error": "Empty query"})
                continue

            # Send acknowledgment
            await websocket.send_json({
                "type": "ack",
                "session_id": session_id,
            })

            try:
                from services.rag_engine import RAGEngine
                rag = RAGEngine()

                # Stream tokens
                async for token_data in rag.stream_query(query, session_id):
                    await websocket.send_json({
                        "type": "token",
                        "content": token_data.get("token", ""),
                    })

                # Send final response with sources
                result = await rag.query(query, session_id)
                await websocket.send_json({
                    "type": "complete",
                    "answer": result["answer"],
                    "sources": [s.model_dump() for s in result.get("sources", [])],
                    "confidence": result.get("confidence", 0.0),
                    "graph_context": result.get("graph_context"),
                    "follow_up_questions": result.get("follow_up_questions", []),
                })
            except ImportError:
                await websocket.send_json({
                    "type": "complete",
                    "answer": f"RAG engine is being configured. Query received: {query}",
                    "sources": [],
                    "confidence": 0.0,
                    "follow_up_questions": [],
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e),
                })

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get conversation history for a session."""
    result = await session.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    messages = result.scalars().all()

    return ChatHistoryResponse(
        session_id=session_id,
        messages=[ChatHistoryItem.model_validate(msg) for msg in messages],
        total=len(messages),
    )


@router.post("/feedback")
async def submit_feedback(
    request: ChatFeedbackRequest,
    session: AsyncSession = Depends(get_session),
):
    """Submit feedback on a chat response."""
    result = await session.execute(
        select(ChatMessage).where(ChatMessage.id == request.message_id)
    )
    msg = result.scalar_one_or_none()

    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    msg.metadata_json = {
        **(msg.metadata_json or {}),
        "feedback_rating": request.rating,
        "feedback_comment": request.comment,
    }
    await session.commit()

    return {"message": "Feedback submitted", "rating": request.rating}
