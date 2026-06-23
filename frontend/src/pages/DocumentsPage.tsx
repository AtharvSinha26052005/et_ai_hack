/* Documents Page — Upload, manage, and view documents */

import { useState, useEffect, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Upload,
  FileText,
  Trash2,
  Eye,
  RefreshCw,
  Filter,
  Check,
  X,
  AlertCircle,
  Loader,
  ChevronDown,
} from 'lucide-react';
import { listDocuments, uploadDocument, deleteDocument } from '../services/api';
import type { Document as DocType, DocumentStatus, DocumentType } from '../types';
import './DocumentsPage.css';

const DOC_TYPE_LABELS: Record<string, string> = {
  equipment_manual: 'Equipment Manual',
  maintenance_record: 'Maintenance Record',
  inspection_report: 'Inspection Report',
  safety_procedure: 'Safety Procedure',
  regulatory: 'Regulatory',
  pid_drawing: 'P&ID Drawing',
  work_order: 'Work Order',
  sop: 'SOP',
  incident_report: 'Incident Report',
  other: 'Other',
};

const STATUS_CONFIG: Record<DocumentStatus, { color: string; icon: any; label: string }> = {
  uploaded: { color: 'blue', icon: Upload, label: 'Uploaded' },
  processing: { color: 'amber', icon: Loader, label: 'Processing' },
  processed: { color: 'emerald', icon: Check, label: 'Processed' },
  failed: { color: 'red', icon: X, label: 'Failed' },
};

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<DocType[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<string[]>([]);
  const [filterType, setFilterType] = useState<string>('');
  const [filterStatus, setFilterStatus] = useState<string>('');
  const [selectedDoc, setSelectedDoc] = useState<DocType | null>(null);

  const fetchDocuments = useCallback(async () => {
    try {
      const data = await listDocuments(1, 50, filterType || undefined, filterStatus || undefined);
      setDocuments(data.documents);
      setTotal(data.total);
    } catch (e) {
      console.error('Failed to fetch documents:', e);
    } finally {
      setLoading(false);
    }
  }, [filterType, filterStatus]);

  useEffect(() => {
    fetchDocuments();
    // Poll for processing status updates
    const interval = setInterval(fetchDocuments, 5000);
    return () => clearInterval(interval);
  }, [fetchDocuments]);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setUploading(true);
    setUploadProgress([]);

    for (const file of acceptedFiles) {
      try {
        setUploadProgress(prev => [...prev, `Uploading ${file.name}...`]);
        await uploadDocument(file);
        setUploadProgress(prev => [...prev, `✓ ${file.name} uploaded`]);
      } catch (e) {
        setUploadProgress(prev => [...prev, `✗ ${file.name} failed`]);
      }
    }

    setUploading(false);
    fetchDocuments();
  }, [fetchDocuments]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
      'text/plain': ['.txt'],
      'image/*': ['.png', '.jpg', '.jpeg', '.tiff', '.bmp'],
    },
  });

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this document?')) return;
    try {
      await deleteDocument(id);
      fetchDocuments();
    } catch (e) {
      console.error('Delete failed:', e);
    }
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="documents-page animate-fade-in">
      <div className="page-header">
        <div>
          <h1>Document Management</h1>
          <p>Upload, process, and manage industrial documents. AI extracts entities and builds knowledge automatically.</p>
        </div>
        <div className="flex items-center gap-md">
          <span className="badge badge-blue">{total} documents</span>
          <button className="btn btn-secondary btn-sm" onClick={fetchDocuments}>
            <RefreshCw size={14} />
            Refresh
          </button>
        </div>
      </div>

      {/* Upload Zone */}
      <div
        {...getRootProps()}
        className={`upload-zone glass-card ${isDragActive ? 'drag-active' : ''} ${uploading ? 'uploading' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="upload-content">
          <div className="upload-icon-circle">
            <Upload size={28} />
          </div>
          {isDragActive ? (
            <div className="upload-text">
              <h3>Drop files here</h3>
              <p>Release to upload</p>
            </div>
          ) : (
            <div className="upload-text">
              <h3>Drag & drop documents</h3>
              <p>or click to browse — PDF, DOCX, Excel, Images supported</p>
            </div>
          )}
        </div>

        {uploadProgress.length > 0 && (
          <div className="upload-progress">
            {uploadProgress.map((msg, i) => (
              <div key={i} className="upload-progress-item">{msg}</div>
            ))}
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="filters-bar">
        <div className="filter-group">
          <Filter size={14} />
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="filter-select"
          >
            <option value="">All Types</option>
            {Object.entries(DOC_TYPE_LABELS).map(([val, label]) => (
              <option key={val} value={val}>{label}</option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="filter-select"
          >
            <option value="">All Statuses</option>
            <option value="processed">Processed</option>
            <option value="processing">Processing</option>
            <option value="uploaded">Uploaded</option>
            <option value="failed">Failed</option>
          </select>
        </div>
      </div>

      {/* Document List */}
      {loading ? (
        <div className="flex flex-col gap-md">
          {[1, 2, 3].map(i => (
            <div key={i} className="skeleton" style={{ height: '80px', borderRadius: '12px' }} />
          ))}
        </div>
      ) : documents.length === 0 ? (
        <div className="empty-state">
          <FileText size={64} />
          <h3>No documents yet</h3>
          <p>Upload your first document to get started</p>
        </div>
      ) : (
        <div className="document-list">
          {documents.map((doc) => {
            const statusConfig = STATUS_CONFIG[doc.status];
            const StatusIcon = statusConfig.icon;

            return (
              <div key={doc.id} className="document-item glass-card">
                <div className="doc-icon">
                  <FileText size={20} />
                </div>
                <div className="doc-info">
                  <div className="doc-name">{doc.original_filename}</div>
                  <div className="doc-meta">
                    <span className={`badge badge-${statusConfig.color}`}>
                      <StatusIcon size={12} className={doc.status === 'processing' ? 'spinning' : ''} />
                      {statusConfig.label}
                    </span>
                    <span className="badge badge-blue">
                      {DOC_TYPE_LABELS[doc.doc_type] || doc.doc_type}
                    </span>
                    <span className="doc-size">{formatSize(doc.file_size)}</span>
                    {doc.page_count > 0 && (
                      <span className="doc-size">{doc.page_count} pages</span>
                    )}
                    {doc.entity_count > 0 && (
                      <span className="doc-size">{doc.entity_count} entities</span>
                    )}
                    {doc.chunk_count > 0 && (
                      <span className="doc-size">{doc.chunk_count} chunks</span>
                    )}
                  </div>
                  {doc.text_preview && (
                    <div className="doc-preview">{doc.text_preview}</div>
                  )}
                </div>
                <div className="doc-actions">
                  <button
                    className="btn btn-ghost btn-icon btn-sm"
                    onClick={() => setSelectedDoc(doc)}
                    title="View details"
                  >
                    <Eye size={16} />
                  </button>
                  <button
                    className="btn btn-ghost btn-icon btn-sm"
                    onClick={() => handleDelete(doc.id)}
                    title="Delete"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Document Detail Modal */}
      {selectedDoc && (
        <div className="modal-overlay" onClick={() => setSelectedDoc(null)}>
          <div className="modal-content glass-card" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{selectedDoc.original_filename}</h2>
              <button className="btn btn-ghost btn-icon" onClick={() => setSelectedDoc(null)}>
                <X size={20} />
              </button>
            </div>
            <div className="modal-body">
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="detail-label">Status</span>
                  <span className={`badge badge-${STATUS_CONFIG[selectedDoc.status].color}`}>
                    {STATUS_CONFIG[selectedDoc.status].label}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Type</span>
                  <span>{DOC_TYPE_LABELS[selectedDoc.doc_type] || selectedDoc.doc_type}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">File Size</span>
                  <span>{formatSize(selectedDoc.file_size)}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Pages</span>
                  <span>{selectedDoc.page_count}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Chunks</span>
                  <span>{selectedDoc.chunk_count}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Entities</span>
                  <span>{selectedDoc.entity_count}</span>
                </div>
                {selectedDoc.processing_time_seconds && (
                  <div className="detail-item">
                    <span className="detail-label">Processing Time</span>
                    <span>{selectedDoc.processing_time_seconds.toFixed(1)}s</span>
                  </div>
                )}
              </div>
              {selectedDoc.text_preview && (
                <div className="detail-preview">
                  <h4>Text Preview</h4>
                  <pre>{selectedDoc.text_preview}</pre>
                </div>
              )}
              {selectedDoc.error_message && (
                <div className="detail-error">
                  <AlertCircle size={16} />
                  <span>{selectedDoc.error_message}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
