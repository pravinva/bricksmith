/**
 * Hook for managing the diagram refinement loop state.
 *
 * Supports two modes:
 * - 'session': Refinement tied to an architect session (existing flow)
 * - 'standalone': Refinement from a raw prompt (no architect session)
 *
 * Flow: startRefinement() or startStandaloneRefinement()
 *       -> auto generateAndEvaluate() -> user sees scores
 *       -> refinePrompt(feedback) -> auto generateAndEvaluate() -> repeat
 */

import { useState, useCallback, useRef } from 'react';
import { refinementApi, standaloneRefinementApi } from '../api/client';
import type { RefinementState, RefinementIteration, GenerationSettingsRequest } from '../types';

type RefinementMode = 'idle' | 'session' | 'standalone';

export interface UseRefinementReturn {
  refinementState: RefinementState | null;
  mode: RefinementMode;
  isActive: boolean;
  isGenerating: boolean;
  isRefining: boolean;
  currentIteration: RefinementIteration | null;
  error: string | null;
  startRefinement: (sessionId: string) => Promise<void>;
  startStandaloneRefinement: (
    prompt: string,
    imageProvider?: 'gemini' | 'openai' | 'databricks',
    apiKey?: string,
  ) => Promise<void>;
  generateAndEvaluate: (settings?: GenerationSettingsRequest) => Promise<void>;
  refinePrompt: (feedback: string, settings?: GenerationSettingsRequest) => Promise<void>;
  acceptResult: () => void;
  clearError: () => void;
}

export function useRefinement(): UseRefinementReturn {
  const [refinementState, setRefinementState] = useState<RefinementState | null>(null);
  const [mode, setMode] = useState<RefinementMode>('idle');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isRefining, setIsRefining] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Use a ref to track the current mode for use in callbacks without stale closure
  const modeRef = useRef<RefinementMode>('idle');

  const isActive = refinementState !== null;

  const currentIteration =
    refinementState && refinementState.iterations.length > 0
      ? refinementState.iterations[refinementState.iterations.length - 1]
      : null;

  /** Get the correct API based on current mode. */
  const getApi = useCallback(() => {
    return modeRef.current === 'standalone' ? standaloneRefinementApi : refinementApi;
  }, []);

  const generateAndEvaluate = useCallback(async (settings?: GenerationSettingsRequest) => {
    if (!refinementState) return;

    setIsGenerating(true);
    setError(null);

    try {
      const api = getApi();
      const result = await api.generateAndEvaluate(
        refinementState.session_id,
        settings,
      );

      if (!result.success) {
        setError(result.error || 'Generation failed');
        return;
      }

      // Refresh full state from server
      const updated = await api.getState(refinementState.session_id);
      setRefinementState(updated);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Generation failed');
    } finally {
      setIsGenerating(false);
    }
  }, [refinementState, getApi]);

  const startRefinement = useCallback(async (sessionId: string) => {
    setError(null);
    setIsGenerating(true);
    setMode('session');
    modeRef.current = 'session';

    try {
      const state = await refinementApi.start(sessionId);
      setRefinementState(state);

      // Auto-trigger first generation
      const result = await refinementApi.generateAndEvaluate(sessionId);
      if (!result.success) {
        setError(result.error || 'Initial generation failed');
      }

      // Refresh state
      const updated = await refinementApi.getState(sessionId);
      setRefinementState(updated);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to start refinement');
    } finally {
      setIsGenerating(false);
    }
  }, []);

  const startStandaloneRefinement = useCallback(async (
    prompt: string,
    imageProvider?: 'gemini' | 'openai' | 'databricks',
    apiKey?: string,
  ) => {
    setError(null);
    setIsGenerating(true);
    setMode('standalone');
    modeRef.current = 'standalone';

    try {
      const state = await standaloneRefinementApi.start({
        prompt,
        image_provider: imageProvider,
        openai_api_key: imageProvider === 'openai' ? apiKey : undefined,
        vertex_api_key: imageProvider === 'gemini' ? apiKey : undefined,
      });
      setRefinementState(state);

      // Auto-trigger first generation
      const result = await standaloneRefinementApi.generateAndEvaluate(state.session_id);
      if (!result.success) {
        setError(result.error || 'Initial generation failed');
      }

      // Refresh state
      const updated = await standaloneRefinementApi.getState(state.session_id);
      setRefinementState(updated);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to start standalone refinement');
    } finally {
      setIsGenerating(false);
    }
  }, []);

  const refinePrompt = useCallback(async (
    feedback: string,
    settings?: GenerationSettingsRequest,
  ) => {
    if (!refinementState) return;

    setIsRefining(true);
    setError(null);

    try {
      const api = getApi();
      const refineResult = await api.refine(
        refinementState.session_id,
        { user_feedback: feedback },
      );

      if (!refineResult.success) {
        setError(refineResult.error || 'Refinement failed');
        setIsRefining(false);
        return;
      }

      // Update local state with new prompt
      setRefinementState(prev =>
        prev
          ? { ...prev, current_prompt: refineResult.refined_prompt || prev.current_prompt }
          : prev,
      );
      setIsRefining(false);

      // Auto-trigger next generation with settings
      setIsGenerating(true);
      const genResult = await api.generateAndEvaluate(
        refinementState.session_id,
        settings,
      );
      if (!genResult.success) {
        setError(genResult.error || 'Regeneration failed');
      }

      // Refresh state
      const updated = await api.getState(refinementState.session_id);
      setRefinementState(updated);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Refinement failed');
    } finally {
      setIsRefining(false);
      setIsGenerating(false);
    }
  }, [refinementState, getApi]);

  const acceptResult = useCallback(() => {
    setRefinementState(null);
    setMode('idle');
    modeRef.current = 'idle';
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    refinementState,
    mode,
    isActive,
    isGenerating,
    isRefining,
    currentIteration,
    error,
    startRefinement,
    startStandaloneRefinement,
    generateAndEvaluate,
    refinePrompt,
    acceptResult,
    clearError,
  };
}
