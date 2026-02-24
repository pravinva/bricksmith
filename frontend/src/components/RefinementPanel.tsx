/**
 * Panel that displays the full diagram refinement loop with feature parity
 * to the CLI `bricksmith chat` command.
 *
 * Layout (top to bottom):
 * 1. Session header bar
 * 2. Current prompt section (collapsible)
 * 3. Image display area (single or multi-variant with selection)
 * 4. Evaluation section (LLM Judge + user score)
 * 5. Feedback and actions section
 * 6. Generation presets row
 * 7. Action buttons (sticky bottom)
 * 8. Iteration history (horizontal scroll)
 */

import { useState, useCallback, useMemo, useEffect, useRef } from 'react';
import type {
  RefinementState,
  RefinementIteration,
  EvaluationScores,
  GenerationSettingsRequest,
} from '../types';
import { IMAGE_SIZES, ASPECT_RATIOS } from '../types';

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface RefinementPanelProps {
  state: RefinementState;
  currentIteration: RefinementIteration | null;
  isGenerating: boolean;
  isRefining: boolean;
  error: string | null;
  onRefine: (feedback: string, settings?: GenerationSettingsRequest, userScore?: number) => Promise<void>;
  onAccept: () => void;
  onRegenerate: (settings?: GenerationSettingsRequest) => Promise<void>;
  onClearError: () => void;
  onUpdatePrompt?: (prompt: string) => Promise<void>;
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const SCORE_LABELS: Record<keyof EvaluationScores, string> = {
  information_hierarchy: 'Info Hierarchy',
  technical_accuracy: 'Technical Acc.',
  logo_fidelity: 'Logo Fidelity',
  visual_clarity: 'Visual Clarity',
  data_flow_legibility: 'Data Flow',
  text_readability: 'Text Readability',
};

const PRESETS = [
  { name: 'Deterministic', value: 'deterministic', color: 'gray', temp: '0.0' },
  { name: 'Conservative', value: 'conservative', color: 'blue', temp: '0.4' },
  { name: 'Balanced', value: 'balanced', color: 'green', temp: '0.8' },
  { name: 'Creative', value: 'creative', color: 'orange', temp: '1.2' },
  { name: 'Wild', value: 'wild', color: 'red', temp: '1.8' },
] as const;

const QUICK_FEEDBACK = [
  'Improve logo clarity',
  'Fix text readability',
  'Simplify layout',
  'More contrast',
  'Fix data flow arrows',
] as const;

/** Map preset color names to Tailwind classes for filled (selected) state. */
const PRESET_FILLED: Record<string, string> = {
  gray: 'bg-gray-600 text-white border-gray-600',
  blue: 'bg-blue-600 text-white border-blue-600',
  green: 'bg-green-600 text-white border-green-600',
  orange: 'bg-orange-500 text-white border-orange-500',
  red: 'bg-red-500 text-white border-red-500',
};

const PRESET_OUTLINE: Record<string, string> = {
  gray: 'border-gray-400 text-gray-600 hover:bg-gray-50',
  blue: 'border-blue-400 text-blue-600 hover:bg-blue-50',
  green: 'border-green-400 text-green-600 hover:bg-green-50',
  orange: 'border-orange-400 text-orange-600 hover:bg-orange-50',
  red: 'border-red-400 text-red-600 hover:bg-red-50',
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function scoreColor(value: number): string {
  if (value >= 8) return 'text-green-600';
  if (value >= 6) return 'text-yellow-600';
  return 'text-red-600';
}

function scoreBgColor(value: number): string {
  if (value >= 8) return 'bg-green-600';
  if (value >= 6) return 'bg-yellow-500';
  return 'bg-red-500';
}

// ---------------------------------------------------------------------------
// Sub-components (inline, no separate files)
// ---------------------------------------------------------------------------

function ScoreBar({ label, value }: { label: string; value: number }) {
  const pct = (value / 10) * 100;
  return (
    <div className="flex items-center gap-2 text-sm">
      <span className="w-28 text-gray-600 truncate" title={label}>
        {label}
      </span>
      <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${scoreBgColor(value)}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className={`w-6 text-right font-mono ${scoreColor(value)}`}>{value}</span>
    </div>
  );
}

function Lightbox({
  src,
  alt,
  onClose,
}: {
  src: string;
  alt: string;
  onClose: () => void;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="relative max-w-[90vw] max-h-[90vh]">
        <img src={src} alt={alt} className="max-w-full max-h-[90vh] rounded-lg shadow-2xl" />
        <button
          onClick={onClose}
          className="absolute -top-3 -right-3 bg-white rounded-full p-1 shadow-lg hover:bg-gray-100"
        >
          <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export function RefinementPanel({
  state,
  currentIteration,
  isGenerating,
  isRefining,
  error,
  onRefine,
  onAccept,
  onRegenerate,
  onClearError,
  onUpdatePrompt,
}: RefinementPanelProps) {
  // -- Local state ----------------------------------------------------------
  const [feedback, setFeedback] = useState('');
  const [selectedHistoryIdx, setSelectedHistoryIdx] = useState(-1);
  const [lightboxUrl, setLightboxUrl] = useState<string | null>(null);
  const [selectedVariant, setSelectedVariant] = useState(0);
  const [userScore, setUserScore] = useState<number | null>(null);
  const [autoRefine, setAutoRefine] = useState(false);
  const [promptExpanded, setPromptExpanded] = useState(false);
  const [promptEditing, setPromptEditing] = useState(false);
  const [editablePrompt, setEditablePrompt] = useState('');
  const [genSettings, setGenSettings] = useState<GenerationSettingsRequest>({
    preset: 'balanced',
    image_size: '2K',
    aspect_ratio: '16:9',
    num_variants: 1,
  });

  const isBusy = isGenerating || isRefining;
  const prevIterationCountRef = useRef(state.iteration_count);

  // -- Derived values -------------------------------------------------------
  const displayIteration = useMemo(() => {
    if (selectedHistoryIdx >= 0 && selectedHistoryIdx < state.iterations.length) {
      return state.iterations[selectedHistoryIdx];
    }
    return currentIteration;
  }, [selectedHistoryIdx, state.iterations, currentIteration]);

  const effectiveScore = useMemo(() => {
    if (userScore !== null) return userScore;
    return displayIteration?.overall_score ?? null;
  }, [userScore, displayIteration]);

  // Reset user score when iteration changes
  useEffect(() => {
    setUserScore(null);
    setSelectedVariant(0);
  }, [currentIteration?.iteration]);

  // Sync editable prompt when entering edit mode
  useEffect(() => {
    if (promptEditing) {
      setEditablePrompt(state.current_prompt);
    }
  }, [promptEditing, state.current_prompt]);

  // -- Auto-refine effect ---------------------------------------------------
  useEffect(() => {
    if (!autoRefine || isBusy) return;

    const newCount = state.iteration_count;
    const oldCount = prevIterationCountRef.current;
    prevIterationCountRef.current = newCount;

    // If a new iteration just completed and auto-refine is on, trigger next round
    if (newCount > oldCount && newCount > 0 && currentIteration) {
      const targetScore = 8;
      const currentScore = currentIteration.overall_score ?? 0;
      if (currentScore < targetScore) {
        // Use the LLM's suggested improvements as feedback
        const autoFeedback = currentIteration.improvements.length > 0
          ? currentIteration.improvements.join('. ')
          : '';
        void onRefine(autoFeedback, genSettings, currentScore);
      } else {
        // Target reached, stop auto-refine
        setAutoRefine(false);
      }
    }
  }, [autoRefine, isBusy, state.iteration_count, currentIteration, genSettings, onRefine]);

  // Keep ref in sync on every render (not just when effect fires)
  useEffect(() => {
    prevIterationCountRef.current = state.iteration_count;
  });

  // -- Handlers -------------------------------------------------------------
  const handleRefine = useCallback(async () => {
    if (isBusy) return;
    const text = feedback.trim();
    setFeedback('');
    setSelectedHistoryIdx(-1);
    await onRefine(text || '', genSettings, effectiveScore ?? undefined);
  }, [isBusy, feedback, genSettings, effectiveScore, onRefine]);

  const handleRegenerate = useCallback(async () => {
    if (isBusy) return;
    setSelectedHistoryIdx(-1);
    await onRegenerate(genSettings);
  }, [isBusy, genSettings, onRegenerate]);

  const handleSavePrompt = useCallback(async () => {
    if (!onUpdatePrompt) return;
    await onUpdatePrompt(editablePrompt);
    setPromptEditing(false);
  }, [onUpdatePrompt, editablePrompt]);

  const appendFeedback = useCallback((text: string) => {
    setFeedback(prev => {
      const trimmed = prev.trim();
      if (trimmed.length === 0) return text;
      return `${trimmed}. ${text}`;
    });
  }, []);

  const updateSettings = useCallback((partial: Partial<GenerationSettingsRequest>) => {
    setGenSettings(prev => ({ ...prev, ...partial }));
  }, []);

  // -- Prompt preview (first 2 lines) --------------------------------------
  const promptPreview = useMemo(() => {
    const lines = state.current_prompt.split('\n');
    return lines.slice(0, 2).join('\n') + (lines.length > 2 ? '...' : '');
  }, [state.current_prompt]);

  // -- Render ---------------------------------------------------------------
  return (
    <div className="flex flex-col h-full">
      {/* Lightbox overlay */}
      {lightboxUrl && (
        <Lightbox
          src={lightboxUrl}
          alt="Diagram preview"
          onClose={() => setLightboxUrl(null)}
        />
      )}

      {/* ================================================================= */}
      {/* 1. Session header bar                                             */}
      {/* ================================================================= */}
      <div className="px-4 py-3 border-b bg-white flex-shrink-0">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-3 min-w-0">
            <h3 className="font-semibold text-gray-900 truncate">Refinement</h3>
            <span className="text-xs font-mono text-gray-500 truncate" title={state.session_id}>
              {state.session_id.slice(0, 12)}
            </span>
            {state.iteration_count > 0 && (
              <span className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">
                iter {state.iteration_count}
              </span>
            )}
            <span className="text-xs bg-indigo-100 text-indigo-700 px-1.5 py-0.5 rounded">
              architect
            </span>
          </div>
          <div className="flex items-center gap-3 flex-shrink-0">
            {/* Settings summary */}
            <span className="text-[11px] text-gray-400 hidden sm:inline">
              {genSettings.aspect_ratio || '16:9'} / {genSettings.image_size || '2K'}
              {(genSettings.num_variants ?? 1) > 1 && ` / ${genSettings.num_variants}x`}
            </span>
            {/* Auto-refine toggle */}
            <label className="flex items-center gap-1.5 cursor-pointer select-none" title="Auto-refine until target score (8+)">
              <span className="text-xs text-gray-500">Auto</span>
              <button
                type="button"
                role="switch"
                aria-checked={autoRefine}
                onClick={() => setAutoRefine(prev => !prev)}
                className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${
                  autoRefine ? 'bg-primary-600' : 'bg-gray-300'
                }`}
              >
                <span
                  className={`inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform ${
                    autoRefine ? 'translate-x-[18px]' : 'translate-x-[3px]'
                  }`}
                />
              </button>
            </label>
            {/* Busy indicator */}
            {isBusy && (
              <span className="text-xs text-primary-600 animate-pulse">
                {isGenerating ? 'Generating...' : 'Refining...'}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* ================================================================= */}
      {/* Scrollable body                                                   */}
      {/* ================================================================= */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-4 space-y-4">

          {/* Error banner */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-sm">
              <div className="flex justify-between items-start">
                <p className="text-red-800">{error}</p>
                <button onClick={onClearError} className="text-red-400 hover:text-red-600 ml-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          )}

          {/* ============================================================= */}
          {/* 2. Current prompt section (collapsible)                        */}
          {/* ============================================================= */}
          <div className="bg-white rounded-lg border">
            <button
              type="button"
              onClick={() => {
                if (promptEditing) return;
                setPromptExpanded(prev => !prev);
              }}
              className="w-full px-3 py-2 flex items-center justify-between text-left hover:bg-gray-50 rounded-lg"
            >
              <div className="flex items-center gap-2 min-w-0">
                <svg
                  className={`w-4 h-4 text-gray-400 transition-transform flex-shrink-0 ${promptExpanded ? 'rotate-90' : ''}`}
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
                <span className="text-sm font-medium text-gray-700">Current prompt</span>
              </div>
              {!promptExpanded && (
                <span className="text-xs text-gray-400 truncate max-w-[60%] ml-2">
                  {promptPreview.split('\n')[0]}
                </span>
              )}
            </button>
            {promptExpanded && (
              <div className="px-3 pb-3 border-t space-y-2">
                {promptEditing ? (
                  <>
                    <textarea
                      value={editablePrompt}
                      onChange={e => setEditablePrompt(e.target.value)}
                      rows={10}
                      className="w-full mt-2 text-xs font-mono bg-white border border-blue-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-400 resize-y"
                    />
                    <div className="flex gap-2 justify-end">
                      <button
                        onClick={() => setPromptEditing(false)}
                        className="px-3 py-1 text-xs text-gray-600 bg-gray-100 rounded hover:bg-gray-200"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={handleSavePrompt}
                        disabled={!onUpdatePrompt}
                        className="px-3 py-1 text-xs text-white bg-blue-600 rounded hover:bg-blue-700 disabled:opacity-50"
                      >
                        Save
                      </button>
                    </div>
                  </>
                ) : (
                  <>
                    <pre className="mt-2 text-xs font-mono bg-gray-50 rounded p-2 whitespace-pre-wrap max-h-60 overflow-y-auto text-gray-700">
                      {state.current_prompt}
                    </pre>
                    {onUpdatePrompt && (
                      <div className="flex justify-end">
                        <button
                          onClick={() => setPromptEditing(true)}
                          className="px-3 py-1 text-xs text-gray-600 bg-gray-100 rounded hover:bg-gray-200"
                        >
                          Edit
                        </button>
                      </div>
                    )}
                  </>
                )}
              </div>
            )}
          </div>

          {/* ============================================================= */}
          {/* Loading placeholder                                            */}
          {/* ============================================================= */}
          {isGenerating && !displayIteration && (
            <div className="bg-gray-100 rounded-lg aspect-video flex items-center justify-center">
              <div className="text-center">
                <div className="inline-block w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mb-2" />
                <p className="text-sm text-gray-500">Generating diagram...</p>
              </div>
            </div>
          )}

          {/* ============================================================= */}
          {/* 3. Image display area                                          */}
          {/* ============================================================= */}
          {displayIteration && (
            <>
              {displayIteration.image_urls && displayIteration.image_urls.length > 1 ? (
                /* -- Multi-variant grid -- */
                <>
                  <div className="grid grid-cols-2 gap-2">
                    {displayIteration.image_urls.map((url, idx) => (
                      <div
                        key={url}
                        className={`relative rounded-lg overflow-hidden border-2 cursor-pointer transition-all ${
                          idx === selectedVariant
                            ? 'border-blue-500 ring-2 ring-blue-300'
                            : 'border-gray-200 hover:border-gray-400'
                        }`}
                        onClick={() => setSelectedVariant(idx)}
                        onDoubleClick={() => setLightboxUrl(url)}
                      >
                        <img src={url} alt={`Variant ${idx + 1}`} className="w-full h-auto" />
                        <span className="absolute top-1 left-1 bg-black/60 text-white text-[10px] px-1.5 py-0.5 rounded">
                          V{idx + 1}
                        </span>
                        {idx === selectedVariant && (
                          <div className="absolute top-1 right-1 bg-blue-600 rounded-full p-0.5">
                            <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                  <p className="text-xs text-gray-500 text-center">
                    Selected: <span className="font-medium">Variant {selectedVariant + 1}</span>
                    <span className="text-gray-400 ml-2">(double-click to expand)</span>
                  </p>
                </>
              ) : (
                /* -- Single image -- */
                <div
                  className="rounded-lg overflow-hidden border cursor-pointer hover:ring-2 hover:ring-primary-400 transition-all"
                  onClick={() => setLightboxUrl(displayIteration.image_url)}
                >
                  <img
                    src={displayIteration.image_url}
                    alt={`Iteration ${displayIteration.iteration}`}
                    className="w-full h-auto"
                  />
                </div>
              )}

              {/* ========================================================= */}
              {/* 4. Evaluation section                                      */}
              {/* ========================================================= */}
              {displayIteration.overall_score != null && (
                <div className="bg-white rounded-lg border p-3">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Left: LLM Judge scores */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700">LLM Judge</span>
                        <span className={`text-lg font-bold ${scoreColor(displayIteration.overall_score)}`}>
                          {displayIteration.overall_score}/10
                        </span>
                      </div>
                      {displayIteration.scores &&
                        (Object.keys(SCORE_LABELS) as (keyof EvaluationScores)[]).map(key => (
                          <ScoreBar key={key} label={SCORE_LABELS[key]} value={displayIteration.scores![key]} />
                        ))}
                    </div>

                    {/* Right: User score */}
                    <div className="flex flex-col items-center justify-center border-l pl-4">
                      <span className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
                        Your score
                      </span>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => setUserScore(prev => Math.max(1, (prev ?? displayIteration.overall_score ?? 5) - 1))}
                          className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-100 hover:bg-gray-200 text-gray-700 text-lg font-bold"
                        >
                          -
                        </button>
                        <span className={`text-4xl font-bold tabular-nums ${scoreColor(effectiveScore ?? 0)}`}>
                          {effectiveScore ?? '-'}
                        </span>
                        <button
                          onClick={() => setUserScore(prev => Math.min(10, (prev ?? displayIteration.overall_score ?? 5) + 1))}
                          className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-100 hover:bg-gray-200 text-gray-700 text-lg font-bold"
                        >
                          +
                        </button>
                      </div>
                      {userScore !== null && userScore !== displayIteration.overall_score && (
                        <button
                          onClick={() => setUserScore(null)}
                          className="text-[10px] text-gray-400 hover:text-gray-600 mt-1"
                        >
                          Reset to LLM score
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Strengths / Issues / Improvements */}
              {(displayIteration.strengths.length > 0 ||
                displayIteration.issues.length > 0 ||
                displayIteration.improvements.length > 0) && (
                <div className="space-y-2">
                  <div className="grid grid-cols-2 gap-2">
                    {displayIteration.strengths.length > 0 && (
                      <div className="bg-green-50 rounded-lg p-3">
                        <h4 className="text-xs font-medium text-green-800 uppercase tracking-wide mb-1">
                          Strengths
                        </h4>
                        <ul className="text-xs text-green-700 space-y-0.5">
                          {displayIteration.strengths.map((s, i) => (
                            <li key={i}>- {s}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {displayIteration.issues.length > 0 && (
                      <div className="bg-amber-50 rounded-lg p-3">
                        <h4 className="text-xs font-medium text-amber-800 uppercase tracking-wide mb-1">
                          Issues
                        </h4>
                        <ul className="text-xs text-amber-700 space-y-0.5">
                          {displayIteration.issues.map((s, i) => (
                            <li key={i}>- {s}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  {displayIteration.improvements.length > 0 && (
                    <div className="bg-blue-50 rounded-lg p-3">
                      <h4 className="text-xs font-medium text-blue-800 uppercase tracking-wide mb-1">
                        Suggested improvements
                      </h4>
                      <ul className="text-xs text-blue-700 space-y-0.5">
                        {displayIteration.improvements.map((s, i) => (
                          <li key={i}>- {s}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </>
          )}

          {/* ============================================================= */}
          {/* 5. Feedback and actions section                                */}
          {/* ============================================================= */}
          <div className="space-y-2">
            <textarea
              value={feedback}
              onChange={e => setFeedback(e.target.value)}
              placeholder="Your feedback for the next iteration..."
              disabled={isBusy || !currentIteration}
              rows={3}
              className="w-full resize-y rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
            {/* Quick feedback buttons */}
            <div className="flex flex-wrap gap-1.5">
              {QUICK_FEEDBACK.map(text => (
                <button
                  key={text}
                  type="button"
                  onClick={() => appendFeedback(text)}
                  disabled={isBusy || !currentIteration}
                  className="px-2.5 py-1 text-[11px] rounded-full border border-gray-300 text-gray-600 hover:bg-gray-100 hover:border-gray-400 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                >
                  {text}
                </button>
              ))}
            </div>
          </div>

          {/* ============================================================= */}
          {/* 6. Generation presets row                                      */}
          {/* ============================================================= */}
          <div className="space-y-3">
            {/* Temperature presets */}
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1.5">Temperature</label>
              <div className="flex gap-1.5">
                {PRESETS.map(p => {
                  const isSelected = (genSettings.preset || 'balanced') === p.value;
                  return (
                    <button
                      key={p.value}
                      type="button"
                      onClick={() => updateSettings({ preset: p.value })}
                      disabled={isBusy}
                      className={`flex-1 px-2 py-1.5 text-xs rounded-full border transition-colors disabled:opacity-50 ${
                        isSelected ? PRESET_FILLED[p.color] : PRESET_OUTLINE[p.color]
                      }`}
                      title={`Temperature ${p.temp}`}
                    >
                      {p.name}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Image size, aspect ratio, variants */}
            <div className="flex gap-3 items-end flex-wrap">
              {/* Image size */}
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1">Size</label>
                <select
                  value={genSettings.image_size || '2K'}
                  onChange={e => updateSettings({ image_size: e.target.value })}
                  disabled={isBusy}
                  className="text-sm border border-gray-300 rounded px-2 py-1.5 focus:outline-none focus:ring-1 focus:ring-primary-500 disabled:opacity-50"
                >
                  {IMAGE_SIZES.map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>

              {/* Aspect ratio */}
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1">Ratio</label>
                <select
                  value={genSettings.aspect_ratio || '16:9'}
                  onChange={e => updateSettings({ aspect_ratio: e.target.value })}
                  disabled={isBusy}
                  className="text-sm border border-gray-300 rounded px-2 py-1.5 focus:outline-none focus:ring-1 focus:ring-primary-500 disabled:opacity-50"
                >
                  {ASPECT_RATIOS.map(r => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
              </div>

              {/* Variants */}
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1">Variants</label>
                <select
                  value={genSettings.num_variants || 1}
                  onChange={e => updateSettings({ num_variants: Number(e.target.value) })}
                  disabled={isBusy}
                  className="text-sm border border-gray-300 rounded px-2 py-1.5 focus:outline-none focus:ring-1 focus:ring-primary-500 disabled:opacity-50"
                >
                  {[1, 2, 3, 4].map(n => (
                    <option key={n} value={n}>{n}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* ============================================================= */}
          {/* 8. Iteration history (horizontal scroll)                       */}
          {/* ============================================================= */}
          {state.iterations.length > 0 && (
            <div>
              <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
                History
              </h4>
              <div className="flex gap-2 overflow-x-auto pb-2">
                {state.iterations.map((it, idx) => {
                  const isActive = idx === selectedHistoryIdx ||
                    (selectedHistoryIdx === -1 && it === currentIteration);
                  return (
                    <button
                      key={it.iteration}
                      onClick={() => setSelectedHistoryIdx(idx === selectedHistoryIdx ? -1 : idx)}
                      className={`flex-shrink-0 w-24 rounded-lg border overflow-hidden transition-all ${
                        isActive
                          ? 'border-primary-500 ring-2 ring-primary-300'
                          : 'border-gray-200 hover:border-gray-400'
                      }`}
                    >
                      {it.image_url && (
                        <img
                          src={it.image_url}
                          alt={`Iteration ${it.iteration}`}
                          className="w-full h-14 object-cover"
                        />
                      )}
                      <div className="px-1.5 py-1 text-center bg-white">
                        <span className="text-[10px] font-mono text-gray-600 block">
                          #{it.iteration}
                        </span>
                        <div className="flex justify-center gap-1 text-[10px]">
                          {it.overall_score != null && (
                            <span className={scoreColor(it.overall_score)}>
                              LLM:{it.overall_score}
                            </span>
                          )}
                          {it.user_feedback && (
                            <span className="text-gray-400" title="Has user feedback">*</span>
                          )}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

        </div>
      </div>

      {/* ================================================================= */}
      {/* 7. Action buttons (sticky at bottom)                              */}
      {/* ================================================================= */}
      <div className="border-t p-4 bg-white flex-shrink-0">
        <div className="flex gap-2">
          <button
            onClick={handleRefine}
            disabled={isBusy || !currentIteration || feedback.trim().length === 0}
            className="flex-1 px-4 py-2.5 text-sm font-medium bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isRefining ? 'Refining...' : isGenerating ? 'Generating...' : 'Refine & Generate'}
          </button>
          <button
            onClick={handleRegenerate}
            disabled={isBusy || !currentIteration}
            className="px-4 py-2.5 text-sm font-medium bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            title="Regenerate with current prompt and selected settings"
          >
            Retry
          </button>
          <button
            onClick={onAccept}
            disabled={isBusy || !currentIteration}
            className="px-4 py-2.5 text-sm font-medium bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Done
          </button>
        </div>
        {autoRefine && (
          <p className="text-[10px] text-primary-500 text-center mt-1.5 animate-pulse">
            Auto-refine active - will continue until score reaches 8+
          </p>
        )}
      </div>
    </div>
  );
}
