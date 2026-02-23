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
  MCPEnrichmentOptions,
  GenerationSettingsRequest,
} from '../types';

interface SessionAuthOptions {
  imageProvider?: 'gemini' | 'openai';
  openaiApiKey?: string;
  vertexApiKey?: string;
  referencePrompt?: string;
  referencePromptPath?: string;
  referenceImageBase64?: string;
  referenceImageFilename?: string;
  mcpEnrichment?: MCPEnrichmentOptions;
}

interface UseArchitectReturn {
  // Session state
  sessions: Session[];
  currentSession: Session | null;
  isLoading: boolean;
  isSessionLoading: boolean;
  isSending: boolean;
  error: string | null;

  // Chat state
  messages: ChatMessage[];
  architecture: ArchitectureState;
  readyForOutput: boolean;
  availableLogos: string[];
  imageProvider: 'gemini' | 'openai';
  credentialMode: 'environment' | 'custom_key';

  // Preview state
  diagramImageUrl: string | null;
  diagramImageUrls: string[];
  isGeneratingPreview: boolean;

  // Actions
  loadSessions: () => Promise<void>;
  createSession: (
    problem: string,
    context?: string,
    authOptions?: SessionAuthOptions
  ) => Promise<void>;
  selectSession: (sessionId: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  sendMessage: (message: string) => Promise<MessageResponse | null>;
  generateOutput: () => Promise<void>;
  generatePreview: (settings?: GenerationSettingsRequest) => Promise<void>;
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
  const [isSessionLoading, setIsSessionLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Chat state
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [architecture, setArchitecture] = useState<ArchitectureState>(emptyArchitecture);
  const [readyForOutput, setReadyForOutput] = useState(false);
  const [availableLogos, setAvailableLogos] = useState<string[]>([]);
  const [imageProvider, setImageProvider] = useState<'gemini' | 'openai'>('gemini');
  const [credentialMode, setCredentialMode] = useState<'environment' | 'custom_key'>(
    'environment'
  );

  // Preview state
  const [diagramImageUrl, setDiagramImageUrl] = useState<string | null>(null);
  const [diagramImageUrls, setDiagramImageUrls] = useState<string[]>([]);
  const [isGeneratingPreview, setIsGeneratingPreview] = useState(false);

  /**
   * Load all sessions from the API.
   */
  const loadSessions = useCallback(async () => {
    setIsSessionLoading(true);
    setError(null);
    try {
      const response = await sessionsApi.list();
      setSessions(response.sessions);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load sessions');
    } finally {
      setIsSessionLoading(false);
    }
  }, []);

  /**
   * Create a new session.
   */
  const createSession = useCallback(async (
    problem: string,
    context?: string,
    authOptions?: SessionAuthOptions
  ) => {
    setIsSessionLoading(true);
    setIsSending(true);
    setError(null);
    try {
      const session = await sessionsApi.create({
        initial_problem: problem,
        custom_context: context,
        image_provider: authOptions?.imageProvider,
        openai_api_key: authOptions?.openaiApiKey,
        vertex_api_key: authOptions?.vertexApiKey,
        reference_prompt: authOptions?.referencePrompt,
        reference_prompt_path: authOptions?.referencePromptPath,
        reference_image_base64: authOptions?.referenceImageBase64,
        reference_image_filename: authOptions?.referenceImageFilename,
        mcp_enrichment: authOptions?.mcpEnrichment,
      });

      setSessions(prev => [session, ...prev]);
      setCurrentSession(session);
      setMessages([]);
      setArchitecture(session.current_architecture || emptyArchitecture);
      setReadyForOutput(false);
      setDiagramImageUrl(null);
      setDiagramImageUrls([]);
      setIsSessionLoading(false);

      // Load status to get available logos
      const status = await chatApi.getStatus(session.session_id);
      setAvailableLogos(status.available_logos);
      setImageProvider(status.image_provider);
      setCredentialMode(status.credential_mode);

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
      setIsSessionLoading(false);
      setIsSending(false);
    }
  }, []);

  /**
   * Select and load an existing session.
   */
  const selectSession = useCallback(async (sessionId: string) => {
    setIsSessionLoading(true);
    setError(null);
    try {
      const session = await sessionsApi.get(sessionId);
      setCurrentSession(session);
      setArchitecture(session.current_architecture || emptyArchitecture);
      setDiagramImageUrl(null);
      setDiagramImageUrls([]);

      // Load status for more details
      const status = await chatApi.getStatus(sessionId);
      setReadyForOutput(status.ready_for_output);
      setAvailableLogos(status.available_logos);
      setImageProvider(status.image_provider);
      setCredentialMode(status.credential_mode);

      // Load full chat history from turns endpoint
      const turnsResponse = await chatApi.getTurns(sessionId);
      const loadedMessages: ChatMessage[] = [];
      for (const turn of turnsResponse.turns) {
        const ts = turn.created_at || new Date().toISOString();
        loadedMessages.push({
          role: 'user',
          content: turn.user_input,
          timestamp: ts,
        });
        loadedMessages.push({
          role: 'assistant',
          content: turn.architect_response,
          timestamp: ts,
        });
      }

      // If no turns found, show the initial problem as a placeholder
      if (loadedMessages.length === 0) {
        loadedMessages.push({
          role: 'user',
          content: session.initial_problem,
          timestamp: session.created_at,
        });
      }

      setMessages(loadedMessages);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load session');
    } finally {
      setIsSessionLoading(false);
    }
  }, []);

  /**
   * Delete a session.
   */
  const deleteSession = useCallback(async (sessionId: string) => {
    setIsSessionLoading(true);
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
        setDiagramImageUrls([]);
        setImageProvider('gemini');
        setCredentialMode('environment');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete session');
    } finally {
      setIsSessionLoading(false);
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

    setIsSending(true);
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
      setIsSending(false);
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

    setIsSending(true);
    setError(null);
    try {
      const response = await chatApi.generateOutput(currentSession.session_id);

      if (response.success) {
        // Also generate a preview image so the user can see the diagram
        let previewUrl: string | undefined;
        try {
          const preview = await chatApi.generatePreview(currentSession.session_id);
          if (preview.success && preview.image_url) {
            previewUrl = preview.image_url;
            setDiagramImageUrl(preview.image_url);
          }
        } catch {
          // Preview generation is best-effort - don't block output
        }

        setMessages(prev => [
          ...prev,
          {
            role: 'assistant',
            content: `**Output saved**\n\n- \`${response.prompt_file}\`\n- \`${response.architecture_file}\``,
            timestamp: new Date().toISOString(),
            imageUrl: previewUrl,
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
      setIsSending(false);
    }
  }, [currentSession]);

  /**
   * Generate a diagram preview image.
   */
  const generatePreview = useCallback(async (settings?: GenerationSettingsRequest) => {
    if (!currentSession) {
      setError('No active session');
      return;
    }

    setIsGeneratingPreview(true);
    setError(null);
    try {
      const response = await chatApi.generatePreview(currentSession.session_id, settings);

      if (response.success && response.image_url) {
        setDiagramImageUrl(response.image_url);
        setDiagramImageUrls(response.image_urls || [response.image_url]);
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

  const isLoading = isSessionLoading || isSending;

  return {
    sessions,
    currentSession,
    isLoading,
    isSessionLoading,
    isSending,
    error,
    messages,
    architecture,
    readyForOutput,
    availableLogos,
    imageProvider,
    credentialMode,
    diagramImageUrl,
    diagramImageUrls,
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
