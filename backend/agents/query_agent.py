"""Query Agent — Interactive RAG with hybrid retrieval."""

from agents.state import AgentState
from services.rag_engine import RAGEngine
from langchain_core.messages import AIMessage, HumanMessage
import logging

logger = logging.getLogger(__name__)


async def query_agent(state: AgentState) -> AgentState:
    """Handle user queries with hybrid retrieval (vector + graph)."""
    logger.info("Query Agent: Processing user query")

    try:
        rag = RAGEngine()

        # Get the latest user message
        messages = state.get("messages", [])
        query = ""
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                query = msg.content
                break

        if not query:
            return {
                **state,
                "current_agent": "query",
                "messages": [AIMessage(content="No query found in messages")],
            }

        # Execute RAG query
        result = await rag.query(query=query, session_id="agent_session")

        return {
            **state,
            "retrieval_results": [
                {"source": s.document_title, "text": s.chunk_text, "score": s.relevance_score}
                for s in result.get("sources", [])
            ],
            "current_agent": "query",
            "messages": [AIMessage(content=result["answer"])],
        }

    except Exception as e:
        logger.error(f"Query agent failed: {e}")
        return {
            **state,
            "current_agent": "query",
            "messages": [AIMessage(content=f"Query failed: {str(e)}")],
        }
