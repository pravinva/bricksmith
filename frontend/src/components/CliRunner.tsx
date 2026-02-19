import { useEffect, useMemo, useState } from 'react';

import { cliApi } from '../api/client';
import type { CLICommandSpec, CliJob } from '../types';

function statusClass(status: CliJob['status']): string {
  if (status === 'succeeded') return 'bg-green-100 text-green-800';
  if (status === 'running' || status === 'queued') return 'bg-blue-100 text-blue-800';
  if (status === 'cancelled' || status === 'timeout') return 'bg-yellow-100 text-yellow-800';
  return 'bg-red-100 text-red-800';
}

export function CliRunner() {
  const [commands, setCommands] = useState<CLICommandSpec[]>([]);
  const [jobs, setJobs] = useState<CliJob[]>([]);
  const [selectedCommand, setSelectedCommand] = useState<string>('');
  const [argsInput, setArgsInput] = useState<string>('');
  const [stdinText, setStdinText] = useState<string>('');
  const [timeoutSeconds, setTimeoutSeconds] = useState<number>(1800);
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const selectedCommandSpec = useMemo(
    () => commands.find((c) => c.name === selectedCommand) || null,
    [commands, selectedCommand]
  );

  const selectedJob = useMemo(
    () => jobs.find((j) => j.job_id === selectedJobId) || null,
    [jobs, selectedJobId]
  );

  const loadCommands = async () => {
    try {
      const response = await cliApi.listCommands();
      setCommands(response.commands);
      if (!selectedCommand && response.commands.length > 0) {
        setSelectedCommand(response.commands[0].name);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load commands');
    }
  };

  const loadJobs = async () => {
    try {
      const response = await cliApi.listJobs();
      setJobs(response);
      if (!selectedJobId && response.length > 0) {
        setSelectedJobId(response[0].job_id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load jobs');
    }
  };

  useEffect(() => {
    loadCommands();
    loadJobs();
  }, []);

  useEffect(() => {
    const activeJob = jobs.some((job) => job.status === 'queued' || job.status === 'running');
    if (!activeJob) return;
    const timer = window.setInterval(() => {
      void loadJobs();
    }, 1500);
    return () => window.clearInterval(timer);
  }, [jobs]);

  const handleRun = async () => {
    if (!selectedCommand) return;
    setIsSubmitting(true);
    setError(null);
    try {
      const args = argsInput
        .split('\n')
        .map((line) => line.trim())
        .filter((line) => line.length > 0);

      const response = await cliApi.startJob({
        command: selectedCommand,
        args,
        stdin_text: stdinText.trim() ? stdinText : undefined,
        timeout_seconds: timeoutSeconds,
      });

      await loadJobs();
      setSelectedJobId(response.job.job_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start command');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = async () => {
    if (!selectedJob) return;
    try {
      await cliApi.cancelJob(selectedJob.job_id);
      await loadJobs();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to cancel job');
    }
  };

  return (
    <div className="h-full flex flex-col bg-gray-50">
      <header className="bg-white border-b px-6 py-3">
        <h2 className="text-lg font-semibold text-gray-900">CLI Runner</h2>
        <p className="text-sm text-gray-500">
          Run `nano-banana` commands directly from the web app.
        </p>
      </header>

      {error && (
        <div className="bg-red-50 border-b border-red-200 px-6 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="flex-1 min-h-0 grid grid-cols-1 lg:grid-cols-3">
        <section className="bg-white border-r p-4 overflow-y-auto">
          <h3 className="font-medium text-gray-900 mb-3">Run Command</h3>

          <label className="block text-sm text-gray-600 mb-1">Command</label>
          <select
            value={selectedCommand}
            onChange={(e) => setSelectedCommand(e.target.value)}
            className="w-full border rounded px-3 py-2 text-sm mb-3"
          >
            {commands.map((command) => (
              <option key={command.name} value={command.name}>
                {command.name}
              </option>
            ))}
          </select>

          {selectedCommandSpec && (
            <div className="text-xs text-gray-600 bg-gray-50 border rounded p-2 mb-3">
              <p>{selectedCommandSpec.description}</p>
              {selectedCommandSpec.examples.length > 0 && (
                <p className="mt-1">
                  Example: <code>{selectedCommandSpec.examples[0]}</code>
                </p>
              )}
            </div>
          )}

          <label className="block text-sm text-gray-600 mb-1">
            Args (one argument per line)
          </label>
          <textarea
            value={argsInput}
            onChange={(e) => setArgsInput(e.target.value)}
            placeholder="--prompt-file&#10;prompts/example.txt&#10;--logo-dir&#10;logos/default"
            rows={8}
            className="w-full border rounded px-3 py-2 text-sm font-mono mb-3"
          />

          <label className="block text-sm text-gray-600 mb-1">
            Stdin (optional, for interactive commands)
          </label>
          <textarea
            value={stdinText}
            onChange={(e) => setStdinText(e.target.value)}
            placeholder="done"
            rows={4}
            className="w-full border rounded px-3 py-2 text-sm font-mono mb-3"
          />

          <label className="block text-sm text-gray-600 mb-1">Timeout (seconds)</label>
          <input
            type="number"
            value={timeoutSeconds}
            min={1}
            max={7200}
            onChange={(e) => setTimeoutSeconds(Number(e.target.value))}
            className="w-full border rounded px-3 py-2 text-sm mb-4"
          />

          <button
            onClick={handleRun}
            disabled={!selectedCommand || isSubmitting}
            className="w-full px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700 disabled:opacity-50"
          >
            {isSubmitting ? 'Starting...' : 'Run Command'}
          </button>
        </section>

        <section className="bg-white border-r p-4 overflow-y-auto">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-gray-900">Recent Jobs</h3>
            <button
              onClick={() => void loadJobs()}
              className="text-xs text-primary-600 hover:text-primary-800"
            >
              Refresh
            </button>
          </div>

          {jobs.length === 0 ? (
            <p className="text-sm text-gray-500">No jobs yet.</p>
          ) : (
            <ul className="space-y-2">
              {jobs.map((job) => (
                <li
                  key={job.job_id}
                  className={`border rounded p-2 cursor-pointer ${
                    selectedJobId === job.job_id ? 'border-primary-500 bg-primary-50' : 'hover:bg-gray-50'
                  }`}
                  onClick={() => setSelectedJobId(job.job_id)}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-sm">{job.job_id}</span>
                    <span className={`px-2 py-0.5 text-xs rounded ${statusClass(job.status)}`}>
                      {job.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 mt-1">
                    {job.command} {job.args.join(' ')}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(job.started_at).toLocaleString()}
                  </p>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="p-4 overflow-y-auto">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-gray-900">Job Output</h3>
            {selectedJob && (selectedJob.status === 'queued' || selectedJob.status === 'running') && (
              <button
                onClick={() => void handleCancel()}
                className="px-3 py-1 text-xs bg-yellow-100 text-yellow-800 rounded hover:bg-yellow-200"
              >
                Cancel Job
              </button>
            )}
          </div>

          {!selectedJob ? (
            <p className="text-sm text-gray-500">Select a job to inspect output.</p>
          ) : (
            <div className="space-y-3">
              <div className="text-sm">
                <p>
                  <span className="text-gray-500">Command:</span>{' '}
                  <span className="font-mono">
                    nano-banana {selectedJob.command} {selectedJob.args.join(' ')}
                  </span>
                </p>
                <p>
                  <span className="text-gray-500">Exit code:</span>{' '}
                  {selectedJob.exit_code !== undefined ? selectedJob.exit_code : 'N/A'}
                </p>
              </div>

              <div>
                <p className="text-xs font-medium text-gray-600 mb-1">STDOUT</p>
                <pre className="bg-gray-900 text-gray-100 rounded p-3 text-xs overflow-auto max-h-64 whitespace-pre-wrap">
                  {selectedJob.stdout || '(empty)'}
                </pre>
              </div>

              <div>
                <p className="text-xs font-medium text-gray-600 mb-1">STDERR</p>
                <pre className="bg-gray-900 text-gray-100 rounded p-3 text-xs overflow-auto max-h-64 whitespace-pre-wrap">
                  {selectedJob.stderr || '(empty)'}
                </pre>
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
