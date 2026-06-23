"""Compliance analysis API routes."""

from fastapi import APIRouter, HTTPException
from database.neo4j_client import Neo4jClient
from schemas.compliance import (
    ComplianceAnalyzeRequest,
    ComplianceAnalyzeResponse,
    ComplianceGap,
    GapSeverity,
    RegulationSummary,
    ComplianceReportResponse,
)
from datetime import datetime
import uuid
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/compliance", tags=["compliance"])


@router.post("/analyze", response_model=ComplianceAnalyzeResponse)
async def analyze_compliance(request: ComplianceAnalyzeRequest):
    """Run compliance gap analysis against regulations in the knowledge graph."""
    start_time = time.time()

    try:
        # Find equipment without required regulatory links
        gap_query = """
        MATCH (r:Regulation)
        OPTIONAL MATCH (e:Equipment)-[:GOVERNED_BY]->(r)
        WITH r, collect(e) as governed_equipment
        WHERE size(governed_equipment) = 0
        RETURN r.standard_id as regulation_id, r.title as title,
               r.body as body, size(governed_equipment) as eq_count
        """

        if request.regulation_id:
            gap_query = """
            MATCH (r:Regulation {standard_id: $reg_id})
            OPTIONAL MATCH (e:Equipment)-[:GOVERNED_BY]->(r)
            WITH r, collect(e) as governed_equipment
            RETURN r.standard_id as regulation_id, r.title as title,
                   r.body as body, size(governed_equipment) as eq_count
            """

        results = await Neo4jClient.execute_query(
            gap_query,
            {"reg_id": request.regulation_id} if request.regulation_id else {},
        )

        gaps = []
        for r in results:
            gaps.append(ComplianceGap(
                id=str(uuid.uuid4()),
                regulation_id=r["regulation_id"] or "unknown",
                regulation_title=r["title"] or "Untitled Regulation",
                requirement="Equipment must be governed by this regulation",
                gap_description=f"No equipment is currently linked to regulation {r['regulation_id']}",
                severity=GapSeverity.HIGH,
                affected_equipment=[],
                evidence=[],
                recommendation="Review and link applicable equipment to this regulatory standard",
            ))

        # Also find equipment missing procedures
        procedure_gaps = await Neo4jClient.execute_query(
            """
            MATCH (e:Equipment)
            WHERE NOT (e)-[:FOLLOWS_PROCEDURE]->()
            RETURN e.tag as tag, e.name as name
            LIMIT 50
            """
        )

        for pg in procedure_gaps:
            gaps.append(ComplianceGap(
                id=str(uuid.uuid4()),
                regulation_id="GENERAL",
                regulation_title="Operating Procedures Requirement",
                requirement="All equipment must have associated operating procedures",
                gap_description=f"Equipment {pg['tag'] or pg['name']} has no linked procedures",
                severity=GapSeverity.MEDIUM,
                affected_equipment=[pg["tag"] or pg["name"] or "Unknown"],
                evidence=[],
                recommendation="Create or link standard operating procedures for this equipment",
            ))

        # Calculate compliance score
        total_regulations = await Neo4jClient.execute_query(
            "MATCH (r:Regulation) RETURN count(r) as count"
        )
        total_equipment = await Neo4jClient.execute_query(
            "MATCH (e:Equipment) RETURN count(e) as count"
        )
        reg_count = total_regulations[0]["count"] if total_regulations else 0
        eq_count = total_equipment[0]["count"] if total_equipment else 0

        if reg_count + eq_count > 0:
            compliance_score = max(0, 100 - (len(gaps) / max(1, reg_count + eq_count) * 100))
        else:
            compliance_score = 100.0

        gaps_by_severity = {}
        for gap in gaps:
            gaps_by_severity[gap.severity] = gaps_by_severity.get(gap.severity, 0) + 1

        return ComplianceAnalyzeResponse(
            total_gaps=len(gaps),
            gaps_by_severity=gaps_by_severity,
            gaps=gaps,
            compliance_score=round(compliance_score, 1),
            analysis_timestamp=datetime.utcnow(),
            processing_time_seconds=time.time() - start_time,
        )

    except Exception as e:
        logger.error(f"Compliance analysis failed: {e}")
        return ComplianceAnalyzeResponse(
            total_gaps=0,
            gaps=[],
            compliance_score=0.0,
            analysis_timestamp=datetime.utcnow(),
            processing_time_seconds=time.time() - start_time,
        )


@router.get("/gaps")
async def list_compliance_gaps():
    """List all identified compliance gaps (quick scan)."""
    request = ComplianceAnalyzeRequest()
    return await analyze_compliance(request)


@router.get("/regulations")
async def list_regulations():
    """List all regulatory standards in the knowledge graph."""
    try:
        results = await Neo4jClient.execute_query(
            """
            MATCH (r:Regulation)
            OPTIONAL MATCH (e:Equipment)-[:GOVERNED_BY]->(r)
            WITH r, count(e) as eq_count
            OPTIONAL MATCH (r)<-[:VIOLATES]-(f:InspectionFinding)
            RETURN r.standard_id as standard_id, r.title as title,
                   r.body as body, r.version as version, r.status as status,
                   eq_count, count(f) as gap_count
            ORDER BY r.standard_id
            """
        )

        regulations = [
            RegulationSummary(
                standard_id=r["standard_id"] or "unknown",
                title=r["title"] or "Untitled",
                body=r.get("body"),
                version=r.get("version"),
                status=r.get("status"),
                equipment_count=r["eq_count"],
                gap_count=r["gap_count"],
            )
            for r in results
        ]

        return {"regulations": regulations, "total": len(regulations)}

    except Exception as e:
        logger.error(f"Failed to list regulations: {e}")
        return {"regulations": [], "total": 0}


@router.get("/report", response_model=ComplianceReportResponse)
async def generate_compliance_report():
    """Generate a full compliance evidence report."""
    # Run full analysis
    analysis = await analyze_compliance(ComplianceAnalyzeRequest(include_evidence=True))

    # Get all regulations
    regs_response = await list_regulations()

    return ComplianceReportResponse(
        report_id=str(uuid.uuid4()),
        generated_at=datetime.utcnow(),
        total_regulations=regs_response["total"],
        total_gaps=analysis.total_gaps,
        overall_score=analysis.compliance_score,
        gaps=analysis.gaps,
        regulations=regs_response["regulations"],
    )
