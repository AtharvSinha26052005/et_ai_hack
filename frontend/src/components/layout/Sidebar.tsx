/* Sidebar component — Navigation with icons */

import { NavLink, useLocation } from 'react-router-dom';
import {
  FileText,
  Network,
  MessageSquare,
  Shield,
  Wrench,
  Activity,
  ChevronLeft,
  ChevronRight,
  Brain,
} from 'lucide-react';
import { useState } from 'react';
import './Sidebar.css';

const navItems = [
  { path: '/', icon: Activity, label: 'Dashboard', description: 'System overview' },
  { path: '/documents', icon: FileText, label: 'Documents', description: 'Upload & manage' },
  { path: '/knowledge-graph', icon: Network, label: 'Knowledge Graph', description: '3D graph explorer' },
  { path: '/chat', icon: MessageSquare, label: 'Chat', description: 'Interactive RAG' },
  { path: '/compliance', icon: Shield, label: 'Compliance', description: 'Gap analysis' },
  { path: '/maintenance', icon: Wrench, label: 'Maintenance', description: 'Intelligence' },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <div className="logo-icon">
            <Brain size={24} />
          </div>
          {!collapsed && (
            <div className="logo-text">
              <span className="logo-title">IntelliPlant</span>
              <span className="logo-subtitle">Knowledge Intelligence</span>
            </div>
          )}
        </div>
        <button
          className="sidebar-toggle"
          onClick={() => setCollapsed(!collapsed)}
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      <nav className="sidebar-nav">
        {navItems.map(item => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `nav-item ${isActive ? 'active' : ''}`
            }
            end={item.path === '/'}
          >
            <item.icon size={20} className="nav-icon" />
            {!collapsed && (
              <div className="nav-text">
                <span className="nav-label">{item.label}</span>
                <span className="nav-description">{item.description}</span>
              </div>
            )}
            {collapsed && (
              <span className="nav-tooltip">{item.label}</span>
            )}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        {!collapsed && (
          <div className="version-info">
            <span className="status-dot status-dot-success" />
            <span>v1.0.0 — AI Hackathon 2026</span>
          </div>
        )}
      </div>
    </aside>
  );
}
