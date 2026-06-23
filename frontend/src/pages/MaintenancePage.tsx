/* Maintenance Intelligence Page */

import { useState, useEffect } from 'react';
import {
  Wrench,
  AlertTriangle,
  Activity,
  Clock,
  TrendingUp,
  Search,
  RefreshCw,
  ChevronRight,
} from 'lucide-react';
import {
  getMaintenanceRecommendations,
  getFailurePatterns,
  getMaintenanceTimeline,
  runRCA,
} from '../services/api';
import type { MaintenanceRecommendation, FailureMode, MaintenanceTimeline } from '../types';
import './MaintenancePage.css';

export default function MaintenancePage() {
  const [recommendations, setRecommendations] = useState<MaintenanceRecommendation[]>([]);
  const [patterns, setPatterns] = useState<FailureMode[]>([]);
  const [timeline, setTimeline] = useState<MaintenanceTimeline[]>([]);
  const [selectedEquipment, setSelectedEquipment] = useState('');
  const [rcaResult, setRcaResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [rcaLoading, setRcaLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'recommendations' | 'patterns' | 'timeline' | 'rca'>('recommendations');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [recData, patData] = await Promise.allSettled([
        getMaintenanceRecommendations(),
        getFailurePatterns(),
      ]);

      if (recData.status === 'fulfilled') setRecommendations(recData.value.recommendations || []);
      if (patData.status === 'fulfilled') setPatterns(patData.value.patterns || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleRunRCA = async () => {
    if (!selectedEquipment.trim()) return;
    setRcaLoading(true);
    try {
      const data = await runRCA(selectedEquipment);
      setRcaResult(data);
      setActiveTab('rca');
    } catch (e) {
      console.error(e);
    } finally {
      setRcaLoading(false);
    }
  };

  const handleViewTimeline = async (tag: string) => {
    try {
      const data = await getMaintenanceTimeline(tag);
      setTimeline(data.timeline || []);
      setSelectedEquipment(tag);
      setActiveTab('timeline');
    } catch (e) {
      console.error(e);
    }
  };

  const getPriorityColor = (priority: string) => {
    if (priority === 'high' || priority === 'critical') return 'red';
    if (priority === 'medium') return 'amber';
    return 'blue';
  };

  return (
    <div className="maintenance-page animate-fade-in">
      <div className="page-header">
        <div>
          <h1>Maintenance Intelligence</h1>
          <p>Root cause analysis, failure pattern detection, and predictive maintenance recommendations.</p>
        </div>
        <button className="btn btn-secondary btn-sm" onClick={fetchData}>
          <RefreshCw size={14} />
          Refresh
        </button>
      </div>

      {/* RCA Input */}
      <div className="glass-card rca-input-section">
        <h3>Root Cause Analysis</h3>
        <p>Enter an equipment tag to analyze failure history and root causes.</p>
        <div className="rca-form">
          <input
            type="text"
            className="input"
            placeholder="Equipment tag (e.g., P-101A, HX-201)"
            value={selectedEquipment}
            onChange={(e) => setSelectedEquipment(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleRunRCA()}
          />
          <button
            className="btn btn-primary"
            onClick={handleRunRCA}
            disabled={rcaLoading || !selectedEquipment.trim()}
          >
            {rcaLoading ? <RefreshCw size={14} className="spinning" /> : <Search size={14} />}
            Run RCA
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="maint-tabs">
        <button
          className={`tab-btn ${activeTab === 'recommendations' ? 'active' : ''}`}
          onClick={() => setActiveTab('recommendations')}
        >
          <TrendingUp size={14} />
          Recommendations ({recommendations.length})
        </button>
        <button
          className={`tab-btn ${activeTab === 'patterns' ? 'active' : ''}`}
          onClick={() => setActiveTab('patterns')}
        >
          <Activity size={14} />
          Failure Patterns ({patterns.length})
        </button>
        <button
          className={`tab-btn ${activeTab === 'timeline' ? 'active' : ''}`}
          onClick={() => setActiveTab('timeline')}
        >
          <Clock size={14} />
          Timeline ({timeline.length})
        </button>
        {rcaResult && (
          <button
            className={`tab-btn ${activeTab === 'rca' ? 'active' : ''}`}
            onClick={() => setActiveTab('rca')}
          >
            <Wrench size={14} />
            RCA Results
          </button>
        )}
      </div>

      {/* Tab Content */}
      <div className="tab-content animate-fade-in">
        {activeTab === 'recommendations' && (
          <div className="recommendations-list">
            {loading ? (
              [1, 2, 3].map(i => (
                <div key={i} className="skeleton" style={{ height: '100px', borderRadius: '12px' }} />
              ))
            ) : recommendations.length > 0 ? (
              recommendations.map((rec, i) => (
                <div key={i} className="recommendation-card glass-card">
                  <div className="rec-header">
                    <div className="rec-equipment">
                      <Wrench size={16} />
                      <span className="mono">{rec.equipment_tag}</span>
                      <span className="rec-name">{rec.equipment_name}</span>
                    </div>
                    <span className={`badge badge-${getPriorityColor(rec.priority)}`}>
                      {rec.priority} priority
                    </span>
                  </div>
                  <p className="rec-text">{rec.recommendation}</p>
                  <div className="rec-footer">
                    {rec.equipment_type && (
                      <span className="badge badge-blue">{rec.equipment_type}</span>
                    )}
                    {rec.last_maintenance && (
                      <span className="rec-last">Last: {rec.last_maintenance}</span>
                    )}
                    <button
                      className="btn btn-ghost btn-sm"
                      onClick={() => handleViewTimeline(rec.equipment_tag)}
                    >
                      View Timeline <ChevronRight size={12} />
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="empty-state">
                <TrendingUp size={48} />
                <h3>No recommendations yet</h3>
                <p>Upload maintenance records to generate predictive recommendations</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'patterns' && (
          <div className="patterns-list">
            {patterns.length > 0 ? (
              patterns.map((pattern, i) => (
                <div key={i} className="pattern-card glass-card">
                  <div className="pattern-header">
                    <div>
                      <span className="mono pattern-code">{pattern.failure_code}</span>
                      <h4>{pattern.description}</h4>
                    </div>
                    <span className={`badge badge-${pattern.severity === 'critical' ? 'red' : pattern.severity === 'high' ? 'amber' : 'blue'}`}>
                      {pattern.severity}
                    </span>
                  </div>
                  {pattern.affected_equipment && pattern.affected_equipment.length > 0 && (
                    <div className="pattern-equipment">
                      <span className="pattern-label">Affected Equipment:</span>
                      {pattern.affected_equipment.map((eq, j) => (
                        <span
                          key={j}
                          className="badge badge-purple"
                          style={{ cursor: 'pointer' }}
                          onClick={() => handleViewTimeline(eq)}
                        >
                          {eq}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))
            ) : (
              <div className="empty-state">
                <Activity size={48} />
                <h3>No failure patterns detected</h3>
                <p>Failure patterns emerge when multiple equipment share common failure modes</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="timeline-section">
            <h3 className="timeline-title">
              Maintenance Timeline — <span className="mono">{selectedEquipment}</span>
            </h3>
            {timeline.length > 0 ? (
              <div className="timeline-list">
                {timeline.map((item, i) => (
                  <div key={i} className="timeline-item">
                    <div className="timeline-dot" />
                    <div className="timeline-content glass-card">
                      <div className="timeline-header">
                        <span className="mono">{item.work_order_id}</span>
                        <span className="badge badge-blue">{item.type}</span>
                        <span className="timeline-date">{item.date}</span>
                      </div>
                      <p>{item.description}</p>
                      {item.personnel.length > 0 && (
                        <div className="timeline-detail">
                          Personnel: {item.personnel.join(', ')}
                        </div>
                      )}
                      {item.failure_modes.length > 0 && (
                        <div className="timeline-detail">
                          Failure: {item.failure_modes.join(', ')}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <Clock size={48} />
                <h3>No timeline data</h3>
                <p>Select equipment or enter a tag to view maintenance history</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'rca' && rcaResult && (
          <div className="rca-results">
            <h3>RCA Results — <span className="mono">{rcaResult.equipment_tag}</span></h3>
            <div className="rca-stats">
              <span className="badge badge-blue">
                {rcaResult.total_failure_modes} failure modes found
              </span>
              <span className="rca-time">
                {rcaResult.processing_time_seconds?.toFixed(2)}s
              </span>
            </div>
            {rcaResult.failure_modes?.map((fm: any, i: number) => (
              <div key={i} className="rca-item glass-card">
                <div className="rca-item-header">
                  <span className="mono">{fm.failure_code}</span>
                  <span className={`badge badge-${fm.severity === 'critical' ? 'red' : 'amber'}`}>
                    {fm.severity}
                  </span>
                </div>
                <p>{fm.description}</p>
                {fm.mitigation_procedures?.length > 0 && (
                  <div className="rca-mitigations">
                    <strong>Mitigations:</strong> {fm.mitigation_procedures.join(', ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
