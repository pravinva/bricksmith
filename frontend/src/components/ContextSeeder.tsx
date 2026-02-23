/**
 * Context seeding component for architect session creation.
 *
 * Provides four collapsible sections:
 * 1. Seed from prompt file
 * 2. Seed from previous result
 * 3. MCP enrichment toggle
 * 4. Additional context textarea with file drop
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { resultsApi } from '../api/client';
import type { PromptFileItem, BestResultItem } from '../types';

interface ContextSeederProps {
  customContext: string;
  referencePrompt: string;
  referencePromptPath: string;
  referenceImageBase64: string;
  referenceImageFilename: string;
  onReferenceImageChange: (base64: string, filename: string) => void;
  mcpEnrichment: { enabled: boolean; sources: string[] };
  onCustomContextChange: (value: string) => void;
  onReferencePromptChange: (value: string) => void;
  onReferencePromptPathChange: (path: string) => void;
  onMCPEnrichmentChange: (options: { enabled: boolean; sources: string[] }) => void;
}

const MCP_SOURCES = [
  { id: 'glean', label: 'Glean' },
  { id: 'confluence', label: 'Confluence' },
  { id: 'slack', label: 'Slack' },
  { id: 'jira', label: 'JIRA' },
];

function ChevronIcon({ open }: { open: boolean }) {
  return (
    <svg
      className={`w-4 h-4 transition-transform ${open ? 'rotate-90' : ''}`}
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
    </svg>
  );
}

export function ContextSeeder({
  customContext,
  referencePrompt,
  referencePromptPath,
  referenceImageBase64,
  referenceImageFilename,
  onReferenceImageChange,
  mcpEnrichment,
  onCustomContextChange,
  onReferencePromptChange,
  onReferencePromptPathChange,
  onMCPEnrichmentChange,
}: ContextSeederProps) {
  // Section open state
  const [fromDocOpen, setFromDocOpen] = useState(false);
  const [refImageOpen, setRefImageOpen] = useState(false);
  const [promptFileOpen, setPromptFileOpen] = useState(false);
  const [prevResultOpen, setPrevResultOpen] = useState(false);
  const [mcpOpen, setMcpOpen] = useState(false);

  // Reference image drop state
  const [refImageDragOver, setRefImageDragOver] = useState(false);

  // Generate-from-document state
  const [docText, setDocText] = useState('');
  const [docFilename, setDocFilename] = useState('');
  const [isGeneratingFromDoc, setIsGeneratingFromDoc] = useState(false);
  const [fromDocError, setFromDocError] = useState('');
  const [fromDocGenerated, setFromDocGenerated] = useState(false);
  const [docIsDragOver, setDocIsDragOver] = useState(false);

  // Prompt file search/list
  const [promptFileQuery, setPromptFileQuery] = useState('');
  const [promptFiles, setPromptFiles] = useState<PromptFileItem[]>([]);
  const [promptFilesLoading, setPromptFilesLoading] = useState(false);

  // Previous results
  const [resultQuery, setResultQuery] = useState('');
  const [prevResults, setPrevResults] = useState<BestResultItem[]>([]);
  const [prevResultsLoading, setPrevResultsLoading] = useState(false);

  // File drop
  const [isDragOver, setIsDragOver] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Load prompt files when section opens
  useEffect(() => {
    if (!promptFileOpen) return;
    setPromptFilesLoading(true);
    resultsApi
      .listPromptFiles(promptFileQuery || undefined, 50)
      .then((res) => setPromptFiles(res.files))
      .catch(() => setPromptFiles([]))
      .finally(() => setPromptFilesLoading(false));
  }, [promptFileOpen, promptFileQuery]);

  // Load previous results when section opens
  useEffect(() => {
    if (!prevResultOpen) return;
    setPrevResultsLoading(true);
    resultsApi
      .listBest(10, resultQuery || undefined, undefined, true)
      .then((res) => setPrevResults(res.results))
      .catch(() => setPrevResults([]))
      .finally(() => setPrevResultsLoading(false));
  }, [prevResultOpen, resultQuery]);

  // File drop handlers
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);

      const files = Array.from(e.dataTransfer.files);
      for (const file of files) {
        if (file.name.endsWith('.txt') || file.name.endsWith('.md')) {
          const reader = new FileReader();
          reader.onload = () => {
            const text = reader.result as string;
            const separator = customContext ? '\n\n---\n\n' : '';
            onCustomContextChange(customContext + separator + `[${file.name}]\n${text}`);
          };
          reader.readAsText(file);
        }
      }
    },
    [customContext, onCustomContextChange]
  );

  const handleSelectPromptFile = (file: PromptFileItem) => {
    onReferencePromptPathChange(file.path);
    onReferencePromptChange(''); // Path takes priority; clear text
  };

  const handleClearPromptFile = () => {
    onReferencePromptPathChange('');
    onReferencePromptChange('');
  };

  const handleSelectResult = (result: BestResultItem) => {
    const prompt = result.full_prompt || result.prompt_preview || '';
    onReferencePromptChange(prompt);
    onReferencePromptPathChange(''); // Text takes priority; clear path

    // Append metadata to context
    const meta = [
      `Source: ${result.source}`,
      result.score !== undefined ? `Score: ${result.score}` : null,
      result.run_id ? `Run: ${result.run_id}` : null,
    ]
      .filter(Boolean)
      .join(' | ');
    const separator = customContext ? '\n\n' : '';
    onCustomContextChange(customContext + separator + `[Seeded from: ${result.title}] ${meta}`);
  };

  const handleClearResult = () => {
    onReferencePromptChange('');
  };

  const toggleMcpSource = (sourceId: string) => {
    const current = mcpEnrichment.sources;
    const next = current.includes(sourceId)
      ? current.filter((s) => s !== sourceId)
      : [...current, sourceId];
    onMCPEnrichmentChange({ ...mcpEnrichment, sources: next });
  };

  // Generate-from-document handlers
  const handleDocDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDocIsDragOver(true);
  }, []);

  const handleDocDragLeave = useCallback(() => {
    setDocIsDragOver(false);
  }, []);

  const handleDocDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDocIsDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    for (const file of files) {
      if (file.name.endsWith('.txt') || file.name.endsWith('.md')) {
        const reader = new FileReader();
        reader.onload = () => {
          setDocText(reader.result as string);
          setDocFilename(file.name);
          setFromDocGenerated(false);
          setFromDocError('');
        };
        reader.readAsText(file);
        break;
      }
    }
  }, []);

  const handleGenerateFromDoc = useCallback(async () => {
    if (!docText.trim()) return;
    setIsGeneratingFromDoc(true);
    setFromDocError('');
    setFromDocGenerated(false);
    try {
      const result = await resultsApi.generateFromDoc({
        document_text: docText,
        filename: docFilename || undefined,
      });
      onReferencePromptChange(result.prompt);
      onReferencePromptPathChange('');
      setFromDocGenerated(true);
    } catch (err) {
      setFromDocError(err instanceof Error ? err.message : 'Generation failed');
    } finally {
      setIsGeneratingFromDoc(false);
    }
  }, [docText, docFilename, onReferencePromptChange, onReferencePromptPathChange]);

  const hasSelectedPromptFile = !!referencePromptPath;
  const hasSelectedResult = !!referencePrompt && !referencePromptPath;

  return (
    <div className="space-y-2">
      {/* Section 0: Generate prompt from architecture document */}
      <div className="border rounded border-primary-200">
        <button
          type="button"
          onClick={() => setFromDocOpen(!fromDocOpen)}
          className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-primary-50"
        >
          <ChevronIcon open={fromDocOpen} />
          <span className="font-medium">Generate prompt from document</span>
          {fromDocGenerated && (
            <span className="ml-auto text-xs text-green-600 font-medium">✓ Generated</span>
          )}
          {!fromDocGenerated && docText && (
            <span className="ml-auto text-xs text-primary-600 font-medium">Doc loaded</span>
          )}
        </button>
        {fromDocOpen && (
          <div className="px-3 pb-3 space-y-2">
            <p className="text-xs text-gray-500">
              Drop an architecture doc (.md or .txt) — Gemini will turn it into a diagram prompt.
            </p>

            {/* Drop zone / textarea */}
            <div
              onDragOver={handleDocDragOver}
              onDragLeave={handleDocDragLeave}
              onDrop={handleDocDrop}
              className={`relative rounded border ${
                docIsDragOver
                  ? 'border-dashed border-primary-400 ring-2 ring-primary-200'
                  : 'border-gray-300'
              }`}
            >
              <textarea
                value={docText}
                onChange={(e) => {
                  setDocText(e.target.value);
                  setFromDocGenerated(false);
                  setFromDocError('');
                  if (!e.target.value) setDocFilename('');
                }}
                placeholder="Drop an architecture .md or .txt file here, or paste the document text…"
                rows={5}
                className="w-full px-3 py-2 text-xs border-0 rounded focus:outline-none focus:ring-0 resize-none"
              />
              {docIsDragOver && (
                <div className="absolute inset-0 flex items-center justify-center bg-primary-50/90 rounded pointer-events-none">
                  <span className="text-sm text-primary-700 font-medium">
                    Drop .md or .txt file here
                  </span>
                </div>
              )}
            </div>

            {docFilename && (
              <p className="text-xs text-gray-500 truncate">
                File: <span className="font-mono text-gray-700">{docFilename}</span>
              </p>
            )}

            {fromDocError && (
              <p className="text-xs text-red-600">{fromDocError}</p>
            )}

            {fromDocGenerated && (
              <p className="text-xs text-green-700 font-medium">
                ✓ Prompt generated — it's now set as the reference prompt below.
              </p>
            )}

            <div className="flex justify-end">
              <button
                type="button"
                onClick={handleGenerateFromDoc}
                disabled={!docText.trim() || isGeneratingFromDoc}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-primary-600 text-white rounded hover:bg-primary-700 disabled:opacity-50"
              >
                {isGeneratingFromDoc ? (
                  <>
                    <svg className="w-3 h-3 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                    </svg>
                    Generating…
                  </>
                ) : (
                  'Generate prompt'
                )}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Section: Analyze reference diagram */}
      <div className="border rounded border-primary-200">
        <button
          type="button"
          onClick={() => setRefImageOpen(!refImageOpen)}
          className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-primary-50"
        >
          <ChevronIcon open={refImageOpen} />
          <span className="font-medium">Analyze reference diagram</span>
          {referenceImageBase64 && (
            <span className="ml-auto text-xs text-green-600 font-medium">Image loaded</span>
          )}
        </button>
        {refImageOpen && (
          <div className="px-3 pb-3 space-y-2">
            <p className="text-xs text-gray-500">
              Drop a whiteboard photo, Visio export, or draw.io screenshot to analyze as starting context.
            </p>
            {!referenceImageBase64 ? (
              <div
                onDragOver={(e) => { e.preventDefault(); setRefImageDragOver(true); }}
                onDragLeave={() => setRefImageDragOver(false)}
                onDrop={(e) => {
                  e.preventDefault();
                  setRefImageDragOver(false);
                  const file = e.dataTransfer.files[0];
                  if (!file) return;
                  const validTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/webp'];
                  if (!validTypes.includes(file.type)) return;
                  if (file.size > 10 * 1024 * 1024) return; // 10MB limit
                  const reader = new FileReader();
                  reader.onload = () => {
                    const dataUrl = reader.result as string;
                    const base64 = dataUrl.replace(/^data:[^;]+;base64,/, '');
                    onReferenceImageChange(base64, file.name);
                  };
                  reader.readAsDataURL(file);
                }}
                className={`flex flex-col items-center justify-center gap-2 py-6 rounded border-2 border-dashed cursor-pointer ${
                  refImageDragOver
                    ? 'border-primary-400 bg-primary-50'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
                onClick={() => {
                  const input = document.createElement('input');
                  input.type = 'file';
                  input.accept = 'image/png,image/jpeg,image/gif,image/webp';
                  input.onchange = () => {
                    const file = input.files?.[0];
                    if (!file) return;
                    if (file.size > 10 * 1024 * 1024) return;
                    const reader = new FileReader();
                    reader.onload = () => {
                      const dataUrl = reader.result as string;
                      const base64 = dataUrl.replace(/^data:[^;]+;base64,/, '');
                      onReferenceImageChange(base64, file.name);
                    };
                    reader.readAsDataURL(file);
                  };
                  input.click();
                }}
              >
                <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span className="text-xs text-gray-500">
                  Drop image here or click to browse (PNG, JPG, GIF, WebP - max 10MB)
                </span>
              </div>
            ) : (
              <div className="flex items-center gap-3 bg-primary-50 px-3 py-2 rounded">
                <img
                  src={`data:image/png;base64,${referenceImageBase64}`}
                  alt="Reference"
                  className="w-16 h-16 object-cover rounded border"
                />
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-medium text-gray-800 truncate">{referenceImageFilename}</p>
                  <p className="text-xs text-gray-500">Image will be analyzed when session starts</p>
                </div>
                <button
                  type="button"
                  onClick={() => onReferenceImageChange('', '')}
                  className="text-xs text-primary-600 hover:text-primary-800 shrink-0"
                >
                  Clear
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Section 1: Seed from prompt file */}
      <div className="border rounded">
        <button
          type="button"
          onClick={() => setPromptFileOpen(!promptFileOpen)}
          className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
        >
          <ChevronIcon open={promptFileOpen} />
          <span className="font-medium">Seed from prompt file</span>
          {hasSelectedPromptFile && (
            <span className="ml-auto text-xs text-primary-600 font-medium">1 selected</span>
          )}
        </button>
        {promptFileOpen && (
          <div className="px-3 pb-3 space-y-2">
            <input
              type="text"
              value={promptFileQuery}
              onChange={(e) => setPromptFileQuery(e.target.value)}
              placeholder="Search prompt files..."
              className="w-full px-2 py-1 text-xs border rounded focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
            {hasSelectedPromptFile && (
              <div className="flex items-center justify-between bg-primary-50 px-2 py-1 rounded text-xs">
                <span className="truncate text-primary-800">
                  {referencePromptPath.split('/').slice(-2).join('/')}
                </span>
                <button
                  type="button"
                  onClick={handleClearPromptFile}
                  className="ml-2 text-primary-600 hover:text-primary-800 shrink-0"
                >
                  Clear
                </button>
              </div>
            )}
            <div className="max-h-40 overflow-y-auto space-y-1">
              {promptFilesLoading ? (
                <p className="text-xs text-gray-400 py-2 text-center">Loading...</p>
              ) : promptFiles.length === 0 ? (
                <p className="text-xs text-gray-400 py-2 text-center">No prompt files found</p>
              ) : (
                promptFiles.map((file) => (
                  <button
                    key={file.path}
                    type="button"
                    onClick={() => handleSelectPromptFile(file)}
                    className={`w-full text-left px-2 py-1.5 text-xs rounded hover:bg-gray-100 ${
                      referencePromptPath === file.path ? 'bg-primary-50 ring-1 ring-primary-300' : ''
                    }`}
                  >
                    <div className="font-medium text-gray-800 truncate">
                      {file.relative_path}
                    </div>
                    <div className="text-gray-500 truncate">{file.preview}</div>
                  </button>
                ))
              )}
            </div>
          </div>
        )}
      </div>

      {/* Section 2: Seed from previous result */}
      <div className="border rounded">
        <button
          type="button"
          onClick={() => setPrevResultOpen(!prevResultOpen)}
          className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
        >
          <ChevronIcon open={prevResultOpen} />
          <span className="font-medium">Seed from previous result</span>
          {hasSelectedResult && (
            <span className="ml-auto text-xs text-primary-600 font-medium">1 selected</span>
          )}
        </button>
        {prevResultOpen && (
          <div className="px-3 pb-3 space-y-2">
            <input
              type="text"
              value={resultQuery}
              onChange={(e) => setResultQuery(e.target.value)}
              placeholder="Search results..."
              className="w-full px-2 py-1 text-xs border rounded focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
            {hasSelectedResult && (
              <div className="flex items-center justify-between bg-primary-50 px-2 py-1 rounded text-xs">
                <span className="truncate text-primary-800">Result selected</span>
                <button
                  type="button"
                  onClick={handleClearResult}
                  className="ml-2 text-primary-600 hover:text-primary-800 shrink-0"
                >
                  Clear
                </button>
              </div>
            )}
            <div className="max-h-40 overflow-y-auto space-y-1">
              {prevResultsLoading ? (
                <p className="text-xs text-gray-400 py-2 text-center">Loading...</p>
              ) : prevResults.length === 0 ? (
                <p className="text-xs text-gray-400 py-2 text-center">No results found</p>
              ) : (
                prevResults.map((result) => (
                  <button
                    key={result.result_id}
                    type="button"
                    onClick={() => handleSelectResult(result)}
                    className="w-full text-left px-2 py-1.5 text-xs rounded hover:bg-gray-100"
                  >
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-gray-800 truncate flex-1">
                        {result.title}
                      </span>
                      {result.score !== undefined && (
                        <span className="text-amber-600 font-mono shrink-0">
                          {result.score.toFixed(1)}
                        </span>
                      )}
                      <span
                        className={`px-1 py-0.5 rounded text-[10px] font-medium shrink-0 ${
                          result.source === 'chat'
                            ? 'bg-blue-100 text-blue-700'
                            : result.source === 'refine'
                              ? 'bg-purple-100 text-purple-700'
                              : 'bg-gray-100 text-gray-600'
                        }`}
                      >
                        {result.source}
                      </span>
                    </div>
                    <div className="text-gray-500 truncate mt-0.5">{result.prompt_preview}</div>
                  </button>
                ))
              )}
            </div>
          </div>
        )}
      </div>

      {/* Section 3: MCP enrichment */}
      <div className="border rounded">
        <button
          type="button"
          onClick={() => setMcpOpen(!mcpOpen)}
          className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
        >
          <ChevronIcon open={mcpOpen} />
          <span className="font-medium">MCP enrichment</span>
          {mcpEnrichment.enabled && (
            <span className="ml-auto text-xs text-green-600 font-medium">On</span>
          )}
        </button>
        {mcpOpen && (
          <div className="px-3 pb-3 space-y-2">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() =>
                  onMCPEnrichmentChange({ ...mcpEnrichment, enabled: !mcpEnrichment.enabled })
                }
                className={`relative inline-flex h-5 w-9 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors ${
                  mcpEnrichment.enabled ? 'bg-primary-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 rounded-full bg-white transition-transform ${
                    mcpEnrichment.enabled ? 'translate-x-4' : 'translate-x-0'
                  }`}
                />
              </button>
              <span className="text-xs text-gray-600">
                Auto-search internal knowledge when customer/product terms detected
              </span>
            </div>
            {mcpEnrichment.enabled && (
              <div className="flex flex-wrap gap-2 mt-1">
                {MCP_SOURCES.map((src) => (
                  <label
                    key={src.id}
                    className="flex items-center gap-1.5 text-xs text-gray-700 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={mcpEnrichment.sources.includes(src.id)}
                      onChange={() => toggleMcpSource(src.id)}
                      className="rounded border-gray-300 text-primary-600 focus:ring-primary-500 h-3.5 w-3.5"
                    />
                    {src.label}
                  </label>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Section 4: Additional context textarea with drop zone */}
      <div>
        <label className="block text-sm text-gray-600 mb-1">Additional context (optional)</label>
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`relative ${
            isDragOver ? 'ring-2 ring-primary-400 ring-dashed rounded' : ''
          }`}
        >
          <textarea
            ref={textareaRef}
            value={customContext}
            onChange={(e) => onCustomContextChange(e.target.value)}
            placeholder="Any additional context or requirements... (drop .txt/.md files here)"
            rows={2}
            className="w-full px-3 py-2 text-sm border rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          {isDragOver && (
            <div className="absolute inset-0 flex items-center justify-center bg-primary-50/80 rounded border-2 border-dashed border-primary-400 pointer-events-none">
              <span className="text-sm text-primary-700 font-medium">
                Drop .txt or .md files here
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
