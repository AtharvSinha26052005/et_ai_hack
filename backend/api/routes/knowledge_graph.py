"""Knowledge Graph API routes."""

from fastapi import APIRouter, HTTPException, Query
from database.neo4j_client import Neo4jClient
from schemas.knowledge_graph import (
    KGStatsResponse,
    KGNode,
    KGRelationship,
    KGSubgraphResponse,
    KGSearchResponse,
    KGSearchResult,
    KGNodeDetailResponse,
)
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/kg", tags=["knowledge-graph"])


@router.get("/stats", response_model=KGStatsResponse)
async def get_kg_stats():
    """Get knowledge graph statistics — node/relationship counts by type."""
    try:
        # Node counts by label
        node_results = await Neo4jClient.execute_query(
            """
            CALL db.labels() YIELD label
            CALL apoc.cypher.run('MATCH (n:`' + label + '`) RETURN count(n) as count', {}) YIELD value
            RETURN label, value.count as count
            """
        )

        nodes_by_type = {}
        total_nodes = 0
        for r in node_results:
            nodes_by_type[r["label"]] = r["count"]
            total_nodes += r["count"]

        # Relationship counts by type
        rel_results = await Neo4jClient.execute_query(
            """
            CALL db.relationshipTypes() YIELD relationshipType
            CALL apoc.cypher.run(
                'MATCH ()-[r:`' + relationshipType + '`]->() RETURN count(r) as count', {}
            ) YIELD value
            RETURN relationshipType, value.count as count
            """
        )

        rels_by_type = {}
        total_rels = 0
        for r in rel_results:
            rels_by_type[r["relationshipType"]] = r["count"]
            total_rels += r["count"]

        return KGStatsResponse(
            total_nodes=total_nodes,
            total_relationships=total_rels,
            nodes_by_type=nodes_by_type,
            relationships_by_type=rels_by_type,
        )
    except Exception as e:
        logger.error(f"Failed to get KG stats: {e}")
        # Return empty stats if Neo4j is not available or APOC is missing
        try:
            # Fallback without APOC
            node_results = await Neo4jClient.execute_query(
                "MATCH (n) RETURN labels(n)[0] as label, count(n) as count GROUP BY label"
            )
            rel_results = await Neo4jClient.execute_query(
                "MATCH ()-[r]->() RETURN type(r) as type, count(r) as count"
            )
            nodes_by_type = {r["label"]: r["count"] for r in node_results}
            rels_by_type = {r["type"]: r["count"] for r in rel_results}
            return KGStatsResponse(
                total_nodes=sum(nodes_by_type.values()),
                total_relationships=sum(rels_by_type.values()),
                nodes_by_type=nodes_by_type,
                relationships_by_type=rels_by_type,
            )
        except Exception:
            return KGStatsResponse()


@router.get("/nodes")
async def list_nodes(
    label: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    """List nodes with optional label filter and pagination."""
    skip = (page - 1) * page_size

    if label:
        query = f"MATCH (n:{label}) RETURN elementId(n) as id, labels(n) as labels, properties(n) as props ORDER BY n.name SKIP $skip LIMIT $limit"
    else:
        query = "MATCH (n) RETURN elementId(n) as id, labels(n) as labels, properties(n) as props ORDER BY labels(n)[0] SKIP $skip LIMIT $limit"

    results = await Neo4jClient.execute_query(query, {"skip": skip, "limit": page_size})

    nodes = []
    for r in results:
        nodes.append(KGNode(
            id=str(r["id"]),
            label=r["labels"][0] if r["labels"] else "Unknown",
            properties=r["props"],
        ))

    return {"nodes": nodes, "page": page, "page_size": page_size}


@router.get("/nodes/{node_id}", response_model=KGNodeDetailResponse)
async def get_node_detail(node_id: str):
    """Get a node with all its relationships and connected nodes."""
    try:
        # Get the node
        node_results = await Neo4jClient.execute_query(
            "MATCH (n) WHERE elementId(n) = $id RETURN elementId(n) as id, labels(n) as labels, properties(n) as props",
            {"id": node_id},
        )

        if not node_results:
            raise HTTPException(status_code=404, detail="Node not found")

        r = node_results[0]
        node = KGNode(
            id=str(r["id"]),
            label=r["labels"][0] if r["labels"] else "Unknown",
            properties=r["props"],
        )

        # Get connected nodes and relationships
        connected_results = await Neo4jClient.execute_query(
            """
            MATCH (n)-[r]-(m) WHERE elementId(n) = $id
            RETURN elementId(m) as m_id, labels(m) as m_labels, properties(m) as m_props,
                   elementId(r) as r_id, type(r) as r_type, properties(r) as r_props,
                   elementId(startNode(r)) as source_id, elementId(endNode(r)) as target_id
            """,
            {"id": node_id},
        )

        connected_nodes = []
        relationships = []
        seen_nodes = set()

        for cr in connected_results:
            m_id = str(cr["m_id"])
            if m_id not in seen_nodes:
                connected_nodes.append(KGNode(
                    id=m_id,
                    label=cr["m_labels"][0] if cr["m_labels"] else "Unknown",
                    properties=cr["m_props"],
                ))
                seen_nodes.add(m_id)

            relationships.append(KGRelationship(
                id=str(cr["r_id"]),
                type=cr["r_type"],
                source_id=str(cr["source_id"]),
                target_id=str(cr["target_id"]),
                properties=cr["r_props"],
            ))

        return KGNodeDetailResponse(
            node=node,
            connected_nodes=connected_nodes,
            relationships=relationships,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get node detail: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=KGSearchResponse)
async def search_kg(
    q: str = Query(..., min_length=1),
    node_types: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100),
):
    """Full-text search across the knowledge graph."""
    try:
        # Try full-text search first
        search_query = """
        CALL db.index.fulltext.queryNodes('equipment_search', $query)
        YIELD node, score
        RETURN elementId(node) as id, labels(node) as labels,
               properties(node) as props, score
        ORDER BY score DESC
        LIMIT $limit
        """

        results = await Neo4jClient.execute_query(
            search_query, {"query": q, "limit": limit}
        )

        # Also search other indexes
        for index_name in ["document_search", "regulation_search"]:
            try:
                more_results = await Neo4jClient.execute_query(
                    f"""
                    CALL db.index.fulltext.queryNodes('{index_name}', $query)
                    YIELD node, score
                    RETURN elementId(node) as id, labels(node) as labels,
                           properties(node) as props, score
                    ORDER BY score DESC
                    LIMIT $limit
                    """,
                    {"query": q, "limit": limit},
                )
                results.extend(more_results)
            except Exception:
                pass

        # Sort by score and deduplicate
        seen = set()
        search_results = []
        for r in sorted(results, key=lambda x: x.get("score", 0), reverse=True):
            rid = str(r["id"])
            if rid not in seen:
                search_results.append(KGSearchResult(
                    node=KGNode(
                        id=rid,
                        label=r["labels"][0] if r["labels"] else "Unknown",
                        properties=r["props"],
                    ),
                    score=r.get("score", 0),
                ))
                seen.add(rid)

        if node_types:
            type_filter = set(node_types.split(","))
            search_results = [r for r in search_results if r.node.label in type_filter]

        return KGSearchResponse(
            results=search_results[:limit],
            total=len(search_results),
            query=q,
        )
    except Exception as e:
        logger.error(f"KG search failed: {e}")
        # Fallback to CONTAINS search
        try:
            fallback_results = await Neo4jClient.execute_query(
                """
                MATCH (n) WHERE any(prop in keys(n) WHERE toString(n[prop]) CONTAINS $query)
                RETURN elementId(n) as id, labels(n) as labels, properties(n) as props
                LIMIT $limit
                """,
                {"query": q, "limit": limit},
            )
            return KGSearchResponse(
                results=[
                    KGSearchResult(
                        node=KGNode(
                            id=str(r["id"]),
                            label=r["labels"][0] if r["labels"] else "Unknown",
                            properties=r["props"],
                        ),
                        score=1.0,
                    )
                    for r in fallback_results
                ],
                total=len(fallback_results),
                query=q,
            )
        except Exception as e2:
            logger.error(f"Fallback search also failed: {e2}")
            return KGSearchResponse(results=[], total=0, query=q)


@router.get("/subgraph", response_model=KGSubgraphResponse)
async def get_subgraph(
    node_id: str = Query(...),
    depth: int = Query(default=2, ge=1, le=5),
    limit: int = Query(default=100, ge=1, le=500),
):
    """Get N-hop subgraph around a node for visualization."""
    try:
        results = await Neo4jClient.execute_query(
            f"""
            MATCH path = (center)-[*1..{depth}]-(connected)
            WHERE elementId(center) = $node_id
            WITH nodes(path) as ns, relationships(path) as rs
            UNWIND ns as n
            WITH collect(DISTINCT n) as allNodes, rs
            UNWIND rs as r
            WITH allNodes, collect(DISTINCT r) as allRels
            UNWIND allNodes as n
            RETURN
                collect(DISTINCT {{
                    id: elementId(n),
                    labels: labels(n),
                    props: properties(n)
                }}) as nodes,
                [r IN allRels | {{
                    id: elementId(r),
                    type: type(r),
                    source: elementId(startNode(r)),
                    target: elementId(endNode(r)),
                    props: properties(r)
                }}] as relationships
            """,
            {"node_id": node_id},
        )

        if not results:
            return KGSubgraphResponse(nodes=[], relationships=[], center_node_id=node_id)

        data = results[0]
        nodes = [
            KGNode(
                id=str(n["id"]),
                label=n["labels"][0] if n["labels"] else "Unknown",
                properties=n["props"],
            )
            for n in (data.get("nodes", []) or [])[:limit]
        ]

        relationships = [
            KGRelationship(
                id=str(r["id"]),
                type=r["type"],
                source_id=str(r["source"]),
                target_id=str(r["target"]),
                properties=r.get("props", {}),
            )
            for r in (data.get("relationships", []) or [])
        ]

        return KGSubgraphResponse(
            nodes=nodes,
            relationships=relationships,
            center_node_id=node_id,
        )
    except Exception as e:
        logger.error(f"Failed to get subgraph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cypher")
async def execute_cypher(query: str):
    """Execute a raw Cypher query (admin/debug endpoint)."""
    try:
        results = await Neo4jClient.execute_query(query)
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cypher error: {str(e)}")
