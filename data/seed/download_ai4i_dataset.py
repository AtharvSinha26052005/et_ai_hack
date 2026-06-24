"""Download and ingest the AI4I 2020 Predictive Maintenance Dataset.
Source: UCI Machine Learning Repository
URL: https://archive.ics.uci.edu/ml/machine-learning-databases/00601/ai4i2020.csv
"""

import asyncio
import sys
import os
import urllib.request
import csv
import random

# Add parent dir to path so we can import from backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend')))

DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00601/ai4i2020.csv"
DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), "ai4i2020.csv")

async def download_dataset():
    if not os.path.exists(DOWNLOAD_PATH):
        print(f"Downloading AI4I 2020 dataset from {DATASET_URL}...")
        try:
            # We add a User-Agent just in case
            req = urllib.request.Request(
                DATASET_URL, 
                data=None, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                with open(DOWNLOAD_PATH, 'w', encoding='utf-8') as f:
                    f.write(content)
            print("Download complete.")
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            sys.exit(1)
    else:
        print("Dataset already downloaded.")

async def ingest_dataset():
    from database.neo4j_client import Neo4jClient
    
    print("Ingesting AI4I dataset into Knowledge Graph...")
    await Neo4jClient.connect()

    # Read CSV
    with open(DOWNLOAD_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    print(f"Loaded {len(data)} records from CSV.")

    # We will pick a few random equipment tags to associate the data with,
    # as 10,000 readings on a single equipment might be too much,
    # or we can just map them to the pumps/motors we generated.
    equipment_tags = [
        "P-101A", "P-101B", "P-201A", "P-201B", 
        "M-101A", "M-101B", "M-201A", "M-201B"
    ]

    # Process Parameters definition for AI4I
    # Air temperature [K], Process temperature [K], Rotational speed [rpm], Torque [Nm], Tool wear [min]
    ai4i_params = [
        {"name": "AI4I-AIR-TEMP", "description": "Air temperature", "unit": "K"},
        {"name": "AI4I-PROC-TEMP", "description": "Process temperature", "unit": "K"},
        {"name": "AI4I-ROT-SPEED", "description": "Rotational speed", "unit": "rpm"},
        {"name": "AI4I-TORQUE", "description": "Torque", "unit": "Nm"},
        {"name": "AI4I-TOOL-WEAR", "description": "Tool wear", "unit": "min"}
    ]

    for param in ai4i_params:
        await Neo4jClient.execute_write(
            "MERGE (pp:ProcessParameter {name: $name}) SET pp += $props",
            {"name": param["name"], "props": param}
        )
        # Link params to our selected equipment
        for tag in equipment_tags:
            await Neo4jClient.execute_write(
                "MATCH (e:Equipment {tag: $tag}), (pp:ProcessParameter {name: $pname}) MERGE (e)-[:MONITORED_BY]->(pp)",
                {"tag": tag, "pname": param["name"]}
            )

    # Ingesting 10,000 sensor readings individually into Neo4j is very slow.
    # We will sample 500 records (including failures) for the demo KG.
    # The full dataset will remain as CSV for pandas/analytical tools.
    
    failures = [row for row in data if row['Machine failure'] == '1']
    normals = [row for row in data if row['Machine failure'] == '0']
    
    # Take all failures (~339) + some normals to make 500
    sample_size = min(500, len(data))
    if len(failures) < sample_size:
        sample_data = failures + random.sample(normals, sample_size - len(failures))
    else:
        sample_data = random.sample(failures, sample_size)
        
    random.shuffle(sample_data)
    
    print(f"Sampling {len(sample_data)} records for Knowledge Graph ingestion (full dataset kept in CSV).")
    
    count = 0
    for row in sample_data:
        reading_id = f"READING-{row['UDI']}"
        eq_tag = random.choice(equipment_tags)
        
        # Create SensorReading Node
        props = {
            "reading_id": reading_id,
            "air_temperature_k": float(row["Air temperature [K]"]),
            "process_temperature_k": float(row["Process temperature [K]"]),
            "rotational_speed_rpm": float(row["Rotational speed [rpm]"]),
            "torque_nm": float(row["Torque [Nm]"]),
            "tool_wear_min": float(row["Tool wear [min]"]),
            "machine_failure": int(row["Machine failure"]),
            "twf": int(row["TWF"]),
            "hdf": int(row["HDF"]),
            "pwf": int(row["PWF"]),
            "osf": int(row["OSF"]),
            "rnf": int(row["RNF"])
        }
        
        await Neo4jClient.execute_write(
            "MERGE (sr:SensorReading {reading_id: $rid}) SET sr += $props",
            {"rid": reading_id, "props": props}
        )
        
        # Link to Equipment
        await Neo4jClient.execute_write(
            "MATCH (e:Equipment {tag: $tag}), (sr:SensorReading {reading_id: $rid}) MERGE (e)-[:HAS_READING]->(sr)",
            {"tag": eq_tag, "rid": reading_id}
        )
        
        # Map AI4I failure modes to KG failure modes if there is a failure
        if props["twf"] == 1:
            await Neo4jClient.execute_write(
                "MATCH (sr:SensorReading {reading_id: $rid}), (fm:FailureMode {code: 'FM-IMPELLER-WEAR'}) MERGE (sr)-[:INDICATES_FAILURE]->(fm)",
                {"rid": reading_id}
            )
        if props["hdf"] == 1:
            await Neo4jClient.execute_write(
                "MATCH (sr:SensorReading {reading_id: $rid}), (fm:FailureMode {code: 'FM-MOTOR-OVH'}) MERGE (sr)-[:INDICATES_FAILURE]->(fm)",
                {"rid": reading_id}
            )
        if props["pwf"] == 1:
            await Neo4jClient.execute_write(
                "MATCH (sr:SensorReading {reading_id: $rid}), (fm:FailureMode {code: 'FM-BEARING-FAIL'}) MERGE (sr)-[:INDICATES_FAILURE]->(fm)",
                {"rid": reading_id}
            )
        if props["osf"] == 1:
            await Neo4jClient.execute_write(
                "MATCH (sr:SensorReading {reading_id: $rid}), (fm:FailureMode {code: 'FM-COUPLING-FAIL'}) MERGE (sr)-[:INDICATES_FAILURE]->(fm)",
                {"rid": reading_id}
            )
            
        count += 1
        if count % 100 == 0:
            print(f"  Ingested {count} readings...")

    print("AI4I Dataset ingestion complete!")
    await Neo4jClient.close()


async def main():
    await download_dataset()
    await ingest_dataset()

if __name__ == "__main__":
    asyncio.run(main())
