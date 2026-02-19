/**
 * React hook for managing architect session state and API interactions.
 */

import { useState, useCallback, useEffect } from 'react';
import { sessionsApi, chatApi } from '../api/client';
import type {
  Session,
  ArchitectureState,
  ChatMessage,
  MessageResponse,
} from '../types';

interface UseArchitectReturn {
  // Session state
  sessions: Session[];
  currentSession: Session | null;
  isLoading: boolean;
  error: string | null;

  // Chat state
  messages: ChatMessage[];
  architecture: ArchitectureState;
  readyForOutput: boolean;
  availableLogos: string[];

  // Preview state
  diagramImageUrl: string | null;
  isGeneratingPreview: boolean;

  // Actions
  loadSessions: () => Promise<void>;
  createSession: (problem: string, context?: string) => Promise<void>;
  selectSession: (sessionId: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  sendMessage: (message: string) => Promise<MessageResponse | null>;
  generateOutput: () => Promise<void>;
  generatePreview: () => Promise<void>;
  clearError: () => void;
}

const emptyArchitecture: ArchitectureState = {
  components: [],
  connections: [],
};

export function useArchitect(): UseArchitectReturn {
  // Session state
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSession, setCurrentSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Chat state
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [architecture, setArchitecture] = useState<ArchitectureState>(emptyArchitecture);
  const [readyForOutput, setReadyForOutput] = useState(false);
  const [availableLogos, setAvailableLogos] = useState<string[]>([]);

  // Preview state
  const [diagramImageUrl, setDiagramImageUrl] = useState<string | null>(null);
  const [isGeneratingPreview, setIsGeneratingPreview] = useState(false);

  /**
   * Load all sessions from the API.
   */
  const loadSessions = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await sessionsApi.list();
      setSessions(response.sessions);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load sessions');
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Create a new session.
   */
  const createSession = useCallback(async (problem: string, context?: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const session = await sessionsApi.create({
        initial_problem: problem,
        custom_context: context,
      });

      setSessions(prev => [session, ...prev]);
      setCurrentSession(session);
      setMessages([]);
      setArchitecture(session.current_architecture || emptyArchitecture);
      setReadyForOutput(false);
      setDiagramImageUrl(null);

      // Load status to get available logos
      const status = await chatApi.getStatus(session.session_id);
      setAvailableLogos(status.available_logos);

      // Send the initial problem as the first message
      const response = await chatApi.sendMessage(session.session_id, {
        message: problem,
      });

      setMessages([
        {
          role: 'user',
          content: problem,
          timestamp: new Date().toISOString(),
        },
        {
          role: 'assistant',
          content: response.response,
          timestamp: new Date().toISOString(),
          architecture: response.architecture,
        },
      ]);
      setArchitecture(response.architecture);
      setReadyForOutput(response.ready_for_output);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create session');
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Select and load an existing session.
   */
  const selectSession = useCallback(async (sessionId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const session = await sessionsApi.get(sessionId);
      setCurrentSession(session);
      setArchitecture(session.current_architecture || emptyArchitecture);
      setDiagramImageUrl(null);

      // Load status for more details
      const status = await chatApi.getStatus(sessionId);
      setReadyForOutput(status.ready_for_output);
      setAvailableLogos(status.available_logos);

      // Messages would need to be loaded from a separate endpoint
      // For now, just show a placeholder
      setMessages([
        {
          role: 'user',
          content: session.initial_problem,
          timestamp: session.created_at,
        },
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load session');
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Delete a session.
   */
  const deleteSession = useCallback(async (sessionId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await sessionsApi.delete(sessionId);
      setSessions(prev => prev.filter(s => s.session_id !== sessionId));

      if (currentSession?.session_id === sessionId) {
        setCurrentSession(null);
        setMessages([]);
        setArchitecture(emptyArchitecture);
        setReadyForOutput(false);
        setDiagramImageUrl(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete session');
    } finally {
      setIsLoading(false);
    }
  }, [currentSession]);

  /**
   * Send a message in the current session.
   */
  const sendMessage = useCallback(async (message: string): Promise<MessageResponse | null> => {
    if (!currentSession) {
      setError('No active session');
      return null;
    }

    setIsLoading(true);
    setError(null);
    try {
      // Add user message immediately
      const userMessage: ChatMessage = {
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, userMessage]);

      // Send to API
      const response = await chatApi.sendMessage(currentSession.session_id, {
        message,
      });

      // Add assistant response
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        architecture: response.architecture,
      };
      setMessages(prev => [...prev, assistantMessage]);

      // Update architecture state
      setArchitecture(response.architecture);
      setReadyForOutput(response.ready_for_output);

      return response;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [currentSession]);

  /**
   * Generate the final diagram output.
   */
  const generateOutput = useCallback(async () => {
    if (!currentSession) {
      setError('No active session');
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const response = await chatApi.generateOutput(currentSession.session_id);

      if (response.success) {
        setMessages(prev => [
          ...prev,
          {
            role: 'assistant',
            content: `Diagram prompt generated successfully!\n\nOutput saved to:\n- ${response.prompt_file}\n- ${response.architecture_file}`,
            timestamp: new Date().toISOString(),
          },
        ]);

        // Update session status
        setCurrentSession(prev =>
          prev ? { ...prev, status: 'completed' } : null
        );
      } else {
        setError(response.error || 'Failed to generate output');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate output');
    } finally {
      setIsLoading(false);
    }
  }, [currentSession]);

  /**
   * Generate a diagram preview image.
   */
  const generatePreview = useCallback(async () => {
    if (!currentSession) {
      setError('No active session');
      return;
    }

    setIsGeneratingPreview(true);
    setError(null);
    try {
      const response = await chatApi.generatePreview(currentSession.session_id);

      if (response.success && response.image_url) {
        setDiagramImageUrl(response.image_url);
        setMessages(prev => [
          ...prev,
          {
            role: 'assistant',
            content: `Diagram preview generated successfully!`,
            timestamp: new Date().toISOString(),
          },
        ]);
      } else {
        setError(response.error || 'Failed to generate preview');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate preview');
    } finally {
      setIsGeneratingPreview(false);
    }
  }, [currentSession]);

  /**
   * Clear the current error.
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Load sessions on mount
  useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  return {
    sessions,
    currentSession,
    isLoading,
    error,
    messages,
    architecture,
    readyForOutput,
    availableLogos,
    diagramImageUrl,
    isGeneratingPreview,
    loadSessions,
    createSession,
    selectSession,
    deleteSession,
    sendMessage,
    generateOutput,
    generatePreview,
    clearError,
  };
}
