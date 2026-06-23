/* Chat Page — Interactive RAG Interface */

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import {
  Send,
  Bot,
  User,
  FileText,
  Sparkles,
  Clock,
  ThumbsUp,
  ThumbsDown,
  RotateCcw,
} from 'lucide-react';
import { sendChatMessage } from '../services/api';
import type { ChatMessage, SourceCitation } from '../types';
import './ChatPage.css';

const SUGGESTED_QUESTIONS = [
  "What is the recommended maintenance interval for centrifugal pumps?",
  "Which equipment items are governed by OISD standards?",
  "Show me all failure modes for heat exchangers",
  "Are our safety procedures compliant with Factory Act?",
  "Which equipment has overdue maintenance?",
];

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (query?: string) => {
    const q = query || input.trim();
    if (!q || loading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: q,
      created_at: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await sendChatMessage({
        query: q,
        session_id: sessionId || undefined,
        include_graph_context: true,
      });

      if (!sessionId) setSessionId(response.session_id);

      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        confidence: response.confidence,
        graph_context: response.graph_context || undefined,
        follow_up_questions: response.follow_up_questions,
        created_at: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMsg]);
    } catch (e: any) {
      const errMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Sorry, I encountered an error: ${e.message || 'Unknown error'}. Please ensure the backend is running.`,
        created_at: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const getConfidenceColor = (conf: number) => {
    if (conf >= 0.7) return 'emerald';
    if (conf >= 0.4) return 'amber';
    return 'red';
  };

  return (
    <div className="chat-page animate-fade-in">
      <div className="chat-container">
        {/* Chat Header */}
        <div className="chat-header">
          <div className="flex items-center gap-md">
            <div className="chat-avatar bot">
              <Bot size={20} />
            </div>
            <div>
              <h2>IntelliPlant AI Assistant</h2>
              <p className="chat-subtitle">
                Ask questions about your industrial documents, equipment, and regulations
              </p>
            </div>
          </div>
          {messages.length > 0 && (
            <button
              className="btn btn-ghost btn-sm"
              onClick={() => {
                setMessages([]);
                setSessionId('');
              }}
            >
              <RotateCcw size={14} />
              New Chat
            </button>
          )}
        </div>

        {/* Messages */}
        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="chat-empty">
              <div className="chat-empty-icon">
                <Sparkles size={48} />
              </div>
              <h3>Ask me anything about your knowledge base</h3>
              <p>I'll search your documents, knowledge graph, and regulations to find answers.</p>

              <div className="suggested-questions">
                <span className="suggested-label">Try asking:</span>
                {SUGGESTED_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    className="suggested-btn"
                    onClick={() => handleSend(q)}
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`chat-message ${msg.role} animate-fade-in`}
              >
                <div className="message-avatar">
                  {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                </div>
                <div className="message-body">
                  <div className="message-content">
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>

                  {/* Source Citations */}
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="message-sources">
                      <span className="sources-label">
                        <FileText size={12} />
                        Sources ({msg.sources.length})
                      </span>
                      <div className="source-pills">
                        {msg.sources.map((src, i) => (
                          <div key={i} className="source-pill tooltip-container">
                            <FileText size={12} />
                            <span>{src.document_title}</span>
                            {src.page_number && (
                              <span className="source-page">p.{src.page_number}</span>
                            )}
                            <span className="tooltip">{src.chunk_text}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Confidence */}
                  {msg.confidence !== undefined && msg.role === 'assistant' && (
                    <div className="message-confidence">
                      <div className="confidence-bar">
                        <div
                          className={`confidence-fill ${getConfidenceColor(msg.confidence)}`}
                          style={{ width: `${msg.confidence * 100}%` }}
                        />
                      </div>
                      <span className="confidence-label">
                        {(msg.confidence * 100).toFixed(0)}% confidence
                      </span>
                    </div>
                  )}

                  {/* Follow-up Questions */}
                  {msg.follow_up_questions && msg.follow_up_questions.length > 0 && (
                    <div className="follow-ups">
                      {msg.follow_up_questions.map((q, i) => (
                        <button
                          key={i}
                          className="follow-up-btn"
                          onClick={() => handleSend(q)}
                        >
                          {q}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}

          {loading && (
            <div className="chat-message assistant animate-fade-in">
              <div className="message-avatar">
                <Bot size={16} />
              </div>
              <div className="message-body">
                <div className="typing-indicator">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="chat-input-area">
          <div className="chat-input-wrapper">
            <textarea
              ref={inputRef}
              className="chat-input"
              placeholder="Ask about equipment, procedures, regulations..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
              disabled={loading}
            />
            <button
              className="btn btn-primary chat-send-btn"
              onClick={() => handleSend()}
              disabled={!input.trim() || loading}
            >
              <Send size={16} />
            </button>
          </div>
          <div className="chat-input-hints">
            <span>Press Enter to send, Shift+Enter for new line</span>
          </div>
        </div>
      </div>
    </div>
  );
}
