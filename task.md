# IntelliPlant — Task Tracker

## Phase 0: Environment Setup & Project Scaffolding
- [ ] Create project directory structure (`d:\ET\IntelliPlant\`)
- [ ] Initialize Python virtual environment (`venv`)
- [ ] Create `backend/requirements.txt` and install all dependencies
- [ ] Download SpaCy English model (`en_core_web_sm`)
- [ ] Install Tesseract OCR (Windows binary)
- [ ] Create `docker-compose.yml` with Neo4j service
- [ ] Start Neo4j via Docker, verify connection
- [ ] Initialize React + Vite + TypeScript frontend (`npx create-vite`)
- [ ] Install frontend dependencies (react-force-graph-3d, axios, react-router-dom, react-markdown, lucide-react)
- [ ] Create `.env.example` and `.env` with all config keys
- [ ] Create `.gitignore` for Python + Node + IDE artifacts
- [ ] Verify full stack starts: FastAPI on :8000, React on :5173, Neo4j on :7687

---

## Phase 1: Backend Foundation (FastAPI)
- [ ] Create `backend/config/settings.py` — Pydantic Settings from .env
- [ ] Create `backend/main.py` — FastAPI app with CORS, lifespan, route registration
- [ ] Create `backend/api/routes/health.py` — Health check endpoint
- [ ] Create `backend/database/neo4j_client.py` — Neo4j async driver singleton
- [ ] Create `backend/database/chroma_client.py` — ChromaDB persistent client
- [ ] Create `backend/database/sqlite_client.py` — SQLAlchemy async session
- [ ] Create `backend/models/database.py` — SQLAlchemy models (Document, AuditLog)
- [ ] Create `backend/schemas/` — All Pydantic request/response models
- [ ] Verify: `GET /health` returns 200 with DB connection statuses

---

## Phase 2: Document Processing Pipeline
- [ ] Create `backend/services/document_processor.py`
  - [ ] `process_pdf()` — PyMuPDF text extraction
  - [ ] `process_pdf_ocr()` — Tesseract fallback for scanned pages
  - [ ] `process_docx()` — python-docx text extraction
  - [ ] `process_spreadsheet()` — openpyxl for Excel
  - [ ] `detect_document_type()` — Classify document category
  - [ ] `chunk_document()` — Industrial-aware text splitting
- [ ] Create `backend/api/routes/documents.py`
  - [ ] `POST /api/documents/upload` — File upload + trigger processing
  - [ ] `GET /api/documents` — List documents with metadata
  - [ ] `GET /api/documents/{id}` — Document detail
  - [ ] `DELETE /api/documents/{id}` — Remove document + KG cleanup
- [ ] Create file storage system (save uploads to `./uploads/`)
- [ ] Test: Upload a PDF → get parsed text + chunks back

---

## Phase 3: Entity Extraction
- [ ] Create `backend/services/entity_extractor.py`
  - [ ] SpaCy NER pipeline for base entities (ORG, DATE, PERSON)
  - [ ] GLiNER zero-shot extraction for industrial entities (EQUIPMENT, PARAMETER, FAILURE_MODE, REGULATION, PROCEDURE, CHEMICAL)
  - [ ] Equipment tag regex patterns (e.g., `P-\d{3}[A-Z]?`, `HX-\d+`, `V-\d+`)
  - [ ] Relationship extraction via Gemini structured output
  - [ ] Entity deduplication / resolution (fuzzy matching)
- [ ] Create `backend/utils/prompts.py` — All LLM prompt templates
  - [ ] Entity extraction prompt
  - [ ] Relationship extraction prompt
  - [ ] Document classification prompt
  - [ ] Compliance analysis prompt
  - [ ] RCA prompt
  - [ ] Query answering prompt
- [ ] Create `backend/services/llm_service.py` — Gemini API wrapper with retry logic
- [ ] Test: Process a pump manual → extract 20+ entities, 10+ relationships

---

## Phase 4: Knowledge Graph (Neo4j)
- [ ] Design Neo4j schema: create constraints + indexes
  - [ ] Unique constraints on: Equipment.tag, Document.id, Regulation.standard_id
  - [ ] Full-text indexes on: Equipment.name, Document.title, Regulation.title
- [ ] Create `backend/services/knowledge_graph_service.py`
  - [ ] `upsert_node()` — MERGE pattern with properties
  - [ ] `upsert_relationship()` — MERGE relationship with properties
  - [ ] `query_subgraph()` — N-hop traversal
  - [ ] `search_nodes()` — Full-text search
  - [ ] `get_stats()` — Count nodes/rels by type
  - [ ] `get_equipment_history()` — Full timeline
  - [ ] `find_compliance_gaps()` — Equipment without required regulation links
  - [ ] `get_failure_patterns()` — Most common failure mode correlations
- [ ] Create `backend/api/routes/knowledge_graph.py`
  - [ ] `GET /api/kg/stats` — Dashboard statistics
  - [ ] `GET /api/kg/nodes` — Paginated listing
  - [ ] `GET /api/kg/nodes/{id}` — Detail with relationships
  - [ ] `GET /api/kg/search?q=` — Full-text search
  - [ ] `GET /api/kg/subgraph?node_id=&depth=` — For visualization
- [ ] Test: Insert entities from Phase 3 → verify graph in Neo4j Browser

---

## Phase 5: Multi-Agent Orchestrator (LangGraph)
- [ ] Create `backend/agents/state.py` — AgentState TypedDict
- [ ] Create `backend/agents/ingestion_agent.py`
  - [ ] Calls document_processor → produces chunks
  - [ ] Stores chunks in ChromaDB
  - [ ] Returns chunk metadata in state
- [ ] Create `backend/agents/extraction_agent.py`
  - [ ] Calls entity_extractor on chunks
  - [ ] Returns entities + relationships in state
- [ ] Create `backend/agents/kg_builder_agent.py`
  - [ ] Takes entities/relationships from state
  - [ ] Calls knowledge_graph_service to upsert
  - [ ] Returns KG update status
- [ ] Create `backend/agents/query_agent.py`
  - [ ] Hybrid retrieval: vector + graph
  - [ ] Answer generation with citations
  - [ ] Confidence scoring
- [ ] Create `backend/agents/orchestrator.py`
  - [ ] LangGraph StateGraph definition
  - [ ] Supervisor routing logic
  - [ ] Edge definitions (ingestion → extraction → kg_builder)
  - [ ] Compile and export workflow
- [ ] Test: Upload document → verify full pipeline runs (parse → extract → KG build)
- [ ] Test: Ask question → verify hybrid retrieval + LLM answer

---

## Phase 6: RAG Engine (Interactive Retrieval)
- [ ] Create `backend/services/vector_store_service.py`
  - [ ] `add_documents()` — Store chunks with embeddings in ChromaDB
  - [ ] `similarity_search()` — Top-K semantic search
  - [ ] `delete_by_document()` — Remove chunks when document deleted
- [ ] Create `backend/services/rag_engine.py`
  - [ ] Vector retrieval path (ChromaDB similarity search)
  - [ ] Graph retrieval path (entity recognition → Cypher query → results)
  - [ ] GraphCypherQAChain for natural language → Cypher
  - [ ] Result fusion + re-ranking
  - [ ] LLM generation with source citations
  - [ ] Confidence score calculation
  - [ ] Conversation memory (last 10 messages)
- [ ] Create `backend/api/routes/chat.py`
  - [ ] `POST /api/chat` — Synchronous RAG query
  - [ ] `WebSocket /api/chat/ws` — Streaming response
  - [ ] `GET /api/chat/history` — Conversation history
- [ ] Test: Ask 5 benchmark questions → verify accuracy + citations

---

## Phase 7: Frontend — Core UI
- [ ] Create `frontend/src/index.css` — Complete dark theme design system
- [ ] Create layout components
  - [ ] `Sidebar.tsx` — Navigation with icons (Documents, KG, Chat, Compliance, Maintenance)
  - [ ] `Header.tsx` — App title, stats bar, notifications
  - [ ] `MainLayout.tsx` — Sidebar + content area layout
- [ ] Create common components
  - [ ] `Button.tsx`, `Card.tsx`, `Badge.tsx`, `Modal.tsx`, `LoadingSpinner.tsx`
- [ ] Create `frontend/src/services/api.ts` — Axios client with all API functions
- [ ] Create `frontend/src/types/index.ts` — TypeScript interfaces
- [ ] Setup React Router with 5 pages

### Page 1: Document Management
- [ ] `DocumentUpload.tsx` — Drag & drop with progress bar, multi-file support
- [ ] `DocumentList.tsx` — Filterable list with type badges, entity count, processing status
- [ ] `DocumentViewer.tsx` — Preview document content + extracted entities highlighted

### Page 2: Knowledge Graph Explorer
- [ ] `GraphViewer3D.tsx` — 3D force-directed graph (react-force-graph-3d)
  - [ ] Color-coded nodes by type
  - [ ] Hover tooltips
  - [ ] Click to select + detail panel
  - [ ] Search highlighting
- [ ] `GraphControls.tsx` — Filter by node type, search bar, depth slider
- [ ] `NodeDetail.tsx` — Side panel with node properties + connected nodes
- [ ] `GraphStats.tsx` — Cards showing node/relationship counts by type

### Page 3: Interactive RAG Chat
- [ ] `ChatInterface.tsx` — Full chat UI with message list + input
  - [ ] Streaming message rendering (WebSocket)
  - [ ] Markdown rendering in responses
  - [ ] Code block styling
- [ ] `ChatMessage.tsx` — User/assistant message bubbles
- [ ] `SourceCitation.tsx` — Clickable citation pills showing document name + page
- [ ] `ConfidenceIndicator.tsx` — Color-coded confidence score bar
- [ ] Side panel: relevant KG subgraph for current answer

### Page 4: Compliance Dashboard
- [ ] `ComplianceDashboard.tsx` — Overview with regulation cards + gap counts
- [ ] `GapAnalysisCard.tsx` — Individual gap with severity, affected equipment, evidence
- [ ] `ComplianceReport.tsx` — Generate + download compliance report

### Page 5: Maintenance Intelligence
- [ ] `MaintenanceDashboard.tsx` — Equipment health overview cards
- [ ] `RCAAnalysis.tsx` — Root cause analysis visualization
- [ ] `MaintenanceTimeline.tsx` — Equipment maintenance history timeline

---

## Phase 8: Compliance & Maintenance Agents
- [ ] Create `backend/agents/compliance_agent.py`
  - [ ] Load regulatory requirements from KG
  - [ ] Compare against current equipment/procedure states
  - [ ] Identify gaps with severity ratings
  - [ ] Generate evidence packages with document references
- [ ] Create `backend/agents/maintenance_agent.py`
  - [ ] Query failure history from KG
  - [ ] Correlate failure modes across equipment types
  - [ ] Generate RCA support (probable causes ranked)
  - [ ] Predict next maintenance actions based on MTBF
- [ ] Create `backend/api/routes/compliance.py` — All compliance endpoints
- [ ] Create `backend/api/routes/maintenance.py` — All maintenance endpoints
- [ ] Test: Run compliance analysis → verify gap detection against known gaps
- [ ] Test: Run RCA → verify causal chain identification

---

## Phase 9: Dataset Preparation & Seeding
- [ ] Create `scripts/download_datasets.py`
  - [ ] Download equipment manuals (Siemens, ABB, Grundfos)
  - [ ] Download regulatory docs (OISD, Factory Act, OSHA)
  - [ ] Download P&ID dataset from Zenodo
  - [ ] Download AI4I predictive maintenance dataset
- [ ] Create `scripts/generate_synthetic_data.py`
  - [ ] Generate 500 work orders (realistic SAP PM format)
  - [ ] Generate 200 inspection reports
  - [ ] Generate 100 incident/near-miss reports
  - [ ] Generate 50 SOP documents
- [ ] Create `data/seed/seed_knowledge_graph.py`
  - [ ] Pre-populate equipment master data (50 equipment items)
  - [ ] Pre-populate regulatory framework (15 standards)
  - [ ] Pre-populate personnel (20 engineers/technicians)
- [ ] Run full ingestion pipeline on all seed data
- [ ] Verify KG has 50K+ nodes with rich interconnections

---

## Phase 10: Polish, Testing & Demo Prep
- [ ] Write backend unit tests
  - [ ] `test_document_processor.py` — PDF/DOCX parsing
  - [ ] `test_entity_extractor.py` — Entity extraction accuracy
  - [ ] `test_rag_engine.py` — RAG answer quality
  - [ ] `test_api.py` — All API endpoints
- [ ] Run all tests, fix failures
- [ ] Performance optimization
  - [ ] Add response caching for common KG queries
  - [ ] Optimize Cypher queries with EXPLAIN
  - [ ] Lazy-load frontend components
- [ ] Create `README.md` in project root
- [ ] Create architecture diagram (export from Mermaid)
- [ ] Build demo script with 5 wow-moments
  - [ ] Live document upload → watch KG grow
  - [ ] Complex cross-document question → cited answer
  - [ ] Knowledge graph exploration → 3D visual
  - [ ] Compliance gap detection → evidence report
  - [ ] Maintenance RCA → causal chain
- [ ] Record demo video (3-5 minutes)
- [ ] Prepare presentation deck (10-12 slides)

---

## Effort Estimates

| Phase | Estimated Hours | Priority |
|---|---|---|
| Phase 0: Setup | 2h | P0 |
| Phase 1: Backend Foundation | 3h | P0 |
| Phase 2: Document Processing | 4h | P0 |
| Phase 3: Entity Extraction | 5h | P0 |
| Phase 4: Knowledge Graph | 4h | P0 |
| Phase 5: Multi-Agent | 6h | P0 |
| Phase 6: RAG Engine | 6h | P0 |
| Phase 7: Frontend | 10h | P0 |
| Phase 8: Compliance + Maintenance | 6h | P1 |
| Phase 9: Dataset Prep | 4h | P0 |
| Phase 10: Polish + Demo | 4h | P0 |
| **Total** | **~54 hours** | |
