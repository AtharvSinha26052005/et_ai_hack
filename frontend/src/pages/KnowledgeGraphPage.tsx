/* Knowledge Graph Page — 3D Explorer */

import { useState, useEffect, useCallback, useRef } from 'react';
import {
  Search,
  Filter,
  Maximize2,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Info,
  X,
} from 'lucide-react';
import { getKGStats, getKGNodes, searchKG, getKGNodeDetail } from '../services/api';
import type { KGStats, KGNode, KGRelationship } from '../types';
import './KnowledgeGraphPage.css';

const NODE_COLORS: Record<string, string> = {
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

export default function KnowledgeGraphPage() {
  const [stats, setStats] = useState<KGStats | null>(null);
  const [nodes, setNodes] = useState<KGNode[]>([]);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [connectedNodes, setConnectedNodes] = useState<KGNode[]>([]);
  const [relationships, setRelationships] = useState<KGRelationship[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [activeFilter, setActiveFilter] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsData, nodesData] = await Promise.allSettled([
          getKGStats(),
          getKGNodes(undefined, 1, 100),
        ]);

        if (statsData.status === 'fulfilled') setStats(statsData.value);
        if (nodesData.status === 'fulfilled') setNodes(nodesData.value.nodes || []);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleSearch = useCallback(async () => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }
    try {
      const data = await searchKG(searchQuery, activeFilter || undefined, 20);
      setSearchResults(data.results || []);
    } catch (e) {
      console.error('Search failed:', e);
    }
  }, [searchQuery, activeFilter]);

  useEffect(() => {
    const timeout = setTimeout(handleSearch, 300);
    return () => clearTimeout(timeout);
  }, [searchQuery, handleSearch]);

  const handleNodeClick = async (node: KGNode) => {
    setDetailLoading(true);
    try {
      const detail = await getKGNodeDetail(node.id);
      setSelectedNode(detail.node);
      setConnectedNodes(detail.connected_nodes || []);
      setRelationships(detail.relationships || []);
    } catch (e) {
      setSelectedNode(node);
      setConnectedNodes([]);
      setRelationships([]);
    } finally {
      setDetailLoading(false);
    }
  };

  const nodeTypes = stats ? Object.keys(stats.nodes_by_type) : [];

  return (
    <div className="kg-page animate-fade-in">
      <div className="page-header">
        <div>
          <h1>Knowledge Graph Explorer</h1>
          <p>Explore your industrial knowledge network — entities, relationships, and connections.</p>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="kg-stats-bar">
        <div className="glass-card stat-card blue">
          <div className="stat-value">{stats?.total_nodes?.toLocaleString() || 0}</div>
          <div className="stat-label">Total Nodes</div>
        </div>
        <div className="glass-card stat-card emerald">
          <div className="stat-value">{stats?.total_relationships?.toLocaleString() || 0}</div>
          <div className="stat-label">Relationships</div>
        </div>
        <div className="glass-card stat-card purple">
          <div className="stat-value">{nodeTypes.length}</div>
          <div className="stat-label">Entity Types</div>
        </div>
        <div className="glass-card stat-card amber">
          <div className="stat-value">
            {stats ? Object.keys(stats.relationships_by_type).length : 0}
          </div>
          <div className="stat-label">Relationship Types</div>
        </div>
      </div>

      {/* Main Content */}
      <div className="kg-content">
        {/* Left Panel — Search & Filter */}
        <div className="kg-sidebar glass-card">
          <div className="kg-search">
            <Search size={14} />
            <input
              type="text"
              className="kg-search-input"
              placeholder="Search entities..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {/* Type Filter */}
          <div className="kg-filters">
            <span className="filter-title">Entity Types</span>
            <button
              className={`type-filter-btn ${!activeFilter ? 'active' : ''}`}
              onClick={() => setActiveFilter('')}
            >
              All
            </button>
            {nodeTypes.map((type) => (
              <button
                key={type}
                className={`type-filter-btn ${activeFilter === type ? 'active' : ''}`}
                onClick={() => setActiveFilter(type === activeFilter ? '' : type)}
                style={{
                  borderColor: activeFilter === type ? NODE_COLORS[type] : undefined,
                }}
              >
                <span
                  className="type-dot"
                  style={{ background: NODE_COLORS[type] || '#64748b' }}
                />
                {type}
                <span className="type-count">{stats?.nodes_by_type[type] || 0}</span>
              </button>
            ))}
          </div>

          {/* Search Results or Node List */}
          <div className="kg-node-list">
            {(searchResults.length > 0 ? searchResults.map(r => r.node) : nodes)
              .filter(n => !activeFilter || n.label === activeFilter)
              .slice(0, 50)
              .map((node) => (
                <div
                  key={node.id}
                  className={`kg-node-item ${selectedNode?.id === node.id ? 'selected' : ''}`}
                  onClick={() => handleNodeClick(node)}
                >
                  <span
                    className="type-dot"
                    style={{ background: NODE_COLORS[node.label] || '#64748b' }}
                  />
                  <div className="node-item-info">
                    <span className="node-item-name">
                      {node.properties.name || node.properties.tag || node.properties.title || node.properties.standard_id || node.id}
                    </span>
                    <span className="node-item-type">{node.label}</span>
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* Center — Graph Visualization Placeholder */}
        <div className="kg-graph-area glass-card">
          {loading ? (
            <div className="kg-graph-placeholder">
              <div className="spinner spinner-lg" />
              <p>Loading knowledge graph...</p>
            </div>
          ) : stats && stats.total_nodes > 0 ? (
            <div className="kg-graph-placeholder">
              <div className="graph-visual">
                {/* Animated nodes for visual effect */}
                {nodeTypes.slice(0, 8).map((type, i) => (
                  <div
                    key={type}
                    className="floating-node"
                    style={{
                      background: NODE_COLORS[type] || '#64748b',
                      left: `${15 + (i % 4) * 20}%`,
                      top: `${20 + Math.floor(i / 4) * 35}%`,
                      animationDelay: `${i * 0.3}s`,
                      width: `${Math.min(60, 20 + (stats.nodes_by_type[type] || 0) / 10)}px`,
                      height: `${Math.min(60, 20 + (stats.nodes_by_type[type] || 0) / 10)}px`,
                    }}
                  >
                    <span className="floating-label">{type}</span>
                  </div>
                ))}
                {/* Connection lines */}
                <svg className="connection-lines" viewBox="0 0 100 100">
                  {nodeTypes.slice(0, 7).map((_, i) => (
                    <line
                      key={i}
                      x1={`${15 + (i % 4) * 20}`}
                      y1={`${20 + Math.floor(i / 4) * 35}`}
                      x2={`${15 + ((i + 1) % 4) * 20}`}
                      y2={`${20 + Math.floor((i + 1) / 4) * 35}`}
                      stroke="rgba(59, 130, 246, 0.2)"
                      strokeWidth="0.3"
                    />
                  ))}
                </svg>
              </div>
              <div className="graph-info">
                <h3>{stats.total_nodes.toLocaleString()} nodes • {stats.total_relationships.toLocaleString()} relationships</h3>
                <p>Click a node in the sidebar to explore its connections</p>
              </div>
            </div>
          ) : (
            <div className="kg-graph-placeholder">
              <Info size={48} style={{ opacity: 0.3 }} />
              <h3>No data in knowledge graph</h3>
              <p>Upload documents to build your knowledge graph</p>
            </div>
          )}
        </div>

        {/* Right Panel — Node Detail */}
        {selectedNode && (
          <div className="kg-detail-panel glass-card animate-slide-right">
            <div className="detail-header">
              <h3>
                <span
                  className="type-dot"
                  style={{ background: NODE_COLORS[selectedNode.label] || '#64748b' }}
                />
                {selectedNode.label}
              </h3>
              <button className="btn btn-ghost btn-icon btn-sm" onClick={() => setSelectedNode(null)}>
                <X size={16} />
              </button>
            </div>

            <div className="detail-properties">
              <h4>Properties</h4>
              {Object.entries(selectedNode.properties || {}).map(([key, value]) => (
                <div key={key} className="property-item">
                  <span className="property-key">{key}</span>
                  <span className="property-value">{String(value)}</span>
                </div>
              ))}
            </div>

            {connectedNodes.length > 0 && (
              <div className="detail-connections">
                <h4>Connected Nodes ({connectedNodes.length})</h4>
                {connectedNodes.slice(0, 20).map((cn) => (
                  <div
                    key={cn.id}
                    className="connected-node-item"
                    onClick={() => handleNodeClick(cn)}
                  >
                    <span
                      className="type-dot"
                      style={{ background: NODE_COLORS[cn.label] || '#64748b' }}
                    />
                    <span>
                      {cn.properties.name || cn.properties.tag || cn.properties.title || cn.id}
                    </span>
                    <span className="connected-type">{cn.label}</span>
                  </div>
                ))}
              </div>
            )}

            {relationships.length > 0 && (
              <div className="detail-relationships">
                <h4>Relationships ({relationships.length})</h4>
                {relationships.slice(0, 20).map((rel, i) => (
                  <div key={i} className="relationship-item">
                    <span className="badge badge-blue">{rel.type}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
