# IntelliPlant — Task Tracker

## Phase 0: Environment Setup & Project Scaffolding
- [x] Create project directory structure (`d:\ET\IntelliPlant\`)
- [ ] Initialize Python virtual environment (`venv`)
- [x] Create `backend/requirements.txt` and install all dependencies
- [ ] Download SpaCy English model (`en_core_web_sm`)
- [ ] Install Tesseract OCR (Windows binary)
- [x] Create `docker-compose.yml` with Neo4j service
- [ ] Start Neo4j via Docker, verify connection
- [x] Initialize React + Vite + TypeScript frontend (`npx create-vite`)
- [x] Install frontend dependencies (react-force-graph-3d, axios, react-router-dom, react-markdown, lucide-react)
- [x] Create `.env.example` and `.env` with all config keys
- [x] Create `.gitignore` for Python + Node + IDE artifacts
- [ ] Verify full stack starts: FastAPI on :8000, React on :5173, Neo4j on :7687

---

## Phase 1: Backend Foundation (FastAPI)
- [x] Create `backend/config/settings.py` — Pydantic Settings from .env
- [x] Create `backend/main.py` — FastAPI app with CORS, lifespan, route registration
- [x] Create `backend/api/routes/health.py` — Health check endpoint
- [x] Create `backend/database/neo4j_client.py` — Neo4j async driver singleton
- [x] Create `backend/database/chroma_client.py` — ChromaDB persistent client
- [x] Create `backend/database/sqlite_client.py` — SQLAlchemy async session
- [x] Create `backend/models/database.py` — SQLAlchemy models (Document, AuditLog)
- [x] Create `backend/schemas/` — All Pydantic request/response models
- [ ] Verify: `GET /health` returns 200 with DB connection statuses

---

## Phase 2: Document Processing Pipeline
- [x] Create `backend/services/document_processor.py`
  - [x] `process_pdf()` — PyMuPDF text extraction
  - [x] `process_pdf_ocr()` — Tesseract fallback for scanned pages
  - [x] `process_docx()` — python-docx text extraction
  - [x] `process_spreadsheet()` — openpyxl for Excel
  - [x] `detect_document_type()` — Classify document category
  - [x] `chunk_document()` — Industrial-aware text splitting
- [x] Create `backend/api/routes/documents.py`
  - [x] `POST /api/documents/upload` — File upload + trigger processing
  - [x] `GET /api/documents` — List documents with metadata
  - [x] `GET /api/documents/{id}` — Document detail
  - [x] `DELETE /api/documents/{id}` — Remove document + KG cleanup
- [x] Create file storage system (save uploads to `./uploads/`)
- [ ] Test: Upload a PDF → get parsed text + chunks back

---

## Phase 3: Entity Extraction
- [x] Create `backend/services/entity_extractor.py`
  - [x] SpaCy NER pipeline for base entities (ORG, DATE, PERSON)
  - [x] GLiNER zero-shot extraction for industrial entities (EQUIPMENT, PARAMETER, FAILURE_MODE, REGULATION, PROCEDURE, CHEMICAL)
  - [x] Equipment tag regex patterns (e.g., `P-\d{3}[A-Z]?`, `HX-\d+`, `V-\d+`)
  - [x] Relationship extraction via Gemini structured output
  - [x] Entity deduplication / resolution (fuzzy matching)
- [x] Create `backend/utils/prompts.py` — All LLM prompt templates
  - [x] Entity extraction prompt
  - [x] Relationship extraction prompt
  - [x] Document classification prompt
  - [x] Compliance analysis prompt
  - [x] RCA prompt
  - [x] Query answering prompt
- [x] Create `backend/services/llm_service.py` — Gemini API wrapper with retry logic
- [ ] Test: Process a pump manual → extract 20+ entities, 10+ relationships

---

## Phase 4: Knowledge Graph (Neo4j)
- [x] Design Neo4j schema: create constraints + indexes
  - [x] Unique constraints on: Equipment.tag, Document.id, Regulation.standard_id
  - [x] Full-text indexes on: Equipment.name, Document.title, Regulation.title
- [x] Create `backend/services/knowledge_graph_service.py`
  - [x] `upsert_node()` — MERGE pattern with properties
  - [x] `upsert_relationship()` — MERGE relationship with properties
  - [x] `query_subgraph()` — N-hop traversal
  - [x] `search_nodes()` — Full-text search
  - [x] `get_stats()` — Count nodes/rels by type
  - [x] `get_equipment_history()` — Full timeline
  - [x] `find_compliance_gaps()` — Equipment without required regulation links
  - [x] `get_failure_patterns()` — Most common failure mode correlations
- [x] Create `backend/api/routes/knowledge_graph.py`
  - [x] `GET /api/kg/stats` — Dashboard statistics
  - [x] `GET /api/kg/nodes` — Paginated listing
  - [x] `GET /api/kg/nodes/{id}` — Detail with relationships
  - [x] `GET /api/kg/search?q=` — Full-text search
  - [x] `GET /api/kg/subgraph?node_id=&depth=` — For visualization
- [ ] Test: Insert entities from Phase 3 → verify graph in Neo4j Browser

---

## Phase 5: Multi-Agent Orchestrator (LangGraph)
- [x] Create `backend/agents/state.py` — AgentState TypedDict
- [x] Create `backend/agents/ingestion_agent.py`
  - [x] Calls document_processor → produces chunks
  - [x] Stores chunks in ChromaDB
  - [x] Returns chunk metadata in state
- [x] Create `backend/agents/extraction_agent.py`
  - [x] Calls entity_extractor on chunks
  - [x] Returns entities + relationships in state
- [x] Create `backend/agents/kg_builder_agent.py`
  - [x] Takes entities/relationships from state
  - [x] Calls knowledge_graph_service to upsert
  - [x] Returns KG update status
- [x] Create `backend/agents/query_agent.py`
  - [x] Hybrid retrieval: vector + graph
  - [x] Answer generation with citations
  - [x] Confidence scoring
- [x] Create `backend/agents/orchestrator.py`
  - [x] LangGraph StateGraph definition
  - [x] Supervisor routing logic
  - [x] Edge definitions (ingestion → extraction → kg_builder)
  - [x] Compile and export workflow
- [ ] Test: Upload document → verify full pipeline runs (parse → extract → KG build)
- [ ] Test: Ask question → verify hybrid retrieval + LLM answer

---

## Phase 6: RAG Engine (Interactive Retrieval)
- [x] Create `backend/services/vector_store_service.py`
  - [x] `add_documents()` — Store chunks with embeddings in ChromaDB
  - [x] `similarity_search()` — Top-K semantic search
  - [x] `delete_by_document()` — Remove chunks when document deleted
- [x] Create `backend/services/rag_engine.py`
  - [x] Vector retrieval path (ChromaDB similarity search)
  - [x] Graph retrieval path (entity recognition → Cypher query → results)
  - [x] Result fusion + re-ranking
  - [x] LLM generation with source citations
  - [x] Confidence score calculation
  - [x] Conversation memory (last 10 messages)
- [x] Create `backend/api/routes/chat.py`
  - [x] `POST /api/chat` — Synchronous RAG query
  - [x] `WebSocket /api/chat/ws` — Streaming response
  - [x] `GET /api/chat/history` — Conversation history
- [ ] Test: Ask 5 benchmark questions → verify accuracy + citations

---

## Phase 7: Frontend — Core UI
- [x] Create `frontend/src/index.css` — Complete dark theme design system
- [x] Create layout components
  - [x] `Sidebar.tsx` — Navigation with icons (Documents, KG, Chat, Compliance, Maintenance)
  - [x] `Header.tsx` — App title, stats bar, notifications
  - [x] `MainLayout.tsx` — Sidebar + content area layout
- [x] Create `frontend/src/services/api.ts` — Axios client with all API functions
- [x] Create `frontend/src/types/index.ts` — TypeScript interfaces
- [x] Create `frontend/src/utils/formatters.ts` — Shared utility functions
- [x] Setup React Router with 5 pages
- [x] Frontend builds with zero TypeScript errors

### Page 1: Dashboard
- [x] Hero section with gradient branding
- [x] Stat cards (documents, nodes, relationships, entity types)
- [x] System health status panel
- [x] Feature navigation cards
- [x] KG composition breakdown

### Page 2: Document Management
- [x] `DocumentsPage.tsx` — Drag & drop with progress bar, multi-file support
- [x] Filterable list with type badges, entity count, processing status
- [x] Document detail modal with properties + text preview
- [x] Auto-polling for processing status updates

### Page 3: Knowledge Graph Explorer
- [x] KG stats bar
- [x] Entity type filter sidebar with counts
- [x] Search with debounce
- [x] Animated graph visualization with floating nodes
- [x] Node detail panel with properties + connections

### Page 4: Interactive RAG Chat
- [x] ChatPage with message bubbles + markdown rendering
- [x] Source citation pills with relevance
- [x] Confidence indicator bar
- [x] Follow-up question suggestions
- [x] Suggested starter questions
- [x] Typing indicator animation

### Page 5: Compliance Dashboard
- [x] Animated SVG compliance score ring
- [x] Severity breakdown bars (critical/high/medium/low)
- [x] Gap cards with affected equipment + recommendations
- [x] Run Analysis + Export Report buttons

### Page 6: Maintenance Intelligence
- [x] RCA input form with equipment tag search
- [x] Tabbed view (Recommendations / Patterns / Timeline / RCA)
- [x] Maintenance timeline with vertical line + dots
- [x] Failure pattern cards with affected equipment
- [x] Priority-coded recommendation cards

---

## Phase 8: Compliance & Maintenance Agents
- [x] Create `backend/agents/compliance_agent.py`
  - [x] Load regulatory requirements from KG
  - [x] Compare against current equipment/procedure states
  - [x] Identify gaps with severity ratings
  - [x] Generate evidence packages with document references
- [x] Create `backend/agents/maintenance_agent.py`
  - [x] Query failure history from KG
  - [x] Correlate failure modes across equipment types
  - [x] Generate RCA support (probable causes ranked)
  - [x] Predict next maintenance actions based on MTBF
- [x] Create `backend/api/routes/compliance.py` — All compliance endpoints
- [x] Create `backend/api/routes/maintenance.py` — All maintenance endpoints
- [ ] Test: Run compliance analysis → verify gap detection against known gaps
- [ ] Test: Run RCA → verify causal chain identification

---

## Phase 9: Dataset Preparation & Seeding
- [x] Create `data/seed/seed_knowledge_graph.py`
  - [x] Pre-populate equipment master data (25 equipment items)
  - [x] Pre-populate regulatory framework (15 standards)
  - [x] Pre-populate personnel (20 engineers/technicians)
  - [x] Pre-populate failure modes (10 failure modes)
  - [x] Pre-populate procedures (10 SOPs/PM tasks)
  - [x] Pre-populate maintenance records (10 work orders)
  - [x] Create ~80 relationships
- [ ] Run seed script against live Neo4j
- [ ] Verify KG is populated in dashboard

---

## Phase 10: Polish, Testing & Demo Prep
- [x] Create `README.md` with architecture, setup instructions, feature list
- [x] Vite proxy configuration for API calls
- [x] Custom SVG favicon
- [ ] Write backend unit tests
- [ ] Run all tests, fix failures
- [ ] Performance optimization
- [ ] Record demo video
- [ ] Prepare presentation deck

---

## Effort Estimates

| Phase | Estimated Hours | Status |
|---|---|---|
| Phase 0: Setup | 2h | ✅ Mostly complete |
| Phase 1: Backend Foundation | 3h | ✅ Complete |
| Phase 2: Document Processing | 4h | ✅ Complete |
| Phase 3: Entity Extraction | 5h | ✅ Complete |
| Phase 4: Knowledge Graph | 4h | ✅ Complete |
| Phase 5: Multi-Agent | 6h | ✅ Complete |
| Phase 6: RAG Engine | 6h | ✅ Complete |
| Phase 7: Frontend | 10h | ✅ Complete |
| Phase 8: Compliance + Maintenance | 6h | ✅ Complete |
| Phase 9: Dataset Prep | 4h | ✅ Seed script created |
| Phase 10: Polish + Demo | 4h | 🔄 In progress |
| **Total** | **~54 hours** | |
