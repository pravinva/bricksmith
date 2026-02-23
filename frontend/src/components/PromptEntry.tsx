/**
 * Home/entry screen for Bricksmith - shows two clear workflow paths:
 * 1. Design with Architect - creates an architect session
 * 2. Refine Directly - goes straight to the generate/evaluate/refine loop
 */

import { useState, useEffect } from 'react';
import { resultsApi } from '../api/client';
import type { Session, PromptFileItem, BestResultItem, MCPEnrichmentOptions } from '../types';

interface PromptEntryProps {
  onStartArchitect: (
    prompt: string,
    context?: string,
    authOptions?: {
      imageProvider?: 'gemini' | 'openai';
      openaiApiKey?: string;
      vertexApiKey?: string;
      referencePrompt?: string;
      referenceImageBase64?: string;
      referenceImageFilename?: string;
      mcpEnrichment?: MCPEnrichmentOptions;
    },
  ) => void;
  onStartRefinement: (
    prompt: string,
    imageProvider?: 'gemini' | 'openai',
    apiKey?: string,
  ) => void;
  isLoading: boolean;
  recentSessions?: Session[];
  onSelectSession?: (sessionId: string) => void;
}

type SourceTab = 'paste' | 'files' | 'results';

export function PromptEntry({
  onStartArchitect,
  onStartRefinement,
  isLoading,
  recentSessions,
  onSelectSession,
}: PromptEntryProps) {
  const [prompt, setPrompt] = useState('');
  const [sourceTab, setSourceTab] = useState<SourceTab>('paste');
  const [imageProvider, setImageProvider] = useState<'gemini' | 'openai'>('gemini');
  const [apiKey, setApiKey] = useState('');
  const [mcpEnabled, setMcpEnabled] = useState(true);
  const [refImageBase64, setRefImageBase64] = useState('');
  const [refImageFilename, setRefImageFilename] = useState('');

  // File browser state
  const [promptFiles, setPromptFiles] = useState<PromptFileItem[]>([]);
  const [filesLoading, setFilesLoading] = useState(false);
  const [fileQuery, setFileQuery] = useState('');

  // Results picker state
  const [bestResults, setBestResults] = useState<BestResultItem[]>([]);
  const [resultsLoading, setResultsLoading] = useState(false);
  const [resultQuery, setResultQuery] = useState('');

  const loadPromptFiles = async (query?: string) => {
    setFilesLoading(true);
    try {
      const resp = await resultsApi.listPromptFiles(query, 30);
      setPromptFiles(resp.files);
    } catch {
      // Silently fail - files list is supplementary
    } finally {
      setFilesLoading(false);
    }
  };

  const loadBestResults = async (query?: string) => {
    setResultsLoading(true);
    try {
      const resp = await resultsApi.listBest(20, query, undefined, true);
      setBestResults(resp.results);
    } catch {
      // Silently fail
    } finally {
      setResultsLoading(false);
    }
  };

  // Load data when switching to file/results tabs
  useEffect(() => {
    if (sourceTab === 'files' && promptFiles.length === 0) {
      void loadPromptFiles();
    }
    if (sourceTab === 'results' && bestResults.length === 0) {
      void loadBestResults();
    }
  }, [sourceTab]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSelectFile = (file: PromptFileItem) => {
    setPrompt(file.preview);
    setSourceTab('paste');
    // Load full content
    void fetch(`/api/results/prompt-files?limit=1&query=${encodeURIComponent(file.relative_path)}`)
      .then(r => r.json())
      .then((data: { files: PromptFileItem[] }) => {
        if (data.files?.[0]?.preview) {
          setPrompt(data.files[0].preview);
        }
      });
  };

  const handleSelectResult = (result: BestResultItem) => {
    setPrompt(result.full_prompt || result.prompt_preview);
    setSourceTab('paste');
  };

  const handleStartArchitect = () => {
    if (!prompt.trim()) return;
    onStartArchitect(
      prompt.trim(),
      undefined,
      {
        referencePrompt: prompt.trim(),
        referenceImageBase64: refImageBase64 || undefined,
        referenceImageFilename: refImageFilename || undefined,
        mcpEnrichment: { enabled: mcpEnabled, sources: ['glean', 'confluence'] },
      },
    );
  };

  const handleStartRefinement = () => {
    if (!prompt.trim()) return;
    onStartRefinement(prompt.trim(), imageProvider, apiKey || undefined);
  };

  const hasPrompt = prompt.trim().length > 0;

  return (
    <div className="max-w-4xl mx-auto py-12 px-6">
      {/* Hero */}
      <div className="text-center mb-10">
        <div className="flex items-center justify-center gap-3 mb-4">
          <img
            src="/logo-mascot.png"
            alt="Bricksmith"
            className="w-14 h-14 rounded-xl object-cover border border-gray-200 bg-white"
          />
          <h1 className="text-3xl font-bold text-gray-900">Bricksmith</h1>
        </div>
        <p className="text-lg text-gray-600">
          How would you like to create your diagram?
        </p>
      </div>

      {/* Prompt input card */}
      <div className="bg-white rounded-xl border shadow-sm p-6 mb-6">
        {/* Source tabs */}
        <div className="flex gap-1 mb-4 bg-gray-100 rounded-lg p-1 w-fit">
          {([
            { key: 'paste' as const, label: 'Paste prompt' },
            { key: 'files' as const, label: 'Browse files' },
            { key: 'results' as const, label: 'Pick from results' },
          ]).map(tab => (
            <button
              key={tab.key}
              onClick={() => setSourceTab(tab.key)}
              className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                sourceTab === tab.key
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Paste tab */}
        {sourceTab === 'paste' && (
          <textarea
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            placeholder="Paste or type your architecture diagram prompt here...&#10;&#10;Example: Create a diagram showing Unity Catalog governance for a data lakehouse with three environments (dev, staging, prod) connected through Delta Sharing..."
            className="w-full h-48 border rounded-lg px-4 py-3 text-sm resize-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        )}

        {/* Files tab */}
        {sourceTab === 'files' && (
          <div className="border rounded-lg">
            <div className="p-3 border-b">
              <input
                value={fileQuery}
                onChange={e => setFileQuery(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && loadPromptFiles(fileQuery || undefined)}
                placeholder="Search prompt files..."
                className="w-full border rounded px-3 py-2 text-sm"
              />
            </div>
            <div className="max-h-56 overflow-y-auto">
              {filesLoading ? (
                <p className="p-4 text-sm text-gray-500">Loading...</p>
              ) : promptFiles.length === 0 ? (
                <p className="p-4 text-sm text-gray-500">No prompt files found.</p>
              ) : (
                <ul className="divide-y">
                  {promptFiles.map(file => (
                    <li
                      key={file.path}
                      onClick={() => handleSelectFile(file)}
                      className="px-4 py-3 hover:bg-gray-50 cursor-pointer"
                    >
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {file.relative_path}
                      </p>
                      <p className="text-xs text-gray-500 line-clamp-2 mt-0.5">
                        {file.preview}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}

        {/* Results tab */}
        {sourceTab === 'results' && (
          <div className="border rounded-lg">
            <div className="p-3 border-b">
              <input
                value={resultQuery}
                onChange={e => setResultQuery(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && loadBestResults(resultQuery || undefined)}
                placeholder="Search best results..."
                className="w-full border rounded px-3 py-2 text-sm"
              />
            </div>
            <div className="max-h-56 overflow-y-auto">
              {resultsLoading ? (
                <p className="p-4 text-sm text-gray-500">Loading...</p>
              ) : bestResults.length === 0 ? (
                <p className="p-4 text-sm text-gray-500">No results found.</p>
              ) : (
                <ul className="divide-y">
                  {bestResults.map(result => (
                    <li
                      key={result.result_id}
                      onClick={() => handleSelectResult(result)}
                      className="px-4 py-3 hover:bg-gray-50 cursor-pointer flex gap-3"
                    >
                      {result.image_url && (
                        <img
                          src={result.image_url}
                          alt=""
                          className="w-10 h-10 rounded object-cover flex-shrink-0"
                        />
                      )}
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center justify-between gap-2">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {result.title}
                          </p>
                          {result.score !== undefined && (
                            <span className="text-xs px-1.5 py-0.5 rounded bg-green-100 text-green-700 flex-shrink-0">
                              {result.score}
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-gray-500 line-clamp-1 mt-0.5">
                          {result.prompt_preview}
                        </p>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}

        {/* Settings row */}
        <div className="flex flex-wrap items-center gap-4 mt-4 pt-4 border-t">
          <div className="flex items-center gap-2">
            <label className="text-xs text-gray-600">Image provider</label>
            <select
              value={imageProvider}
              onChange={e => setImageProvider(e.target.value as 'gemini' | 'openai')}
              className="border rounded px-2 py-1 text-sm"
            >
              <option value="gemini">Gemini</option>
              <option value="openai">OpenAI</option>
            </select>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-xs text-gray-600">API key (optional)</label>
            <input
              type="password"
              value={apiKey}
              onChange={e => setApiKey(e.target.value)}
              placeholder="Uses env default"
              className="border rounded px-2 py-1 text-sm w-44"
            />
          </div>
          <div className="flex items-center gap-2 ml-auto">
            <label className="text-xs text-gray-600">MCP enrichment</label>
            <input
              type="checkbox"
              checked={mcpEnabled}
              onChange={e => setMcpEnabled(e.target.checked)}
              className="rounded"
            />
          </div>
        </div>

        {/* Reference image drop zone */}
        <div className="mt-4 pt-4 border-t">
          <label className="block text-xs text-gray-600 mb-2">Reference diagram (optional)</label>
          {!refImageBase64 ? (
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                const file = e.dataTransfer.files[0];
                if (!file) return;
                const validTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/webp'];
                if (!validTypes.includes(file.type)) return;
                if (file.size > 10 * 1024 * 1024) return;
                const reader = new FileReader();
                reader.onload = () => {
                  const dataUrl = reader.result as string;
                  const base64 = dataUrl.replace(/^data:[^;]+;base64,/, '');
                  setRefImageBase64(base64);
                  setRefImageFilename(file.name);
                };
                reader.readAsDataURL(file);
              }}
              onClick={() => {
                const input = document.createElement('input');
                input.type = 'file';
                input.accept = 'image/png,image/jpeg,image/gif,image/webp';
                input.onchange = () => {
                  const file = input.files?.[0];
                  if (!file || file.size > 10 * 1024 * 1024) return;
                  const reader = new FileReader();
                  reader.onload = () => {
                    const dataUrl = reader.result as string;
                    const base64 = dataUrl.replace(/^data:[^;]+;base64,/, '');
                    setRefImageBase64(base64);
                    setRefImageFilename(file.name);
                  };
                  reader.readAsDataURL(file);
                };
                input.click();
              }}
              className="flex items-center gap-2 px-3 py-2 rounded border-2 border-dashed border-gray-300 hover:border-gray-400 cursor-pointer"
            >
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span className="text-xs text-gray-500">Drop or click to add a reference architecture image</span>
            </div>
          ) : (
            <div className="flex items-center gap-3 bg-gray-50 px-3 py-2 rounded border">
              <img
                src={`data:image/png;base64,${refImageBase64}`}
                alt="Reference"
                className="w-10 h-10 object-cover rounded"
              />
              <span className="text-xs text-gray-700 truncate flex-1">{refImageFilename}</span>
              <button
                onClick={() => { setRefImageBase64(''); setRefImageFilename(''); }}
                className="text-xs text-gray-500 hover:text-red-600"
              >
                Clear
              </button>
            </div>
          )}
        </div>

        {/* Action buttons */}
        <div className="flex gap-3 mt-6">
          <button
            onClick={handleStartArchitect}
            disabled={!hasPrompt || isLoading}
            className="flex-1 px-6 py-3 bg-white border-2 border-primary-600 text-primary-700 rounded-lg font-medium hover:bg-primary-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <div className="flex flex-col items-center gap-1">
              <span>Design with architect</span>
              <span className="text-xs font-normal text-gray-500">
                Chat to refine your architecture first
              </span>
            </div>
          </button>
          <button
            onClick={handleStartRefinement}
            disabled={!hasPrompt || isLoading}
            className="flex-1 px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <div className="flex flex-col items-center gap-1">
              <span>{isLoading ? 'Starting...' : 'Refine directly'}</span>
              <span className="text-xs font-normal text-primary-200">
                Generate, evaluate, and iterate on your prompt
              </span>
            </div>
          </button>
        </div>
      </div>

      {/* Recent sessions */}
      {recentSessions && recentSessions.length > 0 && onSelectSession && (
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-3">Recent sessions</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {recentSessions.slice(0, 6).map(session => (
              <button
                key={session.session_id}
                onClick={() => onSelectSession(session.session_id)}
                className="text-left bg-white border rounded-lg p-4 hover:border-primary-400 hover:bg-primary-50 transition-colors"
              >
                <p className="text-sm font-medium text-gray-900 line-clamp-2">
                  {session.initial_problem}
                </p>
                <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
                  <span className="font-mono">{session.session_id}</span>
                  <span>{session.turn_count} turns</span>
                  <span
                    className={`px-1.5 py-0.5 rounded ${
                      session.status === 'active'
                        ? 'bg-green-100 text-green-700'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {session.status}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
