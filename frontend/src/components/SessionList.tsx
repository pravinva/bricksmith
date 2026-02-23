/**
 * Session list and management component.
 */

import { useState } from 'react';
import type { Session, MCPEnrichmentOptions } from '../types';
import { ContextSeeder } from './ContextSeeder';

interface SessionListProps {
  sessions: Session[];
  currentSessionId?: string;
  onSelectSession: (sessionId: string) => void;
  onDeleteSession: (sessionId: string) => void;
  onCreateSession: (
    problem: string,
    context?: string,
    authOptions?: {
      imageProvider?: 'gemini' | 'openai';
      openaiApiKey?: string;
      vertexApiKey?: string;
      referencePrompt?: string;
      referencePromptPath?: string;
      referenceImageBase64?: string;
      referenceImageFilename?: string;
      mcpEnrichment?: MCPEnrichmentOptions;
    }
  ) => void;
  isLoading: boolean;
}

export function SessionList({
  sessions,
  currentSessionId,
  onSelectSession,
  onDeleteSession,
  onCreateSession,
  isLoading,
}: SessionListProps) {
  const [showNewSession, setShowNewSession] = useState(false);
  const [newProblem, setNewProblem] = useState('');
  const [newContext, setNewContext] = useState('');
  const [imageProvider, setImageProvider] = useState<'gemini' | 'openai'>('gemini');
  const [customApiKey, setCustomApiKey] = useState('');
  const [referencePrompt, setReferencePrompt] = useState('');
  const [referencePromptPath, setReferencePromptPath] = useState('');
  const [referenceImageBase64, setReferenceImageBase64] = useState('');
  const [referenceImageFilename, setReferenceImageFilename] = useState('');
  const [mcpEnrichment, setMcpEnrichment] = useState<MCPEnrichmentOptions>({
    enabled: true,
    sources: ['glean', 'confluence'],
  });

  const handleCreateSession = () => {
    if (!newProblem.trim()) return;
    const key = customApiKey.trim() || undefined;
    onCreateSession(newProblem.trim(), newContext.trim() || undefined, {
      imageProvider,
      openaiApiKey: imageProvider === 'openai' ? key : undefined,
      vertexApiKey: imageProvider === 'gemini' ? key : undefined,
      referencePrompt: referencePrompt || undefined,
      referencePromptPath: referencePromptPath || undefined,
      referenceImageBase64: referenceImageBase64 || undefined,
      referenceImageFilename: referenceImageFilename || undefined,
      mcpEnrichment: mcpEnrichment.enabled ? mcpEnrichment : undefined,
    });
    setNewProblem('');
    setNewContext('');
    setCustomApiKey('');
    setImageProvider('gemini');
    setReferencePrompt('');
    setReferencePromptPath('');
    setReferenceImageBase64('');
    setReferenceImageFilename('');
    setMcpEnrichment({ enabled: true, sources: ['glean', 'confluence'] });
    setShowNewSession(false);
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b">
        <div className="flex items-center justify-between">
          <h2 className="font-semibold text-gray-900">Sessions</h2>
          <button
            onClick={() => setShowNewSession(true)}
            disabled={isLoading}
            className="px-3 py-1 text-sm bg-primary-600 text-white rounded hover:bg-primary-700 disabled:opacity-50"
          >
            + New
          </button>
        </div>
      </div>

      {/* New session form */}
      {showNewSession && (
        <div className="p-4 border-b bg-gray-50">
          <h3 className="font-medium text-gray-900 mb-2">New Session</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm text-gray-600 mb-1">
                Problem Description *
              </label>
              <textarea
                value={newProblem}
                onChange={(e) => setNewProblem(e.target.value)}
                placeholder="Describe your architecture problem..."
                rows={3}
                className="w-full px-3 py-2 text-sm border rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <ContextSeeder
              customContext={newContext}
              referencePrompt={referencePrompt}
              referencePromptPath={referencePromptPath}
              referenceImageBase64={referenceImageBase64}
              referenceImageFilename={referenceImageFilename}
              onReferenceImageChange={(b64, name) => {
                setReferenceImageBase64(b64);
                setReferenceImageFilename(name);
              }}
              mcpEnrichment={mcpEnrichment}
              onCustomContextChange={setNewContext}
              onReferencePromptChange={setReferencePrompt}
              onReferencePromptPathChange={setReferencePromptPath}
              onMCPEnrichmentChange={setMcpEnrichment}
            />
            <div>
              <label className="block text-sm text-gray-600 mb-1">
                Image Provider
              </label>
              <select
                value={imageProvider}
                onChange={(e) => setImageProvider(e.target.value as 'gemini' | 'openai')}
                className="w-full px-3 py-2 text-sm border rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="gemini">Gemini / Vertex</option>
                <option value="openai">OpenAI</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">
                {imageProvider === 'openai'
                  ? 'OpenAI API Key (optional)'
                  : 'Vertex/Gemini API Key (optional)'}
              </label>
              <input
                type="password"
                value={customApiKey}
                onChange={(e) => setCustomApiKey(e.target.value)}
                placeholder={imageProvider === 'openai' ? 'sk-...' : 'AIza...'}
                className="w-full px-3 py-2 text-sm border rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <p className="text-xs text-gray-500 mt-1">
                Used only for this session&apos;s preview generation when provided.
              </p>
            </div>
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => {
                  setShowNewSession(false);
                  setNewProblem('');
                  setNewContext('');
                  setCustomApiKey('');
                  setImageProvider('gemini');
                  setReferencePrompt('');
                  setReferencePromptPath('');
                  setReferenceImageBase64('');
                  setReferenceImageFilename('');
                  setMcpEnrichment({ enabled: true, sources: ['glean', 'confluence'] });
                }}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateSession}
                disabled={!newProblem.trim() || isLoading}
                className="px-3 py-1 text-sm bg-primary-600 text-white rounded hover:bg-primary-700 disabled:opacity-50"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Session list */}
      <div className="flex-1 overflow-y-auto">
        {sessions.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            <p>No sessions yet</p>
            <p className="text-sm mt-1">Create one to get started</p>
          </div>
        ) : (
          <ul className="divide-y">
            {sessions.map((session) => (
              <li
                key={session.session_id}
                className={`relative group ${
                  currentSessionId === session.session_id
                    ? 'bg-primary-50 border-l-2 border-primary-600'
                    : 'hover:bg-gray-50'
                }`}
              >
                <button
                  onClick={() => onSelectSession(session.session_id)}
                  className="w-full text-left p-4"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0 pr-8">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {session.initial_problem.slice(0, 50)}
                        {session.initial_problem.length > 50 ? '...' : ''}
                      </p>
                      <div className="flex items-center mt-1 space-x-2">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                            session.status === 'completed'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-blue-100 text-blue-800'
                          }`}
                        >
                          {session.status}
                        </span>
                        <span className="text-xs text-gray-500">
                          {session.turn_count} turns
                        </span>
                      </div>
                      <p className="text-xs text-gray-400 mt-1">
                        {formatDate(session.created_at)}
                      </p>
                    </div>
                  </div>
                </button>

                {/* Delete button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    if (confirm('Delete this session?')) {
                      onDeleteSession(session.session_id);
                    }
                  }}
                  className="absolute right-2 top-2 p-1 text-gray-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-opacity"
                  title="Delete session"
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
