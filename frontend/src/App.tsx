/**
 * Main application component for Bricksmith.
 *
 * Three tabs:
 *   - Chat Lab: the primary workflow (mirrors `bricksmith chat` CLI)
 *   - Architect Studio: conversational architecture design
 *   - Best Results: browse previous outputs
 */

import { useArchitect } from './hooks/useArchitect';
import { useRefinement } from './hooks/useRefinement';
import { Chat } from './components/Chat';
import { ArchitectureViz } from './components/ArchitectureViz';
import { RefinementPanel } from './components/RefinementPanel';
import { SessionList } from './components/SessionList';
import { StatusPanel } from './components/StatusPanel';
import { BestResults } from './components/BestResults';
import { ChatLab } from './components/ChatLab';
import { useState, useCallback } from 'react';
import type { BestResultItem } from './types';

type AppMode = 'chat' | 'architect' | 'best';

function App() {
  const [mode, setMode] = useState<AppMode>('chat');
  const refinement = useRefinement();
  const {
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
    createSession,
    selectSession,
    deleteSession,
    sendMessage,
    generateOutput,
    generatePreview,
    clearError,
  } = useArchitect();

  const handleCreateArchitectSessionFromResult = async (
    result: BestResultItem
  ) => {
    setMode('architect');

    const problem = `Refine architecture based on: ${result.title}`;
    const contextParts = [
      `Source: ${result.source}`,
      result.run_id ? `Run ID: ${result.run_id}` : null,
      result.prompt_path ? `Prompt file: ${result.prompt_path}` : null,
    ].filter(Boolean);

    const refPrompt = result.full_prompt || result.prompt_preview || '';

    await createSession(problem, contextParts.join('\n\n'), {
      referencePrompt: refPrompt || undefined,
    });
  };

  const handleStartRefinement = useCallback(() => {
    if (currentSession) {
      refinement.startRefinement(currentSession.session_id);
    }
  }, [currentSession, refinement]);

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img
              src="/logo-mascot.png"
              alt="Bricksmith mascot logo"
              className="w-10 h-10 rounded-lg object-cover border border-gray-200 bg-white"
            />
            <div>
              <h1 className="text-xl font-bold text-gray-900">Bricksmith</h1>
              <p className="text-sm text-gray-500">Architecture diagram generation</p>
            </div>
          </div>
          {mode === 'architect' && currentSession && (
            <div className="text-sm text-gray-600 flex items-center gap-2">
              <span>
                Session: <span className="font-mono">{currentSession.session_id}</span>
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  credentialMode === 'custom_key'
                    ? 'bg-amber-100 text-amber-800'
                    : 'bg-gray-100 text-gray-700'
                }`}
              >
                {credentialMode === 'custom_key'
                  ? `Custom key (${imageProvider})`
                  : `Env (${imageProvider})`}
              </span>
            </div>
          )}
        </div>
        <div className="mt-3 flex gap-2">
          <button
            onClick={() => setMode('chat')}
            className={`px-3 py-1.5 text-sm rounded ${
              mode === 'chat'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Chat Lab
          </button>
          <button
            onClick={() => setMode('architect')}
            className={`px-3 py-1.5 text-sm rounded ${
              mode === 'architect'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Architect Studio
          </button>
          <button
            onClick={() => setMode('best')}
            className={`px-3 py-1.5 text-sm rounded ${
              mode === 'best'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Best Results
          </button>
        </div>
      </header>

      {/* Error banner */}
      {error && (
        <div className="bg-red-50 border-b border-red-200 px-6 py-3">
          <div className="flex items-center justify-between">
            <p className="text-red-800">{error}</p>
            <button
              onClick={clearError}
              className="text-red-600 hover:text-red-800"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Chat Lab - primary workflow */}
      {mode === 'chat' && (
        <div className="flex-1 overflow-hidden">
          <ChatLab />
        </div>
      )}

      {/* Architect Studio */}
      {mode === 'architect' && (
        <div className="flex-1 flex overflow-hidden">
          <aside className="w-72 border-r bg-white flex-shrink-0">
            <SessionList
              sessions={sessions}
              currentSessionId={currentSession?.session_id}
              onSelectSession={selectSession}
              onDeleteSession={deleteSession}
              onCreateSession={createSession}
              isLoading={isSessionLoading}
            />
          </aside>

          <main className="flex-1 flex flex-col min-w-0 bg-white">
            <Chat
              messages={messages}
              onSendMessage={sendMessage}
              isSending={isSending}
              isLoading={isLoading}
              readyForOutput={readyForOutput}
              onGenerateOutput={generateOutput}
              onStartRefinement={currentSession ? handleStartRefinement : undefined}
              disabled={!currentSession}
            />
          </main>

          <aside className="w-96 border-l bg-gray-50 flex-shrink-0 overflow-hidden">
            {refinement.isActive ? (
              <RefinementPanel
                state={refinement.refinementState!}
                currentIteration={refinement.currentIteration}
                isGenerating={refinement.isGenerating}
                isRefining={refinement.isRefining}
                error={refinement.error}
                onRefine={refinement.refinePrompt}
                onAccept={refinement.acceptResult}
                onRegenerate={refinement.generateAndEvaluate}
                onClearError={refinement.clearError}
                onUpdatePrompt={refinement.updatePrompt}
              />
            ) : (
              <div className="overflow-y-auto h-full p-4 space-y-4">
                <ArchitectureViz
                  imageUrl={diagramImageUrl ?? undefined}
                  imageUrls={diagramImageUrls}
                  isGenerating={isGeneratingPreview}
                  onRequestGenerate={currentSession ? generatePreview : undefined}
                />

                {currentSession && (
                  <StatusPanel
                    architecture={architecture}
                    availableLogos={availableLogos}
                    sessionStatus={currentSession.status}
                    turnCount={currentSession.turn_count}
                    readyForOutput={readyForOutput}
                    imageProvider={imageProvider}
                    credentialMode={credentialMode}
                  />
                )}
              </div>
            )}
          </aside>
        </div>
      )}

      {/* Best Results */}
      {mode === 'best' && (
        <div className="flex-1 min-h-0">
          <BestResults
            onCreateArchitectSessionFromResult={handleCreateArchitectSessionFromResult}
          />
        </div>
      )}
    </div>
  );
}

export default App;
