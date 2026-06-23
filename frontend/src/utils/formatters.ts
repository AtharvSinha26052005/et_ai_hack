/* Utility formatters for the frontend */

/**
 * Format file size in human-readable form.
 */
export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
}

/**
 * Format a date string into a readable form.
 */
export function formatDate(dateStr: string): string {
  if (!dateStr) return '—';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * Format a relative time (e.g., "5 minutes ago").
 */
export function formatRelativeTime(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHr = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHr / 24);

  if (diffSec < 60) return 'just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  if (diffHr < 24) return `${diffHr}h ago`;
  if (diffDay < 7) return `${diffDay}d ago`;
  return formatDate(dateStr);
}

/**
 * Truncate text with ellipsis.
 */
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '…';
}

/**
 * Format a number with commas.
 */
export function formatNumber(num: number): string {
  return num.toLocaleString('en-IN');
}

/**
 * Convert document type enum to display label.
 */
export function docTypeLabel(docType: string): string {
  const labels: Record<string, string> = {
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
  return labels[docType] || docType;
}

/**
 * Get color for a node type in the knowledge graph.
 */
export function getNodeColor(label: string): string {
  const colors: Record<string, string> = {
    Equipment: '#3b82f6',
    Document: '#10b981',
    Regulation: '#ef4444',
    Procedure: '#8b5cf6',
    Personnel: '#f59e0b',
    MaintenanceRecord: '#06b6d4',
    FailureMode: '#f97316',
    InspectionFinding: '#ec4899',
    ProcessParameter: '#6366f1',
  };
  return colors[label] || '#64748b';
}
