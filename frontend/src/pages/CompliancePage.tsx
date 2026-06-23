/* Compliance Page — Gap analysis dashboard */

import { useState, useEffect } from 'react';
import {
  Shield,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Info,
  RefreshCw,
  Download,
  TrendingUp,
} from 'lucide-react';
import { analyzeCompliance, getRegulations } from '../services/api';
import type { ComplianceAnalysis, ComplianceGap, RegulationSummary } from '../types';
import './CompliancePage.css';

const SEVERITY_CONFIG: Record<string, { color: string; icon: any; bg: string }> = {
  critical: { color: '#ef4444', icon: XCircle, bg: 'rgba(239, 68, 68, 0.1)' },
  high: { color: '#f97316', icon: AlertTriangle, bg: 'rgba(249, 115, 22, 0.1)' },
  medium: { color: '#f59e0b', icon: AlertTriangle, bg: 'rgba(245, 158, 11, 0.1)' },
  low: { color: '#3b82f6', icon: Info, bg: 'rgba(59, 130, 246, 0.1)' },
  info: { color: '#6b7280', icon: Info, bg: 'rgba(107, 114, 128, 0.1)' },
};

export default function CompliancePage() {
  const [analysis, setAnalysis] = useState<ComplianceAnalysis | null>(null);
  const [regulations, setRegulations] = useState<RegulationSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [compData, regData] = await Promise.allSettled([
        analyzeCompliance(),
        getRegulations(),
      ]);

      if (compData.status === 'fulfilled') setAnalysis(compData.value);
      if (regData.status === 'fulfilled') setRegulations(regData.value.regulations || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const runAnalysis = async () => {
    setAnalyzing(true);
    try {
      const data = await analyzeCompliance();
      setAnalysis(data);
    } catch (e) {
      console.error(e);
    } finally {
      setAnalyzing(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'emerald';
    if (score >= 50) return 'amber';
    return 'red';
  };

  if (loading) {
    return (
      <div className="compliance-page">
        <div className="page-header">
          <div className="skeleton" style={{ width: '300px', height: '36px' }} />
        </div>
        <div className="grid grid-cols-3 gap-lg">
          {[1, 2, 3].map(i => (
            <div key={i} className="skeleton" style={{ height: '120px', borderRadius: '16px' }} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="compliance-page animate-fade-in">
      <div className="page-header">
        <div>
          <h1>Compliance Dashboard</h1>
          <p>Monitor regulatory compliance, identify gaps, and generate evidence reports.</p>
        </div>
        <div className="flex items-center gap-md">
          <button className="btn btn-secondary btn-sm" onClick={runAnalysis} disabled={analyzing}>
            <RefreshCw size={14} className={analyzing ? 'spinning' : ''} />
            Run Analysis
          </button>
          <button className="btn btn-primary btn-sm">
            <Download size={14} />
            Export Report
          </button>
        </div>
      </div>

      {/* Score + Stats */}
      <div className="compliance-overview">
        <div className="glass-card compliance-score-card">
          <div className="score-ring">
            <svg viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="50" fill="none" stroke="var(--color-bg-tertiary)" strokeWidth="10" />
              <circle
                cx="60" cy="60" r="50" fill="none"
                stroke={`var(--color-accent-${getScoreColor(analysis?.compliance_score || 0)})`}
                strokeWidth="10"
                strokeLinecap="round"
                strokeDasharray={`${(analysis?.compliance_score || 0) * 3.14} 314`}
                transform="rotate(-90 60 60)"
                style={{ transition: 'stroke-dasharray 1s ease-out' }}
              />
            </svg>
            <div className="score-value">
              {(analysis?.compliance_score || 0).toFixed(0)}%
            </div>
          </div>
          <div className="score-label">Compliance Score</div>
        </div>

        <div className="glass-card stat-card red">
          <div className="stat-value">{analysis?.total_gaps || 0}</div>
          <div className="stat-label">Total Gaps Identified</div>
        </div>

        <div className="glass-card stat-card amber">
          <div className="stat-value">{regulations.length}</div>
          <div className="stat-label">Regulations Tracked</div>
        </div>

        <div className="glass-card stat-card emerald">
          <div className="stat-value">
            {regulations.filter(r => r.gap_count === 0).length}
          </div>
          <div className="stat-label">Fully Compliant</div>
        </div>
      </div>

      {/* Severity Breakdown */}
      {analysis && analysis.total_gaps > 0 && (
        <div className="glass-card severity-breakdown">
          <h3>Gaps by Severity</h3>
          <div className="severity-bars">
            {Object.entries(analysis.gaps_by_severity || {}).map(([severity, count]) => {
              const config = SEVERITY_CONFIG[severity] || SEVERITY_CONFIG.info;
              const Icon = config.icon;
              return (
                <div key={severity} className="severity-row">
                  <div className="severity-label">
                    <Icon size={14} style={{ color: config.color }} />
                    <span style={{ color: config.color, textTransform: 'capitalize' }}>{severity}</span>
                  </div>
                  <div className="severity-bar-track">
                    <div
                      className="severity-bar-fill"
                      style={{
                        width: `${Math.min(100, (Number(count) / analysis.total_gaps) * 100)}%`,
                        background: config.color,
                      }}
                    />
                  </div>
                  <span className="severity-count">{String(count)}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Gap List */}
      <div className="gaps-section">
        <h2>Compliance Gaps</h2>
        {analysis && analysis.gaps.length > 0 ? (
          <div className="gaps-list">
            {analysis.gaps.map((gap) => {
              const config = SEVERITY_CONFIG[gap.severity] || SEVERITY_CONFIG.info;
              const Icon = config.icon;

              return (
                <div key={gap.id} className="gap-card glass-card">
                  <div className="gap-header">
                    <div className="gap-severity" style={{ background: config.bg }}>
                      <Icon size={16} style={{ color: config.color }} />
                      <span style={{ color: config.color, textTransform: 'capitalize' }}>
                        {gap.severity}
                      </span>
                    </div>
                    <span className="badge badge-blue">{gap.regulation_id}</span>
                  </div>

                  <h4>{gap.regulation_title}</h4>
                  <p className="gap-description">{gap.gap_description}</p>

                  {gap.affected_equipment.length > 0 && (
                    <div className="gap-equipment">
                      <span className="gap-label">Affected Equipment:</span>
                      {gap.affected_equipment.map((eq, i) => (
                        <span key={i} className="badge badge-amber">{eq}</span>
                      ))}
                    </div>
                  )}

                  {gap.recommendation && (
                    <div className="gap-recommendation">
                      <CheckCircle2 size={14} />
                      <span>{gap.recommendation}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ) : (
          <div className="empty-state">
            <Shield size={48} />
            <h3>No compliance gaps detected</h3>
            <p>Upload regulatory documents and run analysis to check compliance</p>
          </div>
        )}
      </div>
    </div>
  );
}
