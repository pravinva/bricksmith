import { useEffect, useMemo, useState } from 'react';

import { resultsApi } from '../api/client';
import type { BestResultItem } from '../types';

function sourceClass(source: BestResultItem['source']): string {
  if (source === 'chat') return 'bg-blue-100 text-blue-700';
  if (source === 'refine') return 'bg-purple-100 text-purple-700';
  if (source === 'generate_raw') return 'bg-green-100 text-green-700';
  return 'bg-gray-100 text-gray-700';
}

interface BestResultsProps {
  onCreateArchitectSessionFromResult?: (result: BestResultItem) => Promise<void>;
}

export function BestResults({
  onCreateArchitectSessionFromResult,
}: BestResultsProps) {
  const [results, setResults] = useState<BestResultItem[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [query, setQuery] = useState<string>('');
  const [minScore, setMinScore] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const [isFullscreenOpen, setIsFullscreenOpen] = useState<boolean>(false);

  const selected = useMemo(
    () => results.find((result) => result.result_id === selectedId) || null,
    [results, selectedId]
  );

  const groupedResults = useMemo(() => {
    const groups = new Map<string, BestResultItem[]>();
    for (const result of results) {
      const key = (result.run_group && result.run_group.trim()) || 'Ungrouped';
      const existing = groups.get(key);
      if (existing) {
        existing.push(result);
      } else {
        groups.set(key, [result]);
      }
    }
    return Array.from(groups.entries());
  }, [results]);

  const loadResults = async (includePrompt: boolean) => {
    setIsLoading(true);
    setError(null);
    try {
      const parsedMinScore =
        minScore.trim() === '' ? undefined : Number.parseFloat(minScore);
      const response = await resultsApi.listBest(
        60,
        query.trim() || undefined,
        Number.isNaN(parsedMinScore ?? Number.NaN) ? undefined : parsedMinScore,
        includePrompt
      );
      setResults(response.results);
      if (response.results.length > 0) {
        setSelectedId((prev) =>
          prev && response.results.some((item) => item.result_id === prev)
            ? prev
            : response.results[0].result_id
        );
      } else {
        setSelectedId(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load results');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void loadResults(false);
  }, []);

  useEffect(() => {
    if (!isFullscreenOpen) return;

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsFullscreenOpen(false);
      }
    };

    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [isFullscreenOpen]);

  const refreshWithPrompt = async (result: BestResultItem) => {
    if (result.full_prompt) return;
    await loadResults(true);
  };

  const copyPrompt = async () => {
    if (!selected?.full_prompt) return;
    await navigator.clipboard.writeText(selected.full_prompt);
    setInfo('Prompt copied to clipboard.');
  };

  const createArchitectSessionFromResult = async () => {
    if (!selected || !onCreateArchitectSessionFromResult) return;
    setError(null);
    setInfo(null);
    try {
      await onCreateArchitectSessionFromResult(selected);
      setInfo('Created architect session from selected result.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create architect session');
    }
  };

  return (
    <div className="h-full flex flex-col bg-gray-50">
      <header className="bg-white border-b px-6 py-3">
        <h2 className="text-lg font-semibold text-gray-900">Best Results Explorer</h2>
        <p className="text-sm text-gray-500">
          Find top architecture images and the exact prompts used to generate them.
        </p>
      </header>

      <div className="bg-white border-b px-6 py-3 flex flex-wrap gap-3 items-end">
        <div>
          <label className="block text-xs text-gray-600 mb-1">Search</label>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="customer, run id, prompt keywords..."
            className="border rounded px-3 py-2 text-sm w-80"
          />
        </div>
        <div>
          <label className="block text-xs text-gray-600 mb-1">Min score</label>
          <input
            value={minScore}
            onChange={(e) => setMinScore(e.target.value)}
            placeholder="e.g. 6"
            className="border rounded px-3 py-2 text-sm w-24"
          />
        </div>
        <button
          onClick={() => void loadResults(false)}
          className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
          disabled={isLoading}
        >
          {isLoading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border-b border-red-200 px-6 py-2 text-sm text-red-700">
          {error}
        </div>
      )}
      {info && (
        <div className="bg-blue-50 border-b border-blue-200 px-6 py-2 text-sm text-blue-700">
          {info}
        </div>
      )}

      <div className="flex-1 min-h-0 grid grid-cols-1 lg:grid-cols-3">
        <section className="bg-white border-r p-4 overflow-y-auto">
          <h3 className="font-medium text-gray-900 mb-3">Ranked Results</h3>
          {results.length === 0 ? (
            <p className="text-sm text-gray-500">No ranked results found.</p>
          ) : (
            <div className="space-y-3">
              {groupedResults.map(([groupName, groupItems]) => (
                <div key={groupName} className="space-y-2">
                  <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                    {groupName} ({groupItems.length})
                  </p>
                  <ul className="space-y-2">
                    {groupItems.map((result) => (
                      <li
                        key={result.result_id}
                        onClick={() => setSelectedId(result.result_id)}
                        className={`border rounded p-3 cursor-pointer ${
                          selectedId === result.result_id
                            ? 'border-primary-500 bg-primary-50'
                            : 'hover:bg-gray-50'
                        }`}
                      >
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-sm font-medium text-gray-900 truncate">
                            {result.title}
                          </span>
                          <span
                            className={`px-2 py-0.5 text-xs rounded ${sourceClass(
                              result.source
                            )}`}
                          >
                            {result.source}
                          </span>
                        </div>
                        <div className="mt-1 text-xs text-gray-600">
                          Score:{' '}
                          <span className="font-semibold">
                            {result.score !== undefined ? result.score : 'N/A'}
                          </span>
                          {result.score_source ? ` (${result.score_source})` : ''}
                        </div>
                        <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                          {result.prompt_preview}
                        </p>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="lg:col-span-2 p-4 overflow-y-auto">
          {!selected ? (
            <p className="text-sm text-gray-500">Select a result to inspect details.</p>
          ) : (
            <div className="space-y-4">
              <div className="bg-white rounded border p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{selected.title}</h3>
                    <p className="text-sm text-gray-500">
                      {selected.created_at
                        ? new Date(selected.created_at).toLocaleString()
                        : 'Unknown time'}
                    </p>
                  </div>
                  <div className="text-sm text-right">
                    <p>
                      Score:{' '}
                      <span className="font-semibold">
                        {selected.score !== undefined ? selected.score : 'N/A'}
                      </span>
                    </p>
                    <p className="text-gray-500">{selected.run_group || 'Ungrouped'}</p>
                    <p className="text-gray-500">{selected.run_id || 'No run id'}</p>
                  </div>
                </div>

                {selected.image_url ? (
                  <div className="mt-4">
                    <div className="flex justify-end mb-2">
                      <button
                        onClick={() => setIsFullscreenOpen(true)}
                        className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
                      >
                        Fullscreen
                      </button>
                    </div>
                    <img
                      src={selected.image_url}
                      alt={selected.title}
                      className="border rounded w-full h-auto cursor-zoom-in hover:opacity-95 transition-opacity"
                      onClick={() => setIsFullscreenOpen(true)}
                    />
                  </div>
                ) : (
                  <p className="mt-4 text-sm text-gray-500">No image found for this result.</p>
                )}

                <div className="mt-4">
                  <button
                    onClick={() => void createArchitectSessionFromResult()}
                    className="px-3 py-2 text-sm bg-primary-600 text-white rounded hover:bg-primary-700"
                  >
                    Open in Architect Studio
                  </button>
                </div>
              </div>

              <div className="bg-white rounded border p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900">Prompt</h4>
                  <div className="flex gap-2">
                    <button
                      onClick={() => void refreshWithPrompt(selected)}
                      className="px-3 py-1 text-xs bg-gray-100 rounded hover:bg-gray-200"
                    >
                      Load Full Prompt
                    </button>
                    <button
                      onClick={() => void copyPrompt()}
                      disabled={!selected.full_prompt}
                      className="px-3 py-1 text-xs bg-primary-600 text-white rounded hover:bg-primary-700 disabled:opacity-50"
                    >
                      Copy Prompt
                    </button>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mb-2">
                  {selected.prompt_path || 'Prompt path unavailable'}
                </p>
                <pre className="bg-gray-900 text-gray-100 rounded p-3 text-xs overflow-auto max-h-96 whitespace-pre-wrap">{selected.full_prompt || selected.prompt_preview || '(no prompt text)'}</pre>
              </div>
            </div>
          )}
        </section>
      </div>

      {isFullscreenOpen && selected?.image_url && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
          onClick={() => setIsFullscreenOpen(false)}
        >
          <button
            onClick={() => setIsFullscreenOpen(false)}
            className="absolute top-4 right-4 text-white hover:text-gray-300"
            title="Close fullscreen"
          >
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
          <img
            src={selected.image_url}
            alt={selected.title}
            className="max-w-full max-h-full object-contain"
            onClick={(event) => event.stopPropagation()}
          />
        </div>
      )}
    </div>
  );
}
