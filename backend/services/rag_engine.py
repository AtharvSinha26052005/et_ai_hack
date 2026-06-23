"""RAG Engine — Hybrid retrieval combining vector search and graph traversal."""

from services.vector_store_service import VectorStoreService
from services.knowledge_graph_service import KnowledgeGraphService
from services.llm_service import LLMService
from schemas.chat import SourceCitation
from utils.prompts import RAG_QUERY_PROMPT, FOLLOW_UP_PROMPT
import logging
import json

logger = logging.getLogger(__name__)


class RAGEngine:
    """Core RAG engine with hybrid retrieval (vector + graph)."""

    def __init__(self):
        self.vector_store = VectorStoreService()
        self.kg_service = KnowledgeGraphService()
        self.llm = LLMService()
        self._conversation_memory: dict[str, list] = {}  # session_id -> messages

    async def query(
        self,
        query: str,
        session_id: str = "",
        include_graph_context: bool = True,
        max_sources: int = 5,
    ) -> dict:
        """Execute a hybrid RAG query — vector search + graph traversal + LLM generation."""

        # 1. Vector retrieval
        vector_results = await self._vector_search(query, top_k=max_sources)

        # 2. Graph retrieval
        graph_results = []
        graph_context = None
        if include_graph_context:
            graph_results, graph_context = await self._graph_search(query)

        # 3. Merge and build context
        context = self._build_context(vector_results, graph_results)

        # 4. Get conversation memory
        memory = self._conversation_memory.get(session_id, [])[-10:]

        # 5. Generate answer with LLM
        prompt = RAG_QUERY_PROMPT.format(
            context=context,
            conversation_history=self._format_memory(memory),
            question=query,
        )

        answer = await self.llm.generate(prompt)

        # 6. Calculate confidence
        confidence = self._calculate_confidence(vector_results, graph_results, answer)

        # 7. Build source citations
        sources = self._build_citations(vector_results)

        # 8. Generate follow-up questions
        follow_ups = await self._generate_follow_ups(query, answer)

        # 9. Update conversation memory
        if session_id:
            if session_id not in self._conversation_memory:
                self._conversation_memory[session_id] = []
            self._conversation_memory[session_id].append(
                {"role": "user", "content": query}
            )
            self._conversation_memory[session_id].append(
                {"role": "assistant", "content": answer}
            )

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "graph_context": graph_context,
            "follow_up_questions": follow_ups,
        }

    async def stream_query(self, query: str, session_id: str = ""):
        """Stream a RAG response token by token."""
        # Get context first
        vector_results = await self._vector_search(query, top_k=5)
        graph_results, _ = await self._graph_search(query)
        context = self._build_context(vector_results, graph_results)
        memory = self._conversation_memory.get(session_id, [])[-10:]

        prompt = RAG_QUERY_PROMPT.format(
            context=context,
            conversation_history=self._format_memory(memory),
            question=query,
        )

        async for token_data in self.llm.stream_generate(prompt):
            yield token_data

    async def _vector_search(self, query: str, top_k: int = 5) -> list[dict]:
        """Semantic search over document chunks."""
        try:
            results = await self.vector_store.similarity_search(query, top_k=top_k)
            return results
        except Exception as e:
            logger.warning(f"Vector search failed: {e}")
            return []

    async def _graph_search(self, query: str) -> tuple[list, dict | None]:
        """Knowledge graph traversal for structured facts."""
        try:
            # Search for relevant entities in the query
            search_results = await self.kg_service.search_nodes(query, limit=10)

            graph_facts = []
            graph_context = {"nodes": [], "relationships": []}

            for result in search_results[:3]:  # Top 3 nodes
                node_id = result.get("id", "")
                props = result.get("props", {})
                labels = result.get("labels", [])

                graph_facts.append({
                    "type": labels[0] if labels else "Unknown",
                    "properties": props,
                })

                # Add to graph context for visualization
                graph_context["nodes"].append({
                    "id": str(node_id),
                    "label": labels[0] if labels else "Unknown",
                    "properties": props,
                })

            return graph_facts, graph_context if graph_context["nodes"] else None

        except Exception as e:
            logger.warning(f"Graph search failed: {e}")
            return [], None

    def _build_context(
        self, vector_results: list[dict], graph_results: list[dict]
    ) -> str:
        """Merge and format retrieval results into context string."""
        context_parts = []

        # Vector results
        if vector_results:
            context_parts.append("=== Document Excerpts ===")
            for i, r in enumerate(vector_results, 1):
                source = r.get("metadata", {}).get("source", "Unknown")
                text = r.get("text", "")
                score = r.get("relevance_score", 0)
                context_parts.append(
                    f"[Source {i}: {source} (relevance: {score:.2f})]\n{text}"
                )

        # Graph results
        if graph_results:
            context_parts.append("\n=== Knowledge Graph Facts ===")
            for fact in graph_results:
                fact_type = fact.get("type", "Unknown")
                props = fact.get("properties", {})
                props_str = ", ".join(f"{k}: {v}" for k, v in props.items() if v)
                context_parts.append(f"[{fact_type}] {props_str}")

        return "\n\n".join(context_parts) if context_parts else "No relevant context found."

    def _build_citations(self, vector_results: list[dict]) -> list[SourceCitation]:
        """Build source citation objects from retrieval results."""
        citations = []
        for r in vector_results:
            metadata = r.get("metadata", {})
            citations.append(SourceCitation(
                document_id=metadata.get("document_id", ""),
                document_title=metadata.get("source", "Unknown Document"),
                page_number=metadata.get("page_number"),
                chunk_text=r.get("text", "")[:200],
                relevance_score=r.get("relevance_score", 0),
            ))
        return citations

    def _calculate_confidence(
        self,
        vector_results: list[dict],
        graph_results: list[dict],
        answer: str,
    ) -> float:
        """Calculate confidence score based on retrieval quality."""
        if not vector_results and not graph_results:
            return 0.1

        # Base confidence from vector similarity scores
        if vector_results:
            avg_score = sum(
                r.get("relevance_score", 0) for r in vector_results
            ) / len(vector_results)
        else:
            avg_score = 0.3

        # Boost for graph results
        if graph_results:
            avg_score = min(1.0, avg_score + 0.1 * len(graph_results))

        # Reduce if answer contains uncertainty markers
        uncertainty_markers = [
            "i'm not sure", "i don't know", "unclear",
            "no information", "cannot determine",
        ]
        for marker in uncertainty_markers:
            if marker in answer.lower():
                avg_score *= 0.5
                break

        return round(min(1.0, max(0.0, avg_score)), 2)

    async def _generate_follow_ups(
        self, query: str, answer: str
    ) -> list[str]:
        """Generate suggested follow-up questions."""
        try:
            prompt = FOLLOW_UP_PROMPT.format(
                question=query,
                answer=answer[:500],
            )
            response = await self.llm.generate(prompt)

            # Parse response — expect numbered list
            follow_ups = []
            for line in response.strip().split("\n"):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith("-")):
                    # Remove numbering
                    clean = line.lstrip("0123456789.-) ").strip()
                    if clean:
                        follow_ups.append(clean)

            return follow_ups[:3]
        except Exception as e:
            logger.warning(f"Follow-up generation failed: {e}")
            return []

    def _format_memory(self, memory: list[dict]) -> str:
        """Format conversation memory for the prompt."""
        if not memory:
            return "No previous conversation."

        formatted = []
        for msg in memory[-6:]:  # Last 3 exchanges
            role = msg["role"].capitalize()
            content = msg["content"][:300]
            formatted.append(f"{role}: {content}")

        return "\n".join(formatted)
