/**
 * Panel that displays diagram refinement loop: generated image, evaluation scores,
 * feedback input, and iteration history.
 */

import { useState } from 'react';
import type {
  RefinementState,
  RefinementIteration,
  EvaluationScores,
  GenerationSettingsRequest,
} from '../types';
import { GenerationSettingsPanel } from './GenerationSettings';

interface RefinementPanelProps {
  state: RefinementState;
  currentIteration: RefinementIteration | null;
  isGenerating: boolean;
  isRefining: boolean;
  error: string | null;
  onRefine: (feedback: string, settings?: GenerationSettingsRequest) => Promise<void>;
  onAccept: () => void;
  onRegenerate: (settings?: GenerationSettingsRequest) => Promise<void>;
  onClearError: () => void;
}

const SCORE_LABELS: Record<keyof EvaluationScores, string> = {
  information_hierarchy: 'Info Hierarchy',
  technical_accuracy: 'Technical Acc.',
  logo_fidelity: 'Logo Fidelity',
  visual_clarity: 'Visual Clarity',
  data_flow_legibility: 'Data Flow',
  text_readability: 'Text Readability',
};

function ScoreBar({ label, value }: { label: string; value: number }) {
  const pct = (value / 10) * 100;
  const color =
    value >= 8 ? 'bg-green-500' : value >= 6 ? 'bg-yellow-500' : 'bg-red-500';

  return (
    <div className="flex items-center gap-2 text-sm">
      <span className="w-28 text-gray-600 truncate" title={label}>
        {label}
      </span>
      <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="w-6 text-right font-mono text-gray-700">{value}</span>
    </div>
  );
}

function IterationHistory({
  iterations,
  selectedIndex,
  onSelect,
}: {
  iterations: RefinementIteration[];
  selectedIndex: number;
  onSelect: (idx: number) => void;
}) {
  if (iterations.length <= 1) return null;

  return (
    <div>
      <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
        History
      </h4>
      <div className="flex gap-1.5 flex-wrap">
        {iterations.map((it, idx) => (
          <button
            key={it.iteration}
            onClick={() => onSelect(idx)}
            className={`px-2.5 py-1 text-xs rounded font-mono ${
              idx === selectedIndex
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            #{it.iteration}
            {it.overall_score != null && `:${it.overall_score}`}
          </button>
        ))}
      </div>
    </div>
  );
}

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
}: RefinementPanelProps) {
  const [feedback, setFeedback] = useState('');
  const [selectedIdx, setSelectedIdx] = useState(-1);
  const [imageExpanded, setImageExpanded] = useState(false);
  const [genSettings, setGenSettings] = useState<GenerationSettingsRequest>({
    preset: 'balanced',
    image_size: '2K',
    aspect_ratio: '16:9',
    num_variants: 1,
  });

  const isBusy = isGenerating || isRefining;

  // Show selected iteration or latest
  const displayIteration =
    selectedIdx >= 0 && selectedIdx < state.iterations.length
      ? state.iterations[selectedIdx]
      : currentIteration;

  const handleRefine = async () => {
    if (isBusy) return;
    const text = feedback.trim();
    setFeedback('');
    setSelectedIdx(-1);
    await onRefine(text || '', genSettings);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleRefine();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="px-4 py-3 border-b bg-white">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-gray-900">
            Diagram refinement
            {displayIteration && (
              <span className="text-gray-500 font-normal">
                {' '}- iteration {displayIteration.iteration}
              </span>
            )}
          </h3>
          {isBusy && (
            <span className="text-xs text-primary-600 animate-pulse">
              {isGenerating ? 'Generating...' : 'Refining...'}
            </span>
          )}
        </div>
      </div>

      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-sm">
            <div className="flex justify-between items-start">
              <p className="text-red-800">{error}</p>
              <button
                onClick={onClearError}
                className="text-red-400 hover:text-red-600 ml-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        )}

        {/* Loading placeholder */}
        {isGenerating && !displayIteration && (
          <div className="bg-gray-100 rounded-lg aspect-video flex items-center justify-center">
            <div className="text-center">
              <div className="inline-block w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mb-2" />
              <p className="text-sm text-gray-500">Generating diagram...</p>
            </div>
          </div>
        )}

        {/* Generated image(s) */}
        {displayIteration && (
          <>
            {displayIteration.image_urls && displayIteration.image_urls.length > 1 ? (
              <div className="grid grid-cols-2 gap-2">
                {displayIteration.image_urls.map((url, idx) => (
                  <div
                    key={url}
                    className="relative rounded-lg overflow-hidden border cursor-pointer hover:ring-2 hover:ring-primary-400"
                    onClick={() => setImageExpanded(true)}
                  >
                    <img src={url} alt={`Variant ${idx + 1}`} className="w-full h-auto" />
                    <span className="absolute top-1 left-1 bg-black/60 text-white text-[10px] px-1.5 py-0.5 rounded">
                      V{idx + 1}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div
                className={`rounded-lg overflow-hidden border cursor-pointer transition-all ${
                  imageExpanded ? 'fixed inset-4 z-50 bg-white shadow-2xl' : ''
                }`}
                onClick={() => setImageExpanded(!imageExpanded)}
              >
                <img
                  src={displayIteration.image_url}
                  alt={`Iteration ${displayIteration.iteration}`}
                  className="w-full h-auto"
                />
              </div>
            )}
            {imageExpanded && (
              <div
                className="fixed inset-0 bg-black/30 z-40"
                onClick={() => setImageExpanded(false)}
              />
            )}

            {/* Scores */}
            {displayIteration.overall_score != null && (
              <div className="bg-white rounded-lg border p-3 space-y-2">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">Overall</span>
                  <span
                    className={`text-lg font-bold ${
                      displayIteration.overall_score >= 8
                        ? 'text-green-600'
                        : displayIteration.overall_score >= 6
                        ? 'text-yellow-600'
                        : 'text-red-600'
                    }`}
                  >
                    {displayIteration.overall_score}/10
                  </span>
                </div>
                {displayIteration.scores &&
                  (Object.keys(SCORE_LABELS) as (keyof EvaluationScores)[]).map(
                    (key) => (
                      <ScoreBar
                        key={key}
                        label={SCORE_LABELS[key]}
                        value={displayIteration.scores![key]}
                      />
                    ),
                  )}
              </div>
            )}

            {/* Strengths and issues */}
            {(displayIteration.strengths.length > 0 ||
              displayIteration.issues.length > 0) && (
              <div className="grid grid-cols-2 gap-3">
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
            )}

            {/* Improvements */}
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
          </>
        )}

        {/* Iteration history */}
        <IterationHistory
          iterations={state.iterations}
          selectedIndex={selectedIdx}
          onSelect={setSelectedIdx}
        />

        {/* Generation settings */}
        <GenerationSettingsPanel
          settings={genSettings}
          onChange={setGenSettings}
          disabled={isBusy}
          showVariants
        />
      </div>

      {/* Action bar */}
      <div className="border-t p-4 bg-white space-y-3">
        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Your feedback (optional) - press Enter to refine"
          disabled={isBusy || !currentIteration}
          rows={2}
          className="w-full resize-none rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
        <div className="flex gap-2">
          <button
            onClick={handleRefine}
            disabled={isBusy || !currentIteration}
            className="flex-1 px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isRefining ? 'Refining...' : isGenerating ? 'Generating...' : 'Refine & Regenerate'}
          </button>
          <button
            onClick={() => onRegenerate(genSettings)}
            disabled={isBusy || !currentIteration}
            className="px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Regenerate without changing the prompt"
          >
            Regenerate
          </button>
          <button
            onClick={onAccept}
            disabled={isBusy || !currentIteration}
            className="px-3 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Accept
          </button>
        </div>
      </div>
    </div>
  );
}
