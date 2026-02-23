/**
 * Hook for managing the diagram refinement loop state.
 *
 * Flow: startRefinement() -> auto generateAndEvaluate() -> user sees scores
 *       -> refinePrompt(feedback) -> auto generateAndEvaluate() -> repeat
 */

import { useState, useCallback } from 'react';
import { refinementApi } from '../api/client';
import type { RefinementState, RefinementIteration, GenerationSettingsRequest } from '../types';

export interface UseRefinementReturn {
  refinementState: RefinementState | null;
  isActive: boolean;
  isGenerating: boolean;
  isRefining: boolean;
  currentIteration: RefinementIteration | null;
  error: string | null;
  startRefinement: (sessionId: string) => Promise<void>;
  generateAndEvaluate: (settings?: GenerationSettingsRequest) => Promise<void>;
  refinePrompt: (feedback: string, settings?: GenerationSettingsRequest) => Promise<void>;
  acceptResult: () => void;
  clearError: () => void;
}

export function useRefinement(): UseRefinementReturn {
  const [refinementState, setRefinementState] = useState<RefinementState | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isRefining, setIsRefining] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isActive = refinementState !== null;

  const currentIteration =
    refinementState && refinementState.iterations.length > 0
      ? refinementState.iterations[refinementState.iterations.length - 1]
      : null;

  const generateAndEvaluate = useCallback(async (settings?: GenerationSettingsRequest) => {
    if (!refinementState) return;

    setIsGenerating(true);
    setError(null);

    try {
      const result = await refinementApi.generateAndEvaluate(
        refinementState.session_id,
        settings,
      );

      if (!result.success) {
        setError(result.error || 'Generation failed');
        return;
      }

      // Refresh full state from server
      const updated = await refinementApi.getState(refinementState.session_id);
      setRefinementState(updated);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Generation failed');
    } finally {
      setIsGenerating(false);
    }
  }, [refinementState]);

  const startRefinement = useCallback(async (sessionId: string) => {
    setError(null);
    setIsGenerating(true);

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

  const refinePrompt = useCallback(async (
    feedback: string,
    settings?: GenerationSettingsRequest,
  ) => {
    if (!refinementState) return;

    setIsRefining(true);
    setError(null);

    try {
      const refineResult = await refinementApi.refine(
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
      const genResult = await refinementApi.generateAndEvaluate(
        refinementState.session_id,
        settings,
      );
      if (!genResult.success) {
        setError(genResult.error || 'Regeneration failed');
      }

      // Refresh state
      const updated = await refinementApi.getState(refinementState.session_id);
      setRefinementState(updated);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Refinement failed');
    } finally {
      setIsRefining(false);
      setIsGenerating(false);
    }
  }, [refinementState]);

  const acceptResult = useCallback(() => {
    setRefinementState(null);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    refinementState,
    isActive,
    isGenerating,
    isRefining,
    currentIteration,
    error,
    startRefinement,
    generateAndEvaluate,
    refinePrompt,
    acceptResult,
    clearError,
  };
}
