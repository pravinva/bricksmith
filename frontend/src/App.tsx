/**
 * Main application component for Bricksmith Architect.
 */

import { useArchitect } from './hooks/useArchitect';
import { useRefinement } from './hooks/useRefinement';
import { Chat } from './components/Chat';
import { ArchitectureViz } from './components/ArchitectureViz';
import { RefinementPanel } from './components/RefinementPanel';
import { SessionList } from './components/SessionList';
import { StatusPanel } from './components/StatusPanel';
import { CliRunner } from './components/CliRunner';
import { BestResults } from './components/BestResults';
import { useState, useCallback } from 'react';
import type { BestResultItem } from './types';

function App() {
  const [mode, setMode] = useState<'architect' | 'cli' | 'best'>('architect');
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
    setMode('architect');
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
            <h1 className="text-xl font-bold text-gray-900">
              Bricksmith Architect
            </h1>
            <p className="text-sm text-gray-500">
              Collaborative architecture diagram design
            </p>
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
                title="Image generation auth mode for this session"
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
            onClick={() => setMode('cli')}
            className={`px-3 py-1.5 text-sm rounded ${
              mode === 'cli'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            CLI Mirror
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

      {mode === 'architect' ? (
        <div className="flex-1 flex overflow-hidden">
          {/* Left sidebar - Session list */}
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

          {/* Main area - Chat */}
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

          {/* Right sidebar - Refinement panel or architecture visualization */}
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
              />
            ) : (
              <div className="overflow-y-auto h-full p-4 space-y-4">
                <ArchitectureViz
                  imageUrl={diagramImageUrl ?? undefined}
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
      ) : mode === 'cli' ? (
        <div className="flex-1 min-h-0">
          <CliRunner />
        </div>
      ) : (
        <div className="flex-1 min-h-0">
          <BestResults
            onCreateArchitectSessionFromResult={
              handleCreateArchitectSessionFromResult
            }
            onOpenCliMirror={() => setMode('cli')}
          />
        </div>
      )}
    </div>
  );
}

export default App;
