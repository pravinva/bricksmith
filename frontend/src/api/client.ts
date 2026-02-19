/**
 * API client for communicating with the Bricksmith Architect backend.
 */

import type {
  Session,
  SessionListResponse,
  CreateSessionRequest,
  SendMessageRequest,
  MessageResponse,
  StatusResponse,
  GenerateOutputResponse,
  GeneratePreviewResponse,
  CLICommandsResponse,
  CliJob,
  StartCliJobRequest,
  StartCliJobResponse,
  BestResultsResponse,
  TurnsResponse,
} from '../types';

const API_BASE = '/api';

/**
 * Generic fetch wrapper with error handling.
 */
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Session API endpoints.
 */
export const sessionsApi = {
  /**
   * Create a new architect session.
   */
  create: (request: CreateSessionRequest): Promise<Session> =>
    fetchApi('/sessions', {
      method: 'POST',
      body: JSON.stringify(request),
    }),

  /**
   * List all sessions.
   */
  list: (limit = 50, offset = 0): Promise<SessionListResponse> =>
    fetchApi(`/sessions?limit=${limit}&offset=${offset}`),

  /**
   * Get a session by ID.
   */
  get: (sessionId: string): Promise<Session> =>
    fetchApi(`/sessions/${sessionId}`),

  /**
   * Delete a session.
   */
  delete: (sessionId: string): Promise<{ status: string; session_id: string }> =>
    fetchApi(`/sessions/${sessionId}`, { method: 'DELETE' }),
};

/**
 * Chat API endpoints.
 */
export const chatApi = {
  /**
   * Get all conversation turns for a session.
   */
  getTurns: (sessionId: string): Promise<TurnsResponse> =>
    fetchApi(`/sessions/${sessionId}/turns`),

  /**
   * Send a message and get a response.
   */
  sendMessage: (
    sessionId: string,
    request: SendMessageRequest
  ): Promise<MessageResponse> =>
    fetchApi(`/sessions/${sessionId}/message`, {
      method: 'POST',
      body: JSON.stringify(request),
    }),

  /**
   * Get the current architecture status.
   */
  getStatus: (sessionId: string): Promise<StatusResponse> =>
    fetchApi(`/sessions/${sessionId}/status`),

  /**
   * Generate the final diagram output.
   */
  generateOutput: (
    sessionId: string,
    outputDir?: string
  ): Promise<GenerateOutputResponse> =>
    fetchApi(`/sessions/${sessionId}/output`, {
      method: 'POST',
      body: JSON.stringify({ output_dir: outputDir }),
    }),

  /**
   * Generate a diagram preview image.
   */
  generatePreview: (sessionId: string): Promise<GeneratePreviewResponse> =>
    fetchApi(`/sessions/${sessionId}/generate-preview`, {
      method: 'POST',
    }),
};

/**
 * Health check endpoint.
 */
export const healthApi = {
  check: (): Promise<{ status: string; service: string }> =>
    fetchApi('/health'),
};

/**
 * CLI mirror API endpoints.
 */
export const cliApi = {
  listCommands: (): Promise<CLICommandsResponse> =>
    fetchApi('/cli/commands'),

  startJob: (request: StartCliJobRequest): Promise<StartCliJobResponse> =>
    fetchApi('/cli/jobs', {
      method: 'POST',
      body: JSON.stringify(request),
    }),

  listJobs: (): Promise<CliJob[]> =>
    fetchApi('/cli/jobs'),

  getJob: (jobId: string): Promise<CliJob> =>
    fetchApi(`/cli/jobs/${jobId}`),

  cancelJob: (jobId: string): Promise<CliJob> =>
    fetchApi(`/cli/jobs/${jobId}`, { method: 'DELETE' }),
};

export const resultsApi = {
  listBest: (
    limit = 30,
    query?: string,
    minScore?: number,
    includePrompt = false
  ): Promise<BestResultsResponse> => {
    const params = new URLSearchParams();
    params.set('limit', String(limit));
    params.set('include_prompt', String(includePrompt));
    if (query) params.set('query', query);
    if (minScore !== undefined) params.set('min_score', String(minScore));
    return fetchApi(`/results/best?${params.toString()}`);
  },
};
