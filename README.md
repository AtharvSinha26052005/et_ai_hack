# IntelliPlant — AI-Powered Industrial Knowledge Intelligence Platform

> **Unified Asset & Operations Brain** — making industrial knowledge queryable, actionable, and continuously updated at the point of need.

## 🏗️ Architecture

```
┌──────────────┐     ┌───────────────────────────────────────────────┐
│  React/Vite  │────▶│              FastAPI Backend                  │
│   Frontend   │     │                                               │
│  (Port 5173) │     │  ┌─────────┐  ┌─────────────┐  ┌──────────┐ │
│              │     │  │  API    │  │  LangGraph   │  │   RAG    │ │
│  Dashboard   │     │  │ Routes  │  │ Multi-Agent  │  │  Engine  │ │
│  Documents   │     │  └────┬────┘  │ Orchestrator │  └────┬─────┘ │
│  KG Explorer │     │       │       └──────┬───────┘       │       │
│  Chat (RAG)  │     │       ▼              ▼               ▼       │
│  Compliance  │     │  ┌────────┐   ┌────────────┐  ┌──────────┐  │
│  Maintenance │     │  │SQLite  │   │   Neo4j     │  │ ChromaDB │  │
│              │     │  │Metadata│   │  Knowledge  │  │  Vector  │  │
│              │     │  │  Store │   │   Graph     │  │  Store   │  │
└──────────────┘     │  └────────┘   └────────────┘  └──────────┘  │
                     └──────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop (for Neo4j)
- Google Gemini API key ([get one free](https://aistudio.google.com/apikey))

### 1. Start Neo4j

```bash
docker-compose up -d
```

This starts Neo4j with APOC plugin on `bolt://localhost:7687` (credentials: `neo4j/intelliplant2026`).

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and set your GOOGLE_API_KEY
```

### 3. Set Up Backend

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm    # For NER
```

### 4. Seed the Knowledge Graph (Optional)

```bash
cd data/seed
python seed_knowledge_graph.py
```

This pre-populates Neo4j with 25 equipment items, 15 regulations, 20 personnel, 10 failure modes, 10 procedures, 10 work orders, and ~80 relationships.

### 5. Start the Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at: http://localhost:8000/docs

### 6. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

---

## 🧩 Key Features

| Feature | Description |
|---|---|
| **Document Intelligence** | Upload PDFs, DOCX, Excel, images — AI extracts entities, builds KG, stores embeddings |
| **Knowledge Graph** | Neo4j-powered graph with Equipment, Regulations, Personnel, Failure Modes, Procedures |
| **Interactive RAG Chat** | Hybrid retrieval (vector + graph) with cited answers, confidence scores, follow-ups |
| **Compliance Dashboard** | Detects regulatory gaps, calculates compliance scores, generates evidence reports |
| **Maintenance Intelligence** | Root cause analysis, failure pattern detection, predictive recommendations |
| **Multi-Agent Orchestrator** | LangGraph supervisor-worker pattern coordinating 6 specialized agents |

## 🧪 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19 + TypeScript + Vite |
| Backend | FastAPI (async) |
| LLM | Google Gemini 2.0 Flash |
| Knowledge Graph | Neo4j + APOC |
| Vector Store | ChromaDB + all-MiniLM-L6-v2 |
| NER | SpaCy + GLiNER (zero-shot) |
| Multi-Agent | LangGraph (supervisor-worker) |
| Metadata Store | SQLite + SQLAlchemy (async) |

## 📂 Project Structure

```
IntelliPlant/
├── backend/
│   ├── agents/          # LangGraph multi-agent nodes
│   ├── api/routes/      # FastAPI REST endpoints
│   ├── config/          # Pydantic settings
│   ├── database/        # Neo4j, ChromaDB, SQLite clients
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic v2 API schemas
│   ├── services/        # Core business logic
│   ├── utils/           # Prompts and helpers
│   └── main.py          # FastAPI application entry
├── frontend/
│   ├── src/
│   │   ├── components/  # Layout, shared UI
│   │   ├── pages/       # Dashboard, Docs, KG, Chat, Compliance, Maintenance
│   │   ├── services/    # API client (Axios)
│   │   ├── types/       # TypeScript interfaces
│   │   └── utils/       # Formatters
│   └── index.html
├── data/seed/           # KG seed data scripts
├── docker-compose.yml   # Neo4j + APOC
└── .env.example         # Environment template
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Service health status |
| POST | `/api/documents/upload` | Upload document |
| GET | `/api/documents` | List documents |
| GET | `/api/kg/stats` | KG statistics |
| GET | `/api/kg/search?q=...` | Full-text KG search |
| GET | `/api/kg/nodes/{id}` | Node detail + connections |
| POST | `/api/chat` | RAG query with citations |
| WS | `/api/chat/ws` | Streaming chat |
| POST | `/api/compliance/analyze` | Run compliance analysis |
| POST | `/api/maintenance/rca` | Root cause analysis |
| GET | `/api/maintenance/failure-patterns` | Cross-equipment patterns |

---

**Built for AI Hackathon 2026** 🏆
