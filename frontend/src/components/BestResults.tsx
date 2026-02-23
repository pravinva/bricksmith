import { useEffect, useMemo, useState } from 'react';

import { resultsApi } from '../api/client';
import type { BestResultItem } from '../types';

// --- Types & constants ---

type GroupByMode = 'date' | 'run_group' | 'source';

const GROUP_BY_OPTIONS: { value: GroupByMode; label: string }[] = [
  { value: 'date', label: 'Date' },
  { value: 'run_group', label: 'Run group' },
  { value: 'source', label: 'Source type' },
];

interface ResultGroup {
  key: string;
  items: BestResultItem[];
  bestScore: number | null;
}

// --- Helpers ---

function sourceClass(source: BestResultItem['source']): string {
  if (source === 'chat') return 'bg-blue-100 text-blue-700';
  if (source === 'refine') return 'bg-purple-100 text-purple-700';
  if (source === 'generate_raw') return 'bg-green-100 text-green-700';
  return 'bg-gray-100 text-gray-700';
}

function friendlyDateLabel(isoString: string | undefined): string {
  if (!isoString) return 'Unknown date';
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return 'Unknown date';

  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const target = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  const diffDays = Math.round((today.getTime() - target.getTime()) / 86_400_000);

  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return target.toLocaleDateString('en-US', { weekday: 'long' });
  return target.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function getGroupKey(result: BestResultItem, mode: GroupByMode): string {
  if (mode === 'date') return friendlyDateLabel(result.created_at);
  if (mode === 'run_group') return (result.run_group && result.run_group.trim()) || 'Ungrouped';
  if (mode === 'source') return result.source || 'unknown';
  return 'Other';
}

function getGroupSortKey(result: BestResultItem, mode: GroupByMode): string {
  if (mode === 'date') {
    if (!result.created_at) return '9999-99-99';
    return result.created_at.slice(0, 10);
  }
  if (mode === 'run_group') {
    const key = (result.run_group && result.run_group.trim()) || '';
    return key === '' ? '\uffff' : key.toLowerCase();
  }
  if (mode === 'source') {
    const s = result.source || 'unknown';
    return s === 'unknown' ? '\uffff' : s;
  }
  return '';
}

function ChevronIcon({ expanded }: { expanded: boolean }) {
  return (
    <svg
      className={`w-4 h-4 text-gray-500 transition-transform ${expanded ? 'rotate-90' : ''}`}
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
    </svg>
  );
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
  const [groupBy, setGroupBy] = useState<GroupByMode>('date');
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(new Set());
  const [editingRunGroup, setEditingRunGroup] = useState(false);
  const [runGroupDraft, setRunGroupDraft] = useState('');
  const [isSavingRunGroup, setIsSavingRunGroup] = useState(false);

  const selected = useMemo(
    () => results.find((result) => result.result_id === selectedId) || null,
    [results, selectedId]
  );

  // Reset run group editing when selection changes
  useEffect(() => {
    setEditingRunGroup(false);
  }, [selectedId]);

  const groupedResults = useMemo<ResultGroup[]>(() => {
    const groupMap = new Map<string, { items: BestResultItem[]; sortKey: string }>();
    for (const result of results) {
      const key = getGroupKey(result, groupBy);
      const existing = groupMap.get(key);
      if (existing) {
        existing.items.push(result);
        const sk = getGroupSortKey(result, groupBy);
        if (sk < existing.sortKey) existing.sortKey = sk;
      } else {
        groupMap.set(key, { items: [result], sortKey: getGroupSortKey(result, groupBy) });
      }
    }

    const sorted = Array.from(groupMap.entries()).sort(([, a], [, b]) => {
      if (groupBy === 'date') return a.sortKey > b.sortKey ? -1 : a.sortKey < b.sortKey ? 1 : 0;
      return a.sortKey < b.sortKey ? -1 : a.sortKey > b.sortKey ? 1 : 0;
    });

    return sorted.map(([key, { items }]) => {
      const scores = items.map((r) => r.score).filter((s): s is number => s !== undefined);
      return { key, items, bestScore: scores.length > 0 ? Math.max(...scores) : null };
    });
  }, [results, groupBy]);

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

  // Reset collapse state when grouping mode or results change: first group expanded, rest collapsed
  useEffect(() => {
    if (groupedResults.length <= 1) {
      setCollapsedGroups(new Set());
    } else {
      setCollapsedGroups(new Set(groupedResults.slice(1).map((g) => g.key)));
    }
  }, [groupBy, results.length]); // eslint-disable-line react-hooks/exhaustive-deps

  const toggleGroup = (key: string) => {
    setCollapsedGroups((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  const refreshWithPrompt = async (result: BestResultItem) => {
    if (result.full_prompt) return;
    await loadResults(true);
  };

  const copyPrompt = async () => {
    if (!selected?.full_prompt) return;
    await navigator.clipboard.writeText(selected.full_prompt);
    setInfo('Prompt copied to clipboard.');
  };

  const saveRunGroup = async () => {
    if (!selected || isSavingRunGroup) return;
    const newValue = runGroupDraft.trim() || undefined;
    // Skip save if value hasn't changed
    if ((newValue || '') === (selected.run_group || '')) {
      setEditingRunGroup(false);
      return;
    }
    setIsSavingRunGroup(true);
    try {
      const updated = await resultsApi.updateResult(selected.result_id, {
        run_group: newValue,
      });
      setResults((prev) =>
        prev.map((r) => (r.result_id === updated.result_id ? updated : r))
      );
      setEditingRunGroup(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save run group');
    } finally {
      setIsSavingRunGroup(false);
    }
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
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-gray-900">Ranked Results</h3>
            <select
              value={groupBy}
              onChange={(e) => setGroupBy(e.target.value as GroupByMode)}
              className="border rounded px-2 py-1 text-xs text-gray-700"
            >
              {GROUP_BY_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          {results.length === 0 ? (
            <p className="text-sm text-gray-500">No ranked results found.</p>
          ) : (
            <div className="space-y-2">
              {groupedResults.map((group) => {
                const expanded = !collapsedGroups.has(group.key);
                return (
                  <div key={group.key}>
                    <button
                      onClick={() => toggleGroup(group.key)}
                      className="w-full flex items-center gap-2 py-1.5 px-1 rounded hover:bg-gray-50 text-left"
                    >
                      <ChevronIcon expanded={expanded} />
                      <span className="text-xs font-semibold uppercase tracking-wide text-gray-500 flex-1 truncate">
                        {group.key} ({group.items.length})
                      </span>
                      {group.bestScore !== null && (
                        <span className="text-xs px-1.5 py-0.5 rounded bg-green-100 text-green-700 font-medium">
                          {group.bestScore}
                        </span>
                      )}
                    </button>
                    {expanded && (
                      <ul className="space-y-2 mt-1">
                        {group.items.map((result) => (
                          <li
                            key={result.result_id}
                            onClick={() => setSelectedId(result.result_id)}
                            className={`border rounded p-2 cursor-pointer flex gap-3 ${
                              selectedId === result.result_id
                                ? 'border-primary-500 bg-primary-50'
                                : 'hover:bg-gray-50'
                            }`}
                          >
                            {result.image_url ? (
                              <img
                                src={result.image_url}
                                alt=""
                                className="w-10 h-10 rounded object-cover flex-shrink-0"
                              />
                            ) : (
                              <div className="w-10 h-10 rounded bg-gray-100 flex items-center justify-center flex-shrink-0">
                                <svg
                                  className="w-5 h-5 text-gray-400"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={1.5}
                                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                                  />
                                </svg>
                              </div>
                            )}
                            <div className="min-w-0 flex-1">
                              <div className="flex items-center justify-between gap-2">
                                <span className="text-sm font-medium text-gray-900 truncate">
                                  {result.title}
                                </span>
                                <span
                                  className={`px-2 py-0.5 text-xs rounded flex-shrink-0 ${sourceClass(
                                    result.source
                                  )}`}
                                >
                                  {result.source}
                                </span>
                              </div>
                              <div className="mt-0.5 text-xs text-gray-600">
                                Score:{' '}
                                <span className="font-semibold">
                                  {result.score !== undefined ? result.score : 'N/A'}
                                </span>
                                {result.score_source ? ` (${result.score_source})` : ''}
                              </div>
                              <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">
                                {result.prompt_preview}
                              </p>
                            </div>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                );
              })}
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
                    {editingRunGroup ? (
                      <div className="flex items-center gap-1">
                        <input
                          autoFocus
                          value={runGroupDraft}
                          onChange={(e) => setRunGroupDraft(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') void saveRunGroup();
                            if (e.key === 'Escape') setEditingRunGroup(false);
                          }}
                          onBlur={() => void saveRunGroup()}
                          className="border rounded px-1.5 py-0.5 text-xs w-32"
                          placeholder="Group name..."
                          disabled={isSavingRunGroup}
                        />
                        {isSavingRunGroup && (
                          <svg className="w-3 h-3 animate-spin text-gray-400" viewBox="0 0 24 24" fill="none">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                          </svg>
                        )}
                      </div>
                    ) : (
                      <button
                        onClick={() => {
                          setRunGroupDraft(selected.run_group || '');
                          setEditingRunGroup(true);
                        }}
                        className="text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded px-1.5 py-0.5 text-sm transition-colors"
                        title="Click to edit run group"
                      >
                        {selected.run_group || 'Ungrouped'}
                      </button>
                    )}
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
