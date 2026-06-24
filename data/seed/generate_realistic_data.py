"""
Generate realistic industrial data for IntelliPlant Knowledge Graph.

Produces JSON files with domain-accurate CMMS-style records based on real
industrial naming conventions, manufacturers, failure patterns, and MTBF
benchmarks. Data models follow SAP PM / Maximo formats.

Usage:
    python generate_realistic_data.py

Output:
    data/seed/generated/equipment.json
    data/seed/generated/regulations.json
    data/seed/generated/personnel.json
    data/seed/generated/failure_modes.json
    data/seed/generated/procedures.json
    data/seed/generated/maintenance_records.json
    data/seed/generated/inspection_findings.json
    data/seed/generated/process_parameters.json
    data/seed/generated/relationships.json
"""

import json
import random
import os
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)  # Reproducible output

OUTPUT_DIR = Path(__file__).parent / "generated"
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================================
# 1. EQUIPMENT MASTER DATA (75 items)
# ============================================================================

def generate_equipment():
    """Generate 75 equipment items with realistic specs."""
    equipment = []

    # --- Pumps (15) ---
    pumps = [
        {"tag": "P-101A", "name": "Feed Water Pump A", "type": "Centrifugal Pump", "manufacturer": "Grundfos", "model": "CR 64-3-2", "location": "Unit-1 / Pump House / Bay-A", "status": "operational", "install_date": "2019-03-15", "design_pressure": "16 bar", "material": "SS316", "power_kw": 55},
        {"tag": "P-101B", "name": "Feed Water Pump B (Standby)", "type": "Centrifugal Pump", "manufacturer": "Grundfos", "model": "CR 64-3-2", "location": "Unit-1 / Pump House / Bay-A", "status": "standby", "install_date": "2019-03-15", "design_pressure": "16 bar", "material": "SS316", "power_kw": 55},
        {"tag": "P-102", "name": "Chemical Dosing Pump - Caustic", "type": "Diaphragm Pump", "manufacturer": "Milton Roy", "model": "mRoy-A 161-138", "location": "Unit-1 / Chemical Injection / Skid-1", "status": "operational", "install_date": "2020-06-01", "design_pressure": "10 bar", "material": "PVDF", "power_kw": 0.75},
        {"tag": "P-103", "name": "Chemical Dosing Pump - HCl", "type": "Diaphragm Pump", "manufacturer": "Milton Roy", "model": "mRoy-A 141-116", "location": "Unit-1 / Chemical Injection / Skid-2", "status": "operational", "install_date": "2020-06-01", "design_pressure": "10 bar", "material": "PVDF", "power_kw": 0.55},
        {"tag": "P-201A", "name": "Cooling Water Circ. Pump A", "type": "Centrifugal Pump", "manufacturer": "KSB", "model": "Etanorm 100-200", "location": "Unit-2 / Cooling Tower / Pump Bay", "status": "operational", "install_date": "2018-11-20", "design_pressure": "10 bar", "material": "CI / SS Impeller", "power_kw": 90},
        {"tag": "P-201B", "name": "Cooling Water Circ. Pump B", "type": "Centrifugal Pump", "manufacturer": "KSB", "model": "Etanorm 100-200", "location": "Unit-2 / Cooling Tower / Pump Bay", "status": "standby", "install_date": "2018-11-20", "design_pressure": "10 bar", "material": "CI / SS Impeller", "power_kw": 90},
        {"tag": "P-202", "name": "Reactor Feed Pump", "type": "Centrifugal Pump", "manufacturer": "Flowserve", "model": "Durco Mark3 3x2-13", "location": "Unit-2 / Process Area / Ground Floor", "status": "operational", "install_date": "2019-07-22", "design_pressure": "25 bar", "material": "CD4MCu", "power_kw": 37},
        {"tag": "P-301", "name": "Product Transfer Pump", "type": "Positive Displacement Pump", "manufacturer": "Flowserve", "model": "SIHI 6510", "location": "Unit-3 / Loading Bay / Pump Pit", "status": "operational", "install_date": "2021-01-10", "design_pressure": "12 bar", "material": "CS/SS316 trim", "power_kw": 22},
        {"tag": "P-302", "name": "Slop Oil Pump", "type": "Progressive Cavity Pump", "manufacturer": "Seepex", "model": "BN 35-12", "location": "Unit-3 / ETP / Pump House", "status": "operational", "install_date": "2020-09-05", "design_pressure": "8 bar", "material": "SS304", "power_kw": 7.5},
        {"tag": "P-401", "name": "Boiler Feed Water Pump", "type": "Multistage Centrifugal Pump", "manufacturer": "Grundfos", "model": "CRN 90-3-2", "location": "Utility / Boiler House / Pump Room", "status": "operational", "install_date": "2017-08-20", "design_pressure": "25 bar", "material": "SS316L", "power_kw": 75},
        {"tag": "P-402", "name": "DM Water Transfer Pump", "type": "Centrifugal Pump", "manufacturer": "Kirloskar", "model": "DB 65/26", "location": "Utility / DM Plant / Pump Bay", "status": "operational", "install_date": "2018-04-12", "design_pressure": "6 bar", "material": "SS304", "power_kw": 15},
        {"tag": "P-501", "name": "Fire Water Jockey Pump", "type": "Centrifugal Pump", "manufacturer": "Kirloskar", "model": "KDI 0815+", "location": "Fire Station / Pump House", "status": "operational", "install_date": "2017-06-01", "design_pressure": "12 bar", "material": "CI", "power_kw": 15},
        {"tag": "P-502", "name": "Fire Water Main Pump (Electric)", "type": "Centrifugal Pump", "manufacturer": "Kirloskar", "model": "KPD 1050+", "location": "Fire Station / Pump House", "status": "standby", "install_date": "2017-06-01", "design_pressure": "12 bar", "material": "CI", "power_kw": 125},
        {"tag": "P-503", "name": "Fire Water Main Pump (Diesel)", "type": "Centrifugal Pump", "manufacturer": "Kirloskar", "model": "KPD 1050+", "location": "Fire Station / Pump House", "status": "standby", "install_date": "2017-06-01", "design_pressure": "12 bar", "material": "CI", "power_kw": 125},
        {"tag": "P-601", "name": "Condensate Return Pump", "type": "Centrifugal Pump", "manufacturer": "Grundfos", "model": "CR 32-5", "location": "Utility / Boiler House / Condensate Bay", "status": "operational", "install_date": "2018-02-15", "design_pressure": "16 bar", "material": "SS316", "power_kw": 18.5},
    ]

    # --- Heat Exchangers (8) ---
    heat_exchangers = [
        {"tag": "HX-201", "name": "Reactor Feed Preheater", "type": "Shell & Tube Heat Exchanger", "manufacturer": "Alfa Laval", "model": "M10-BFG", "location": "Unit-2 / Process Area / Mezzanine", "status": "operational", "install_date": "2018-05-22", "design_pressure": "20 bar (S) / 10 bar (T)", "material": "CS Shell / SS316 Tubes", "heat_duty_kw": 1200},
        {"tag": "HX-202", "name": "Product Cooler", "type": "Plate Heat Exchanger", "manufacturer": "Alfa Laval", "model": "T20-BFG", "location": "Unit-2 / Process Area / Ground Floor", "status": "operational", "install_date": "2019-08-14", "design_pressure": "16 bar", "material": "SS316 Plates / EPDM Gaskets", "heat_duty_kw": 800},
        {"tag": "HX-203", "name": "Reactor Effluent Cooler", "type": "Shell & Tube Heat Exchanger", "manufacturer": "Kelvion", "model": "NX-50M", "location": "Unit-2 / Process Area / Ground Floor", "status": "operational", "install_date": "2018-05-22", "design_pressure": "25 bar (S) / 10 bar (T)", "material": "CS / CuNi 90/10 Tubes", "heat_duty_kw": 2500},
        {"tag": "HX-301", "name": "Air Cooled Fin Fan Exchanger", "type": "Air Cooled Heat Exchanger", "manufacturer": "Kelvion", "model": "ACFIN-500", "location": "Unit-3 / Pipe Rack / Elevated", "status": "operational", "install_date": "2020-02-28", "design_pressure": "15 bar", "material": "CS / Al Fins", "heat_duty_kw": 3000},
        {"tag": "HX-401", "name": "Boiler Economizer", "type": "Finned Tube Heat Exchanger", "manufacturer": "Thermax", "model": "ECO-200", "location": "Utility / Boiler House / Stack Section", "status": "operational", "install_date": "2017-08-20", "design_pressure": "30 bar", "material": "CS / CS Fins", "heat_duty_kw": 500},
        {"tag": "HX-101", "name": "Feed Water Heater", "type": "Shell & Tube Heat Exchanger", "manufacturer": "Alfa Laval", "model": "M6-MFG", "location": "Unit-1 / Water Treatment / Indoor", "status": "operational", "install_date": "2019-03-15", "design_pressure": "10 bar (S) / 6 bar (T)", "material": "SS304 / SS316 Tubes", "heat_duty_kw": 400},
        {"tag": "HX-501", "name": "Lube Oil Cooler - Compressor", "type": "Plate Heat Exchanger", "manufacturer": "Alfa Laval", "model": "CB76-30H", "location": "Unit-2 / Compressor House / Aux Bay", "status": "operational", "install_date": "2019-09-01", "design_pressure": "12 bar", "material": "SS316 / Cu Brazed", "heat_duty_kw": 150},
        {"tag": "HX-502", "name": "Compressor Intercooler", "type": "Shell & Tube Heat Exchanger", "manufacturer": "Kelvion", "model": "NX-25S", "location": "Unit-2 / Compressor House / Aux Bay", "status": "operational", "install_date": "2019-09-01", "design_pressure": "30 bar (S) / 10 bar (T)", "material": "CS / CuNi Tubes", "heat_duty_kw": 600},
    ]

    # --- Vessels & Tanks (10) ---
    vessels = [
        {"tag": "V-101", "name": "Feed Water Storage Tank", "type": "Atmospheric Storage Tank", "manufacturer": "Bharat Tanks & Vessels", "model": "BTV-50KL", "location": "Unit-1 / Tank Farm / Bay-1", "status": "operational", "install_date": "2017-04-10", "design_pressure": "Atmospheric", "material": "MS with epoxy lining", "capacity_m3": 50},
        {"tag": "V-201", "name": "Reactor Vessel R-201", "type": "Pressure Reactor", "manufacturer": "Larsen & Toubro", "model": "LTPV-2500", "location": "Unit-2 / Reactor Building / Ground Level", "status": "operational", "install_date": "2018-03-05", "design_pressure": "45 bar @ 280°C", "material": "SA516 Gr.70 / SS321 Clad", "capacity_m3": 12.5},
        {"tag": "V-202", "name": "Flash Drum", "type": "Pressure Vessel", "manufacturer": "L&T", "model": "LTHV-1000", "location": "Unit-2 / Process Area / Elevated", "status": "operational", "install_date": "2018-05-22", "design_pressure": "8 bar @ 150°C", "material": "SA516 Gr.60", "capacity_m3": 5},
        {"tag": "V-301", "name": "Product Storage Tank T-301", "type": "Floating Roof Storage Tank", "manufacturer": "Bharat Tanks & Vessels", "model": "BTV-FR-100KL", "location": "Unit-3 / Tank Farm / Dyke-A", "status": "operational", "install_date": "2019-06-18", "design_pressure": "Atmospheric", "material": "CS with internal coating", "capacity_m3": 100},
        {"tag": "V-302", "name": "Product Storage Tank T-302", "type": "Floating Roof Storage Tank", "manufacturer": "Bharat Tanks & Vessels", "model": "BTV-FR-100KL", "location": "Unit-3 / Tank Farm / Dyke-A", "status": "operational", "install_date": "2019-06-18", "design_pressure": "Atmospheric", "material": "CS with internal coating", "capacity_m3": 100},
        {"tag": "V-401", "name": "Boiler Steam Drum", "type": "Pressure Vessel", "manufacturer": "Thermax", "model": "SD-6000", "location": "Utility / Boiler House / Top Floor", "status": "operational", "install_date": "2017-08-20", "design_pressure": "21 kg/cm² @ 200°C", "material": "SA515 Gr.70", "capacity_m3": 8},
        {"tag": "V-402", "name": "Deaerator Head + Storage", "type": "Pressure Vessel", "manufacturer": "Thermax", "model": "DA-3000", "location": "Utility / Boiler House / Mezzanine", "status": "operational", "install_date": "2017-08-20", "design_pressure": "3.5 kg/cm²", "material": "CS", "capacity_m3": 15},
        {"tag": "V-501", "name": "Fire Water Storage Tank", "type": "Atmospheric Storage Tank", "manufacturer": "Caldwell Tanks", "model": "CT-500KL", "location": "Fire Station / Tank Farm", "status": "operational", "install_date": "2017-06-01", "design_pressure": "Atmospheric", "material": "CS with epoxy lining", "capacity_m3": 500},
        {"tag": "V-103", "name": "Neutralization Tank", "type": "Agitated Vessel", "manufacturer": "Forbes Marshall", "model": "FM-AV-5K", "location": "Unit-1 / ETP / Chemical Treatment", "status": "operational", "install_date": "2020-03-10", "design_pressure": "Atmospheric", "material": "FRP", "capacity_m3": 5},
        {"tag": "V-203", "name": "Reflux Drum", "type": "Pressure Vessel", "manufacturer": "ISGEC Heavy Engineering", "model": "ISGEC-HV-800", "location": "Unit-2 / Distillation Area / Elevated", "status": "operational", "install_date": "2018-05-22", "design_pressure": "6 bar @ 120°C", "material": "SA516 Gr.60", "capacity_m3": 4},
    ]

    # --- Compressors (5) ---
    compressors = [
        {"tag": "C-101", "name": "Instrument Air Compressor", "type": "Rotary Screw Compressor", "manufacturer": "Atlas Copco", "model": "GA 55+ VSD", "location": "Utility / Compressor House / Bay-1", "status": "operational", "install_date": "2020-01-15", "design_pressure": "7.5 bar", "material": "CI/Al", "power_kw": 55},
        {"tag": "C-102", "name": "Plant Air Compressor", "type": "Rotary Screw Compressor", "manufacturer": "Atlas Copco", "model": "GA 45", "location": "Utility / Compressor House / Bay-2", "status": "standby", "install_date": "2020-01-15", "design_pressure": "7.5 bar", "material": "CI/Al", "power_kw": 45},
        {"tag": "C-201", "name": "Process Gas Compressor (1st Stage)", "type": "Reciprocating Compressor", "manufacturer": "Siemens", "model": "STC-GV 50/3", "location": "Unit-2 / Compressor House / Bay-1", "status": "operational", "install_date": "2019-09-01", "design_pressure": "35 bar", "material": "Forged Steel / PTFE rings", "power_kw": 250},
        {"tag": "C-202", "name": "Process Gas Compressor (2nd Stage)", "type": "Reciprocating Compressor", "manufacturer": "Siemens", "model": "STC-GV 50/3", "location": "Unit-2 / Compressor House / Bay-1", "status": "operational", "install_date": "2019-09-01", "design_pressure": "70 bar", "material": "Forged Steel / PTFE rings", "power_kw": 315},
        {"tag": "C-301", "name": "Nitrogen Compressor", "type": "Reciprocating Compressor", "manufacturer": "Ingersoll Rand", "model": "ESV-SSR 100", "location": "Utility / N2 Generation / Outdoor", "status": "operational", "install_date": "2019-02-28", "design_pressure": "10 bar", "material": "CS", "power_kw": 75},
    ]

    # --- Electric Motors (8) ---
    motors = [
        {"tag": "M-101A", "name": "Motor - Feed Water Pump A", "type": "Squirrel Cage Induction Motor", "manufacturer": "ABB", "model": "M3BP 315 SMC 4", "location": "Unit-1 / Pump House / Bay-A", "status": "operational", "install_date": "2019-03-15", "power_kw": 55, "voltage": "415V", "speed_rpm": 1480},
        {"tag": "M-101B", "name": "Motor - Feed Water Pump B", "type": "Squirrel Cage Induction Motor", "manufacturer": "ABB", "model": "M3BP 315 SMC 4", "location": "Unit-1 / Pump House / Bay-A", "status": "standby", "install_date": "2019-03-15", "power_kw": 55, "voltage": "415V", "speed_rpm": 1480},
        {"tag": "M-201A", "name": "Motor - CW Pump A", "type": "Squirrel Cage Induction Motor", "manufacturer": "Siemens", "model": "1LA7 316-4AA", "location": "Unit-2 / CT / Pump Bay", "status": "operational", "install_date": "2018-11-20", "power_kw": 90, "voltage": "415V", "speed_rpm": 1485},
        {"tag": "M-201B", "name": "Motor - CW Pump B", "type": "Squirrel Cage Induction Motor", "manufacturer": "Siemens", "model": "1LA7 316-4AA", "location": "Unit-2 / CT / Pump Bay", "status": "standby", "install_date": "2018-11-20", "power_kw": 90, "voltage": "415V", "speed_rpm": 1485},
        {"tag": "M-202", "name": "Motor - Reactor Feed Pump", "type": "Squirrel Cage Induction Motor", "manufacturer": "ABB", "model": "M3BP 280 SMB 4", "location": "Unit-2 / Process Area / GF", "status": "operational", "install_date": "2019-07-22", "power_kw": 37, "voltage": "415V", "speed_rpm": 1475},
        {"tag": "M-C201", "name": "Motor - Process Gas Compr. 1st Stage", "type": "Synchronous Motor", "manufacturer": "Siemens", "model": "1FJ6 354-4", "location": "Unit-2 / Compressor House", "status": "operational", "install_date": "2019-09-01", "power_kw": 250, "voltage": "6600V", "speed_rpm": 740},
        {"tag": "M-C202", "name": "Motor - Process Gas Compr. 2nd Stage", "type": "Synchronous Motor", "manufacturer": "Siemens", "model": "1FJ6 404-4", "location": "Unit-2 / Compressor House", "status": "operational", "install_date": "2019-09-01", "power_kw": 315, "voltage": "6600V", "speed_rpm": 740},
        {"tag": "M-401", "name": "Motor - BFW Pump", "type": "Squirrel Cage Induction Motor", "manufacturer": "ABB", "model": "M3BP 315 MLA 4", "location": "Utility / Boiler House / Pump Room", "status": "operational", "install_date": "2017-08-20", "power_kw": 75, "voltage": "415V", "speed_rpm": 1480},
    ]

    # --- Control Valves (8) ---
    valves = [
        {"tag": "FV-101", "name": "Feed Flow Control Valve", "type": "Globe Control Valve", "manufacturer": "Emerson", "model": "Fisher ED V150S", "location": "Unit-1 / Process Area / Pipe Rack", "status": "operational", "install_date": "2020-07-12", "size": "4 inch", "material": "WCB / SS316 Trim"},
        {"tag": "FV-201", "name": "Reactor Inlet Flow Control Valve", "type": "Globe Control Valve", "manufacturer": "Emerson", "model": "Fisher V250", "location": "Unit-2 / Reactor Building / Feed Line", "status": "operational", "install_date": "2018-03-05", "size": "3 inch", "material": "CF8M"},
        {"tag": "TV-201", "name": "Reactor Temperature Control Valve", "type": "Globe Control Valve", "manufacturer": "Emerson", "model": "Fisher ET 1-in", "location": "Unit-2 / Reactor Building / Cooling Line", "status": "operational", "install_date": "2018-03-05", "size": "2 inch", "material": "WCB / SS316"},
        {"tag": "PV-201", "name": "Reactor Pressure Control Valve", "type": "Globe Control Valve", "manufacturer": "Masoneilan", "model": "41005 Series", "location": "Unit-2 / Process Area / Off-gas Line", "status": "operational", "install_date": "2018-05-22", "size": "3 inch", "material": "WCB / 17-4PH Trim"},
        {"tag": "LV-301", "name": "Product Tank Level Control Valve", "type": "Butterfly Control Valve", "manufacturer": "Metso", "model": "Neles NDX", "location": "Unit-3 / Tank Farm / Outlet Line", "status": "operational", "install_date": "2019-06-18", "size": "6 inch", "material": "CS / SS316 Disc"},
        {"tag": "FV-401", "name": "Boiler Feed Water Control Valve", "type": "Globe Control Valve", "manufacturer": "Emerson", "model": "Fisher EZ", "location": "Utility / Boiler House / Feed Line", "status": "operational", "install_date": "2017-08-20", "size": "3 inch", "material": "WCB / Stellite Trim"},
        {"tag": "SDV-201", "name": "Reactor Emergency Shutdown Valve", "type": "Ball Valve (Automated)", "manufacturer": "Neles", "model": "Jamesbury 9000", "location": "Unit-2 / Reactor Building / Feed Line", "status": "operational", "install_date": "2018-03-05", "size": "3 inch", "material": "SS316 / PTFE Seats"},
        {"tag": "BDV-201", "name": "Reactor Blowdown Valve", "type": "Ball Valve (Automated)", "manufacturer": "Cameron", "model": "WKM 370D6", "location": "Unit-2 / Reactor Building / Blowdown Line", "status": "operational", "install_date": "2018-03-05", "size": "2 inch", "material": "CS / SS316"},
    ]

    # --- Safety Valves (5) ---
    safety_valves = [
        {"tag": "PSV-101", "name": "Relief Valve - Feed System", "type": "Spring Loaded Safety Valve", "manufacturer": "Leser", "model": "441 HP", "location": "Unit-1 / Process Area / P-101A Discharge", "status": "operational", "install_date": "2019-03-15", "set_pressure": "18 bar", "material": "WCB / SS316 Trim"},
        {"tag": "PSV-201", "name": "Relief Valve - Reactor", "type": "Spring Loaded Safety Valve", "manufacturer": "Leser", "model": "526 HiP", "location": "Unit-2 / Reactor Building / Reactor Top", "status": "operational", "install_date": "2018-03-05", "set_pressure": "49.5 bar", "material": "A217 WC6 / Stellite Trim"},
        {"tag": "PSV-202", "name": "Relief Valve - Flash Drum", "type": "Spring Loaded Safety Valve", "manufacturer": "Crosby", "model": "JOS-E", "location": "Unit-2 / Process Area / V-202 Top", "status": "operational", "install_date": "2018-05-22", "set_pressure": "8.8 bar", "material": "WCB / SS316 Nozzle"},
        {"tag": "PSV-401", "name": "Relief Valve - Boiler Drum", "type": "Spring Loaded Safety Valve", "manufacturer": "Leser", "model": "441 HiP", "location": "Utility / Boiler House / Steam Drum", "status": "operational", "install_date": "2017-08-20", "set_pressure": "23 kg/cm²", "material": "WCB / Stellite"},
        {"tag": "PSV-301", "name": "Relief Valve - Product Tank Vent", "type": "Pressure/Vacuum Vent Valve", "manufacturer": "Groth", "model": "1200A", "location": "Unit-3 / Tank Farm / T-301 Roof", "status": "operational", "install_date": "2019-06-18", "set_pressure": "+35 / -8 mmWC", "material": "Al"},
    ]

    # --- Columns & Towers (3) ---
    columns = [
        {"tag": "T-201", "name": "Distillation Column", "type": "Tray Column", "manufacturer": "ISGEC Heavy Engineering", "model": "ISGEC-DC-3500", "location": "Unit-2 / Distillation Area / Outdoor", "status": "operational", "install_date": "2018-05-22", "design_pressure": "6 bar @ 200°C", "material": "SA516 Gr.70 / SS410 Trays", "trays": 40},
        {"tag": "T-202", "name": "Absorption Tower", "type": "Packed Column", "manufacturer": "ISGEC Heavy Engineering", "model": "ISGEC-AT-2000", "location": "Unit-2 / Gas Treatment / Outdoor", "status": "operational", "install_date": "2018-05-22", "design_pressure": "4 bar @ 80°C", "material": "CS / PP Packing", "packing_height_m": 8},
        {"tag": "T-101", "name": "Stripper Column", "type": "Packed Column", "manufacturer": "L&T", "model": "LT-SC-1500", "location": "Unit-1 / Water Treatment / Indoor", "status": "operational", "install_date": "2019-03-15", "design_pressure": "2 bar @ 105°C", "material": "SS304 / SS316 Packing", "packing_height_m": 5},
    ]

    # --- Boiler (2) ---
    boilers = [
        {"tag": "B-101", "name": "Process Steam Boiler (Coal/Gas)", "type": "Water Tube Boiler", "manufacturer": "Thermax", "model": "Shellmax 6000", "location": "Utility / Boiler House / Main Bay", "status": "operational", "install_date": "2017-08-20", "design_pressure": "21 kg/cm² @ 200°C", "material": "SA515 Gr.70", "steam_capacity_tph": 6},
        {"tag": "B-102", "name": "Thermic Fluid Heater", "type": "Thermic Fluid Heater", "manufacturer": "Thermax", "model": "Thermion 2000", "location": "Utility / TF Heater House", "status": "operational", "install_date": "2018-11-10", "design_pressure": "10 bar @ 300°C", "material": "CS / SA106 Gr.B Coils", "heat_output_kw": 2000},
    ]

    # --- Others (11) ---
    others = [
        {"tag": "AG-101", "name": "Diesel Generator Set (Standby)", "type": "Diesel Generator", "manufacturer": "Cummins India", "model": "C1000D5 (KTA50-G3)", "location": "Utility / DG Room / Bay-1", "status": "standby", "install_date": "2018-01-15", "power_kw": 1000},
        {"tag": "CT-101", "name": "Induced Draft Cooling Tower", "type": "Cooling Tower", "manufacturer": "Paharpur Cooling Towers", "model": "CTI-500/4", "location": "Unit-2 / Outdoor / North Side", "status": "operational", "install_date": "2018-06-10", "material": "FRP / PVC Fill", "cooling_capacity_kw": 5000},
        {"tag": "TK-101", "name": "Liquid Nitrogen Storage Tank", "type": "Cryogenic Storage Vessel", "manufacturer": "Inox India", "model": "CVS-20000", "location": "Utility / N2 Area / Outdoor", "status": "operational", "install_date": "2019-02-28", "design_pressure": "18 bar", "material": "SS304L Inner / CS Outer", "capacity_m3": 20},
        {"tag": "AD-101", "name": "Instrument Air Dryer", "type": "Desiccant Air Dryer", "manufacturer": "Atlas Copco", "model": "CD 250+", "location": "Utility / Compressor House / Bay-3", "status": "operational", "install_date": "2020-01-15", "dew_point": "-40°C"},
        {"tag": "FLT-101", "name": "Instrument Air Filter", "type": "Coalescing Filter", "manufacturer": "Parker Domnick Hunter", "model": "OIL-X AA0700G", "location": "Utility / Compressor House / Bay-3", "status": "operational", "install_date": "2020-01-15"},
        {"tag": "TR-101", "name": "Power Transformer 6.6kV/415V", "type": "Oil Filled Transformer", "manufacturer": "Siemens", "model": "TUMETIC 1600 kVA", "location": "Electrical / Substation / Outdoor", "status": "operational", "install_date": "2017-04-01", "power_kw": 1600, "voltage": "6600V/415V"},
        {"tag": "SW-101", "name": "Main HT Switchgear Panel", "type": "HT Switchgear", "manufacturer": "ABB", "model": "UniGear ZS1 12kV", "location": "Electrical / Substation / Indoor", "status": "operational", "install_date": "2017-04-01"},
        {"tag": "UPS-101", "name": "UPS System - DCS/SIS", "type": "Online UPS", "manufacturer": "Emerson / Vertiv", "model": "Liebert eXL S1 100kVA", "location": "Electrical / UPS Room", "status": "operational", "install_date": "2018-03-01", "power_kw": 100},
        {"tag": "WTP-101", "name": "RO Water Treatment Plant", "type": "Reverse Osmosis System", "manufacturer": "Ion Exchange India", "model": "INDION RO-500", "location": "Utility / WTP / Indoor", "status": "operational", "install_date": "2018-04-12", "capacity_m3_hr": 25},
        {"tag": "ETP-101", "name": "Effluent Treatment Plant", "type": "Biological ETP", "manufacturer": "Thermax", "model": "PRISM ETP-50", "location": "Utility / ETP / Outdoor", "status": "operational", "install_date": "2019-05-15", "capacity_m3_hr": 50},
        {"tag": "CRA-101", "name": "EOT Crane - Boiler House", "type": "Electric Overhead Traveling Crane", "manufacturer": "Anupam Industries", "model": "EOT 10T x 15m Span", "location": "Utility / Boiler House / Overhead", "status": "operational", "install_date": "2017-08-20", "capacity_tons": 10},
    ]

    equipment.extend(pumps)
    equipment.extend(heat_exchangers)
    equipment.extend(vessels)
    equipment.extend(compressors)
    equipment.extend(motors)
    equipment.extend(valves)
    equipment.extend(safety_valves)
    equipment.extend(columns)
    equipment.extend(boilers)
    equipment.extend(others)

    return equipment


# ============================================================================
# 2. REGULATIONS (25 items with real clause descriptions)
# ============================================================================

def generate_regulations():
    """Generate 25 regulatory standards with real clause-level detail."""
    return [
        {"standard_id": "OISD-STD-105", "title": "Work Permit System", "body": "Establishes a mandatory work permit system for all petroleum industry installations. Covers cold work permits, hot work permits, confined space entry permits, electrical isolation permits, and excavation permits. Requires identification of hazards, precautions, PPE requirements, and authorization levels for each permit type. Mandates permit validity periods, monitoring requirements, and closure procedures.", "version": "2024", "status": "active", "category": "Safety"},
        {"standard_id": "OISD-STD-116", "title": "Fire Protection for Onshore Hydrocarbon Installations", "body": "Comprehensive standard for fire protection facilities at petroleum refineries, gas processing plants, and petrochemical complexes. Specifies minimum water storage requirements (4 hours at design rate), hydrant spacing (max 45m), foam system design for atmospheric and pressure storage tanks, fire water pump redundancy (min 2 pumps, one diesel-driven), deluge systems for critical equipment, and fire detection/alarm requirements.", "version": "2023", "status": "active", "category": "Fire Safety"},
        {"standard_id": "OISD-STD-117", "title": "Fire Protection for Terminals and Depots", "body": "Specifies fire protection requirements for petroleum storage terminals and depots including tank-to-tank spacing, dyke wall design, foam pourer sizing for fixed/semi-fixed systems, fire water ring main design, and emergency response organization. Requires periodic mock drills and equipment testing schedules.", "version": "2023", "status": "active", "category": "Fire Safety"},
        {"standard_id": "OISD-STD-118", "title": "Layout for Oil and Gas Installations", "body": "Specifies minimum separation distances between process units, storage tanks, flares, buildings, and plant boundaries. Defines block-in valve requirements, emergency access road widths (min 6m), and clearances from overhead power lines. Includes API RP 752 blast zone considerations for occupied buildings.", "version": "2022", "status": "active", "category": "Layout & Design"},
        {"standard_id": "OISD-STD-144", "title": "Petroleum Industry Safety in Electrical Installations", "body": "Covers hazardous area classification (Zone 0, 1, 2 for gas/vapour; Zone 20, 21, 22 for dust) per IS/IEC 60079 series. Specifies selection of explosion-proof, increased safety, and intrinsically safe electrical equipment. Mandates periodic inspection of Ex equipment, cable gland integrity, earthing/bonding requirements, and lightning protection.", "version": "2022", "status": "active", "category": "Electrical Safety"},
        {"standard_id": "OISD-STD-154", "title": "Safety Aspects in Functional Design", "body": "Covers safety requirements during functional design of process plants. Includes HAZOP study requirements, SIL assessment criteria, safety instrumented system (SIS) design per IEC 61511, relief system sizing, flare system design, and blowdown philosophy. Mandates independent safety layers including BPCS, SIS, and mechanical protection.", "version": "2021", "status": "active", "category": "Design Safety"},
        {"standard_id": "OISD-GDN-206", "title": "Guidelines on Safety Management System", "body": "Comprehensive SMS framework covering 15 elements: leadership and commitment, policy, organization and competency, risk identification and assessment, design and operations, change management, emergency preparedness, investigation and reporting, audit and review, documentation, contractor safety, occupation health, process safety information, mechanical integrity, and management review. Aligned with OSHA PSM 29 CFR 1910.119.", "version": "2024", "status": "active", "category": "Management System"},
        {"standard_id": "OISD-STD-137", "title": "Inspection of Cross Country Pipelines", "body": "Covers inspection methods for hydrocarbon cross-country pipelines including intelligent pigging (MFL, caliper, geometry tools), hydrostatic testing, cathodic protection survey, coating condition assessment, and pipeline integrity management systems (PIMS). Defines inspection intervals based on risk.", "version": "2023", "status": "active", "category": "Inspection"},
        {"standard_id": "FACTORY-ACT-1948", "title": "The Factories Act, 1948", "body": "Central legislation governing occupational safety, health, and welfare in factories employing 10+ workers (with power) or 20+ workers (without power). Key chapters: Chapter III (Health) - cleanliness, ventilation, lighting, drinking water; Chapter IV (Safety) - fencing of machinery, pressure plant registration, lifting equipment testing, fire exits; Chapter V (Welfare) - first aid, canteens, restrooms; Chapter VI (Working Hours) - 48 hrs/week, overtime, weekly holidays; Chapter VII (Employment of Young Persons). Amended multiple times, latest major amendment in 2016.", "version": "2016-amendment", "status": "active", "category": "Indian Law"},
        {"standard_id": "FACTORY-RULES-STATE", "title": "State Factory Rules (Model)", "body": "State-level rules implementing the Factories Act, 1948. Cover specific requirements for boiler inspections, pressure vessel registration, annual factory license renewal, occupier/manager responsibilities, accident reporting timelines (within 4 hours for fatal, 12 hours for serious), and factory inspector powers.", "version": "2020", "status": "active", "category": "Indian Law"},
        {"standard_id": "IS-2825", "title": "Code for Unfired Pressure Vessels", "body": "Bureau of Indian Standards code for design, fabrication, inspection, and testing of unfired pressure vessels. Covers material selection (carbon steel, alloy steel, stainless steel), design by rule calculations, welding procedures and qualifications per IS 28/ASME Sec IX, post-weld heat treatment requirements, NDE acceptance criteria, hydrostatic test procedures (1.5x design pressure for 30 min minimum), and nameplate stamping requirements.", "version": "2021", "status": "active", "category": "Design Standard"},
        {"standard_id": "IS-803", "title": "Code of Practice for Industrial Lighting", "body": "Prescribes minimum illumination levels for different industrial areas: process areas (200 lux), control rooms (500 lux), workshops (300-500 lux), storage areas (100 lux), outdoor walkways (20 lux), emergency lighting (10% of normal). Covers glare limitation, uniformity ratios, color rendering requirements, and emergency lighting with battery backup duration.", "version": "2019", "status": "active", "category": "Facility Standard"},
        {"standard_id": "API-570", "title": "Piping Inspection Code - In-service", "body": "In-service inspection, rating, repair, and alteration of piping systems. Defines inspection intervals based on corrosion rates and remaining life: maximum 10 years or half remaining life (whichever is less) for general inspection, maximum 5 years for thickness measurement locations. Covers CML (Condition Monitoring Location) selection, corrosion rate calculation methods (short-term, long-term, next inspection rate), minimum remaining thickness calculations per ASME B31.3, and fitness-for-service assessments per API 579.", "version": "2020", "status": "active", "category": "Inspection"},
        {"standard_id": "API-510", "title": "Pressure Vessel Inspection Code - In-service", "body": "In-service inspection, rating, repair, and alteration of pressure vessels built to ASME Section VIII. Defines maximum inspection intervals: internal/on-stream — 10 years or half remaining life; external visual — 5 years. Covers MAWP recalculation, retirement thickness determination, repair/alteration requirements including welding requalification, fitness-for-service evaluation per API 579, and pressure testing requirements after repairs.", "version": "2020", "status": "active", "category": "Inspection"},
        {"standard_id": "API-653", "title": "Tank Inspection, Repair, Alteration and Reconstruction", "body": "Covers in-service inspection of aboveground storage tanks built to API 650 or API 12C. Specifies shell thickness evaluation, bottom plate scanning requirements, settlement surveys, floating roof seal inspection, tank internal inspection intervals (max 20 years with RBI), external inspection every 5 years, and robotic/NDT methods for in-service bottom plate assessment.", "version": "2021", "status": "active", "category": "Inspection"},
        {"standard_id": "ASME-B31.3", "title": "Process Piping", "body": "ASME code for design, materials, fabrication, assembly, erection, examination, inspection, and testing of process piping systems. Covers pressure design calculations for straight pipe, branch connections, and expansion joints. Specifies allowable stresses for materials at temperature, weld joint efficiency factors, NDE requirements per fluid category (Category D, Normal, Category M), and leak/hydrostatic test requirements.", "version": "2022", "status": "active", "category": "Design Standard"},
        {"standard_id": "ASME-SEC-VIII-D1", "title": "ASME Boiler & Pressure Vessel Code, Section VIII Division 1", "body": "Rules for construction of pressure vessels. Covers design by rule for shells, heads, nozzles, and supports. Specifies material requirements, welding qualifications per ASME Sec IX, post-weld heat treatment, NDE requirements based on joint category and efficiency, hydrostatic testing (min 1.3x MAWP), and U-stamp certification requirements.", "version": "2023", "status": "active", "category": "Design Standard"},
        {"standard_id": "NFPA-30", "title": "Flammable and Combustible Liquids Code", "body": "NFPA standard covering storage, handling, and use of flammable (flash point <100°F) and combustible (flash point ≥100°F) liquids. Classifies liquids as Class I (IA, IB, IC), II, IIIA, IIIB. Specifies storage requirements: tank spacing, venting, overflow protection, secondary containment (110% of largest tank), piping materials, and fire protection for storage areas.", "version": "2021", "status": "active", "category": "Fire Safety"},
        {"standard_id": "ISO-45001", "title": "Occupational Health and Safety Management Systems", "body": "International standard for OH&S management systems replacing OHSAS 18001. Based on Annex SL high-level structure with Plan-Do-Check-Act. Key clauses: 4 (Context of organization), 5 (Leadership and worker participation), 6 (Planning — hazard identification, risk assessment, legal requirements), 7 (Support — competence, awareness, communication), 8 (Operation — hierarchy of controls, emergency preparedness, procurement, contractor management), 9 (Performance evaluation — monitoring, audit, management review), 10 (Improvement — incident investigation, corrective actions, continual improvement).", "version": "2018", "status": "active", "category": "Management System"},
        {"standard_id": "ISO-14001", "title": "Environmental Management Systems", "body": "Specifies requirements for establishing, implementing, maintaining, and improving an environmental management system. Covers environmental aspects and impacts identification, legal compliance obligations, environmental objectives and targets, operational controls for significant aspects, emergency preparedness and response, monitoring and measurement, compliance evaluation, and management review.", "version": "2015", "status": "active", "category": "Management System"},
        {"standard_id": "PESO-RULES", "title": "Petroleum and Explosives Safety Organization Rules", "body": "Rules governing storage, transport, and handling of petroleum products and explosives in India under PESO (formerly CCOE — Chief Controller of Explosives). Covers storage license requirements, tank design approvals, overfill protection, vapor recovery systems, tank truck loading/unloading safety, and periodic inspection requirements. License renewal every 5 years.", "version": "2023", "status": "active", "category": "Indian Law"},
        {"standard_id": "IBR-1950", "title": "Indian Boiler Regulations, 1950", "body": "Regulations governing design, construction, inspection, and operation of boilers in India. Mandates annual IBR inspection by competent person (state boiler inspector or insurance company surveyor), boiler registration and certificate of fitness, operator competency certificate requirements, and boiler attendant staffing based on boiler capacity. Covers safety valve testing, water level indicator testing, and steam pressure gauge calibration requirements.", "version": "2023-amendment", "status": "active", "category": "Indian Law"},
        {"standard_id": "IS-3589", "title": "Specification for Electrically Welded Steel Pipes for Water, Gas and Sewage", "body": "BIS standard specifying requirements for ERW and SAW steel pipes for utility services. Covers pipe dimensions, material grades (IS 2062 Fe410/Fe490), weld inspection requirements, hydrostatic test pressure, protective coating (bituminous or epoxy), and cement mortar lining for water service.", "version": "2018", "status": "active", "category": "Material Standard"},
        {"standard_id": "IEC-61511", "title": "Safety Instrumented Systems for the Process Industry", "body": "International standard for design, installation, operation, and maintenance of safety instrumented systems (SIS) in the process industry. Defines Safety Integrity Level (SIL) requirements: SIL 1 (RRF 10-100), SIL 2 (RRF 100-1000), SIL 3 (RRF 1000-10000). Covers SIS lifecycle, proof test requirements, diagnostic coverage, common cause failure analysis, and periodic functional testing intervals based on SIL level.", "version": "2023", "status": "active", "category": "Instrumentation"},
        {"standard_id": "API-RP-580", "title": "Risk-Based Inspection", "body": "Recommended practice for risk-based inspection (RBI) methodology. Defines probability of failure (PoF) based on damage mechanisms, corrosion rates, and inspection effectiveness. Consequence of failure (CoF) assessment includes flammable/toxic release scenarios, business impact, and environmental impact. Risk matrix (5x5) determines inspection priority and interval. Covers RBI reassessment triggers including process changes, incidents, and new damage mechanism identification.", "version": "2022", "status": "active", "category": "Inspection"},
    ]


# ============================================================================
# 3. PERSONNEL (40 items with certifications)
# ============================================================================

def generate_personnel():
    """Generate 40 personnel with realistic designations and certifications."""
    return [
        {"employee_id": "EMP-001", "name": "Rajesh Kumar Sharma", "role": "Senior Maintenance Engineer", "department": "Maintenance", "certification": "API-510, API-570", "experience_years": 18},
        {"employee_id": "EMP-002", "name": "Suresh Patel", "role": "Mechanical Fitter (Senior)", "department": "Maintenance", "certification": "ITI Fitter, Rigging Level-2", "experience_years": 15},
        {"employee_id": "EMP-003", "name": "Amit Kumar Singh", "role": "Electrical Technician (Senior)", "department": "Electrical", "certification": "Electrical Supervisor Certificate of Competency", "experience_years": 12},
        {"employee_id": "EMP-004", "name": "Priya Sharma", "role": "Process Engineer", "department": "Operations", "certification": "B.Tech Chemical Engineering", "experience_years": 8},
        {"employee_id": "EMP-005", "name": "Vikram Reddy", "role": "Plant Manager", "department": "Management", "certification": "M.Tech Chemical, MBA", "experience_years": 25},
        {"employee_id": "EMP-006", "name": "Deepak Verma", "role": "Safety Officer", "department": "HSE", "certification": "ADIS (Advanced Diploma in Industrial Safety)", "experience_years": 14},
        {"employee_id": "EMP-007", "name": "Arun Nair", "role": "Instrument Technician (Senior)", "department": "Instrumentation", "certification": "ISA CCST Level II", "experience_years": 11},
        {"employee_id": "EMP-008", "name": "Sanjay Gupta", "role": "Rotating Equipment Specialist", "department": "Maintenance", "certification": "Vibration Analyst Cat-III (ISO 18436-2)", "experience_years": 20},
        {"employee_id": "EMP-009", "name": "Kavitha Rajan", "role": "Reliability Engineer", "department": "Maintenance", "certification": "CMRP (Certified Maintenance & Reliability Professional)", "experience_years": 10},
        {"employee_id": "EMP-010", "name": "Mohan Das", "role": "Welding Inspector", "department": "QC", "certification": "CSWIP 3.1, ASNT Level II (RT/UT/MT/PT)", "experience_years": 16},
        {"employee_id": "EMP-011", "name": "Anita Desai", "role": "Compliance & Regulatory Officer", "department": "HSE", "certification": "NEBOSH IGC, ISO 45001 Lead Auditor", "experience_years": 12},
        {"employee_id": "EMP-012", "name": "Ravi Shankar", "role": "Shift Supervisor (Operations)", "department": "Operations", "certification": "B.Sc Chemistry, Process Safety Mgmt Training", "experience_years": 16},
        {"employee_id": "EMP-013", "name": "Bharat Mehta", "role": "Planning Engineer (Maintenance)", "department": "Planning", "certification": "SAP PM Module Certified", "experience_years": 9},
        {"employee_id": "EMP-014", "name": "Sunita Rao", "role": "Inspection Engineer", "department": "QC", "certification": "API-510, API-570, API-653, ASNT Level II", "experience_years": 14},
        {"employee_id": "EMP-015", "name": "Naveen Joshi", "role": "Fire & Safety Officer", "department": "HSE", "certification": "B.E. Fire Engineering, Sub Divisional Fire Officer Certificate", "experience_years": 13},
        {"employee_id": "EMP-016", "name": "Pooja Iyer", "role": "Environmental Engineer", "department": "HSE", "certification": "M.Sc Environmental Science, ISO 14001 LA", "experience_years": 7},
        {"employee_id": "EMP-017", "name": "Ramesh Chandra Tiwari", "role": "Store Keeper (Technical)", "department": "Stores", "certification": "SAP MM Module", "experience_years": 20},
        {"employee_id": "EMP-018", "name": "Kiran Babu", "role": "DCS Operator (Panel)", "department": "Operations", "certification": "DCS Operation Training (Honeywell Experion)", "experience_years": 8},
        {"employee_id": "EMP-019", "name": "Manoj Tiwari", "role": "Crane Operator", "department": "Operations", "certification": "Crane Operator License (PESO)", "experience_years": 15},
        {"employee_id": "EMP-020", "name": "Lakshmi Nair", "role": "Lab Analyst (Senior)", "department": "Quality", "certification": "M.Sc Analytical Chemistry", "experience_years": 10},
        {"employee_id": "EMP-021", "name": "Dinesh Yadav", "role": "Mechanical Fitter", "department": "Maintenance", "certification": "ITI Fitter", "experience_years": 6},
        {"employee_id": "EMP-022", "name": "Vinod Kumar", "role": "Helper (Mechanical)", "department": "Maintenance", "certification": "10th Pass, OJT", "experience_years": 4},
        {"employee_id": "EMP-023", "name": "Gopal Krishna", "role": "Instrument Technician", "department": "Instrumentation", "certification": "Diploma Instrumentation", "experience_years": 5},
        {"employee_id": "EMP-024", "name": "Arjun Mishra", "role": "Electrical Technician", "department": "Electrical", "certification": "ITI Electrician", "experience_years": 7},
        {"employee_id": "EMP-025", "name": "Sandeep Kulkarni", "role": "Process Engineer (Senior)", "department": "Operations", "certification": "M.Tech Chemical, Six Sigma Green Belt", "experience_years": 15},
        {"employee_id": "EMP-026", "name": "Meera Krishnan", "role": "HSE Coordinator", "department": "HSE", "certification": "IOSH Managing Safely, First Aid Trainer", "experience_years": 8},
        {"employee_id": "EMP-027", "name": "Rohit Saxena", "role": "Shift Supervisor (Operations)", "department": "Operations", "certification": "Diploma Chemical Engineering", "experience_years": 18},
        {"employee_id": "EMP-028", "name": "Ashok Pillai", "role": "Boiler Operator (1st Class)", "department": "Utility", "certification": "First Class Boiler Attendant Certificate", "experience_years": 22},
        {"employee_id": "EMP-029", "name": "Pramod Shetty", "role": "Welder (Special Class)", "department": "Maintenance", "certification": "IBR Welder, 6G Qualified (SMAW/GTAW)", "experience_years": 14},
        {"employee_id": "EMP-030", "name": "Nandini Rao", "role": "Safety Trainer", "department": "HSE", "certification": "NEBOSH International Diploma, OSHA 511", "experience_years": 11},
        {"employee_id": "EMP-031", "name": "Vijay Prakash", "role": "Condition Monitoring Technician", "department": "Maintenance", "certification": "Vibration Analyst Cat-II, Thermography Level-I", "experience_years": 9},
        {"employee_id": "EMP-032", "name": "Harish Bhat", "role": "NDT Technician (Senior)", "department": "QC", "certification": "ASNT Level II (UT, RT, MT, PT, TOFD)", "experience_years": 13},
        {"employee_id": "EMP-033", "name": "Sunil Jha", "role": "Piping Engineer", "department": "Engineering", "certification": "B.Tech Mechanical, CAESAR II Certified", "experience_years": 10},
        {"employee_id": "EMP-034", "name": "Rakesh Pandey", "role": "DCS Operator (Field)", "department": "Operations", "certification": "Diploma Instrumentation", "experience_years": 6},
        {"employee_id": "EMP-035", "name": "Asha Devi", "role": "Lab Analyst", "department": "Quality", "certification": "B.Sc Chemistry", "experience_years": 4},
        {"employee_id": "EMP-036", "name": "Praveen Kumar", "role": "Electrician (HT)", "department": "Electrical", "certification": "HT Switching Authorization", "experience_years": 12},
        {"employee_id": "EMP-037", "name": "Srinivas Reddy", "role": "Maintenance Manager", "department": "Maintenance", "certification": "B.Tech Mechanical, CMRP, Six Sigma Black Belt", "experience_years": 22},
        {"employee_id": "EMP-038", "name": "Ajay Thakur", "role": "Civil Maintenance Supervisor", "department": "Maintenance", "certification": "Diploma Civil Engineering", "experience_years": 16},
        {"employee_id": "EMP-039", "name": "Deepa Menon", "role": "Document Controller", "department": "Engineering", "certification": "ISO 9001 Certified Document Controller", "experience_years": 8},
        {"employee_id": "EMP-040", "name": "Mukesh Agarwal", "role": "Procurement Officer (Technical)", "department": "Procurement", "certification": "B.Tech Mechanical, SAP MM Certified", "experience_years": 11},
    ]


# ============================================================================
# 4. FAILURE MODES (30 items with RCM data)
# ============================================================================

def generate_failure_modes():
    """Generate 30 failure modes based on real RCM patterns."""
    return [
        {"code": "FM-SEAL-LEAK", "description": "Mechanical seal leakage — excessive dripping or spray from seal housing", "severity": "high", "frequency": 12, "mtbf_hours": 8760, "equipment_types": ["Centrifugal Pump", "Positive Displacement Pump", "Multistage Centrifugal Pump"], "root_causes": "Dry running, thermal shock, misalignment, incorrect seal face material, shaft runout > 0.05mm"},
        {"code": "FM-BEARING-FAIL", "description": "Bearing failure — noise, vibration, overheating at bearing housing", "severity": "critical", "frequency": 8, "mtbf_hours": 17520, "equipment_types": ["Centrifugal Pump", "Electric Motor", "Compressor"], "root_causes": "Fatigue spalling, inadequate lubrication, contaminated grease, misalignment, overloading"},
        {"code": "FM-IMPELLER-WEAR", "description": "Impeller erosion/cavitation wear — reduced head and flow, vibration", "severity": "medium", "frequency": 4, "mtbf_hours": 26280, "equipment_types": ["Centrifugal Pump", "Multistage Centrifugal Pump"], "root_causes": "Cavitation (low NPSH), abrasive particles in fluid, chemical attack, vane tip recirculation"},
        {"code": "FM-CAVITATION", "description": "Pump cavitation — rumbling noise, flow fluctuation, impeller damage", "severity": "high", "frequency": 6, "mtbf_hours": 4380, "equipment_types": ["Centrifugal Pump"], "root_causes": "Insufficient NPSH available, suction strainer blockage, high fluid temperature, excessive suction losses"},
        {"code": "FM-TUBE-FOUL", "description": "Heat exchanger tube fouling — reduced heat transfer, increased pressure drop", "severity": "medium", "frequency": 10, "mtbf_hours": 4380, "equipment_types": ["Shell & Tube Heat Exchanger", "Finned Tube Heat Exchanger"], "root_causes": "Scaling (CaCO3/CaSO4), biological growth, particulate deposition, corrosion product accumulation"},
        {"code": "FM-TUBE-LEAK", "description": "Heat exchanger tube leak — product contamination, pressure loss", "severity": "high", "frequency": 3, "mtbf_hours": 35040, "equipment_types": ["Shell & Tube Heat Exchanger"], "root_causes": "Erosion-corrosion, tube vibration fatigue, pitting corrosion, stress corrosion cracking"},
        {"code": "FM-VALVE-STICK", "description": "Control valve sticking/seizure — erratic control, hunting", "severity": "medium", "frequency": 5, "mtbf_hours": 8760, "equipment_types": ["Globe Control Valve", "Butterfly Control Valve"], "root_causes": "Packing friction, stem corrosion, process deposits, actuator diaphragm failure, positioner drift"},
        {"code": "FM-MOTOR-OVH", "description": "Electric motor overheating — high winding temperature alarm/trip", "severity": "high", "frequency": 4, "mtbf_hours": 17520, "equipment_types": ["Squirrel Cage Induction Motor", "Synchronous Motor"], "root_causes": "Overloading, voltage imbalance >2%, blocked ventilation, high ambient temperature, single phasing"},
        {"code": "FM-CORROSION-INT", "description": "Internal corrosion — wall thinning, pitting, metal loss", "severity": "critical", "frequency": 2, "mtbf_hours": 43800, "equipment_types": ["Atmospheric Storage Tank", "Pressure Vessel", "Pressure Reactor"], "root_causes": "CO2 corrosion, H2S corrosion, under-deposit corrosion, microbiologically influenced corrosion (MIC)"},
        {"code": "FM-VIBRATION-MISALIGN", "description": "Excessive vibration due to misalignment — 2x RPM dominant", "severity": "high", "frequency": 7, "mtbf_hours": 8760, "equipment_types": ["Centrifugal Pump", "Electric Motor", "Compressor"], "root_causes": "Angular misalignment, parallel offset, soft foot, foundation settlement, thermal growth"},
        {"code": "FM-GASKET-LEAK", "description": "Flange gasket leak — visible leak or emission detection", "severity": "medium", "frequency": 8, "mtbf_hours": 17520, "equipment_types": ["Shell & Tube Heat Exchanger", "Plate Heat Exchanger", "Pressure Vessel"], "root_causes": "Bolt relaxation, thermal cycling, incorrect gasket type, improper bolt torquing sequence"},
        {"code": "FM-COMPRESSOR-VALVE", "description": "Compressor valve failure — increased temperature, reduced capacity", "severity": "high", "frequency": 6, "mtbf_hours": 8760, "equipment_types": ["Reciprocating Compressor"], "root_causes": "Valve plate fatigue, spring failure, liquid carryover, high delta-P across valve, contaminated gas"},
        {"code": "FM-BELT-WEAR", "description": "V-belt/coupling wear — noise, slippage, power transmission loss", "severity": "low", "frequency": 10, "mtbf_hours": 4380, "equipment_types": ["Air Cooled Heat Exchanger", "Cooling Tower"], "root_causes": "Normal wear, misalignment of sheaves, incorrect belt tension, environmental degradation"},
        {"code": "FM-INSTRUMT-DRIFT", "description": "Instrument calibration drift — inaccurate readings, false alarms", "severity": "medium", "frequency": 15, "mtbf_hours": 4380, "equipment_types": ["Globe Control Valve"], "root_causes": "Sensor aging, process buildup on sensor, EMI, temperature effects, transmitter electronics failure"},
        {"code": "FM-COATING-FAIL", "description": "Internal coating/lining failure — exposure of base metal, accelerated corrosion", "severity": "medium", "frequency": 3, "mtbf_hours": 35040, "equipment_types": ["Atmospheric Storage Tank", "Agitated Vessel"], "root_causes": "Chemical attack, abrasion, holiday in original coating, improper surface preparation, exceeded temperature rating"},
        {"code": "FM-SAFETY-VALVE-LEAK", "description": "Safety valve seat leak — audible leak, pressure drop", "severity": "high", "frequency": 4, "mtbf_hours": 17520, "equipment_types": ["Spring Loaded Safety Valve"], "root_causes": "Seat damage from popping, corrosion, process deposits on seating surface, vibration-induced chatter"},
        {"code": "FM-MOTOR-INSUL", "description": "Motor winding insulation degradation — low megger readings", "severity": "critical", "frequency": 2, "mtbf_hours": 43800, "equipment_types": ["Squirrel Cage Induction Motor", "Synchronous Motor"], "root_causes": "Thermal aging, moisture ingress, voltage spikes, partial discharge, contamination"},
        {"code": "FM-FOUNDATION-CRACK", "description": "Equipment foundation cracking/settlement — increased vibration baseline", "severity": "medium", "frequency": 2, "mtbf_hours": 87600, "equipment_types": ["Centrifugal Pump", "Reciprocating Compressor"], "root_causes": "Soil settlement, dynamic loading fatigue, chemical attack on concrete, inadequate design for dynamic loads"},
        {"code": "FM-COOLING-TOWER-FILL", "description": "Cooling tower fill degradation — reduced cooling efficiency, increased approach", "severity": "medium", "frequency": 2, "mtbf_hours": 43800, "equipment_types": ["Cooling Tower"], "root_causes": "Scaling, biological fouling, UV degradation of PVC fill, mechanical damage from maintenance"},
        {"code": "FM-BOILER-TUBE-FAIL", "description": "Boiler tube failure — water/steam leak, forced outage", "severity": "critical", "frequency": 1, "mtbf_hours": 43800, "equipment_types": ["Water Tube Boiler"], "root_causes": "Overheating (departure from nucleate boiling), hydrogen damage, caustic gouging, oxygen pitting, fatigue cracking"},
        {"code": "FM-DG-START-FAIL", "description": "Diesel generator fail to start — no start on demand", "severity": "critical", "frequency": 3, "mtbf_hours": 8760, "equipment_types": ["Diesel Generator"], "root_causes": "Battery failure, fuel system air lock, starter motor failure, control circuit fault, low coolant"},
        {"code": "FM-TRANSFORMER-OIL", "description": "Transformer oil degradation — high DGA values, reduced BDV", "severity": "high", "frequency": 2, "mtbf_hours": 43800, "equipment_types": ["Oil Filled Transformer"], "root_causes": "Thermal aging, moisture ingress, partial discharge, winding hot spots, cellulose decomposition"},
        {"code": "FM-UPS-BATTERY", "description": "UPS battery degradation — reduced backup time, cell failure", "severity": "high", "frequency": 4, "mtbf_hours": 17520, "equipment_types": ["Online UPS"], "root_causes": "Calendar aging, thermal runaway, sulfation, electrolyte dry-out, cell imbalance"},
        {"code": "FM-RO-MEMBRANE", "description": "RO membrane fouling/degradation — increased rejection rate drop, high TDS in permeate", "severity": "medium", "frequency": 4, "mtbf_hours": 8760, "equipment_types": ["Reverse Osmosis System"], "root_causes": "Scaling (silica, CaCO3), biofouling, membrane oxidation by chlorine, colloidal fouling"},
        {"code": "FM-PACKING-LEAK", "description": "Valve packing leak — visible leak at valve stem", "severity": "low", "frequency": 20, "mtbf_hours": 4380, "equipment_types": ["Globe Control Valve", "Ball Valve (Automated)"], "root_causes": "Packing wear, stem scoring, thermal cycling, incorrect packing type, over/under tightening"},
        {"code": "FM-COUPLING-FAIL", "description": "Coupling failure — sudden vibration increase, noise, loss of drive", "severity": "high", "frequency": 3, "mtbf_hours": 26280, "equipment_types": ["Centrifugal Pump", "Reciprocating Compressor"], "root_causes": "Fatigue, misalignment, overloading, elastomer degradation, incorrect coupling selection"},
        {"code": "FM-LUBE-OIL-DEG", "description": "Lubrication oil degradation — high TAN, low viscosity, water contamination", "severity": "medium", "frequency": 6, "mtbf_hours": 4380, "equipment_types": ["Reciprocating Compressor", "Diesel Generator"], "root_causes": "Thermal breakdown, oxidation, water ingress, particle contamination, extended oil change interval"},
        {"code": "FM-FLAME-FAILURE", "description": "Burner flame failure — boiler trip on flame failure", "severity": "critical", "frequency": 3, "mtbf_hours": 8760, "equipment_types": ["Water Tube Boiler", "Thermic Fluid Heater"], "root_causes": "Flame scanner fouling, fuel quality change, air/fuel ratio upset, igniter failure, scanner misalignment"},
        {"code": "FM-LEVEL-TRANSM", "description": "Level transmitter failure — false high/low level alarms", "severity": "medium", "frequency": 5, "mtbf_hours": 8760, "equipment_types": ["Atmospheric Storage Tank", "Pressure Vessel"], "root_causes": "Impulse line blockage, diaphragm failure, electronics failure, process buildup, calibration drift"},
        {"code": "FM-CORROSION-EXT", "description": "External corrosion under insulation (CUI) — wall loss under insulation", "severity": "high", "frequency": 3, "mtbf_hours": 26280, "equipment_types": ["Shell & Tube Heat Exchanger", "Pressure Vessel", "Tray Column"], "root_causes": "Moisture ingress through damaged insulation, operating temperature 60-175°C (CUI susceptible range), chloride in insulation material, damaged vapor barrier"},
    ]


# ============================================================================
# 5. PROCEDURES (40 items)
# ============================================================================

def generate_procedures():
    """Generate 40 realistic procedures and SOPs."""
    return [
        {"procedure_id": "SOP-PUMP-START-001", "title": "Centrifugal Pump Startup Procedure", "type": "SOP", "revision": "Rev 4", "status": "approved", "effective_date": "2024-01-15", "next_review": "2026-01-15"},
        {"procedure_id": "SOP-PUMP-STOP-001", "title": "Centrifugal Pump Normal Shutdown Procedure", "type": "SOP", "revision": "Rev 4", "status": "approved", "effective_date": "2024-01-15", "next_review": "2026-01-15"},
        {"procedure_id": "SOP-PUMP-EMSTOP-001", "title": "Centrifugal Pump Emergency Shutdown Procedure", "type": "Emergency", "revision": "Rev 3", "status": "approved", "effective_date": "2024-06-01", "next_review": "2025-06-01"},
        {"procedure_id": "SOP-HX-CLEAN-001", "title": "Shell & Tube Heat Exchanger Cleaning (CIP) Procedure", "type": "SOP", "revision": "Rev 3", "status": "approved", "effective_date": "2024-03-10", "next_review": "2026-03-10"},
        {"procedure_id": "SOP-HX-CLEAN-002", "title": "Plate Heat Exchanger Disassembly & Cleaning Procedure", "type": "SOP", "revision": "Rev 2", "status": "approved", "effective_date": "2024-03-10", "next_review": "2026-03-10"},
        {"procedure_id": "SOP-VESSEL-ENTRY-001", "title": "Confined Space Entry Procedure", "type": "Safety", "revision": "Rev 5", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
        {"procedure_id": "SOP-HOT-WORK-001", "title": "Hot Work Permit & Procedure", "type": "Safety", "revision": "Rev 6", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
        {"procedure_id": "SOP-LOTO-001", "title": "Lockout/Tagout (LOTO) Procedure", "type": "Safety", "revision": "Rev 4", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
        {"procedure_id": "SOP-ERP-001", "title": "Emergency Response Plan - Fire", "type": "Emergency", "revision": "Rev 7", "status": "approved", "effective_date": "2024-06-01", "next_review": "2025-06-01"},
        {"procedure_id": "SOP-ERP-002", "title": "Emergency Response Plan - Chemical Spill", "type": "Emergency", "revision": "Rev 5", "status": "approved", "effective_date": "2024-06-01", "next_review": "2025-06-01"},
        {"procedure_id": "SOP-ERP-003", "title": "Emergency Response Plan - Gas Leak / Toxic Release", "type": "Emergency", "revision": "Rev 4", "status": "approved", "effective_date": "2024-06-01", "next_review": "2025-06-01"},
        {"procedure_id": "SOP-VALVE-MAINT-001", "title": "Control Valve Maintenance & Calibration Procedure", "type": "SOP", "revision": "Rev 3", "status": "approved", "effective_date": "2024-02-15", "next_review": "2026-02-15"},
        {"procedure_id": "SOP-PSV-TEST-001", "title": "Safety Valve Testing & Reseat Procedure", "type": "SOP", "revision": "Rev 4", "status": "approved", "effective_date": "2024-03-01", "next_review": "2025-03-01"},
        {"procedure_id": "SOP-COMP-START-001", "title": "Reciprocating Compressor Startup Procedure", "type": "SOP", "revision": "Rev 3", "status": "approved", "effective_date": "2024-01-20", "next_review": "2026-01-20"},
        {"procedure_id": "SOP-BOILER-START-001", "title": "Steam Boiler Cold Start Procedure", "type": "SOP", "revision": "Rev 5", "status": "approved", "effective_date": "2024-05-01", "next_review": "2025-05-01"},
        {"procedure_id": "SOP-BOILER-STOP-001", "title": "Steam Boiler Normal Shutdown Procedure", "type": "SOP", "revision": "Rev 4", "status": "approved", "effective_date": "2024-05-01", "next_review": "2025-05-01"},
        {"procedure_id": "PM-PUMP-QTRLY-001", "title": "Quarterly Preventive Maintenance — Centrifugal Pumps", "type": "PM", "revision": "Rev 4", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-PUMP-ANNUAL-001", "title": "Annual Overhaul Procedure — Centrifugal Pumps", "type": "PM", "revision": "Rev 3", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-MOTOR-ANNUAL-001", "title": "Annual Motor Inspection & Insulation Testing Procedure", "type": "PM", "revision": "Rev 3", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-MOTOR-QTRLY-001", "title": "Quarterly Motor Greasing & Vibration Check", "type": "PM", "revision": "Rev 3", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-COMP-6MONTH-001", "title": "Six-Monthly Compressor Valve Inspection", "type": "PM", "revision": "Rev 2", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-HX-ANNUAL-001", "title": "Annual Heat Exchanger Inspection Procedure", "type": "PM", "revision": "Rev 2", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-VALVE-ANNUAL-001", "title": "Annual Control Valve Overhaul & Calibration", "type": "PM", "revision": "Rev 2", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-DG-MONTHLY-001", "title": "Monthly Diesel Generator Testing & Inspection", "type": "PM", "revision": "Rev 3", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-BOILER-ANNUAL-001", "title": "Annual Boiler IBR Inspection Preparation Procedure", "type": "PM", "revision": "Rev 3", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-CT-ANNUAL-001", "title": "Annual Cooling Tower Inspection & Fill Cleaning", "type": "PM", "revision": "Rev 2", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-TRANSFORMER-ANNUAL-001", "title": "Annual Transformer Oil Testing & Inspection", "type": "PM", "revision": "Rev 2", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "PM-UPS-QTRLY-001", "title": "Quarterly UPS Battery Testing & Inspection", "type": "PM", "revision": "Rev 2", "status": "approved", "effective_date": "2024-01-01", "next_review": "2025-12-31"},
        {"procedure_id": "SOP-CHEM-HANDLE-001", "title": "Hazardous Chemical Handling & Storage Procedure", "type": "Safety", "revision": "Rev 4", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
        {"procedure_id": "SOP-HEIGHT-WORK-001", "title": "Working at Height Procedure", "type": "Safety", "revision": "Rev 3", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
        {"procedure_id": "SOP-EXCAVATION-001", "title": "Excavation & Trenching Procedure", "type": "Safety", "revision": "Rev 2", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
        {"procedure_id": "SOP-RADIOGRAPHY-001", "title": "Radiographic Testing (RT) Safety Procedure", "type": "Safety", "revision": "Rev 3", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
        {"procedure_id": "SOP-SCAFFOLDING-001", "title": "Scaffolding Erection & Inspection Procedure", "type": "Safety", "revision": "Rev 3", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
        {"procedure_id": "SOP-BLINDING-001", "title": "Line/Equipment Blinding Procedure (Spade/Spectacle Blind)", "type": "Safety", "revision": "Rev 3", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
        {"procedure_id": "SOP-MOC-001", "title": "Management of Change (MOC) Procedure", "type": "Management", "revision": "Rev 4", "status": "approved", "effective_date": "2024-03-01", "next_review": "2025-03-01"},
        {"procedure_id": "SOP-INCIDENT-001", "title": "Incident Investigation & Reporting Procedure", "type": "Management", "revision": "Rev 5", "status": "approved", "effective_date": "2024-06-01", "next_review": "2025-06-01"},
        {"procedure_id": "SOP-PTW-001", "title": "Permit to Work (PTW) System — General", "type": "Safety", "revision": "Rev 6", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
        {"procedure_id": "SOP-HYDRO-TEST-001", "title": "Hydrostatic Testing Procedure for Piping & Vessels", "type": "SOP", "revision": "Rev 3", "status": "approved", "effective_date": "2024-02-01", "next_review": "2026-02-01"},
        {"procedure_id": "SOP-ALIGNMENT-001", "title": "Pump-Motor Shaft Alignment Procedure (Laser)", "type": "SOP", "revision": "Rev 2", "status": "approved", "effective_date": "2024-01-15", "next_review": "2026-01-15"},
        {"procedure_id": "SOP-CRANE-OPS-001", "title": "Crane Operation & Lifting Plan Procedure", "type": "Safety", "revision": "Rev 4", "status": "approved", "effective_date": "2024-04-01", "next_review": "2025-04-01"},
    ]


# ============================================================================
# 6. PROCESS PARAMETERS (30 items)
# ============================================================================

def generate_process_parameters():
    """Generate 30 process parameters with real ranges."""
    return [
        {"name": "TI-201", "description": "Reactor Inlet Temperature", "unit": "°C", "normal_min": 180, "normal_max": 220, "alarm_low": 170, "alarm_high": 230, "trip_high": 250, "equipment_tag": "V-201"},
        {"name": "TI-202", "description": "Reactor Outlet Temperature", "unit": "°C", "normal_min": 250, "normal_max": 280, "alarm_low": 240, "alarm_high": 290, "trip_high": 300, "equipment_tag": "V-201"},
        {"name": "PI-201", "description": "Reactor Operating Pressure", "unit": "bar", "normal_min": 30, "normal_max": 40, "alarm_low": 25, "alarm_high": 42, "trip_high": 45, "equipment_tag": "V-201"},
        {"name": "LI-201", "description": "Reactor Level", "unit": "%", "normal_min": 40, "normal_max": 70, "alarm_low": 30, "alarm_high": 80, "trip_low": 20, "trip_high": 90, "equipment_tag": "V-201"},
        {"name": "FI-201", "description": "Reactor Feed Flow", "unit": "m³/hr", "normal_min": 8, "normal_max": 12, "alarm_low": 6, "alarm_high": 14, "equipment_tag": "P-202"},
        {"name": "PI-101A", "description": "Feed Water Pump A Discharge Pressure", "unit": "bar", "normal_min": 10, "normal_max": 14, "alarm_low": 8, "alarm_high": 16, "equipment_tag": "P-101A"},
        {"name": "FI-101", "description": "Feed Water Flow", "unit": "m³/hr", "normal_min": 20, "normal_max": 30, "alarm_low": 15, "alarm_high": 35, "equipment_tag": "P-101A"},
        {"name": "TI-101", "description": "Feed Water Temperature", "unit": "°C", "normal_min": 25, "normal_max": 45, "alarm_high": 55, "equipment_tag": "V-101"},
        {"name": "VI-101A", "description": "Feed Water Pump A Vibration (Overall)", "unit": "mm/s RMS", "normal_min": 0, "normal_max": 4.5, "alarm_high": 7.1, "trip_high": 11.2, "equipment_tag": "P-101A"},
        {"name": "VI-201A", "description": "CW Pump A Vibration (Overall)", "unit": "mm/s RMS", "normal_min": 0, "normal_max": 4.5, "alarm_high": 7.1, "trip_high": 11.2, "equipment_tag": "P-201A"},
        {"name": "TI-M101A-DE", "description": "Motor P-101A DE Bearing Temperature", "unit": "°C", "normal_min": 30, "normal_max": 75, "alarm_high": 85, "trip_high": 95, "equipment_tag": "M-101A"},
        {"name": "TI-M101A-NDE", "description": "Motor P-101A NDE Bearing Temperature", "unit": "°C", "normal_min": 30, "normal_max": 70, "alarm_high": 80, "trip_high": 90, "equipment_tag": "M-101A"},
        {"name": "TI-M101A-WIND", "description": "Motor P-101A Winding Temperature", "unit": "°C", "normal_min": 30, "normal_max": 110, "alarm_high": 130, "trip_high": 150, "equipment_tag": "M-101A"},
        {"name": "AI-M101A", "description": "Motor P-101A Current", "unit": "A", "normal_min": 60, "normal_max": 85, "alarm_high": 95, "trip_high": 105, "equipment_tag": "M-101A"},
        {"name": "TI-HX201-SHELL-IN", "description": "HX-201 Shell Inlet Temperature", "unit": "°C", "normal_min": 60, "normal_max": 90, "alarm_high": 100, "equipment_tag": "HX-201"},
        {"name": "TI-HX201-TUBE-OUT", "description": "HX-201 Tube Outlet Temperature", "unit": "°C", "normal_min": 40, "normal_max": 65, "alarm_high": 75, "equipment_tag": "HX-201"},
        {"name": "DPI-HX201", "description": "HX-201 Shell Side Differential Pressure", "unit": "bar", "normal_min": 0.2, "normal_max": 0.8, "alarm_high": 1.5, "equipment_tag": "HX-201"},
        {"name": "PI-C201-DISCH", "description": "Process Gas Compressor 1st Stage Discharge Pressure", "unit": "bar", "normal_min": 28, "normal_max": 35, "alarm_high": 37, "trip_high": 38, "equipment_tag": "C-201"},
        {"name": "TI-C201-DISCH", "description": "Process Gas Compressor 1st Stage Discharge Temperature", "unit": "°C", "normal_min": 100, "normal_max": 140, "alarm_high": 155, "trip_high": 165, "equipment_tag": "C-201"},
        {"name": "VI-C201-DE", "description": "Compressor C-201 DE Bearing Vibration", "unit": "mm/s RMS", "normal_min": 0, "normal_max": 6.3, "alarm_high": 10, "trip_high": 16, "equipment_tag": "C-201"},
        {"name": "PI-B101-DRUM", "description": "Boiler B-101 Steam Drum Pressure", "unit": "kg/cm²", "normal_min": 15, "normal_max": 19, "alarm_high": 20, "trip_high": 21, "equipment_tag": "B-101"},
        {"name": "LI-B101-DRUM", "description": "Boiler B-101 Steam Drum Level", "unit": "mm", "normal_min": -25, "normal_max": 25, "alarm_low": -50, "alarm_high": 50, "trip_low": -75, "trip_high": 75, "equipment_tag": "B-101"},
        {"name": "TI-B101-FLUE", "description": "Boiler B-101 Flue Gas Temperature (Stack)", "unit": "°C", "normal_min": 140, "normal_max": 200, "alarm_high": 250, "equipment_tag": "B-101"},
        {"name": "TI-CT101-CW-IN", "description": "Cooling Tower Inlet (Hot Water) Temperature", "unit": "°C", "normal_min": 35, "normal_max": 42, "alarm_high": 48, "equipment_tag": "CT-101"},
        {"name": "TI-CT101-CW-OUT", "description": "Cooling Tower Outlet (Cold Water) Temperature", "unit": "°C", "normal_min": 28, "normal_max": 33, "alarm_high": 36, "equipment_tag": "CT-101"},
        {"name": "LI-V301", "description": "Product Tank T-301 Level", "unit": "%", "normal_min": 10, "normal_max": 85, "alarm_low": 5, "alarm_high": 90, "trip_high": 95, "equipment_tag": "V-301"},
        {"name": "TI-T201-TOP", "description": "Distillation Column Top Temperature", "unit": "°C", "normal_min": 70, "normal_max": 95, "alarm_low": 60, "alarm_high": 105, "equipment_tag": "T-201"},
        {"name": "TI-T201-BTM", "description": "Distillation Column Bottom Temperature", "unit": "°C", "normal_min": 150, "normal_max": 180, "alarm_low": 140, "alarm_high": 190, "equipment_tag": "T-201"},
        {"name": "PI-T201-TOP", "description": "Distillation Column Top Pressure", "unit": "bar", "normal_min": 1.5, "normal_max": 3.0, "alarm_low": 1.0, "alarm_high": 3.5, "trip_high": 5.0, "equipment_tag": "T-201"},
        {"name": "AI-WTP-PERM-TDS", "description": "RO Permeate TDS", "unit": "ppm", "normal_min": 0, "normal_max": 50, "alarm_high": 100, "equipment_tag": "WTP-101"},
    ]


# ============================================================================
# 7. MAINTENANCE RECORDS (500+ work orders)
# ============================================================================

def generate_maintenance_records(equipment, personnel, failure_modes, procedures):
    """Generate 500+ realistic work orders spanning 3 years."""
    eq_tags = [e["tag"] for e in equipment]
    eq_by_tag = {e["tag"]: e for e in equipment}
    maint_personnel = [p for p in personnel if p["department"] in ("Maintenance", "Electrical", "Instrumentation", "Utility", "QC")]
    ops_personnel = [p for p in personnel if p["department"] == "Operations"]

    # WO description templates per equipment type
    wo_templates = {
        "Centrifugal Pump": [
            ("PM", "Quarterly PM: Vibration check (overall {vib} mm/s), bearing temperature check (DE: {temp}°C), alignment verification, coupling inspection, seal face inspection. All readings within acceptable limits."),
            ("PM", "Annual overhaul: Impeller, wear rings, mechanical seal (John Crane Type 5610), and bearings (SKF {bearing}) replaced. Alignment set to 0.05mm/0.03mm. Performance test: head {head}m, flow {flow}m³/hr."),
            ("CM", "Corrective: Mechanical seal replaced due to excessive leakage (~{leak_rate} drops/min). Root cause: dry running during suction strainer cleaning. New seal installed (John Crane 5610). No shaft damage."),
            ("CM", "Corrective: DE bearing replaced (SKF {bearing}). High vibration detected during routine round ({vib} mm/s overall, alarm at 7.1). Bearing showed inner race spalling. Vibration after replacement: {vib_after} mm/s."),
            ("EM", "Emergency: Pump tripped on high vibration ({vib} mm/s). Coupling guard removed — found coupling spider completely disintegrated. Coupling replaced (Rexnord Omega E40). Alignment checked and adjusted. Pump restarted after {hours}hrs."),
            ("PdM", "Predictive: Oil analysis showed high Fe content ({fe} ppm vs normal <50 ppm). Bearing inspection revealed early stage pitting on outer race. Bearing preemptively replaced (SKF {bearing}). Oil flushed and replaced."),
        ],
        "Multistage Centrifugal Pump": [
            ("PM", "Quarterly PM: Vibration measurement on all bearing positions. DE axial: {vib} mm/s, NDE radial: {vib2} mm/s. Coupling guard inspection, oil level check, seal leakage check — all satisfactory."),
            ("CM", "Corrective: Stage ring wear — pump head dropped from {head}m to {head2}m. Pump opened, wear rings replaced. Performance test satisfactory after reassembly."),
        ],
        "Shell & Tube Heat Exchanger": [
            ("PM", "Annual CIP cleaning: Shell side circulated with 5% HCl solution for 4 hours at 60°C, followed by neutralization and passivation. Fouling factor improved from {ff_before} to {ff_after} m².K/kW."),
            ("CM", "Corrective: {n_tubes} tubes plugged after eddy current inspection revealed wall loss >40%. IRIS inspection on remaining tubes — {n_remaining} tubes show 20-30% wall loss (next inspection in 2 years). Tube bundle remaining life estimated at {life} years."),
            ("PM", "Annual inspection: Bundle pulled for visual inspection. Light scaling on OD observed. Gaskets replaced (Klingersil C-4430). Shell flange faces inspected — no damage. Bolts re-torqued to {torque} Nm using cross-pattern."),
        ],
        "Reciprocating Compressor": [
            ("PM", "Six-monthly valve inspection: 1st stage suction and discharge valves removed and inspected. Suction valve plate showing wear ({wear}mm remaining vs 3mm new). Replaced both suction valve plates and springs. Discharge valves satisfactory."),
            ("CM", "Corrective: 2nd stage discharge temperature high ({temp}°C vs alarm at 155°C). Found stuck discharge valve (plate fragment lodged). Valve replaced. Intercooler checked — satisfactory."),
            ("PM", "Annual overhaul: Piston rings, rider rings, and packing rings replaced on both stages. Cylinder bore measured — within tolerance ({bore}mm vs nominal {bore_nom}mm). Crosshead pin and bearing clearance checked — satisfactory."),
        ],
        "Globe Control Valve": [
            ("PM", "Annual overhaul: Valve removed from line. Trim (plug, seat ring, cage) inspected — moderate erosion on seat ring. Seat lapped. Packing replaced (PTFE/graphite). Actuator diaphragm inspected — no cracks. Positioner calibrated: 4-20mA input, 3-15 psi output, linearity < 0.5%."),
            ("CM", "Corrective: Valve sticking at {pos}% open. Field investigation found corroded stem. Stem cleaned and polished, packing replaced, actuator bench set adjusted. Stroke time improved from {time_before}s to {time_after}s."),
        ],
        "Spring Loaded Safety Valve": [
            ("PM", "Annual pop test: Valve removed and bench tested. Set pressure: {set_p} bar (nameplate: {np_p} bar). Reseat pressure: {reseat_p} bar. Valve reseated — set pressure adjusted to {np_p} bar ±{tol}%. New gaskets installed. Tag sealed."),
        ],
        "Water Tube Boiler": [
            ("PM", "Annual IBR inspection preparation: Boiler cooled down, waterside opened for inspection. Tube thickness measurements taken at 24 CMLs — minimum remaining: {min_thick}mm (original: {orig}mm). Corrosion rate: {cr} mm/yr. Next inspection due: {next_insp}."),
            ("CM", "Corrective: Boiler tripped on low drum level. Investigation found BFW pump tripped on overload. BFW pump motor checked — found single phasing due to loose terminal. Terminal re-crimped, motor megger: {megger} MΩ. Boiler restarted after {hours} hours."),
        ],
        "Squirrel Cage Induction Motor": [
            ("PM", "Annual insulation test: Megger at 500V DC — Phase R: {megR} MΩ, Phase Y: {megY} MΩ, Phase B: {megB} MΩ. PI (Polarization Index): {pi}. All within acceptable limits (>100 MΩ corrected to 40°C, PI > 2.0)."),
            ("PM", "Quarterly greasing: DE bearing — {grease_de}g of {grease_type}. NDE bearing — {grease_nde}g. Vibration before/after: DE {vib_before}/{vib_after} mm/s, NDE {vib_before2}/{vib_after2} mm/s. No abnormal noise."),
        ],
        "Rotary Screw Compressor": [
            ("PM", "8000-hour service: Air/oil filter replaced, oil separator element replaced, minimum pressure valve checked. Oil (Atlas Copco Roto-Inject) replaced — 28 liters. Air end inlet valve inspected. Running hours: {hours}."),
            ("CM", "Corrective: High discharge air temperature ({temp}°C vs alarm at 110°C). Found blocked oil cooler (external dust buildup). Cooler cleaned with compressed air. Temperature normalized to {temp_after}°C."),
        ],
        "Diesel Generator": [
            ("PM", "Monthly test run: DG started on auto — start time {start_time}s (spec <10s). Loaded to {load}% for 30 minutes. Parameters normal: voltage {voltage}V, frequency {freq}Hz, oil pressure {oil_p} bar, coolant temp {coolant}°C. Fuel level: {fuel}%."),
        ],
    }

    records = []
    wo_counter = 1

    # Generate 3 years of work orders: 2023-01 to 2025-12
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)

    for eq in equipment:
        eq_type = eq["type"]
        templates = wo_templates.get(eq_type, None)
        if not templates:
            continue

        # Generate 3-15 WOs per equipment depending on type
        num_wos = random.randint(3, min(15, len(templates) * 5))

        for _ in range(num_wos):
            wo_type, template = random.choice(templates)
            wo_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

            # Fill in template placeholders with realistic values
            desc = template.format(
                vib=round(random.uniform(1.5, 12.0), 1),
                vib2=round(random.uniform(1.0, 5.0), 1),
                vib_after=round(random.uniform(1.0, 3.5), 1),
                vib_before=round(random.uniform(2.0, 6.0), 1),
                vib_before2=round(random.uniform(1.5, 5.0), 1),
                vib_after2=round(random.uniform(1.0, 3.0), 1),
                temp=random.randint(60, 170),
                temp_after=random.randint(60, 85),
                head=random.randint(80, 150),
                head2=random.randint(50, 70),
                flow=random.randint(15, 50),
                bearing=random.choice(["6316", "6318", "6314", "6320", "7314", "NU316"]),
                leak_rate=random.randint(5, 60),
                hours=round(random.uniform(2, 24), 1),
                fe=random.randint(60, 200),
                ff_before=round(random.uniform(0.0003, 0.0008), 4),
                ff_after=round(random.uniform(0.0001, 0.0002), 4),
                n_tubes=random.randint(1, 6),
                n_remaining=random.randint(5, 20),
                life=random.randint(3, 8),
                torque=random.randint(120, 350),
                wear=round(random.uniform(1.5, 2.5), 1),
                bore=round(random.uniform(200.0, 200.3), 1),
                bore_nom=200.0,
                pos=random.randint(30, 70),
                time_before=round(random.uniform(8, 25), 1),
                time_after=round(random.uniform(3, 6), 1),
                set_p=round(random.uniform(17, 50), 1),
                np_p=round(random.uniform(18, 50), 1),
                reseat_p=round(random.uniform(15, 45), 1),
                tol=3,
                min_thick=round(random.uniform(4.0, 8.0), 1),
                orig=round(random.uniform(8.0, 12.0), 1),
                cr=round(random.uniform(0.05, 0.30), 2),
                next_insp="2026",
                megger=random.randint(200, 2000),
                megR=random.randint(200, 5000),
                megY=random.randint(200, 5000),
                megB=random.randint(200, 5000),
                pi=round(random.uniform(2.0, 6.0), 1),
                grease_de=random.randint(15, 40),
                grease_nde=random.randint(10, 30),
                grease_type=random.choice(["SKF LGMT 2", "Shell Gadus S2 V220", "Mobil Polyrex EM"]),
                start_time=round(random.uniform(4, 9), 1),
                load=random.randint(50, 100),
                voltage=random.randint(395, 420),
                freq=round(random.uniform(49.5, 50.5), 1),
                oil_p=round(random.uniform(3.5, 5.0), 1),
                coolant=random.randint(75, 90),
                fuel=random.randint(60, 95),
            )

            # Assign personnel
            assigned = random.sample(maint_personnel, min(random.randint(1, 3), len(maint_personnel)))
            duration_hours = round(random.uniform(1, 72), 1) if wo_type != "EM" else round(random.uniform(2, 48), 1)

            # Estimate cost
            if wo_type == "PM":
                cost = round(random.uniform(5000, 50000), 0)
            elif wo_type == "CM":
                cost = round(random.uniform(10000, 200000), 0)
            elif wo_type == "EM":
                cost = round(random.uniform(50000, 500000), 0)
            else:
                cost = round(random.uniform(5000, 30000), 0)

            records.append({
                "work_order_id": f"WO-{wo_date.year}-{wo_counter:04d}",
                "type": wo_type,
                "date": wo_date.strftime("%Y-%m-%d"),
                "status": "completed",
                "equipment_tag": eq["tag"],
                "description": desc,
                "duration_hours": duration_hours,
                "estimated_cost_inr": cost,
                "personnel": [p["employee_id"] for p in assigned],
            })
            wo_counter += 1

    # Sort by date
    records.sort(key=lambda x: x["date"])
    return records


# ============================================================================
# 8. INSPECTION FINDINGS (200+)
# ============================================================================

def generate_inspection_findings(equipment, personnel):
    """Generate 200+ inspection findings."""
    inspectors = [p for p in personnel if p["department"] in ("QC", "HSE")]
    inspectable = [e for e in equipment if e["type"] in (
        "Atmospheric Storage Tank", "Pressure Reactor", "Pressure Vessel",
        "Shell & Tube Heat Exchanger", "Floating Roof Storage Tank",
        "Spring Loaded Safety Valve", "Water Tube Boiler", "Tray Column",
        "Packed Column", "Cryogenic Storage Vessel", "Oil Filled Transformer",
    )]

    finding_templates = [
        {"severity": "critical", "desc": "Wall thickness below retirement thickness at CML-{cml}. Measured: {thick}mm, Min required: {min_thick}mm. Immediate repair/replacement required.", "method": "UT Thickness"},
        {"severity": "major", "desc": "Pitting corrosion found on {surface}. Max pit depth: {pit}mm. Remaining wall: {remain}mm. Fitness-for-service assessment per API 579 required.", "method": "UT Thickness + Visual"},
        {"severity": "minor", "desc": "Surface corrosion on {surface}. No measurable wall loss. Coating touch-up required during next available opportunity.", "method": "Visual Inspection"},
        {"severity": "observation", "desc": "Insulation jacketing damaged at {location}. Potential moisture ingress — recommend repair to prevent CUI.", "method": "External Visual"},
        {"severity": "minor", "desc": "Flange bolt corrosion observed on {location}. Bolts functional but recommend replacement during next turnaround.", "method": "Visual Inspection"},
        {"severity": "major", "desc": "Crack indication found at {location} by {method}. Length: {length}mm. Recommend grinding out and re-welding per approved WPS.", "method": "MT/PT"},
        {"severity": "critical", "desc": "Safety valve failed to pop at set pressure during bench test. Actual pop: {actual_p} bar vs set: {set_p} bar (+{dev}% deviation, limit ±3%). Valve requires overhaul and recalibration.", "method": "Bench Test"},
        {"severity": "minor", "desc": "Foundation grout cracking observed at {location}. No displacement detected. Monitor during next vibration survey.", "method": "Visual Inspection"},
        {"severity": "major", "desc": "Corrosion under insulation (CUI) detected at {location}. Wall loss: {loss}mm from original {orig}mm. Insulation removed, area sandblasted, UT grid mapped.", "method": "UT + CUI Inspection"},
        {"severity": "observation", "desc": "Earth pit resistance measured at {resistance} ohms (specification: <1 ohm for lightning protection, <5 ohms for equipment earthing). Within limits.", "method": "Earth Pit Testing"},
    ]

    findings = []
    finding_counter = 1
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)

    for eq in inspectable:
        num_findings = random.randint(3, 12)
        for _ in range(num_findings):
            template = random.choice(finding_templates)
            insp_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            inspector = random.choice(inspectors)

            desc = template["desc"].format(
                cml=random.randint(1, 30),
                thick=round(random.uniform(2.0, 6.0), 1),
                min_thick=round(random.uniform(3.0, 5.0), 1),
                pit=round(random.uniform(0.5, 3.0), 1),
                remain=round(random.uniform(3.0, 8.0), 1),
                surface=random.choice(["shell internal surface", "tube sheet face", "nozzle weld", "bottom plate", "knuckle region"]),
                location=random.choice(["12 o'clock position at nozzle N1", "bottom head-to-shell weld", "inlet nozzle flange", "support saddle area", "manhole flange region"]),
                method=random.choice(["Magnetic Particle Testing (MT)", "Dye Penetrant Testing (PT)"]),
                length=random.randint(5, 50),
                actual_p=round(random.uniform(18, 52), 1),
                set_p=round(random.uniform(18, 50), 1),
                dev=round(random.uniform(3.5, 15), 1),
                loss=round(random.uniform(1.0, 4.0), 1),
                orig=round(random.uniform(8.0, 14.0), 1),
                resistance=round(random.uniform(0.3, 4.5), 1),
            )

            findings.append({
                "finding_id": f"IF-{insp_date.year}-{finding_counter:04d}",
                "equipment_tag": eq["tag"],
                "date": insp_date.strftime("%Y-%m-%d"),
                "severity": template["severity"],
                "description": desc,
                "inspection_method": template["method"],
                "inspector_id": inspector["employee_id"],
                "status": random.choice(["open", "closed", "in_progress"]) if template["severity"] in ("critical", "major") else "closed",
                "corrective_action": "Refer to linked work order" if template["severity"] in ("critical", "major") else "Noted for next turnaround",
            })
            finding_counter += 1

    findings.sort(key=lambda x: x["date"])
    return findings


# ============================================================================
# 9. RELATIONSHIPS
# ============================================================================

def generate_relationships(equipment, regulations, failure_modes, procedures, maintenance_records, inspection_findings, process_parameters, personnel):
    """Generate all relationship data."""
    rels = {
        "equipment_failure_modes": [],
        "equipment_regulations": [],
        "equipment_procedures": [],
        "procedure_regulations": [],
        "failure_mode_procedures": [],
        "equipment_maintenance": [],
        "maintenance_personnel": [],
        "maintenance_failure_modes": [],
        "inspection_equipment": [],
        "inspection_personnel": [],
        "inspection_regulations": [],
        "equipment_process_params": [],
    }

    eq_by_tag = {e["tag"]: e for e in equipment}
    fm_by_code = {f["code"]: f for f in failure_modes}

    # Equipment -> Failure Modes (based on equipment type matching)
    for eq in equipment:
        for fm in failure_modes:
            if eq["type"] in fm.get("equipment_types", []):
                rels["equipment_failure_modes"].append((eq["tag"], fm["code"]))

    # Equipment -> Regulations (logical mapping)
    pressure_vessels = [e["tag"] for e in equipment if e["type"] in ("Pressure Vessel", "Pressure Reactor", "Cryogenic Storage Vessel")]
    storage_tanks = [e["tag"] for e in equipment if "Storage" in e["type"] or "Floating" in e["type"]]
    boilers = [e["tag"] for e in equipment if "Boiler" in e["type"]]
    electrical = [e["tag"] for e in equipment if e["type"] in ("Squirrel Cage Induction Motor", "Synchronous Motor", "Oil Filled Transformer", "HT Switchgear", "Online UPS")]
    all_tags = [e["tag"] for e in equipment]

    for tag in pressure_vessels:
        rels["equipment_regulations"].append((tag, "IS-2825"))
        rels["equipment_regulations"].append((tag, "API-510"))
    for tag in storage_tanks:
        rels["equipment_regulations"].append((tag, "API-653"))
        rels["equipment_regulations"].append((tag, "NFPA-30"))
        rels["equipment_regulations"].append((tag, "PESO-RULES"))
    for tag in boilers:
        rels["equipment_regulations"].append((tag, "IBR-1950"))
        rels["equipment_regulations"].append((tag, "FACTORY-ACT-1948"))
    for tag in electrical:
        rels["equipment_regulations"].append((tag, "OISD-STD-144"))
    # All equipment governed by general safety standards
    for tag in all_tags:
        rels["equipment_regulations"].append((tag, "OISD-STD-154"))

    # Equipment -> Procedures (based on type)
    pump_tags = [e["tag"] for e in equipment if "Pump" in e["type"]]
    hx_tags = [e["tag"] for e in equipment if "Heat Exchanger" in e["type"]]
    valve_tags = [e["tag"] for e in equipment if "Control Valve" in e["type"] or "Butterfly" in e["type"]]
    psv_tags = [e["tag"] for e in equipment if "Safety Valve" in e["type"]]
    motor_tags = [e["tag"] for e in equipment if "Motor" in e["type"]]
    comp_tags = [e["tag"] for e in equipment if "Compressor" in e["type"]]
    boiler_tags = [e["tag"] for e in equipment if "Boiler" in e["type"] or "Heater" in e["type"]]

    for tag in pump_tags:
        rels["equipment_procedures"].append((tag, "SOP-PUMP-START-001"))
        rels["equipment_procedures"].append((tag, "SOP-PUMP-STOP-001"))
        rels["equipment_procedures"].append((tag, "PM-PUMP-QTRLY-001"))
        rels["equipment_procedures"].append((tag, "SOP-LOTO-001"))
    for tag in hx_tags:
        rels["equipment_procedures"].append((tag, "SOP-HX-CLEAN-001"))
        rels["equipment_procedures"].append((tag, "PM-HX-ANNUAL-001"))
    for tag in valve_tags:
        rels["equipment_procedures"].append((tag, "SOP-VALVE-MAINT-001"))
        rels["equipment_procedures"].append((tag, "PM-VALVE-ANNUAL-001"))
    for tag in psv_tags:
        rels["equipment_procedures"].append((tag, "SOP-PSV-TEST-001"))
    for tag in motor_tags:
        rels["equipment_procedures"].append((tag, "PM-MOTOR-ANNUAL-001"))
        rels["equipment_procedures"].append((tag, "PM-MOTOR-QTRLY-001"))
        rels["equipment_procedures"].append((tag, "SOP-LOTO-001"))
    for tag in comp_tags:
        rels["equipment_procedures"].append((tag, "SOP-COMP-START-001"))
        rels["equipment_procedures"].append((tag, "PM-COMP-6MONTH-001"))
        rels["equipment_procedures"].append((tag, "SOP-LOTO-001"))
    for tag in boiler_tags:
        rels["equipment_procedures"].append((tag, "SOP-BOILER-START-001"))
        rels["equipment_procedures"].append((tag, "SOP-BOILER-STOP-001"))
        rels["equipment_procedures"].append((tag, "PM-BOILER-ANNUAL-001"))

    # Procedure -> Regulation (compliance mapping)
    rels["procedure_regulations"] = [
        ("SOP-VESSEL-ENTRY-001", "FACTORY-ACT-1948"),
        ("SOP-HOT-WORK-001", "OISD-STD-105"),
        ("SOP-LOTO-001", "OISD-STD-105"),
        ("SOP-PTW-001", "OISD-STD-105"),
        ("SOP-ERP-001", "OISD-GDN-206"),
        ("SOP-ERP-001", "ISO-45001"),
        ("SOP-ERP-002", "ISO-45001"),
        ("SOP-ERP-003", "ISO-45001"),
        ("SOP-CHEM-HANDLE-001", "FACTORY-ACT-1948"),
        ("SOP-CHEM-HANDLE-001", "ISO-45001"),
        ("SOP-HEIGHT-WORK-001", "FACTORY-ACT-1948"),
        ("SOP-HEIGHT-WORK-001", "ISO-45001"),
        ("SOP-CRANE-OPS-001", "FACTORY-ACT-1948"),
        ("SOP-SCAFFOLDING-001", "ISO-45001"),
        ("SOP-INCIDENT-001", "OISD-GDN-206"),
        ("SOP-MOC-001", "OISD-GDN-206"),
        ("SOP-MOC-001", "ISO-45001"),
        ("SOP-PSV-TEST-001", "API-510"),
        ("SOP-PSV-TEST-001", "ASME-SEC-VIII-D1"),
        ("SOP-HYDRO-TEST-001", "ASME-B31.3"),
        ("SOP-HYDRO-TEST-001", "IS-2825"),
        ("PM-BOILER-ANNUAL-001", "IBR-1950"),
        ("PM-TRANSFORMER-ANNUAL-001", "OISD-STD-144"),
        ("SOP-RADIOGRAPHY-001", "ISO-45001"),
    ]

    # FailureMode -> Procedure (mitigation)
    rels["failure_mode_procedures"] = [
        ("FM-SEAL-LEAK", "PM-PUMP-QTRLY-001"),
        ("FM-SEAL-LEAK", "SOP-ALIGNMENT-001"),
        ("FM-BEARING-FAIL", "PM-PUMP-QTRLY-001"),
        ("FM-BEARING-FAIL", "PM-MOTOR-QTRLY-001"),
        ("FM-IMPELLER-WEAR", "PM-PUMP-ANNUAL-001"),
        ("FM-CAVITATION", "SOP-PUMP-START-001"),
        ("FM-TUBE-FOUL", "SOP-HX-CLEAN-001"),
        ("FM-TUBE-FOUL", "PM-HX-ANNUAL-001"),
        ("FM-TUBE-LEAK", "PM-HX-ANNUAL-001"),
        ("FM-VALVE-STICK", "SOP-VALVE-MAINT-001"),
        ("FM-VALVE-STICK", "PM-VALVE-ANNUAL-001"),
        ("FM-MOTOR-OVH", "PM-MOTOR-ANNUAL-001"),
        ("FM-MOTOR-INSUL", "PM-MOTOR-ANNUAL-001"),
        ("FM-VIBRATION-MISALIGN", "SOP-ALIGNMENT-001"),
        ("FM-VIBRATION-MISALIGN", "PM-PUMP-QTRLY-001"),
        ("FM-COMPRESSOR-VALVE", "PM-COMP-6MONTH-001"),
        ("FM-SAFETY-VALVE-LEAK", "SOP-PSV-TEST-001"),
        ("FM-BOILER-TUBE-FAIL", "PM-BOILER-ANNUAL-001"),
        ("FM-DG-START-FAIL", "PM-DG-MONTHLY-001"),
        ("FM-TRANSFORMER-OIL", "PM-TRANSFORMER-ANNUAL-001"),
        ("FM-UPS-BATTERY", "PM-UPS-QTRLY-001"),
        ("FM-RO-MEMBRANE", "PM-CT-ANNUAL-001"),
        ("FM-COOLING-TOWER-FILL", "PM-CT-ANNUAL-001"),
        ("FM-LUBE-OIL-DEG", "PM-COMP-6MONTH-001"),
        ("FM-FLAME-FAILURE", "SOP-BOILER-START-001"),
    ]

    # Equipment -> Maintenance Records (from the WO data)
    for mr in maintenance_records:
        rels["equipment_maintenance"].append((mr["equipment_tag"], mr["work_order_id"]))

    # Maintenance -> Personnel
    for mr in maintenance_records:
        for pid in mr.get("personnel", []):
            rels["maintenance_personnel"].append((mr["work_order_id"], pid))

    # Maintenance -> FailureMode (for CM/EM work orders, assign relevant failure mode)
    for mr in maintenance_records:
        if mr["type"] in ("CM", "EM"):
            eq_tag = mr["equipment_tag"]
            eq = eq_by_tag.get(eq_tag)
            if eq:
                matching_fms = [fm["code"] for fm in failure_modes if eq["type"] in fm.get("equipment_types", [])]
                if matching_fms:
                    rels["maintenance_failure_modes"].append((mr["work_order_id"], random.choice(matching_fms)))

    # Inspection -> Equipment, Personnel
    for inf in inspection_findings:
        rels["inspection_equipment"].append((inf["finding_id"], inf["equipment_tag"]))
        rels["inspection_personnel"].append((inf["finding_id"], inf["inspector_id"]))

    # Inspection -> Regulation (for severity critical/major)
    for inf in inspection_findings:
        if inf["severity"] in ("critical", "major"):
            eq = eq_by_tag.get(inf["equipment_tag"])
            if eq and eq["type"] in ("Pressure Vessel", "Pressure Reactor"):
                rels["inspection_regulations"].append((inf["finding_id"], "API-510"))
            elif eq and ("Storage" in eq.get("type", "") or "Floating" in eq.get("type", "")):
                rels["inspection_regulations"].append((inf["finding_id"], "API-653"))

    # Process Parameters -> Equipment
    for pp in process_parameters:
        rels["equipment_process_params"].append((pp["equipment_tag"], pp["name"]))

    return rels


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("🏭 IntelliPlant — Generating Realistic Industrial Dataset")
    print("=" * 60)

    equipment = generate_equipment()
    print(f"✓ Equipment:           {len(equipment)} items")

    regulations = generate_regulations()
    print(f"✓ Regulations:         {len(regulations)} standards")

    personnel = generate_personnel()
    print(f"✓ Personnel:           {len(personnel)} people")

    failure_modes = generate_failure_modes()
    print(f"✓ Failure Modes:       {len(failure_modes)} modes")

    procedures = generate_procedures()
    print(f"✓ Procedures:          {len(procedures)} procedures")

    process_params = generate_process_parameters()
    print(f"✓ Process Parameters:  {len(process_params)} parameters")

    maintenance_records = generate_maintenance_records(equipment, personnel, failure_modes, procedures)
    print(f"✓ Maintenance Records: {len(maintenance_records)} work orders")

    inspection_findings = generate_inspection_findings(equipment, personnel)
    print(f"✓ Inspection Findings: {len(inspection_findings)} findings")

    relationships = generate_relationships(
        equipment, regulations, failure_modes, procedures,
        maintenance_records, inspection_findings, process_params, personnel
    )
    rel_count = sum(len(v) for v in relationships.values())
    print(f"✓ Relationships:       {rel_count} total")

    print(f"\n{'=' * 60}")
    print(f"📊 Total Dataset Size:")
    total_nodes = len(equipment) + len(regulations) + len(personnel) + len(failure_modes) + \
                  len(procedures) + len(process_params) + len(maintenance_records) + len(inspection_findings)
    print(f"   Nodes:         {total_nodes}")
    print(f"   Relationships: {rel_count}")

    # Save to JSON files
    print(f"\n💾 Saving to {OUTPUT_DIR}...")

    datasets = {
        "equipment": equipment,
        "regulations": regulations,
        "personnel": personnel,
        "failure_modes": failure_modes,
        "procedures": procedures,
        "process_parameters": process_params,
        "maintenance_records": maintenance_records,
        "inspection_findings": inspection_findings,
        "relationships": relationships,
    }

    for name, data in datasets.items():
        filepath = OUTPUT_DIR / f"{name}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"   ✓ {filepath.name} ({len(data) if isinstance(data, list) else 'dict'})")

    print(f"\n🎉 Dataset generation complete!")


if __name__ == "__main__":
    main()
