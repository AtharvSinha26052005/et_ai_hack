/* TypeScript interfaces for IntelliPlant frontend */

// ============================================================
// Document Types
// ============================================================

export type DocumentStatus = 'uploaded' | 'processing' | 'processed' | 'failed';

export type DocumentType =
  | 'equipment_manual'
  | 'maintenance_record'
  | 'inspection_report'
  | 'safety_procedure'
  | 'regulatory'
  | 'pid_drawing'
  | 'work_order'
  | 'sop'
  | 'incident_report'
  | 'other';

export interface Document {
  id: string;
  filename: string;
  original_filename: string;
  file_size: number;
  mime_type?: string;
  doc_type: DocumentType;
  status: DocumentStatus;
  page_count: number;
  chunk_count: number;
  entity_count: number;
  text_preview?: string;
  processing_time_seconds?: number;
  error_message?: string;
  created_at?: string;
  updated_at?: string;
}

export interface DocumentListResponse {
  documents: Document[];
  total: number;
  page: number;
  page_size: number;
}

export interface DocumentUploadResponse {
  id: string;
  filename: string;
  status: DocumentStatus;
  message: string;
}

// ============================================================
// Knowledge Graph Types
// ============================================================

export interface KGNode {
  id: string;
  label: string;
  properties: Record<string, any>;
}

export interface KGRelationship {
  id: string;
  type: string;
  source_id: string;
  target_id: string;
  properties: Record<string, any>;
}

export interface KGStats {
  total_nodes: number;
  total_relationships: number;
  nodes_by_type: Record<string, number>;
  relationships_by_type: Record<string, number>;
}

export interface KGSubgraph {
  nodes: KGNode[];
  relationships: KGRelationship[];
  center_node_id?: string;
}

export interface KGSearchResult {
  node: KGNode;
  score: number;
  matched_field?: string;
}

// ============================================================
// Chat Types
// ============================================================

export interface SourceCitation {
  document_id: string;
  document_title: string;
  page_number?: number;
  chunk_text: string;
  relevance_score: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceCitation[];
  confidence?: number;
  graph_context?: KGSubgraph;
  follow_up_questions?: string[];
  created_at: string;
}

export interface ChatRequest {
  query: string;
  session_id?: string;
  include_graph_context?: boolean;
  max_sources?: number;
}

export interface ChatResponse {
  answer: string;
  sources: SourceCitation[];
  confidence: number;
  session_id: string;
  graph_context?: KGSubgraph;
  follow_up_questions: string[];
  processing_time_seconds: number;
}

// ============================================================
// Compliance Types
// ============================================================

export type GapSeverity = 'critical' | 'high' | 'medium' | 'low' | 'info';

export interface ComplianceGap {
  id: string;
  regulation_id: string;
  regulation_title: string;
  requirement: string;
  gap_description: string;
  severity: GapSeverity;
  affected_equipment: string[];
  evidence: string[];
  recommendation: string;
}

export interface ComplianceAnalysis {
  total_gaps: number;
  gaps_by_severity: Record<string, number>;
  gaps: ComplianceGap[];
  compliance_score: number;
  analysis_timestamp: string;
  processing_time_seconds: number;
}

export interface RegulationSummary {
  standard_id: string;
  title: string;
  body?: string;
  version?: string;
  status?: string;
  equipment_count: number;
  gap_count: number;
}

// ============================================================
// Maintenance Types
// ============================================================

export interface FailureMode {
  failure_code: string;
  description: string;
  severity: string;
  frequency: number;
  mtbf?: number;
  work_orders?: string[];
  mitigation_procedures?: string[];
  affected_equipment?: string[];
}

export interface MaintenanceRecommendation {
  equipment_tag: string;
  equipment_name: string;
  equipment_type: string;
  last_maintenance?: string;
  last_maintenance_type?: string;
  failure_modes: any[];
  priority: string;
  recommendation: string;
}

export interface MaintenanceTimeline {
  work_order_id: string;
  type: string;
  date: string;
  status: string;
  description: string;
  personnel: string[];
  failure_modes: string[];
  referenced_documents: string[];
}

// ============================================================
// Health Types
// ============================================================

export interface HealthStatus {
  status: string;
  services: {
    neo4j: { status: string; label_count?: number };
    chromadb: { status: string; document_count?: number };
    sqlite: { status: string };
  };
  version: string;
  app: string;
}

// ============================================================
// Graph Visualization Types
// ============================================================

export interface GraphNode {
  id: string;
  name: string;
  type: string;
  color: string;
  val: number;
  properties: Record<string, any>;
}

export interface GraphLink {
  source: string;
  target: string;
  type: string;
  color: string;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}
