/* Header component */

import { Bell, Search, Settings } from 'lucide-react';
import { useState, useEffect } from 'react';
import { checkHealth } from '../../services/api';
import type { HealthStatus } from '../../types';
import './Header.css';

export default function Header() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const data = await checkHealth();
        setHealth(data);
      } catch {
        setHealth(null);
      }
    };
    fetchHealth();
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="header">
      <div className="header-search">
        <Search size={16} className="search-icon" />
        <input
          type="text"
          className="search-input"
          placeholder="Search knowledge base..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <kbd className="search-shortcut">⌘K</kbd>
      </div>

      <div className="header-right">
        {/* Service Status */}
        <div className="service-status">
          <div className="status-item tooltip-container">
            <span
              className={`status-dot ${
                health?.services?.neo4j?.status === 'connected'
                  ? 'status-dot-success'
                  : 'status-dot-error'
              }`}
            />
            <span className="status-label">Neo4j</span>
            <span className="tooltip">
              {health?.services?.neo4j?.status || 'unknown'}
            </span>
          </div>
          <div className="status-item tooltip-container">
            <span
              className={`status-dot ${
                health?.services?.chromadb?.status === 'connected'
                  ? 'status-dot-success'
                  : 'status-dot-error'
              }`}
            />
            <span className="status-label">ChromaDB</span>
            <span className="tooltip">
              {health?.services?.chromadb?.status || 'unknown'}
            </span>
          </div>
        </div>

        <button className="btn btn-ghost btn-icon">
          <Bell size={18} />
        </button>
        <button className="btn btn-ghost btn-icon">
          <Settings size={18} />
        </button>
      </div>
    </header>
  );
}
