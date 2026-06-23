"""Knowledge Graph service — Neo4j CRUD + Cypher queries."""

from database.neo4j_client import Neo4jClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class KnowledgeGraphService:
    """High-level service for knowledge graph operations."""

    async def upsert_node(
        self,
        label: str,
        properties: dict,
        unique_key: str,
    ) -> str:
        """Create or merge a node in Neo4j."""
        unique_value = properties.get(unique_key)
        if not unique_value:
            raise ValueError(f"Missing unique key '{unique_key}' in properties")

        # Build property string
        prop_items = ", ".join(
            f"n.{k} = ${k}" for k in properties.keys()
        )

        query = f"""
        MERGE (n:{label} {{{unique_key}: ${unique_key}}})
        SET {prop_items}
        RETURN elementId(n) as id
        """

        results = await Neo4jClient.execute_query(query, properties)
        node_id = results[0]["id"] if results else None
        logger.debug(f"Upserted {label} node: {unique_value} -> {node_id}")
        return node_id

    async def upsert_relationship(
        self,
        source_label: str,
        source_key: str,
        source_value: str,
        target_label: str,
        target_key: str,
        target_value: str,
        rel_type: str,
        properties: dict = None,
    ) -> None:
        """Create a relationship between two nodes."""
        prop_str = ""
        params = {
            "source_val": source_value,
            "target_val": target_value,
        }

        if properties:
            prop_items = ", ".join(f"r.{k} = ${k}" for k in properties.keys())
            prop_str = f"SET {prop_items}"
            params.update(properties)

        query = f"""
        MATCH (a:{source_label} {{{source_key}: $source_val}})
        MATCH (b:{target_label} {{{target_key}: $target_val}})
        MERGE (a)-[r:{rel_type}]->(b)
        {prop_str}
        """

        await Neo4jClient.execute_write(query, params)
        logger.debug(f"Upserted relationship: {source_value} -[{rel_type}]-> {target_value}")

    async def query_subgraph(
        self,
        center_label: str,
        center_key: str,
        center_value: str,
        depth: int = 2,
        limit: int = 100,
    ) -> dict:
        """N-hop traversal from a center node."""
        query = f"""
        MATCH (center:{center_label} {{{center_key}: $value}})
        CALL apoc.path.subgraphAll(center, {{maxLevel: $depth}})
        YIELD nodes, relationships
        RETURN nodes, relationships
        """

        try:
            results = await Neo4jClient.execute_query(
                query, {"value": center_value, "depth": depth}
            )

            if results:
                return {
                    "nodes": results[0].get("nodes", [])[:limit],
                    "relationships": results[0].get("relationships", []),
                }
        except Exception:
            # Fallback without APOC
            fallback_query = f"""
            MATCH path = (center:{center_label} {{{center_key}: $value}})-[*1..{depth}]-(connected)
            WITH nodes(path) as ns, relationships(path) as rs
            UNWIND ns as n
            WITH collect(DISTINCT n) as allNodes, rs
            UNWIND rs as r
            RETURN collect(DISTINCT allNodes) as nodes, collect(DISTINCT r) as relationships
            """
            results = await Neo4jClient.execute_query(
                fallback_query, {"value": center_value}
            )

        return {"nodes": [], "relationships": []}

    async def search_nodes(
        self, query: str, node_types: list = None, limit: int = 20
    ) -> list:
        """Full-text search across the knowledge graph."""
        search_results = []

        indexes = ["equipment_search", "document_search", "regulation_search"]
        for index in indexes:
            try:
                results = await Neo4jClient.execute_query(
                    f"""
                    CALL db.index.fulltext.queryNodes('{index}', $query)
                    YIELD node, score
                    RETURN elementId(node) as id, labels(node) as labels,
                           properties(node) as props, score
                    ORDER BY score DESC
                    LIMIT $limit
                    """,
                    {"query": query, "limit": limit},
                )
                search_results.extend(results)
            except Exception as e:
                logger.warning(f"Search on index {index} failed: {e}")

        # Sort by score and deduplicate
        seen = set()
        unique_results = []
        for r in sorted(search_results, key=lambda x: x.get("score", 0), reverse=True):
            rid = str(r["id"])
            if rid not in seen:
                unique_results.append(r)
                seen.add(rid)

        if node_types:
            unique_results = [
                r for r in unique_results
                if r["labels"][0] in node_types
            ]

        return unique_results[:limit]

    async def get_stats(self) -> dict:
        """Get aggregate statistics."""
        try:
            node_query = """
            MATCH (n)
            RETURN labels(n)[0] as label, count(n) as count
            """
            rel_query = """
            MATCH ()-[r]->()
            RETURN type(r) as type, count(r) as count
            """

            node_results = await Neo4jClient.execute_query(node_query)
            rel_results = await Neo4jClient.execute_query(rel_query)

            nodes_by_type = {r["label"]: r["count"] for r in node_results}
            rels_by_type = {r["type"]: r["count"] for r in rel_results}

            return {
                "total_nodes": sum(nodes_by_type.values()),
                "total_relationships": sum(rels_by_type.values()),
                "nodes_by_type": nodes_by_type,
                "relationships_by_type": rels_by_type,
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                "total_nodes": 0,
                "total_relationships": 0,
                "nodes_by_type": {},
                "relationships_by_type": {},
            }

    async def find_compliance_gaps(self) -> list:
        """Find equipment without required regulatory links."""
        query = """
        MATCH (e:Equipment)
        WHERE NOT (e)-[:GOVERNED_BY]->(:Regulation)
        RETURN e.tag as tag, e.name as name, e.type as type
        ORDER BY e.tag
        """
        return await Neo4jClient.execute_query(query)

    async def get_failure_patterns(self) -> list:
        """Get most common failure mode → equipment correlations."""
        query = """
        MATCH (e:Equipment)-[:HAS_FAILURE_MODE]->(fm:FailureMode)
        WITH fm, collect(DISTINCT e.tag) as equipment, count(e) as count
        WHERE count > 1
        RETURN fm.code as code, fm.description as description,
               fm.severity as severity, equipment, count
        ORDER BY count DESC
        LIMIT 20
        """
        return await Neo4jClient.execute_query(query)

    async def get_equipment_history(self, equipment_tag: str) -> list:
        """Full maintenance timeline for an equipment tag."""
        query = """
        MATCH (e:Equipment {tag: $tag})-[:HAS_MAINTENANCE]->(m:MaintenanceRecord)
        OPTIONAL MATCH (m)-[:PERFORMED_BY]->(p:Personnel)
        OPTIONAL MATCH (m)-[:CAUSED_BY]->(fm:FailureMode)
        RETURN m.work_order_id as work_order_id,
               m.type as type, m.date as date,
               m.status as status, m.description as description,
               collect(DISTINCT p.name) as personnel,
               collect(DISTINCT fm.description) as failure_modes
        ORDER BY m.date DESC
        """
        return await Neo4jClient.execute_query(query, {"tag": equipment_tag})

    async def add_document_entities(
        self,
        document_id: str,
        entities: list[dict],
        relationships: list[dict],
    ) -> dict:
        """Add extracted entities and relationships from a document to the KG."""
        node_count = 0
        rel_count = 0

        # First, ensure the Document node exists
        await self.upsert_node(
            "Document",
            {"doc_id": document_id, "title": document_id},
            "doc_id",
        )

        # Create entity nodes
        for entity in entities:
            entity_type = entity.get("type", "Entity")
            text = entity.get("text", "")

            if entity_type == "EQUIPMENT":
                await self.upsert_node("Equipment", {"tag": text, "name": text}, "tag")
                await self.upsert_relationship(
                    "Document", "doc_id", document_id,
                    "Equipment", "tag", text,
                    "MENTIONS",
                )
            elif entity_type == "REGULATION":
                await self.upsert_node("Regulation", {"standard_id": text, "title": text}, "standard_id")
                await self.upsert_relationship(
                    "Document", "doc_id", document_id,
                    "Regulation", "standard_id", text,
                    "REFERENCES",
                )
            elif entity_type == "PERSONNEL":
                await self.upsert_node("Personnel", {"employee_id": text, "name": text}, "employee_id")
            elif entity_type == "FAILURE_MODE":
                await self.upsert_node("FailureMode", {"code": text, "description": text}, "code")
            elif entity_type == "PROCEDURE":
                await self.upsert_node("Procedure", {"procedure_id": text, "title": text}, "procedure_id")

            node_count += 1

        # Create explicit relationships
        for rel in relationships:
            try:
                source = rel.get("source", "")
                target = rel.get("target", "")
                rel_type = rel.get("type", "RELATED_TO")
                source_type = rel.get("source_type", "")
                target_type = rel.get("target_type", "")

                if source and target:
                    # Map entity types to Neo4j labels and keys
                    source_label, source_key = self._map_entity_to_label(source_type)
                    target_label, target_key = self._map_entity_to_label(target_type)

                    await self.upsert_relationship(
                        source_label, source_key, source,
                        target_label, target_key, target,
                        rel_type,
                    )
                    rel_count += 1
            except Exception as e:
                logger.warning(f"Failed to create relationship: {e}")

        return {"nodes_created": node_count, "relationships_created": rel_count}

    def _map_entity_to_label(self, entity_type: str) -> tuple[str, str]:
        """Map entity type to Neo4j label and unique key."""
        mapping = {
            "EQUIPMENT": ("Equipment", "tag"),
            "DOCUMENT": ("Document", "doc_id"),
            "REGULATION": ("Regulation", "standard_id"),
            "PERSONNEL": ("Personnel", "employee_id"),
            "FAILURE_MODE": ("FailureMode", "code"),
            "PROCEDURE": ("Procedure", "procedure_id"),
            "PROCESS_PARAMETER": ("ProcessParameter", "name"),
        }
        return mapping.get(entity_type, ("Entity", "name"))
