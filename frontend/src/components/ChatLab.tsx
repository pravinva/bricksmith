/**
 * ChatLab - multi-session tab for generating, evaluating, and refining
 * architecture diagrams. Mirrors `bricksmith chat` in the browser.
 *
 * Supports running multiple sessions concurrently: start one generating,
 * switch to set up another, and monitor all of them via session tabs.
 */

import { useState, useCallback, useEffect } from 'react';
import { resultsApi } from '../api/client';
import { useMultiSession, latestIteration } from '../hooks/useMultiSession';
import { RefinementPanel } from './RefinementPanel';
import type {
  PromptFileItem,
  StartStandaloneRefinementRequest,
} from '../types';
import { GEMINI_MODELS } from '../types';

// ---------------------------------------------------------------------------
// CLI command parser
// ---------------------------------------------------------------------------

function parseChatCommand(raw: string): StartStandaloneRefinementRequest | null {
  const cmd = raw.replace(/\\\s*\n/g, ' ').trim();
  if (!/(?:^|\s)bricksmith\s+chat\b/.test(cmd)) return null;

  const get = (flag: string): string | undefined => {
    const re = new RegExp(`${flag}[=\\s]+([^\\s]+)`);
    return cmd.match(re)?.[1];
  };

  return {
    prompt_file: get('--prompt-file'),
    persona: get('--persona') as StartStandaloneRefinementRequest['persona'],
    aspect_ratio: get('--aspect-ratio'),
    image_size: get('--size'),
    folder: get('--folder') || get('--name'),
    image_provider: get('--image-provider') as StartStandaloneRefinementRequest['image_provider'],
    num_variants: get('--num-variants') ? parseInt(get('--num-variants')!, 10) : undefined,
  };
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

type SourceTab = 'paste' | 'files';

const PERSONAS = [
  { value: 'architect', label: 'Architect', desc: 'Universal best practices' },
  { value: 'executive', label: 'Executive', desc: 'Strategic, CTO lens' },
  { value: 'developer', label: 'Developer', desc: 'Implementation focus' },
  { value: 'auto', label: 'Auto', desc: 'Let the LLM decide' },
] as const;

const PROVIDERS = [
  { value: 'gemini', label: 'Gemini' },
  { value: 'openai', label: 'OpenAI' },
  { value: 'databricks', label: 'Databricks (AWS US)' },
] as const;

const SIZES = ['1K', '2K', '4K'] as const;
const RATIOS = ['16:9', '1:1', '4:3', '9:16', '3:4', '21:9'] as const;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function tabScoreColor(value: number): string {
  if (value >= 8) return 'text-green-600';
  if (value >= 6) return 'text-yellow-600';
  return 'text-red-600';
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export function ChatLab() {
  const multi = useMultiSession();
  const { startSession, count: sessionCount } = multi;

  // ── Setup state ──────────────────────────────────────────────────────────
  const [prompt, setPrompt] = useState('');
  const [sourceTab, setSourceTab] = useState<SourceTab>('paste');
  const [persona, setPersona] = useState<string>('architect');
  const [provider, setProvider] = useState<string>('gemini');
  const [aspectRatio, setAspectRatio] = useState('16:9');
  const [imageSize, setImageSize] = useState('2K');
  const [numVariants, setNumVariants] = useState(1);
  const [folder, setFolder] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [geminiModel, setGeminiModel] = useState('gemini-3-pro-image-preview');
  const [advancedOpen, setAdvancedOpen] = useState(false);
  const [isStarting, setIsStarting] = useState(false);
  const [startError, setStartError] = useState<string | null>(null);

  // File browser
  const [promptFiles, setPromptFiles] = useState<PromptFileItem[]>([]);
  const [filesLoading, setFilesLoading] = useState(false);
  const [fileQuery, setFileQuery] = useState('');
  const [selectedFile, setSelectedFile] = useState<PromptFileItem | null>(null);

  // CLI detection
  const detected = prompt.trim() ? parseChatCommand(prompt) : null;
  const isCliCommand = detected !== null && (!!detected.prompt_file || !!detected.folder);

  // ── File browser helpers ─────────────────────────────────────────────────
  const loadFiles = useCallback(async (q?: string) => {
    setFilesLoading(true);
    try {
      const resp = await resultsApi.listPromptFiles(q, 50);
      setPromptFiles(resp.files);
    } catch {
      /* silent */
    } finally {
      setFilesLoading(false);
    }
  }, []);

  useEffect(() => {
    if (sourceTab === 'files' && promptFiles.length === 0) {
      void loadFiles();
    }
  }, [sourceTab]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSelectFile = useCallback((file: PromptFileItem) => {
    setSelectedFile(file);
    setPrompt(file.preview);
    void fetch(`/api/results/prompt-files?limit=1&query=${encodeURIComponent(file.relative_path)}`)
      .then(r => r.json())
      .then((data: { files: PromptFileItem[] }) => {
        if (data.files?.[0]?.preview) {
          setPrompt(data.files[0].preview);
        }
      });
    if (!folder) {
      const name = file.relative_path.replace(/\.txt$/, '').replace(/[/\\]/g, '-');
      setFolder(name);
    }
  }, [folder]);

  // ── Start the loop ───────────────────────────────────────────────────────
  const handleStart = useCallback(async () => {
    setStartError(null);
    setIsStarting(true);

    let request: StartStandaloneRefinementRequest;

    // Common fields for all request modes
    const geminiModelOverride = provider === 'gemini' ? geminiModel : undefined;

    if (isCliCommand && detected) {
      request = {
        ...detected,
        image_provider: (detected.image_provider || provider) as StartStandaloneRefinementRequest['image_provider'],
        gemini_model: geminiModelOverride,
        persona: (detected.persona || persona) as StartStandaloneRefinementRequest['persona'],
        aspect_ratio: detected.aspect_ratio || aspectRatio,
        image_size: detected.image_size || imageSize,
        folder: detected.folder || folder || undefined,
        num_variants: detected.num_variants || (numVariants > 1 ? numVariants : undefined),
        openai_api_key: provider === 'openai' ? apiKey || undefined : undefined,
        vertex_api_key: provider === 'gemini' ? apiKey || undefined : undefined,
      };
    } else if (selectedFile) {
      request = {
        prompt_file: selectedFile.path,
        image_provider: provider as StartStandaloneRefinementRequest['image_provider'],
        gemini_model: geminiModelOverride,
        persona: persona as StartStandaloneRefinementRequest['persona'],
        aspect_ratio: aspectRatio,
        image_size: imageSize,
        folder: folder || undefined,
        num_variants: numVariants > 1 ? numVariants : undefined,
        openai_api_key: provider === 'openai' ? apiKey || undefined : undefined,
        vertex_api_key: provider === 'gemini' ? apiKey || undefined : undefined,
      };
    } else {
      request = {
        prompt: prompt.trim(),
        image_provider: provider as StartStandaloneRefinementRequest['image_provider'],
        gemini_model: geminiModelOverride,
        persona: persona as StartStandaloneRefinementRequest['persona'],
        aspect_ratio: aspectRatio,
        image_size: imageSize,
        folder: folder || undefined,
        num_variants: numVariants > 1 ? numVariants : undefined,
        openai_api_key: provider === 'openai' ? apiKey || undefined : undefined,
        vertex_api_key: provider === 'gemini' ? apiKey || undefined : undefined,
      };
    }

    const label =
      folder ||
      selectedFile?.relative_path?.replace(/\.txt$/, '').split('/').pop() ||
      prompt.trim().slice(0, 30) ||
      `Session ${sessionCount + 1}`;

    try {
      await startSession(request, label);
    } catch (e) {
      setStartError(e instanceof Error ? e.message : 'Failed to start session');
    } finally {
      setIsStarting(false);
    }
  }, [
    isCliCommand, detected, selectedFile, prompt, provider, persona, geminiModel,
    aspectRatio, imageSize, folder, numVariants, apiKey, startSession, sessionCount,
  ]);

  const hasInput = prompt.trim().length > 0 || selectedFile !== null;
  const active = multi.active;

  // ── Render ───────────────────────────────────────────────────────────────
  return (
    <div className="h-full flex flex-col">
      {/* ── Session tab bar ──────────────────────────────────────────────── */}
      {multi.count > 0 && (
        <div className="flex items-center gap-1 px-4 py-2 bg-white border-b overflow-x-auto flex-shrink-0">
          {multi.order.map(id => {
            const session = multi.sessions[id];
            const isActiveTab = id === multi.activeId && !multi.showSetup;
            const iter = latestIteration(session.refinementState);
            return (
              <button
                key={id}
                onClick={() => multi.setActive(id)}
                className={`group flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-lg border transition-colors flex-shrink-0 max-w-[200px] ${
                  isActiveTab
                    ? 'bg-primary-50 border-primary-300 text-primary-700'
                    : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
                }`}
              >
                {/* Status indicator */}
                {session.isGenerating || session.isRefining ? (
                  <span className="w-3 h-3 border-2 border-primary-300 border-t-primary-600 rounded-full animate-spin flex-shrink-0" />
                ) : session.error ? (
                  <span className="w-2.5 h-2.5 rounded-full bg-red-500 flex-shrink-0" />
                ) : iter?.overall_score != null ? (
                  <span className={`text-xs font-bold flex-shrink-0 ${tabScoreColor(iter.overall_score)}`}>
                    {iter.overall_score}
                  </span>
                ) : (
                  <span className="w-2 h-2 rounded-full bg-gray-300 flex-shrink-0" />
                )}

                <span className="truncate">{session.label}</span>

                {session.refinementState && session.refinementState.iteration_count > 0 && (
                  <span className="text-[10px] text-gray-400 flex-shrink-0">
                    #{session.refinementState.iteration_count}
                  </span>
                )}

                {/* Close button */}
                <span
                  onClick={e => { e.stopPropagation(); multi.removeSession(id); }}
                  className="ml-0.5 opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-500 transition-opacity cursor-pointer flex-shrink-0"
                >
                  &times;
                </span>
              </button>
            );
          })}

          {/* New session button */}
          <button
            onClick={multi.showSetupScreen}
            className={`flex items-center gap-1 px-3 py-1.5 text-sm rounded-lg border transition-colors flex-shrink-0 ${
              multi.showSetup
                ? 'bg-primary-50 border-primary-300 text-primary-700'
                : 'border-dashed border-gray-300 text-gray-500 hover:bg-gray-50 hover:border-gray-400'
            }`}
          >
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New
          </button>
        </div>
      )}

      {/* ── Main content ─────────────────────────────────────────────────── */}
      {!multi.showSetup && active?.refinementState ? (
        /* Active session: RefinementPanel */
        <div className="flex-1 overflow-hidden max-w-5xl mx-auto w-full">
          <RefinementPanel
            state={active.refinementState}
            currentIteration={latestIteration(active.refinementState)}
            isGenerating={active.isGenerating}
            isRefining={active.isRefining}
            error={active.error}
            onRefine={(feedback, settings, score) =>
              multi.refinePrompt(active.id, feedback, settings, score)
            }
            onAccept={() => multi.removeSession(active.id)}
            onRegenerate={settings => multi.generateAndEvaluate(active.id, settings)}
            onClearError={() => multi.clearError(active.id)}
            onUpdatePrompt={p => multi.updatePrompt(active.id, p)}
          />
        </div>
      ) : (
        /* Setup screen */
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto py-10 px-6">
            {/* Header */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900">Chat Lab</h2>
              <p className="text-gray-500 mt-1">
                Generate, evaluate, and iteratively refine architecture diagrams - same as{' '}
                <code className="text-sm bg-gray-100 px-1.5 py-0.5 rounded">bricksmith chat</code>
              </p>
              {multi.count > 0 && (
                <p className="text-sm text-primary-600 mt-2">
                  {multi.count} session{multi.count > 1 ? 's' : ''} running in background
                </p>
              )}
            </div>

            {/* ── Step 1: Prompt source ─────────────────────────────────── */}
            <section className="bg-white rounded-xl border shadow-sm p-5 mb-5">
              <h3 className="text-sm font-semibold text-gray-800 mb-3">1. Prompt</h3>

              {/* Tab switcher */}
              <div className="flex gap-1 mb-3 bg-gray-100 rounded-lg p-1 w-fit">
                {([
                  { key: 'paste' as const, label: 'Paste / type' },
                  { key: 'files' as const, label: 'Browse files' },
                ]).map(tab => (
                  <button
                    key={tab.key}
                    onClick={() => { setSourceTab(tab.key); setSelectedFile(null); }}
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
                <>
                  <textarea
                    value={prompt}
                    onChange={e => { setPrompt(e.target.value); setSelectedFile(null); }}
                    placeholder={'Paste your diagram prompt here, or paste a CLI command:\n\nbricksmith chat \\\n  --prompt-file prompts/my_prompt.txt \\\n  --persona executive --aspect-ratio 16:9'}
                    rows={8}
                    className={`w-full border rounded-lg px-4 py-3 text-sm resize-y focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                      isCliCommand ? 'font-mono text-xs bg-gray-50' : ''
                    }`}
                  />
                  {isCliCommand && detected && (
                    <div className="mt-2 px-3 py-2 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-800 flex flex-wrap gap-x-4 gap-y-1">
                      <span className="font-semibold">CLI command detected</span>
                      {detected.prompt_file && <span>File: <code className="bg-blue-100 px-1 rounded">{detected.prompt_file}</code></span>}
                      {detected.persona && <span>Persona: {detected.persona}</span>}
                      {detected.aspect_ratio && <span>Ratio: {detected.aspect_ratio}</span>}
                      {detected.image_size && <span>Size: {detected.image_size}</span>}
                      {detected.folder && <span>Folder: {detected.folder}</span>}
                      {detected.image_provider && <span>Provider: {detected.image_provider}</span>}
                      {detected.num_variants && <span>Variants: {detected.num_variants}</span>}
                    </div>
                  )}
                </>
              )}

              {/* File browser tab */}
              {sourceTab === 'files' && (
                <div className="border rounded-lg">
                  <div className="p-3 border-b">
                    <input
                      value={fileQuery}
                      onChange={e => setFileQuery(e.target.value)}
                      onKeyDown={e => e.key === 'Enter' && loadFiles(fileQuery || undefined)}
                      placeholder="Search prompt files..."
                      className="w-full border rounded px-3 py-2 text-sm"
                    />
                  </div>
                  <div className="max-h-64 overflow-y-auto">
                    {filesLoading ? (
                      <p className="p-4 text-sm text-gray-500">Loading...</p>
                    ) : promptFiles.length === 0 ? (
                      <p className="p-4 text-sm text-gray-500">No prompt files found in outputs/.</p>
                    ) : (
                      <ul className="divide-y">
                        {promptFiles.map(file => {
                          const isSelected = selectedFile?.path === file.path;
                          return (
                            <li
                              key={file.path}
                              onClick={() => handleSelectFile(file)}
                              className={`px-4 py-3 cursor-pointer transition-colors ${
                                isSelected
                                  ? 'bg-primary-50 border-l-4 border-l-primary-500'
                                  : 'hover:bg-gray-50'
                              }`}
                            >
                              <p className="text-sm font-medium text-gray-900 truncate">
                                {file.relative_path}
                              </p>
                              <p className="text-xs text-gray-500 line-clamp-2 mt-0.5">
                                {file.preview}
                              </p>
                            </li>
                          );
                        })}
                      </ul>
                    )}
                  </div>
                </div>
              )}
            </section>

            {/* ── Step 2: Settings ──────────────────────────────────────── */}
            <section className="bg-white rounded-xl border shadow-sm p-5 mb-5">
              <h3 className="text-sm font-semibold text-gray-800 mb-3">2. Settings</h3>

              <div className="space-y-4">
                {/* Persona */}
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5">Evaluation persona</label>
                  <div className="grid grid-cols-4 gap-2">
                    {PERSONAS.map(p => (
                      <button
                        key={p.value}
                        onClick={() => setPersona(p.value)}
                        className={`px-3 py-2 rounded-lg border text-sm transition-colors ${
                          persona === p.value
                            ? 'border-primary-500 bg-primary-50 text-primary-700'
                            : 'border-gray-200 hover:border-gray-400 text-gray-700'
                        }`}
                      >
                        <div className="font-medium">{p.label}</div>
                        <div className="text-[10px] text-gray-500 mt-0.5">{p.desc}</div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Image settings row */}
                <div className="flex flex-wrap gap-4">
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Aspect ratio</label>
                    <select
                      value={aspectRatio}
                      onChange={e => setAspectRatio(e.target.value)}
                      className="border rounded px-3 py-2 text-sm"
                    >
                      {RATIOS.map(r => <option key={r} value={r}>{r}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Image size</label>
                    <select
                      value={imageSize}
                      onChange={e => setImageSize(e.target.value)}
                      className="border rounded px-3 py-2 text-sm"
                    >
                      {SIZES.map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Variants</label>
                    <select
                      value={numVariants}
                      onChange={e => setNumVariants(Number(e.target.value))}
                      className="border rounded px-3 py-2 text-sm"
                    >
                      {[1, 2, 3, 4].map(n => <option key={n} value={n}>{n}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Provider</label>
                    <select
                      value={provider}
                      onChange={e => setProvider(e.target.value)}
                      className="border rounded px-3 py-2 text-sm"
                    >
                      {PROVIDERS.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
                    </select>
                  </div>
                </div>

                {/* Folder name + API key */}
                <div className="flex flex-wrap gap-4">
                  <div className="flex-1 min-w-[200px]">
                    <label className="block text-xs font-medium text-gray-500 mb-1">
                      Folder name <span className="text-gray-400">(optional)</span>
                    </label>
                    <input
                      value={folder}
                      onChange={e => setFolder(e.target.value)}
                      placeholder="e.g. coles-future-state"
                      className="w-full border rounded px-3 py-2 text-sm"
                    />
                  </div>
                  <div className="flex-1 min-w-[200px]">
                    <label className="block text-xs font-medium text-gray-500 mb-1">
                      API key <span className="text-gray-400">(uses env default)</span>
                    </label>
                    <input
                      type="password"
                      value={apiKey}
                      onChange={e => setApiKey(e.target.value)}
                      placeholder="Optional override"
                      className="w-full border rounded px-3 py-2 text-sm"
                    />
                  </div>
                </div>
              </div>
            </section>

            {/* ── Step 3: Advanced (collapsible) ────────────────────────── */}
            <section className="bg-white rounded-xl border shadow-sm mb-5">
              <button
                type="button"
                onClick={() => setAdvancedOpen(prev => !prev)}
                className="w-full px-5 py-3 flex items-center justify-between text-left hover:bg-gray-50 rounded-xl"
              >
                <h3 className="text-sm font-semibold text-gray-800">3. Advanced</h3>
                <svg
                  className={`w-4 h-4 text-gray-400 transition-transform ${advancedOpen ? 'rotate-180' : ''}`}
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              {advancedOpen && (
                <div className="px-5 pb-5 border-t space-y-4">
                  {/* Gemini model selector */}
                  {provider === 'gemini' && (
                    <div className="pt-3">
                      <label className="block text-xs font-medium text-gray-500 mb-1.5">
                        Gemini model (Nano Banana)
                      </label>
                      <div className="grid grid-cols-2 gap-2">
                        {GEMINI_MODELS.map(m => (
                          <button
                            key={m.value}
                            onClick={() => setGeminiModel(m.value)}
                            className={`px-3 py-2 rounded-lg border text-sm text-left transition-colors ${
                              geminiModel === m.value
                                ? 'border-primary-500 bg-primary-50 text-primary-700'
                                : 'border-gray-200 hover:border-gray-400 text-gray-700'
                            }`}
                          >
                            <div className="font-medium">{m.label}</div>
                            <div className="text-[10px] text-gray-500 mt-0.5">{m.desc}</div>
                            <div className="text-[10px] font-mono text-gray-400 mt-0.5">{m.value}</div>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {provider !== 'gemini' && (
                    <p className="pt-3 text-sm text-gray-500">
                      Model selection is available when using the Gemini provider.
                    </p>
                  )}
                </div>
              )}
            </section>

            {/* ── Start button ──────────────────────────────────────────── */}
            <button
              onClick={handleStart}
              disabled={!hasInput || isStarting}
              className="w-full py-4 bg-primary-600 text-white rounded-xl text-lg font-semibold hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
            >
              {isStarting ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="inline-block w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Starting session...
                </span>
              ) : (
                'Start chat loop'
              )}
            </button>

            {/* Error */}
            {startError && (
              <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-800">
                {startError}
                <button onClick={() => setStartError(null)} className="ml-2 underline text-red-600">
                  Dismiss
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
