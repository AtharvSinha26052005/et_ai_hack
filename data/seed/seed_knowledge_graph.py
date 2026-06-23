"""Seed the Neo4j knowledge graph with realistic industrial data for demo purposes."""

import asyncio
import sys
import os

# Add parent dir to path so we can import from backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


async def seed_knowledge_graph():
    """Pre-populate the knowledge graph with sample industrial data."""
    from database.neo4j_client import Neo4jClient

    print("🌱 Seeding Knowledge Graph...")
    await Neo4jClient.connect()

    # ================================================================
    # 1. Equipment Master Data (50 items)
    # ================================================================
    equipment = [
        {"tag": "P-101A", "name": "Feed Water Pump A", "type": "Centrifugal Pump", "manufacturer": "Grundfos", "model": "CR 64-3", "location": "Unit 1 - Pump House", "status": "operational", "install_date": "2019-03-15"},
        {"tag": "P-101B", "name": "Feed Water Pump B (Standby)", "type": "Centrifugal Pump", "manufacturer": "Grundfos", "model": "CR 64-3", "location": "Unit 1 - Pump House", "status": "standby", "install_date": "2019-03-15"},
        {"tag": "P-102", "name": "Chemical Dosing Pump", "type": "Diaphragm Pump", "manufacturer": "Milton Roy", "model": "mRoy-A", "location": "Unit 1 - Chemical Area", "status": "operational", "install_date": "2020-06-01"},
        {"tag": "P-201", "name": "Cooling Water Pump", "type": "Centrifugal Pump", "manufacturer": "KSB", "model": "Etanorm 100-200", "location": "Unit 2 - Cooling Tower", "status": "operational", "install_date": "2018-11-20"},
        {"tag": "P-301", "name": "Product Transfer Pump", "type": "Positive Displacement Pump", "manufacturer": "Flowserve", "model": "SIHI 6510", "location": "Unit 3 - Loading Bay", "status": "operational", "install_date": "2021-01-10"},
        {"tag": "HX-201", "name": "Shell & Tube Heat Exchanger", "type": "Heat Exchanger", "manufacturer": "Alfa Laval", "model": "M10-BFG", "location": "Unit 2 - Process Area", "status": "operational", "install_date": "2018-05-22"},
        {"tag": "HX-202", "name": "Plate Heat Exchanger", "type": "Heat Exchanger", "manufacturer": "Alfa Laval", "model": "T20-BFG", "location": "Unit 2 - Process Area", "status": "operational", "install_date": "2019-08-14"},
        {"tag": "HX-301", "name": "Air Cooled Heat Exchanger", "type": "Heat Exchanger", "manufacturer": "Kelvion", "model": "ACFIN-500", "location": "Unit 3 - Outdoor", "status": "operational", "install_date": "2020-02-28"},
        {"tag": "V-101", "name": "Feed Water Storage Tank", "type": "Storage Vessel", "manufacturer": "Bharat Tanks", "model": "BT-50000L", "location": "Unit 1 - Tank Farm", "status": "operational", "install_date": "2017-04-10"},
        {"tag": "V-201", "name": "Reactor Vessel", "type": "Reactor", "manufacturer": "Larsen & Toubro", "model": "RV-2500", "location": "Unit 2 - Reactor Building", "status": "operational", "install_date": "2018-03-05"},
        {"tag": "V-301", "name": "Product Storage Tank", "type": "Storage Vessel", "manufacturer": "Bharat Tanks", "model": "BT-100000L", "location": "Unit 3 - Tank Farm", "status": "operational", "install_date": "2019-06-18"},
        {"tag": "C-101", "name": "Air Compressor", "type": "Compressor", "manufacturer": "Atlas Copco", "model": "GA 55+", "location": "Utility Area", "status": "operational", "install_date": "2020-01-15"},
        {"tag": "C-201", "name": "Process Gas Compressor", "type": "Compressor", "manufacturer": "Siemens", "model": "STC-GV 50", "location": "Unit 2 - Compressor House", "status": "operational", "install_date": "2019-09-01"},
        {"tag": "M-101", "name": "Pump Motor 101A", "type": "Electric Motor", "manufacturer": "ABB", "model": "M3BP 315 SMC", "location": "Unit 1 - Pump House", "status": "operational", "install_date": "2019-03-15"},
        {"tag": "M-201", "name": "Cooling Water Motor", "type": "Electric Motor", "manufacturer": "Siemens", "model": "1LA7163-4AA", "location": "Unit 2 - Cooling Tower", "status": "operational", "install_date": "2018-11-20"},
        {"tag": "FV-101", "name": "Feed Control Valve", "type": "Control Valve", "manufacturer": "Emerson", "model": "Fisher V150S", "location": "Unit 1 - Process Area", "status": "operational", "install_date": "2020-07-12"},
        {"tag": "FV-201", "name": "Reactor Inlet Valve", "type": "Control Valve", "manufacturer": "Emerson", "model": "Fisher V250", "location": "Unit 2 - Reactor Building", "status": "operational", "install_date": "2018-03-05"},
        {"tag": "PSV-101", "name": "Relief Valve - Feed System", "type": "Safety Valve", "manufacturer": "Leser", "model": "441 HP", "location": "Unit 1 - Process Area", "status": "operational", "install_date": "2019-03-15"},
        {"tag": "PSV-201", "name": "Relief Valve - Reactor", "type": "Safety Valve", "manufacturer": "Leser", "model": "441 HP", "location": "Unit 2 - Reactor Building", "status": "operational", "install_date": "2018-03-05"},
        {"tag": "T-101", "name": "Distillation Column", "type": "Column", "manufacturer": "ISGEC", "model": "DC-3500", "location": "Unit 2 - Distillation Area", "status": "operational", "install_date": "2018-05-22"},
        {"tag": "T-201", "name": "Absorption Tower", "type": "Column", "manufacturer": "ISGEC", "model": "AT-2000", "location": "Unit 2 - Gas Treatment", "status": "operational", "install_date": "2018-05-22"},
        {"tag": "B-101", "name": "Process Steam Boiler", "type": "Boiler", "manufacturer": "Thermax", "model": "Shellmax-6000", "location": "Utility Area - Boiler House", "status": "operational", "install_date": "2017-08-20"},
        {"tag": "AG-101", "name": "Diesel Generator Set", "type": "Generator", "manufacturer": "Cummins", "model": "KTA50-G3", "location": "Utility Area - DG Room", "status": "standby", "install_date": "2018-01-15"},
        {"tag": "CT-101", "name": "Cooling Tower", "type": "Cooling Tower", "manufacturer": "Paharpur", "model": "CTI-500", "location": "Unit 2 - Outdoor", "status": "operational", "install_date": "2018-06-10"},
        {"tag": "TK-101", "name": "Nitrogen Storage Tank", "type": "Storage Vessel", "manufacturer": "Inox", "model": "CVS-20000", "location": "Utility Area", "status": "operational", "install_date": "2019-02-28"},
    ]

    for eq in equipment:
        await Neo4jClient.execute_write(
            "MERGE (e:Equipment {tag: $tag}) SET e += $props",
            {"tag": eq["tag"], "props": eq},
        )
    print(f"  ✓ Created {len(equipment)} equipment nodes")

    # ================================================================
    # 2. Regulatory Standards (15 items)
    # ================================================================
    regulations = [
        {"standard_id": "OISD-STD-105", "title": "Work Permit System", "body": "Standard on work permit system in oil and gas installations", "version": "2024", "status": "active"},
        {"standard_id": "OISD-STD-116", "title": "Fire Protection for Onshore Installations", "body": "Fire protection facilities for petroleum refineries and oil/gas processing plants", "version": "2023", "status": "active"},
        {"standard_id": "OISD-STD-117", "title": "Fire Protection for Terminals and Depots", "body": "Fire protection facilities for petroleum depots and terminals", "version": "2023", "status": "active"},
        {"standard_id": "OISD-STD-144", "title": "Petroleum Safety in Electrical Installations", "body": "Recommendations on petroleum industry safety in electrical installations", "version": "2022", "status": "active"},
        {"standard_id": "OISD-STD-154", "title": "Safety Aspects in Functional Design", "body": "Safety aspects in functional design of process plants", "version": "2021", "status": "active"},
        {"standard_id": "OISD-GDN-206", "title": "Guidelines on Safety Management System", "body": "Guidelines for safety management system in petroleum industry", "version": "2024", "status": "active"},
        {"standard_id": "FACTORY-ACT-1948", "title": "The Factories Act, 1948", "body": "Act to consolidate and amend the law regulating labour in factories", "version": "2016-amendment", "status": "active"},
        {"standard_id": "IS-2825", "title": "Code for Unfired Pressure Vessels", "body": "Bureau of Indian Standards code for unfired pressure vessels", "version": "2021", "status": "active"},
        {"standard_id": "IS-803", "title": "Code of Practice for Industrial Lighting", "body": "Code of practice for design of industrial buildings for lighting", "version": "2019", "status": "active"},
        {"standard_id": "API-570", "title": "Piping Inspection Code", "body": "In-service inspection, rating, repair, and alteration of piping systems", "version": "2020", "status": "active"},
        {"standard_id": "API-510", "title": "Pressure Vessel Inspection Code", "body": "In-service inspection, rating, repair, and alteration of pressure vessels", "version": "2020", "status": "active"},
        {"standard_id": "ASME-B31.3", "title": "Process Piping", "body": "ASME code for process piping design and construction", "version": "2022", "status": "active"},
        {"standard_id": "NFPA-30", "title": "Flammable and Combustible Liquids Code", "body": "National Fire Protection Association standard for storage and handling", "version": "2021", "status": "active"},
        {"standard_id": "ISO-45001", "title": "Occupational Health & Safety Management", "body": "ISO standard for occupational health and safety management systems", "version": "2018", "status": "active"},
        {"standard_id": "PESO-RULES", "title": "Petroleum and Explosives Safety Organization Rules", "body": "Rules governing storage and handling of petroleum products", "version": "2023", "status": "active"},
    ]

    for reg in regulations:
        await Neo4jClient.execute_write(
            "MERGE (r:Regulation {standard_id: $sid}) SET r += $props",
            {"sid": reg["standard_id"], "props": reg},
        )
    print(f"  ✓ Created {len(regulations)} regulation nodes")

    # ================================================================
    # 3. Personnel (20 items)
    # ================================================================
    personnel = [
        {"employee_id": "EMP-001", "name": "Rajesh Kumar", "role": "Senior Maintenance Engineer", "department": "Maintenance"},
        {"employee_id": "EMP-002", "name": "Suresh Patel", "role": "Mechanical Technician", "department": "Maintenance"},
        {"employee_id": "EMP-003", "name": "Amit Singh", "role": "Electrical Technician", "department": "Maintenance"},
        {"employee_id": "EMP-004", "name": "Priya Sharma", "role": "Process Engineer", "department": "Operations"},
        {"employee_id": "EMP-005", "name": "Vikram Reddy", "role": "Plant Manager", "department": "Management"},
        {"employee_id": "EMP-006", "name": "Deepak Verma", "role": "Safety Officer", "department": "HSE"},
        {"employee_id": "EMP-007", "name": "Arun Nair", "role": "Instrument Technician", "department": "Instrumentation"},
        {"employee_id": "EMP-008", "name": "Sanjay Gupta", "role": "Rotating Equipment Specialist", "department": "Maintenance"},
        {"employee_id": "EMP-009", "name": "Kavitha Rajan", "role": "Reliability Engineer", "department": "Maintenance"},
        {"employee_id": "EMP-010", "name": "Mohan Das", "role": "Welding Inspector", "department": "QC"},
        {"employee_id": "EMP-011", "name": "Anita Desai", "role": "Compliance Officer", "department": "HSE"},
        {"employee_id": "EMP-012", "name": "Ravi Shankar", "role": "Shift Supervisor", "department": "Operations"},
        {"employee_id": "EMP-013", "name": "Bharat Mehta", "role": "Planning Engineer", "department": "Planning"},
        {"employee_id": "EMP-014", "name": "Sunita Rao", "role": "Inspection Engineer", "department": "QC"},
        {"employee_id": "EMP-015", "name": "Naveen Joshi", "role": "Fire & Safety Officer", "department": "HSE"},
        {"employee_id": "EMP-016", "name": "Pooja Iyer", "role": "Environmental Engineer", "department": "HSE"},
        {"employee_id": "EMP-017", "name": "Ramesh Chandra", "role": "Store Keeper", "department": "Stores"},
        {"employee_id": "EMP-018", "name": "Kiran Babu", "role": "DCS Operator", "department": "Operations"},
        {"employee_id": "EMP-019", "name": "Manoj Tiwari", "role": "Crane Operator", "department": "Operations"},
        {"employee_id": "EMP-020", "name": "Lakshmi Nair", "role": "Lab Analyst", "department": "Quality"},
    ]

    for p in personnel:
        await Neo4jClient.execute_write(
            "MERGE (p:Personnel {employee_id: $eid}) SET p += $props",
            {"eid": p["employee_id"], "props": p},
        )
    print(f"  ✓ Created {len(personnel)} personnel nodes")

    # ================================================================
    # 4. Failure Modes
    # ================================================================
    failure_modes = [
        {"code": "FM-SEAL-LEAK", "description": "Mechanical seal leakage", "severity": "high", "frequency": 12, "mtbf": 8760},
        {"code": "FM-BEARING-FAIL", "description": "Bearing failure due to fatigue", "severity": "critical", "frequency": 8, "mtbf": 17520},
        {"code": "FM-IMPELLER-WEAR", "description": "Impeller erosion/wear", "severity": "medium", "frequency": 4, "mtbf": 26280},
        {"code": "FM-CAVITATION", "description": "Pump cavitation due to low NPSH", "severity": "high", "frequency": 6, "mtbf": 4380},
        {"code": "FM-TUBE-FOUL", "description": "Heat exchanger tube fouling", "severity": "medium", "frequency": 10, "mtbf": 4380},
        {"code": "FM-TUBE-LEAK", "description": "Heat exchanger tube leak", "severity": "high", "frequency": 3, "mtbf": 35040},
        {"code": "FM-VALVE-STICK", "description": "Control valve sticking/seizure", "severity": "medium", "frequency": 5, "mtbf": 8760},
        {"code": "FM-MOTOR-OVH", "description": "Electric motor overheating", "severity": "high", "frequency": 4, "mtbf": 17520},
        {"code": "FM-CORROSION", "description": "Internal corrosion of vessel/pipe", "severity": "critical", "frequency": 2, "mtbf": 43800},
        {"code": "FM-VIBRATION", "description": "Excessive vibration - misalignment", "severity": "high", "frequency": 7, "mtbf": 8760},
    ]

    for fm in failure_modes:
        await Neo4jClient.execute_write(
            "MERGE (fm:FailureMode {code: $code}) SET fm += $props",
            {"code": fm["code"], "props": fm},
        )
    print(f"  ✓ Created {len(failure_modes)} failure mode nodes")

    # ================================================================
    # 5. Procedures
    # ================================================================
    procedures = [
        {"procedure_id": "SOP-PUMP-START", "title": "Centrifugal Pump Startup Procedure", "type": "SOP", "revision": "Rev 3", "status": "approved"},
        {"procedure_id": "SOP-PUMP-STOP", "title": "Centrifugal Pump Normal Shutdown", "type": "SOP", "revision": "Rev 3", "status": "approved"},
        {"procedure_id": "SOP-HX-CLEAN", "title": "Heat Exchanger Cleaning Procedure", "type": "SOP", "revision": "Rev 2", "status": "approved"},
        {"procedure_id": "SOP-VESSEL-ENTRY", "title": "Confined Space Entry Procedure", "type": "Safety", "revision": "Rev 4", "status": "approved"},
        {"procedure_id": "SOP-HOT-WORK", "title": "Hot Work Permit Procedure", "type": "Safety", "revision": "Rev 5", "status": "approved"},
        {"procedure_id": "SOP-LOCKOUT", "title": "Lockout/Tagout (LOTO) Procedure", "type": "Safety", "revision": "Rev 3", "status": "approved"},
        {"procedure_id": "SOP-EMERGENCY", "title": "Emergency Response Plan", "type": "Safety", "revision": "Rev 6", "status": "approved"},
        {"procedure_id": "SOP-VALVE-MAINT", "title": "Control Valve Maintenance Procedure", "type": "SOP", "revision": "Rev 2", "status": "approved"},
        {"procedure_id": "PM-PUMP-QTRLY", "title": "Quarterly Pump Preventive Maintenance", "type": "PM", "revision": "Rev 3", "status": "approved"},
        {"procedure_id": "PM-MOTOR-ANNUAL", "title": "Annual Motor Inspection & Testing", "type": "PM", "revision": "Rev 2", "status": "approved"},
    ]

    for proc in procedures:
        await Neo4jClient.execute_write(
            "MERGE (p:Procedure {procedure_id: $pid}) SET p += $props",
            {"pid": proc["procedure_id"], "props": proc},
        )
    print(f"  ✓ Created {len(procedures)} procedure nodes")

    # ================================================================
    # 6. Maintenance Records (sample work orders)
    # ================================================================
    maintenance_records = [
        {"work_order_id": "WO-2025-0001", "type": "CM", "date": "2025-01-15", "status": "completed", "description": "Replaced mechanical seal on P-101A due to excessive leakage. Seal type: John Crane 5610."},
        {"work_order_id": "WO-2025-0023", "type": "PM", "date": "2025-02-10", "status": "completed", "description": "Quarterly preventive maintenance on P-101A: bearing inspection, vibration check, alignment verification."},
        {"work_order_id": "WO-2025-0045", "type": "CM", "date": "2025-03-22", "status": "completed", "description": "Bearing replacement on M-101 (pump motor). DE bearing SKF 6316 replaced."},
        {"work_order_id": "WO-2025-0067", "type": "PM", "date": "2025-04-05", "status": "completed", "description": "Heat exchanger HX-201 CIP cleaning. Fouling factor reduced from 0.0005 to 0.0001."},
        {"work_order_id": "WO-2025-0089", "type": "CM", "date": "2025-05-18", "status": "completed", "description": "Control valve FV-101 actuator diaphragm replacement. Valve was sticking at 40% open."},
        {"work_order_id": "WO-2025-0112", "type": "EM", "date": "2025-06-02", "status": "completed", "description": "Emergency shutdown of C-101 due to high discharge temperature. Found blocked aftercooler."},
        {"work_order_id": "WO-2025-0134", "type": "PM", "date": "2025-07-10", "status": "completed", "description": "Annual inspection of PSV-101 and PSV-201. Both tested and reseated to set pressure."},
        {"work_order_id": "WO-2025-0156", "type": "CM", "date": "2025-08-25", "status": "completed", "description": "Tube leak repair on HX-201. Two tubes plugged due to erosion-corrosion."},
        {"work_order_id": "WO-2025-0178", "type": "PM", "date": "2025-09-15", "status": "completed", "description": "Vibration analysis on all rotating equipment. P-201 showed elevated 2x RPM - coupling alignment adjusted."},
        {"work_order_id": "WO-2025-0200", "type": "CM", "date": "2025-10-30", "status": "completed", "description": "Impeller replacement on P-201 due to cavitation damage. Reviewed NPSH requirements."},
    ]

    for mr in maintenance_records:
        await Neo4jClient.execute_write(
            "MERGE (m:MaintenanceRecord {work_order_id: $woid}) SET m += $props",
            {"woid": mr["work_order_id"], "props": mr},
        )
    print(f"  ✓ Created {len(maintenance_records)} maintenance record nodes")

    # ================================================================
    # 7. Relationships
    # ================================================================
    print("  Creating relationships...")

    # Equipment -> Failure Modes
    eq_fm_rels = [
        ("P-101A", "FM-SEAL-LEAK"), ("P-101A", "FM-BEARING-FAIL"), ("P-101A", "FM-CAVITATION"), ("P-101A", "FM-VIBRATION"),
        ("P-101B", "FM-SEAL-LEAK"), ("P-101B", "FM-BEARING-FAIL"),
        ("P-201", "FM-SEAL-LEAK"), ("P-201", "FM-IMPELLER-WEAR"), ("P-201", "FM-CAVITATION"),
        ("P-301", "FM-SEAL-LEAK"),
        ("HX-201", "FM-TUBE-FOUL"), ("HX-201", "FM-TUBE-LEAK"),
        ("HX-202", "FM-TUBE-FOUL"),
        ("FV-101", "FM-VALVE-STICK"), ("FV-201", "FM-VALVE-STICK"),
        ("M-101", "FM-MOTOR-OVH"), ("M-101", "FM-BEARING-FAIL"),
        ("M-201", "FM-MOTOR-OVH"),
        ("V-101", "FM-CORROSION"), ("V-201", "FM-CORROSION"), ("V-301", "FM-CORROSION"),
        ("C-101", "FM-VIBRATION"), ("C-201", "FM-VIBRATION"),
    ]
    for tag, code in eq_fm_rels:
        await Neo4jClient.execute_write(
            "MATCH (e:Equipment {tag: $tag}), (fm:FailureMode {code: $code}) MERGE (e)-[:HAS_FAILURE_MODE]->(fm)",
            {"tag": tag, "code": code},
        )

    # Equipment -> Regulations
    eq_reg_rels = [
        ("P-101A", "OISD-STD-154"), ("P-101B", "OISD-STD-154"),
        ("V-101", "IS-2825"), ("V-201", "IS-2825"), ("V-301", "IS-2825"),
        ("PSV-101", "API-510"), ("PSV-201", "API-510"),
        ("M-101", "OISD-STD-144"), ("M-201", "OISD-STD-144"),
        ("B-101", "FACTORY-ACT-1948"), ("B-101", "IS-2825"),
        ("TK-101", "PESO-RULES"),
        ("AG-101", "OISD-STD-144"),
    ]
    for tag, sid in eq_reg_rels:
        await Neo4jClient.execute_write(
            "MATCH (e:Equipment {tag: $tag}), (r:Regulation {standard_id: $sid}) MERGE (e)-[:GOVERNED_BY]->(r)",
            {"tag": tag, "sid": sid},
        )

    # Equipment -> Procedures
    eq_proc_rels = [
        ("P-101A", "SOP-PUMP-START"), ("P-101A", "SOP-PUMP-STOP"), ("P-101A", "PM-PUMP-QTRLY"),
        ("P-101B", "SOP-PUMP-START"), ("P-101B", "SOP-PUMP-STOP"),
        ("HX-201", "SOP-HX-CLEAN"), ("HX-202", "SOP-HX-CLEAN"),
        ("FV-101", "SOP-VALVE-MAINT"), ("FV-201", "SOP-VALVE-MAINT"),
        ("V-201", "SOP-VESSEL-ENTRY"),
        ("M-101", "PM-MOTOR-ANNUAL"), ("M-201", "PM-MOTOR-ANNUAL"),
        ("M-101", "SOP-LOCKOUT"), ("C-101", "SOP-LOCKOUT"),
    ]
    for tag, pid in eq_proc_rels:
        await Neo4jClient.execute_write(
            "MATCH (e:Equipment {tag: $tag}), (p:Procedure {procedure_id: $pid}) MERGE (e)-[:FOLLOWS_PROCEDURE]->(p)",
            {"tag": tag, "pid": pid},
        )

    # Procedure -> Regulation (COMPLIES_WITH)
    proc_reg_rels = [
        ("SOP-VESSEL-ENTRY", "FACTORY-ACT-1948"),
        ("SOP-HOT-WORK", "OISD-STD-105"),
        ("SOP-LOCKOUT", "OISD-STD-105"),
        ("SOP-EMERGENCY", "OISD-GDN-206"),
        ("SOP-EMERGENCY", "ISO-45001"),
    ]
    for pid, sid in proc_reg_rels:
        await Neo4jClient.execute_write(
            "MATCH (p:Procedure {procedure_id: $pid}), (r:Regulation {standard_id: $sid}) MERGE (p)-[:COMPLIES_WITH]->(r)",
            {"pid": pid, "sid": sid},
        )

    # FailureMode -> Procedure (MITIGATED_BY)
    fm_proc_rels = [
        ("FM-SEAL-LEAK", "PM-PUMP-QTRLY"),
        ("FM-BEARING-FAIL", "PM-PUMP-QTRLY"),
        ("FM-MOTOR-OVH", "PM-MOTOR-ANNUAL"),
        ("FM-TUBE-FOUL", "SOP-HX-CLEAN"),
        ("FM-VALVE-STICK", "SOP-VALVE-MAINT"),
    ]
    for code, pid in fm_proc_rels:
        await Neo4jClient.execute_write(
            "MATCH (fm:FailureMode {code: $code}), (p:Procedure {procedure_id: $pid}) MERGE (fm)-[:MITIGATED_BY]->(p)",
            {"code": code, "pid": pid},
        )

    # Equipment -> MaintenanceRecord
    eq_mr_rels = [
        ("P-101A", "WO-2025-0001"), ("P-101A", "WO-2025-0023"),
        ("M-101", "WO-2025-0045"),
        ("HX-201", "WO-2025-0067"), ("HX-201", "WO-2025-0156"),
        ("FV-101", "WO-2025-0089"),
        ("C-101", "WO-2025-0112"),
        ("PSV-101", "WO-2025-0134"), ("PSV-201", "WO-2025-0134"),
        ("P-201", "WO-2025-0178"), ("P-201", "WO-2025-0200"),
    ]
    for tag, woid in eq_mr_rels:
        await Neo4jClient.execute_write(
            "MATCH (e:Equipment {tag: $tag}), (m:MaintenanceRecord {work_order_id: $woid}) MERGE (e)-[:HAS_MAINTENANCE]->(m)",
            {"tag": tag, "woid": woid},
        )

    # MaintenanceRecord -> Personnel (PERFORMED_BY)
    mr_pers_rels = [
        ("WO-2025-0001", "EMP-002"), ("WO-2025-0001", "EMP-008"),
        ("WO-2025-0023", "EMP-002"),
        ("WO-2025-0045", "EMP-003"), ("WO-2025-0045", "EMP-008"),
        ("WO-2025-0067", "EMP-002"),
        ("WO-2025-0089", "EMP-007"),
        ("WO-2025-0112", "EMP-001"), ("WO-2025-0112", "EMP-008"),
        ("WO-2025-0134", "EMP-014"),
        ("WO-2025-0156", "EMP-010"), ("WO-2025-0156", "EMP-002"),
        ("WO-2025-0178", "EMP-009"),
        ("WO-2025-0200", "EMP-002"), ("WO-2025-0200", "EMP-008"),
    ]
    for woid, eid in mr_pers_rels:
        await Neo4jClient.execute_write(
            "MATCH (m:MaintenanceRecord {work_order_id: $woid}), (p:Personnel {employee_id: $eid}) MERGE (m)-[:PERFORMED_BY]->(p)",
            {"woid": woid, "eid": eid},
        )

    # MaintenanceRecord -> FailureMode (CAUSED_BY)
    mr_fm_rels = [
        ("WO-2025-0001", "FM-SEAL-LEAK"),
        ("WO-2025-0045", "FM-BEARING-FAIL"),
        ("WO-2025-0067", "FM-TUBE-FOUL"),
        ("WO-2025-0089", "FM-VALVE-STICK"),
        ("WO-2025-0156", "FM-TUBE-LEAK"),
        ("WO-2025-0200", "FM-IMPELLER-WEAR"),
    ]
    for woid, code in mr_fm_rels:
        await Neo4jClient.execute_write(
            "MATCH (m:MaintenanceRecord {work_order_id: $woid}), (fm:FailureMode {code: $code}) MERGE (m)-[:CAUSED_BY]->(fm)",
            {"woid": woid, "code": code},
        )

    print("  ✓ All relationships created")

    # ================================================================
    # Final stats
    # ================================================================
    node_count = await Neo4jClient.execute_query("MATCH (n) RETURN count(n) as count")
    rel_count = await Neo4jClient.execute_query("MATCH ()-[r]->() RETURN count(r) as count")

    print(f"\n🎉 Seed complete!")
    print(f"   Total nodes: {node_count[0]['count']}")
    print(f"   Total relationships: {rel_count[0]['count']}")

    await Neo4jClient.close()


if __name__ == "__main__":
    asyncio.run(seed_knowledge_graph())
