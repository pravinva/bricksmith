/**
 * ChatLab - a self-contained tab that mirrors `bricksmith chat` in the browser.
 *
 * Two phases:
 *   1. Setup  - pick a prompt (file browser, paste, or CLI command), configure
 *               settings (persona, aspect ratio, size, provider, variants)
 *   2. Running - the generate / evaluate / refine loop (RefinementPanel)
 *
 * Owns its own `useRefinement` hook so it's fully independent of the rest of
 * the app.  Click "Chat Lab" in the header tab bar and everything lives here.
 */

import { useState, useCallback, useEffect } from 'react';
import { resultsApi } from '../api/client';
import { useRefinement } from '../hooks/useRefinement';
import { RefinementPanel } from './RefinementPanel';
import type {
  PromptFileItem,
  StartStandaloneRefinementRequest,
} from '../types';

// ---------------------------------------------------------------------------
// CLI command parser (reused logic from PromptEntry)
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
// Component
// ---------------------------------------------------------------------------

export function ChatLab() {
  const refinement = useRefinement();

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
    // Load full content
    void fetch(`/api/results/prompt-files?limit=1&query=${encodeURIComponent(file.relative_path)}`)
      .then(r => r.json())
      .then((data: { files: PromptFileItem[] }) => {
        if (data.files?.[0]?.preview) {
          setPrompt(data.files[0].preview);
        }
      });
    // Pre-fill folder from filename
    if (!folder) {
      const name = file.relative_path.replace(/\.txt$/, '').replace(/[/\\]/g, '-');
      setFolder(name);
    }
  }, [folder]);

  // ── Start the loop ───────────────────────────────────────────────────────
  const handleStart = useCallback(() => {
    let request: StartStandaloneRefinementRequest;

    if (isCliCommand && detected) {
      // CLI command mode - use parsed flags, override with form settings where empty
      request = {
        ...detected,
        image_provider: (detected.image_provider || provider) as StartStandaloneRefinementRequest['image_provider'],
        persona: (detected.persona || persona) as StartStandaloneRefinementRequest['persona'],
        aspect_ratio: detected.aspect_ratio || aspectRatio,
        image_size: detected.image_size || imageSize,
        folder: detected.folder || folder || undefined,
        num_variants: detected.num_variants || (numVariants > 1 ? numVariants : undefined),
        openai_api_key: provider === 'openai' ? apiKey || undefined : undefined,
        vertex_api_key: provider === 'gemini' ? apiKey || undefined : undefined,
      };
    } else if (selectedFile) {
      // File mode - send the path so backend reads it
      request = {
        prompt_file: selectedFile.path,
        image_provider: provider as StartStandaloneRefinementRequest['image_provider'],
        persona: persona as StartStandaloneRefinementRequest['persona'],
        aspect_ratio: aspectRatio,
        image_size: imageSize,
        folder: folder || undefined,
        num_variants: numVariants > 1 ? numVariants : undefined,
        openai_api_key: provider === 'openai' ? apiKey || undefined : undefined,
        vertex_api_key: provider === 'gemini' ? apiKey || undefined : undefined,
      };
    } else {
      // Raw prompt text
      request = {
        prompt: prompt.trim(),
        image_provider: provider as StartStandaloneRefinementRequest['image_provider'],
        persona: persona as StartStandaloneRefinementRequest['persona'],
        aspect_ratio: aspectRatio,
        image_size: imageSize,
        folder: folder || undefined,
        num_variants: numVariants > 1 ? numVariants : undefined,
        openai_api_key: provider === 'openai' ? apiKey || undefined : undefined,
        vertex_api_key: provider === 'gemini' ? apiKey || undefined : undefined,
      };
    }

    void refinement.startStandaloneRefinement(request);
  }, [isCliCommand, detected, selectedFile, prompt, provider, persona, aspectRatio, imageSize, folder, numVariants, apiKey, refinement]);

  const handleDone = useCallback(() => {
    refinement.acceptResult();
  }, [refinement]);

  const hasInput = prompt.trim().length > 0 || selectedFile !== null;
  const isStarting = refinement.isGenerating && !refinement.isActive;

  // ── If the loop is running, show the RefinementPanel fullscreen ──────────
  if (refinement.isActive) {
    return (
      <div className="h-full max-w-5xl mx-auto">
        <RefinementPanel
          state={refinement.refinementState!}
          currentIteration={refinement.currentIteration}
          isGenerating={refinement.isGenerating}
          isRefining={refinement.isRefining}
          error={refinement.error}
          onRefine={refinement.refinePrompt}
          onAccept={handleDone}
          onRegenerate={refinement.generateAndEvaluate}
          onClearError={refinement.clearError}
          onUpdatePrompt={refinement.updatePrompt}
        />
      </div>
    );
  }

  // ── Setup screen ─────────────────────────────────────────────────────────
  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-3xl mx-auto py-10 px-6">
        {/* Header */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Chat Lab</h2>
          <p className="text-gray-500 mt-1">
            Generate, evaluate, and iteratively refine architecture diagrams - same as{' '}
            <code className="text-sm bg-gray-100 px-1.5 py-0.5 rounded">bricksmith chat</code>
          </p>
        </div>

        {/* ── Step 1: Prompt source ─────────────────────────────────────── */}
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

        {/* ── Step 2: Settings ──────────────────────────────────────────── */}
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

        {/* ── Start button ──────────────────────────────────────────────── */}
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
        {refinement.error && (
          <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-800">
            {refinement.error}
            <button onClick={refinement.clearError} className="ml-2 underline text-red-600">
              Dismiss
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
