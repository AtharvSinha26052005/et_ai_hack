<p align="center">
  <img src="docs/logo.png" alt="IntelliPlant Logo" width="120" />
</p>

<h1 align="center">IntelliPlant</h1>
<h3 align="center">AI-Powered Industrial Knowledge Intelligence Platform</h3>

<p align="center">
  <strong>Unified Asset & Operations Brain — ET AI Hackathon 2026 (Problem Statement 8)</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?logo=react" alt="React" />
  <img src="https://img.shields.io/badge/Neo4j-5.x-008CC1?logo=neo4j" alt="Neo4j" />
  <img src="https://img.shields.io/badge/LangGraph-0.4+-orange" alt="LangGraph" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License" />
</p>

---

## 🧠 What is IntelliPlant?

IntelliPlant is an **AI-powered Industrial Knowledge Intelligence platform** that solves the critical problem of knowledge fragmentation in asset-intensive industries. It ingests heterogeneous industrial documents — equipment manuals, maintenance records, safety procedures, inspection reports, P&IDs, and regulatory standards — and transforms them into a **unified, queryable knowledge graph** with an **interactive RAG-powered copilot**.

### The Problem We Solve

> *"Professionals in asset-intensive industries spend 35% of their working hours searching for information, clarifying instructions, or recreating documents that already exist."* — McKinsey, 2024

- **7-12 disconnected document systems** per average Indian industrial plant (NASSCOM-EY)
- **18-22% of unplanned downtime** caused by information fragmentation (BIS Research)
- **25% of experienced industrial engineers** retiring in the next decade, taking undocumented knowledge with them

### Our Solution

IntelliPlant uses a **multi-agent AI system** to:

1. 📥 **Ingest** — Parse PDFs, P&IDs, scanned forms, spreadsheets, and manuals with OCR
2. 🔍 **Extract** — Identify equipment tags, failure modes, regulatory references, and relationships using NER + LLM
3. 🕸️ **Connect** — Build a unified knowledge graph in Neo4j with 50,000+ entities and 15 relationship types
4. 💬 **Query** — Answer complex cross-document questions via Interactive RAG (vector search + graph traversal) with source citations
5. 📋 **Comply** — Detect regulatory compliance gaps against OISD, Factory Act, and PESO standards
6. 🛠️ **Maintain** — Generate root cause analyses and predictive maintenance recommendations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    React + Vite Frontend                        │
│  ┌──────────┐ ┌──────────────┐ ┌──────┐ ┌──────────┐ ┌──────┐ │
│  │ Document │ │ Knowledge    │ │ RAG  │ │Compliance│ │Maint.│ │
│  │ Manager  │ │ Graph 3D     │ │ Chat │ │Dashboard │ │Intel.│ │
│  └──────────┘ └──────────────┘ └──────┘ └──────────┘ └──────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │ REST + WebSocket
┌────────────────────────┴────────────────────────────────────────┐
│                    FastAPI Backend                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           LangGraph Multi-Agent Orchestrator              │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐               │   │
│  │  │ Ingestion │→│Extraction │→│KG Builder │               │   │
│  │  │   Agent   │ │   Agent   │ │   Agent   │               │   │
│  │  └───────────┘ └───────────┘ └───────────┘               │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐               │   │
│  │  │  Query    │ │Compliance │ │Maintenance│               │   │
│  │  │  Agent    │ │   Agent   │ │   Agent   │               │   │
│  │  └───────────┘ └───────────┘ └───────────┘               │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────┬──────────────┬──────────────┬────────────────────────┘
           │              │              │
    ┌──────┴──────┐ ┌─────┴─────┐ ┌──────┴──────┐
    │   Neo4j     │ │ ChromaDB  │ │   SQLite    │
    │ Knowledge   │ │  Vector   │ │  Metadata   │
    │   Graph     │ │   Store   │ │  + Audit    │
    └─────────────┘ └───────────┘ └─────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | FastAPI + Python 3.11 | REST API + WebSocket server |
| **Frontend** | React 19 + Vite 6 + TypeScript | Interactive dashboard |
| **Knowledge Graph** | Neo4j 5.x | Entity-relationship storage |
| **Vector Store** | ChromaDB | Semantic search over document chunks |
| **Multi-Agent** | LangGraph | Supervisor-Worker agent orchestration |
| **RAG** | LangChain + langchain-neo4j | GraphRAG hybrid retrieval |
| **LLM** | Google Gemini 2.0 Flash | Generation, extraction, classification |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | Local, free, 384-dim vectors |
| **Document Processing** | PyMuPDF + Tesseract OCR | PDF/image parsing |
| **NER** | SpaCy + GLiNER | Industrial entity extraction |
| **Graph Visualization** | react-force-graph-3d | Interactive 3D knowledge graph |

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Install |
|---|---|---|
| Python | 3.11+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 20+ | [nodejs.org](https://nodejs.org/) |
| Docker Desktop | Latest | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Tesseract OCR | 5.x | [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) |
| Google Gemini API Key | Free tier | [aistudio.google.com](https://aistudio.google.com/apikey) |

### Step 1: Clone & Setup

```powershell
# Navigate to project
cd d:\ET\IntelliPlant

# Create Python virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cd ..
```

### Step 2: Start Neo4j

```powershell
# Start Neo4j database via Docker
docker-compose up -d neo4j

# Verify Neo4j is running (wait ~30 seconds)
# Visit http://localhost:7474 in your browser
# Login: neo4j / intelliplant2026
```

### Step 3: Configure Environment

```powershell
# Copy example env and add your API key
copy .env.example .env

# Edit .env — add your GOOGLE_API_KEY
notepad .env
```

### Step 4: Setup Frontend

```powershell
cd frontend
npm install
cd ..
```

### Step 5: Seed Sample Data (Optional)

```powershell
# Download sample documents + generate synthetic data
.\venv\Scripts\activate
python scripts/download_datasets.py
python scripts/generate_synthetic_data.py
python data/seed/seed_knowledge_graph.py
```

### Step 6: Run!

```powershell
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

**Open** → [http://localhost:5173](http://localhost:5173)  
**API Docs** → [http://localhost:8000/docs](http://localhost:8000/docs)  
**Neo4j Browser** → [http://localhost:7474](http://localhost:7474)

---

## 📊 Knowledge Graph Schema

```
Equipment ──HAS_DOCUMENT──→ Document
Equipment ──HAS_MAINTENANCE──→ MaintenanceRecord
Equipment ──HAS_FAILURE_MODE──→ FailureMode
Equipment ──GOVERNED_BY──→ Regulation
Equipment ──FOLLOWS_PROCEDURE──→ Procedure
Equipment ──HAS_INSPECTION──→ InspectionFinding
Equipment ──MONITORS──→ ProcessParameter
MaintenanceRecord ──PERFORMED_BY──→ Personnel
MaintenanceRecord ──CAUSED_BY──→ FailureMode
MaintenanceRecord ──REFERENCES──→ Document
InspectionFinding ──FOUND_BY──→ Personnel
InspectionFinding ──VIOLATES──→ Regulation
Procedure ──COMPLIES_WITH──→ Regulation
Document ──MENTIONS──→ Equipment
Document ──REFERENCES──→ Regulation
FailureMode ──MITIGATED_BY──→ Procedure
```

**9 node types** · **15 relationship types** · **50,000+ entities** at demo scale

---

## 📂 Dataset Sources

| Category | Source | Type | Access |
|---|---|---|---|
| Equipment Manuals | Siemens, ABB, Grundfos, Honeywell | Real PDFs | Free download from manufacturer sites |
| Regulatory Standards | OISD, Factory Act, PESO, BIS | Real documents | Free from oisd.gov.in, indiacode.nic.in |
| P&ID Drawings | Zenodo PID_dataset | Academic dataset | [zenodo.org/records/4588402](https://zenodo.org/records/4588402) |
| Maintenance Records | Generated (SAP PM format) | Synthetic | `scripts/generate_synthetic_data.py` |
| Inspection Reports | Generated (OISD format) | Synthetic | `scripts/generate_synthetic_data.py` |
| Sensor Data | NASA C-MAPSS, AI4I 2020 | Public datasets | NASA Prognostics Repo, UCI ML Repo |

---

## 🤖 Multi-Agent System

IntelliPlant uses a **LangGraph Supervisor-Worker** architecture with 6 specialized agents:

| Agent | Role | Tools |
|---|---|---|
| **Supervisor** | Routes requests, orchestrates workflows | Intent classifier |
| **Ingestion Agent** | Parses documents, applies OCR, chunks text | PyMuPDF, Tesseract, text splitter |
| **Extraction Agent** | Extracts entities and relationships | SpaCy, GLiNER, Gemini |
| **KG Builder Agent** | Constructs/updates knowledge graph | Neo4j Cypher |
| **Query Agent** | Interactive RAG with hybrid retrieval | ChromaDB + Neo4j + Gemini |
| **Compliance Agent** | Regulatory gap analysis | Neo4j Cypher + Gemini |
| **Maintenance Agent** | RCA + predictive maintenance | Neo4j Cypher + Gemini |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/documents/upload` | Upload and process documents |
| `GET` | `/api/documents` | List all documents |
| `GET` | `/api/documents/{id}` | Document detail + entities |
| `POST` | `/api/chat` | RAG query with citations |
| `WS` | `/api/chat/ws` | Streaming RAG chat |
| `GET` | `/api/kg/stats` | Knowledge graph statistics |
| `GET` | `/api/kg/subgraph` | Get subgraph for visualization |
| `GET` | `/api/kg/search` | Search knowledge graph |
| `POST` | `/api/compliance/analyze` | Run compliance gap analysis |
| `GET` | `/api/maintenance/recommendations` | Maintenance recommendations |
| `POST` | `/api/maintenance/rca` | Root cause analysis |

Full API documentation available at `/docs` (Swagger UI) when the backend is running.

---

## 🎯 Evaluation Criteria Alignment

| Hackathon Criteria (Weight) | How IntelliPlant Delivers |
|---|---|
| **Innovation (25%)** | Multi-agent GraphRAG combining vector search + knowledge graph traversal — cutting-edge hybrid retrieval |
| **Business Impact (25%)** | Reduces information retrieval from hours to seconds, prevents knowledge loss from retiring workforce |
| **Technical Excellence (20%)** | LangGraph supervisor-worker, Neo4j knowledge graph, hybrid RAG, industrial NER pipeline |
| **Scalability (15%)** | Containerized with Docker, async FastAPI, Neo4j scales to billions of nodes |
| **User Experience (15%)** | 3D interactive knowledge graph, streaming chat with citations, glassmorphism dark UI |

---

## 📁 Project Structure

```
IntelliPlant/
├── README.md
├── .env.example
├── docker-compose.yml
├── backend/
│   ├── requirements.txt
│   ├── main.py
│   ├── config/settings.py
│   ├── api/routes/          # FastAPI route handlers
│   ├── schemas/             # Pydantic models
│   ├── services/            # Business logic
│   ├── agents/              # LangGraph agents
│   ├── models/              # Database models
│   ├── database/            # DB clients
│   └── utils/               # Helpers
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── hooks/           # Custom hooks
│   │   ├── services/        # API client
│   │   └── pages/           # Route pages
│   └── package.json
├── data/
│   ├── sample_documents/    # Demo documents
│   └── seed/                # KG seeding scripts
└── scripts/
    ├── setup_windows.ps1
    ├── download_datasets.py
    └── generate_synthetic_data.py
```

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm run test

# Lint
cd backend && ruff check .
cd frontend && npm run lint
```

---

## 👥 Team

**ET AI Hackathon 2026** — Problem Statement 8: AI for Industrial Knowledge Intelligence

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.
