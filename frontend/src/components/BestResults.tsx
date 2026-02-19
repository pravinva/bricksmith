import { useEffect, useMemo, useState } from 'react';

import { cliApi, resultsApi } from '../api/client';
import type { BestResultItem } from '../types';

function sourceClass(source: BestResultItem['source']): string {
  if (source === 'chat') return 'bg-blue-100 text-blue-700';
  if (source === 'refine') return 'bg-purple-100 text-purple-700';
  if (source === 'generate_raw') return 'bg-green-100 text-green-700';
  return 'bg-gray-100 text-gray-700';
}

interface BestResultsProps {
  onCreateArchitectSessionFromResult?: (result: BestResultItem) => Promise<void>;
  onOpenCliMirror?: () => void;
}

export function BestResults({
  onCreateArchitectSessionFromResult,
  onOpenCliMirror,
}: BestResultsProps) {
  const [results, setResults] = useState<BestResultItem[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [query, setQuery] = useState<string>('');
  const [minScore, setMinScore] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const [logoDir, setLogoDir] = useState<string>('logos/default');
  const [logoFilesText, setLogoFilesText] = useState<string>('');
  const [brandingFile, setBrandingFile] = useState<string>('prompts/branding/minimal.txt');
  const [runName, setRunName] = useState<string>('');
  const [tagsText, setTagsText] = useState<string>('');
  const [temperature, setTemperature] = useState<string>('0.8');
  const [topP, setTopP] = useState<string>('0.95');
  const [topK, setTopK] = useState<string>('50');
  const [presencePenalty, setPresencePenalty] = useState<string>('0.1');
  const [frequencyPenalty, setFrequencyPenalty] = useState<string>('0.1');
  const [systemInstruction, setSystemInstruction] = useState<string>('');
  const [count, setCount] = useState<string>('1');
  const [size, setSize] = useState<string>('1K');
  const [aspectRatio, setAspectRatio] = useState<string>('16:9');
  const [avoid, setAvoid] = useState<string>('');
  const [feedbackEnabled, setFeedbackEnabled] = useState<boolean>(false);
  const [databricksStyle, setDatabricksStyle] = useState<boolean>(false);

  const selected = useMemo(
    () => results.find((result) => result.result_id === selectedId) || null,
    [results, selectedId]
  );

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

  const refreshWithPrompt = async (result: BestResultItem) => {
    if (result.full_prompt) return;
    await loadResults(true);
  };

  const copyPrompt = async () => {
    if (!selected?.full_prompt) return;
    await navigator.clipboard.writeText(selected.full_prompt);
    setInfo('Prompt copied to clipboard.');
  };

  const createChatJobFromPrompt = async () => {
    if (!selected?.prompt_path) {
      setError('No prompt file available for this result.');
      return;
    }

    setError(null);
    setInfo(null);
    try {
      const response = await cliApi.startJob({
        command: 'chat',
        args: ['--prompt-file', selected.prompt_path],
      });
      setInfo(
        `Started chat job ${response.job.job_id}. Open the CLI Mirror tab to monitor output.`
      );
      onOpenCliMirror?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start chat job');
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

  const generateRawFromPrompt = async () => {
    if (!selected?.prompt_path) {
      setError('No prompt file available for this result.');
      return;
    }

    const resolvedRunName =
      runName.trim() || selected.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 50);

    const parsedTemperature = Number.parseFloat(temperature);
    const parsedTopP = Number.parseFloat(topP);
    const parsedTopK = Number.parseInt(topK, 10);
    const parsedPresencePenalty = Number.parseFloat(presencePenalty);
    const parsedFrequencyPenalty = Number.parseFloat(frequencyPenalty);
    const parsedCount = Number.parseInt(count, 10);

    if (
      Number.isNaN(parsedTemperature) ||
      Number.isNaN(parsedTopP) ||
      Number.isNaN(parsedTopK) ||
      Number.isNaN(parsedPresencePenalty) ||
      Number.isNaN(parsedFrequencyPenalty) ||
      Number.isNaN(parsedCount)
    ) {
      setError('Invalid numeric values in generate-raw fields.');
      return;
    }

    const args: string[] = ['--prompt-file', selected.prompt_path];
    const logoFiles = logoFilesText
      .split('\n')
      .map((line) => line.trim())
      .filter((line) => line.length > 0);

    if (logoFiles.length > 0) {
      logoFiles.forEach((logoPath) => {
        args.push('--logo', logoPath);
      });
    } else {
      args.push('--logo-dir', logoDir.trim() || 'logos/default');
    }

    if (brandingFile.trim()) {
      args.push('--branding', brandingFile.trim());
    }

    args.push('--run-name', resolvedRunName);

    const tags = tagsText
      .split('\n')
      .map((line) => line.trim())
      .filter((line) => line.length > 0);
    tags.forEach((tag) => {
      args.push('--tag', tag);
    });

    args.push(
      '--temperature',
      String(parsedTemperature),
      '--top-p',
      String(parsedTopP),
      '--top-k',
      String(parsedTopK),
      '--presence-penalty',
      String(parsedPresencePenalty),
      '--frequency-penalty',
      String(parsedFrequencyPenalty),
      '--count',
      String(parsedCount),
      '--size',
      size,
      '--aspect-ratio',
      aspectRatio
    );

    if (systemInstruction.trim()) {
      args.push('--system-instruction', systemInstruction.trim());
    }

    if (avoid.trim()) {
      args.push('--avoid', avoid.trim());
    }

    if (feedbackEnabled) {
      args.push('--feedback');
    }

    if (databricksStyle) {
      args.push('--databricks-style');
    }

    setError(null);
    setInfo(null);
    try {
      const response = await cliApi.startJob({
        command: 'generate-raw',
        args,
      });
      setInfo(
        `Started generate-raw job ${response.job.job_id}. Open CLI Mirror to monitor generation.`
      );
      onOpenCliMirror?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start generate-raw job');
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
            <ul className="space-y-2">
              {results.map((result) => (
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
                    <p className="text-gray-500">{selected.run_id || 'No run id'}</p>
                  </div>
                </div>

                {selected.image_url ? (
                  <img
                    src={selected.image_url}
                    alt={selected.title}
                    className="mt-4 border rounded w-full h-auto"
                  />
                ) : (
                  <p className="mt-4 text-sm text-gray-500">No image found for this result.</p>
                )}

                <div className="mt-4 flex flex-wrap gap-2">
                  <button
                    onClick={() => void createChatJobFromPrompt()}
                    disabled={!selected.prompt_path}
                    className="px-3 py-2 text-sm bg-primary-600 text-white rounded hover:bg-primary-700 disabled:opacity-50"
                  >
                    Create Chat Job from Prompt
                  </button>
                  <button
                    onClick={() => void createArchitectSessionFromResult()}
                    className="px-3 py-2 text-sm bg-gray-100 text-gray-800 rounded hover:bg-gray-200"
                  >
                    Create Architect Session from Result
                  </button>
                </div>

                <div className="mt-4 border rounded p-3 bg-gray-50">
                  <p className="text-sm font-medium text-gray-900 mb-2">
                    Generate Raw from this Prompt
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Logo directory</label>
                      <input
                        value={logoDir}
                        onChange={(e) => setLogoDir(e.target.value)}
                        placeholder="logos/default"
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Branding file</label>
                      <input
                        value={brandingFile}
                        onChange={(e) => setBrandingFile(e.target.value)}
                        placeholder="prompts/branding/minimal.txt"
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Run name</label>
                      <input
                        value={runName}
                        onChange={(e) => setRunName(e.target.value)}
                        placeholder="optional, auto-derived if empty"
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Temperature</label>
                      <input
                        value={temperature}
                        onChange={(e) => setTemperature(e.target.value)}
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Top P</label>
                      <input
                        value={topP}
                        onChange={(e) => setTopP(e.target.value)}
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Top K</label>
                      <input
                        value={topK}
                        onChange={(e) => setTopK(e.target.value)}
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">
                        Presence penalty
                      </label>
                      <input
                        value={presencePenalty}
                        onChange={(e) => setPresencePenalty(e.target.value)}
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">
                        Frequency penalty
                      </label>
                      <input
                        value={frequencyPenalty}
                        onChange={(e) => setFrequencyPenalty(e.target.value)}
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Count</label>
                      <input
                        value={count}
                        onChange={(e) => setCount(e.target.value)}
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Size</label>
                      <select
                        value={size}
                        onChange={(e) => setSize(e.target.value)}
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      >
                        <option value="1K">1K</option>
                        <option value="2K">2K</option>
                        <option value="4K">4K</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Aspect ratio</label>
                      <select
                        value={aspectRatio}
                        onChange={(e) => setAspectRatio(e.target.value)}
                        className="w-full border rounded px-2 py-1.5 text-sm"
                      >
                        <option value="1:1">1:1</option>
                        <option value="4:3">4:3</option>
                        <option value="16:9">16:9</option>
                        <option value="9:16">9:16</option>
                        <option value="3:4">3:4</option>
                        <option value="21:9">21:9</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-2">
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">
                        Logos (one file path per line, optional)
                      </label>
                      <textarea
                        value={logoFilesText}
                        onChange={(e) => setLogoFilesText(e.target.value)}
                        placeholder="logos/default/databricks-full.png"
                        rows={3}
                        className="w-full border rounded px-2 py-1.5 text-sm font-mono"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">
                        Tags (one key=value per line, optional)
                      </label>
                      <textarea
                        value={tagsText}
                        onChange={(e) => setTagsText(e.target.value)}
                        placeholder="customer=nab"
                        rows={3}
                        className="w-full border rounded px-2 py-1.5 text-sm font-mono"
                      />
                    </div>
                  </div>

                  <div className="mt-2">
                    <label className="block text-xs text-gray-600 mb-1">
                      System instruction (optional)
                    </label>
                    <textarea
                      value={systemInstruction}
                      onChange={(e) => setSystemInstruction(e.target.value)}
                      rows={2}
                      className="w-full border rounded px-2 py-1.5 text-sm"
                    />
                  </div>

                  <div className="mt-2">
                    <label className="block text-xs text-gray-600 mb-1">Avoid (optional)</label>
                    <input
                      value={avoid}
                      onChange={(e) => setAvoid(e.target.value)}
                      placeholder="blurry, spelling errors"
                      className="w-full border rounded px-2 py-1.5 text-sm"
                    />
                  </div>

                  <div className="mt-2 flex gap-4">
                    <label className="text-xs text-gray-700 flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={feedbackEnabled}
                        onChange={(e) => setFeedbackEnabled(e.target.checked)}
                      />
                      Enable feedback prompt
                    </label>
                    <label className="text-xs text-gray-700 flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={databricksStyle}
                        onChange={(e) => setDatabricksStyle(e.target.checked)}
                      />
                      Use Databricks style
                    </label>
                  </div>
                  <button
                    onClick={() => void generateRawFromPrompt()}
                    disabled={!selected.prompt_path}
                    className="mt-3 px-3 py-2 text-sm bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
                  >
                    Run generate-raw
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
                <pre className="bg-gray-900 text-gray-100 rounded p-3 text-xs overflow-auto max-h-96 whitespace-pre-wrap">
                  {selected.full_prompt || selected.prompt_preview || '(no prompt text)'}
                </pre>
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
