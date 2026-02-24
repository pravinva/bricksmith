/**
 * Hook for managing multiple concurrent chat/refinement sessions.
 *
 * Each session runs independently in the background - while one is
 * generating an image, the user can switch to another or start a new one.
 *
 * Uses useReducer for deterministic state updates across concurrent async ops.
 */

import { useReducer, useCallback, useRef } from 'react';
import { standaloneRefinementApi } from '../api/client';
import type {
  RefinementState,
  RefinementIteration,
  GenerationSettingsRequest,
  StartStandaloneRefinementRequest,
} from '../types';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface ChatSession {
  id: string;
  label: string;
  refinementState: RefinementState | null;
  isGenerating: boolean;
  isRefining: boolean;
  error: string | null;
  createdAt: string;
}

interface State {
  sessions: Record<string, ChatSession>;
  order: string[];
  activeId: string | null;
  showSetup: boolean;
}

// ---------------------------------------------------------------------------
// Reducer
// ---------------------------------------------------------------------------

type Action =
  | { type: 'ADD'; session: ChatSession }
  | { type: 'PATCH'; id: string; patch: Partial<ChatSession> }
  | { type: 'REMOVE'; id: string }
  | { type: 'ACTIVATE'; id: string }
  | { type: 'SETUP' };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'ADD':
      return {
        ...state,
        sessions: { ...state.sessions, [action.session.id]: action.session },
        order: [...state.order, action.session.id],
        activeId: action.session.id,
        showSetup: false,
      };

    case 'PATCH': {
      const s = state.sessions[action.id];
      if (!s) return state;
      return {
        ...state,
        sessions: { ...state.sessions, [action.id]: { ...s, ...action.patch } },
      };
    }

    case 'REMOVE': {
      const { [action.id]: _removed, ...rest } = state.sessions;
      const order = state.order.filter(x => x !== action.id);
      const activeId =
        state.activeId === action.id
          ? order.length > 0
            ? order[order.length - 1]
            : null
          : state.activeId;
      return { sessions: rest, order, activeId, showSetup: order.length === 0 };
    }

    case 'ACTIVATE':
      return { ...state, activeId: action.id, showSetup: false };

    case 'SETUP':
      return { ...state, showSetup: true };

    default:
      return state;
  }
}

const INIT: State = { sessions: {}, order: [], activeId: null, showSetup: true };

// ---------------------------------------------------------------------------
// Public helpers
// ---------------------------------------------------------------------------

export function latestIteration(rs: RefinementState | null): RefinementIteration | null {
  if (!rs || rs.iterations.length === 0) return null;
  return rs.iterations[rs.iterations.length - 1];
}

// ---------------------------------------------------------------------------
// Hook
// ---------------------------------------------------------------------------

export function useMultiSession() {
  const [state, dispatch] = useReducer(reducer, INIT);

  // Ref for reading latest sessions inside async callbacks (avoids stale closures)
  const sessionsRef = useRef(state.sessions);
  sessionsRef.current = state.sessions;

  const patch = useCallback(
    (id: string, p: Partial<ChatSession>) => dispatch({ type: 'PATCH', id, patch: p }),
    [],
  );

  // ── Lifecycle ─────────────────────────────────────────────────────────────

  /** Start a new standalone refinement session.
   *  Returns after the session is created (fast). Image generation continues
   *  in the background so the caller can immediately start another session. */
  const startSession = useCallback(
    async (request: StartStandaloneRefinementRequest, label: string): Promise<string> => {
      // Step 1: create session on backend (fast, ~1-2s)
      const rs = await standaloneRefinementApi.start(request);
      const id = rs.session_id;

      dispatch({
        type: 'ADD',
        session: {
          id,
          label,
          refinementState: rs,
          isGenerating: true,
          isRefining: false,
          error: null,
          createdAt: new Date().toISOString(),
        },
      });

      // Step 2: generate first image (slow - fire and forget)
      void (async () => {
        try {
          const result = await standaloneRefinementApi.generateAndEvaluate(id);
          if (!result.success) {
            patch(id, { error: result.error || 'Generation failed', isGenerating: false });
            return;
          }
          const updated = await standaloneRefinementApi.getState(id);
          patch(id, { refinementState: updated, isGenerating: false });
        } catch (e) {
          patch(id, {
            isGenerating: false,
            error: e instanceof Error ? e.message : 'Generation failed',
          });
        }
      })();

      return id;
    },
    [patch],
  );

  const removeSession = useCallback((id: string) => dispatch({ type: 'REMOVE', id }), []);
  const setActive = useCallback((id: string) => dispatch({ type: 'ACTIVATE', id }), []);
  const showSetup = useCallback(() => dispatch({ type: 'SETUP' }), []);

  // ── Per-session operations ────────────────────────────────────────────────

  const generateAndEvaluate = useCallback(
    async (id: string, settings?: GenerationSettingsRequest) => {
      patch(id, { isGenerating: true, error: null });
      try {
        const result = await standaloneRefinementApi.generateAndEvaluate(id, settings);
        if (!result.success) {
          patch(id, { error: result.error || 'Generation failed', isGenerating: false });
          return;
        }
        const updated = await standaloneRefinementApi.getState(id);
        patch(id, { refinementState: updated, isGenerating: false });
      } catch (e) {
        patch(id, {
          isGenerating: false,
          error: e instanceof Error ? e.message : 'Generation failed',
        });
      }
    },
    [patch],
  );

  const refinePrompt = useCallback(
    async (
      id: string,
      feedback: string,
      settings?: GenerationSettingsRequest,
      userScore?: number,
    ) => {
      patch(id, { isRefining: true, error: null });
      try {
        const res = await standaloneRefinementApi.refine(id, {
          user_feedback: feedback,
          user_score: userScore,
        });
        if (!res.success) {
          patch(id, { error: res.error || 'Refinement failed', isRefining: false });
          return;
        }
        patch(id, { isRefining: false, isGenerating: true });

        const gen = await standaloneRefinementApi.generateAndEvaluate(id, settings);
        if (!gen.success) {
          patch(id, { error: gen.error || 'Regeneration failed', isGenerating: false });
          return;
        }
        const updated = await standaloneRefinementApi.getState(id);
        patch(id, { refinementState: updated, isGenerating: false });
      } catch (e) {
        patch(id, {
          isRefining: false,
          isGenerating: false,
          error: e instanceof Error ? e.message : 'Refinement failed',
        });
      }
    },
    [patch],
  );

  const updatePrompt = useCallback(
    async (id: string, prompt: string) => {
      patch(id, { error: null });
      try {
        await standaloneRefinementApi.updatePrompt(id, prompt);
        const s = sessionsRef.current[id];
        if (s?.refinementState) {
          patch(id, { refinementState: { ...s.refinementState, current_prompt: prompt } });
        }
      } catch (e) {
        patch(id, { error: e instanceof Error ? e.message : 'Failed to update prompt' });
      }
    },
    [patch],
  );

  const clearError = useCallback((id: string) => patch(id, { error: null }), [patch]);

  // ── Derived ───────────────────────────────────────────────────────────────

  const active = state.activeId ? state.sessions[state.activeId] ?? null : null;

  return {
    sessions: state.sessions,
    order: state.order,
    activeId: state.activeId,
    active,
    showSetup: state.showSetup,
    count: state.order.length,
    startSession,
    removeSession,
    setActive,
    showSetupScreen: showSetup,
    generateAndEvaluate,
    refinePrompt,
    updatePrompt,
    clearError,
  };
}
