/* API client for IntelliPlant backend */

import axios from 'axios';
import type {
  DocumentListResponse,
  DocumentUploadResponse,
  Document,
  ChatRequest,
  ChatResponse,
  KGStats,
  KGSubgraph,
  KGSearchResult,
  KGNode,
  ComplianceAnalysis,
  HealthStatus,
  MaintenanceRecommendation,
  MaintenanceTimeline,
  FailureMode,
} from '../types';

const API_BASE = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================================
// Health
// ============================================================

export const checkHealth = () =>
  api.get<HealthStatus>('/api/health').then(r => r.data);

// ============================================================
// Documents
// ============================================================

export const uploadDocument = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api
    .post<DocumentUploadResponse>('/api/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then(r => r.data);
};

export const batchUploadDocuments = (files: File[]) => {
  const formData = new FormData();
  files.forEach(f => formData.append('files', f));
  return api
    .post<DocumentUploadResponse[]>('/api/documents/batch-upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then(r => r.data);
};

export const listDocuments = (page = 1, pageSize = 20, docType?: string, status?: string) => {
  const params: Record<string, any> = { page, page_size: pageSize };
  if (docType) params.doc_type = docType;
  if (status) params.status = status;
  return api.get<DocumentListResponse>('/api/documents', { params }).then(r => r.data);
};

export const getDocument = (id: string) =>
  api.get<Document>(`/api/documents/${id}`).then(r => r.data);

export const deleteDocument = (id: string) =>
  api.delete(`/api/documents/${id}`).then(r => r.data);

export const getDocumentEntities = (id: string) =>
  api.get(`/api/documents/${id}/entities`).then(r => r.data);

// ============================================================
// Knowledge Graph
// ============================================================

export const getKGStats = () =>
  api.get<KGStats>('/api/kg/stats').then(r => r.data);

export const getKGNodes = (label?: string, page = 1, pageSize = 20) => {
  const params: Record<string, any> = { page, page_size: pageSize };
  if (label) params.label = label;
  return api.get('/api/kg/nodes', { params }).then(r => r.data);
};

export const getKGNodeDetail = (nodeId: string) =>
  api.get(`/api/kg/nodes/${encodeURIComponent(nodeId)}`).then(r => r.data);

export const searchKG = (query: string, nodeTypes?: string, limit = 20) => {
  const params: Record<string, any> = { q: query, limit };
  if (nodeTypes) params.node_types = nodeTypes;
  return api.get<{ results: KGSearchResult[]; total: number }>('/api/kg/search', { params }).then(r => r.data);
};

export const getKGSubgraph = (nodeId: string, depth = 2, limit = 100) =>
  api.get<KGSubgraph>('/api/kg/subgraph', {
    params: { node_id: nodeId, depth, limit },
  }).then(r => r.data);

// ============================================================
// Chat / RAG
// ============================================================

export const sendChatMessage = (request: ChatRequest) =>
  api.post<ChatResponse>('/api/chat', request).then(r => r.data);

export const getChatHistory = (sessionId: string) =>
  api.get(`/api/chat/history`, { params: { session_id: sessionId } }).then(r => r.data);

export const submitFeedback = (messageId: string, rating: number, comment?: string) =>
  api.post('/api/chat/feedback', { message_id: messageId, rating, comment }).then(r => r.data);

// WebSocket for streaming chat
export const createChatWebSocket = (onMessage: (data: any) => void) => {
  const ws = new WebSocket(`ws://localhost:8000/api/chat/ws`);

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (e) {
      console.error('WebSocket parse error:', e);
    }
  };

  return ws;
};

// ============================================================
// Compliance
// ============================================================

export const analyzeCompliance = (regulationId?: string, equipmentTags?: string[]) =>
  api
    .post<ComplianceAnalysis>('/api/compliance/analyze', {
      regulation_id: regulationId,
      equipment_tags: equipmentTags,
    })
    .then(r => r.data);

export const getComplianceGaps = () =>
  api.get<ComplianceAnalysis>('/api/compliance/gaps').then(r => r.data);

export const getRegulations = () =>
  api.get('/api/compliance/regulations').then(r => r.data);

export const getComplianceReport = () =>
  api.get('/api/compliance/report').then(r => r.data);

// ============================================================
// Maintenance
// ============================================================

export const runRCA = (equipmentTag?: string) =>
  api.post('/api/maintenance/rca', null, { params: { equipment_tag: equipmentTag } }).then(r => r.data);

export const getMaintenanceRecommendations = () =>
  api.get<{ recommendations: MaintenanceRecommendation[]; total: number }>(
    '/api/maintenance/recommendations'
  ).then(r => r.data);

export const getMaintenanceTimeline = (equipmentTag: string) =>
  api.get<{ equipment: any; timeline: MaintenanceTimeline[]; total_records: number }>(
    `/api/maintenance/timeline/${equipmentTag}`
  ).then(r => r.data);

export const getFailurePatterns = () =>
  api.get<{ patterns: FailureMode[]; total: number }>(
    '/api/maintenance/failure-patterns'
  ).then(r => r.data);

export default api;
