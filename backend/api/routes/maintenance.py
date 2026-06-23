"""Maintenance intelligence API routes."""

from fastapi import APIRouter, HTTPException, Query
from database.neo4j_client import Neo4jClient
from typing import Optional
import uuid
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/maintenance", tags=["maintenance"])


@router.post("/rca")
async def root_cause_analysis(
    equipment_tag: Optional[str] = None,
    failure_description: Optional[str] = None,
):
    """Perform root cause analysis for equipment failures."""
    start_time = time.time()

    try:
        # Get failure history for the equipment
        if equipment_tag:
            failure_query = """
            MATCH (e:Equipment {tag: $tag})-[:HAS_FAILURE_MODE]->(fm:FailureMode)
            OPTIONAL MATCH (m:MaintenanceRecord)-[:CAUSED_BY]->(fm)
            OPTIONAL MATCH (fm)-[:MITIGATED_BY]->(p:Procedure)
            RETURN fm.code as failure_code, fm.description as description,
                   fm.severity as severity, fm.frequency as frequency,
                   fm.mtbf as mtbf,
                   collect(DISTINCT m.work_order_id) as work_orders,
                   collect(DISTINCT p.title) as mitigation_procedures
            ORDER BY fm.frequency DESC
            """
            results = await Neo4jClient.execute_query(
                failure_query, {"tag": equipment_tag}
            )
        else:
            # Get top failure modes across all equipment
            failure_query = """
            MATCH (e:Equipment)-[:HAS_FAILURE_MODE]->(fm:FailureMode)
            RETURN fm.code as failure_code, fm.description as description,
                   fm.severity as severity, fm.frequency as frequency,
                   collect(DISTINCT e.tag) as affected_equipment
            ORDER BY fm.frequency DESC
            LIMIT 20
            """
            results = await Neo4jClient.execute_query(failure_query)

        # Build RCA response
        failure_modes = []
        for r in results:
            failure_modes.append({
                "failure_code": r.get("failure_code", ""),
                "description": r.get("description", ""),
                "severity": r.get("severity", "unknown"),
                "frequency": r.get("frequency", 0),
                "mtbf": r.get("mtbf"),
                "work_orders": r.get("work_orders", []),
                "mitigation_procedures": r.get("mitigation_procedures", []),
                "affected_equipment": r.get("affected_equipment", []),
            })

        return {
            "equipment_tag": equipment_tag,
            "failure_modes": failure_modes,
            "total_failure_modes": len(failure_modes),
            "analysis_type": "root_cause_analysis",
            "processing_time_seconds": time.time() - start_time,
        }

    except Exception as e:
        logger.error(f"RCA failed: {e}")
        return {
            "equipment_tag": equipment_tag,
            "failure_modes": [],
            "total_failure_modes": 0,
            "error": str(e),
            "processing_time_seconds": time.time() - start_time,
        }


@router.get("/recommendations")
async def get_maintenance_recommendations():
    """Get predictive maintenance recommendations based on MTBF and failure patterns."""
    try:
        # Find equipment with upcoming maintenance needs
        results = await Neo4jClient.execute_query(
            """
            MATCH (e:Equipment)-[:HAS_MAINTENANCE]->(m:MaintenanceRecord)
            WITH e, m ORDER BY m.date DESC
            WITH e, collect(m)[0] as latest_maintenance
            OPTIONAL MATCH (e)-[:HAS_FAILURE_MODE]->(fm:FailureMode)
            RETURN e.tag as tag, e.name as name, e.type as type,
                   latest_maintenance.date as last_maintenance,
                   latest_maintenance.type as maintenance_type,
                   collect(DISTINCT {code: fm.code, severity: fm.severity, mtbf: fm.mtbf}) as failure_modes
            ORDER BY latest_maintenance.date ASC
            LIMIT 20
            """
        )

        recommendations = []
        for r in results:
            rec = {
                "equipment_tag": r["tag"],
                "equipment_name": r["name"],
                "equipment_type": r["type"],
                "last_maintenance": r.get("last_maintenance"),
                "last_maintenance_type": r.get("maintenance_type"),
                "failure_modes": r.get("failure_modes", []),
                "priority": "high" if any(
                    fm.get("severity") == "critical" for fm in r.get("failure_modes", [])
                ) else "medium",
                "recommendation": f"Schedule preventive maintenance for {r['tag']} - {r['name']}",
            }
            recommendations.append(rec)

        return {
            "recommendations": recommendations,
            "total": len(recommendations),
        }

    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}")
        return {"recommendations": [], "total": 0}


@router.get("/timeline/{equipment_tag}")
async def get_maintenance_timeline(equipment_tag: str):
    """Get full maintenance history timeline for an equipment item."""
    try:
        results = await Neo4jClient.execute_query(
            """
            MATCH (e:Equipment {tag: $tag})-[:HAS_MAINTENANCE]->(m:MaintenanceRecord)
            OPTIONAL MATCH (m)-[:PERFORMED_BY]->(p:Personnel)
            OPTIONAL MATCH (m)-[:CAUSED_BY]->(fm:FailureMode)
            OPTIONAL MATCH (m)-[:REFERENCES]->(d:Document)
            RETURN m.work_order_id as work_order_id,
                   m.type as type, m.date as date,
                   m.status as status, m.description as description,
                   collect(DISTINCT p.name) as personnel,
                   collect(DISTINCT fm.description) as failure_modes,
                   collect(DISTINCT d.title) as referenced_documents
            ORDER BY m.date DESC
            """,
            {"tag": equipment_tag},
        )

        # Get equipment details
        eq_results = await Neo4jClient.execute_query(
            "MATCH (e:Equipment {tag: $tag}) RETURN properties(e) as props",
            {"tag": equipment_tag},
        )

        equipment = eq_results[0]["props"] if eq_results else {}

        timeline = []
        for r in results:
            timeline.append({
                "work_order_id": r["work_order_id"],
                "type": r["type"],
                "date": r["date"],
                "status": r["status"],
                "description": r["description"],
                "personnel": r["personnel"],
                "failure_modes": r["failure_modes"],
                "referenced_documents": r["referenced_documents"],
            })

        return {
            "equipment": equipment,
            "equipment_tag": equipment_tag,
            "timeline": timeline,
            "total_records": len(timeline),
        }

    except Exception as e:
        logger.error(f"Failed to get timeline for {equipment_tag}: {e}")
        return {
            "equipment_tag": equipment_tag,
            "timeline": [],
            "total_records": 0,
            "error": str(e),
        }


@router.get("/failure-patterns")
async def get_failure_patterns():
    """Cross-equipment failure pattern analysis."""
    try:
        results = await Neo4jClient.execute_query(
            """
            MATCH (e:Equipment)-[:HAS_FAILURE_MODE]->(fm:FailureMode)
            WITH fm, collect(DISTINCT e.tag) as equipment_tags,
                 count(e) as equipment_count
            WHERE equipment_count > 1
            RETURN fm.code as failure_code, fm.description as description,
                   fm.severity as severity,
                   equipment_tags, equipment_count
            ORDER BY equipment_count DESC
            LIMIT 20
            """
        )

        patterns = []
        for r in results:
            patterns.append({
                "failure_code": r["failure_code"],
                "description": r["description"],
                "severity": r["severity"],
                "affected_equipment": r["equipment_tags"],
                "equipment_count": r["equipment_count"],
            })

        return {
            "patterns": patterns,
            "total": len(patterns),
        }

    except Exception as e:
        logger.error(f"Failed to get failure patterns: {e}")
        return {"patterns": [], "total": 0}
