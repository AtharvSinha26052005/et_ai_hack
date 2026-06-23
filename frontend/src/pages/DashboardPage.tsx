/* Dashboard Page — System overview with stats */

import { useState, useEffect } from 'react';
import {
  FileText,
  Network,
  MessageSquare,
  Shield,
  Wrench,
  TrendingUp,
  Database,
  Cpu,
  Zap,
  ArrowUpRight,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { getKGStats, checkHealth, listDocuments } from '../services/api';
import type { KGStats, HealthStatus } from '../types';
import './DashboardPage.css';

export default function DashboardPage() {
  const [stats, setStats] = useState<KGStats | null>(null);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [docCount, setDocCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [kgStats, healthData, docsData] = await Promise.allSettled([
          getKGStats(),
          checkHealth(),
          listDocuments(1, 1),
        ]);

        if (kgStats.status === 'fulfilled') setStats(kgStats.value);
        if (healthData.status === 'fulfilled') setHealth(healthData.value);
        if (docsData.status === 'fulfilled') setDocCount(docsData.value.total);
      } catch (e) {
        console.error('Dashboard fetch error:', e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const statCards = [
    {
      label: 'Documents Ingested',
      value: docCount,
      icon: FileText,
      color: 'blue',
      link: '/documents',
    },
    {
      label: 'Knowledge Graph Nodes',
      value: stats?.total_nodes || 0,
      icon: Network,
      color: 'emerald',
      link: '/knowledge-graph',
    },
    {
      label: 'Relationships',
      value: stats?.total_relationships || 0,
      icon: Zap,
      color: 'purple',
      link: '/knowledge-graph',
    },
    {
      label: 'Entity Types',
      value: Object.keys(stats?.nodes_by_type || {}).length,
      icon: Database,
      color: 'amber',
      link: '/knowledge-graph',
    },
  ];

  const features = [
    {
      title: 'Document Intelligence',
      description: 'Upload PDFs, manuals, work orders — AI extracts entities and builds knowledge.',
      icon: FileText,
      link: '/documents',
      color: '#3b82f6',
    },
    {
      title: 'Knowledge Graph Explorer',
      description: 'Interactive 3D visualization of your industrial knowledge network.',
      icon: Network,
      link: '/knowledge-graph',
      color: '#10b981',
    },
    {
      title: 'Interactive RAG Chat',
      description: 'Ask questions — get cited answers from your entire document corpus.',
      icon: MessageSquare,
      link: '/chat',
      color: '#8b5cf6',
    },
    {
      title: 'Compliance Analysis',
      description: 'Detect regulatory gaps and generate compliance evidence reports.',
      icon: Shield,
      link: '/compliance',
      color: '#f59e0b',
    },
    {
      title: 'Maintenance Intelligence',
      description: 'Root cause analysis, failure patterns, and predictive recommendations.',
      icon: Wrench,
      link: '/maintenance',
      color: '#ef4444',
    },
  ];

  if (loading) {
    return (
      <div className="dashboard">
        <div className="dashboard-hero">
          <div className="skeleton" style={{ width: '400px', height: '48px' }} />
          <div className="skeleton" style={{ width: '600px', height: '24px', marginTop: '16px' }} />
        </div>
        <div className="grid grid-cols-4 gap-lg">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="skeleton" style={{ height: '120px', borderRadius: '16px' }} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard animate-fade-in">
      {/* Hero Section */}
      <div className="dashboard-hero">
        <div className="hero-badge">
          <Cpu size={14} />
          <span>AI-Powered Industrial Knowledge Intelligence</span>
        </div>
        <h1 className="hero-title">
          Welcome to <span className="gradient-text">IntelliPlant</span>
        </h1>
        <p className="hero-subtitle">
          Unified Asset & Operations Brain — making industrial knowledge queryable,
          actionable, and continuously updated at the point of need.
        </p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-4 gap-lg">
        {statCards.map((card) => (
          <Link to={card.link} key={card.label} className={`glass-card stat-card ${card.color}`}>
            <div className="flex items-center justify-between">
              <card.icon size={20} style={{ color: 'var(--color-text-muted)' }} />
              <ArrowUpRight size={14} style={{ color: 'var(--color-text-muted)' }} />
            </div>
            <div className="stat-value">{card.value.toLocaleString()}</div>
            <div className="stat-label">{card.label}</div>
          </Link>
        ))}
      </div>

      {/* System Status */}
      <div className="dashboard-status glass-card">
        <h3>System Status</h3>
        <div className="status-grid">
          <div className="status-service">
            <span
              className={`status-dot ${
                health?.services?.neo4j?.status === 'connected'
                  ? 'status-dot-success'
                  : 'status-dot-error'
              }`}
            />
            <div>
              <div className="status-service-name">Neo4j Knowledge Graph</div>
              <div className="status-service-detail">
                {health?.services?.neo4j?.status || 'disconnected'}
              </div>
            </div>
          </div>
          <div className="status-service">
            <span
              className={`status-dot ${
                health?.services?.chromadb?.status === 'connected'
                  ? 'status-dot-success'
                  : 'status-dot-error'
              }`}
            />
            <div>
              <div className="status-service-name">ChromaDB Vector Store</div>
              <div className="status-service-detail">
                {health?.services?.chromadb?.document_count ?? 0} chunks stored
              </div>
            </div>
          </div>
          <div className="status-service">
            <span className="status-dot status-dot-success" />
            <div>
              <div className="status-service-name">SQLite Metadata</div>
              <div className="status-service-detail">connected</div>
            </div>
          </div>
          <div className="status-service">
            <span className="status-dot status-dot-info" />
            <div>
              <div className="status-service-name">Gemini 2.0 Flash LLM</div>
              <div className="status-service-detail">15 RPM free tier</div>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="features-section">
        <h2>Platform Capabilities</h2>
        <div className="features-grid">
          {features.map((feature) => (
            <Link to={feature.link} key={feature.title} className="feature-card glass-card">
              <div
                className="feature-icon"
                style={{ background: `${feature.color}15`, color: feature.color }}
              >
                <feature.icon size={24} />
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
              <div className="feature-arrow">
                <ArrowUpRight size={16} />
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* KG Node Type Breakdown */}
      {stats && Object.keys(stats.nodes_by_type).length > 0 && (
        <div className="glass-card kg-breakdown">
          <h3>Knowledge Graph Composition</h3>
          <div className="breakdown-grid">
            {Object.entries(stats.nodes_by_type).map(([type, count]) => (
              <div key={type} className="breakdown-item">
                <div className="breakdown-bar">
                  <div
                    className="breakdown-fill"
                    style={{
                      width: `${Math.min(100, (count / stats.total_nodes) * 100)}%`,
                    }}
                  />
                </div>
                <div className="breakdown-info">
                  <span className="breakdown-type">{type}</span>
                  <span className="breakdown-count">{count.toLocaleString()}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
