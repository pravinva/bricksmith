/**
 * Main application component for Nano Banana Architect.
 */

import { useArchitect } from './hooks/useArchitect';
import { Chat } from './components/Chat';
import { ArchitectureViz } from './components/ArchitectureViz';
import { SessionList } from './components/SessionList';
import { StatusPanel } from './components/StatusPanel';

function App() {
  const {
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
    createSession,
    selectSession,
    deleteSession,
    sendMessage,
    generateOutput,
    generatePreview,
    clearError,
  } = useArchitect();

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b px-6 py-3">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              Nano Banana Architect
            </h1>
            <p className="text-sm text-gray-500">
              Collaborative architecture diagram design
            </p>
          </div>
          {currentSession && (
            <div className="text-sm text-gray-600">
              Session: <span className="font-mono">{currentSession.session_id}</span>
            </div>
          )}
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

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left sidebar - Session list */}
        <aside className="w-72 border-r bg-white flex-shrink-0">
          <SessionList
            sessions={sessions}
            currentSessionId={currentSession?.session_id}
            onSelectSession={selectSession}
            onDeleteSession={deleteSession}
            onCreateSession={createSession}
            isLoading={isLoading}
          />
        </aside>

        {/* Main area - Chat */}
        <main className="flex-1 flex flex-col min-w-0 bg-white">
          <Chat
            messages={messages}
            onSendMessage={sendMessage}
            isLoading={isLoading}
            readyForOutput={readyForOutput}
            onGenerateOutput={generateOutput}
            disabled={!currentSession}
          />
        </main>

        {/* Right sidebar - Architecture visualization and status */}
        <aside className="w-96 border-l bg-gray-50 flex-shrink-0 overflow-y-auto p-4 space-y-4">
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
            />
          )}
        </aside>
      </div>
    </div>
  );
}

export default App;
