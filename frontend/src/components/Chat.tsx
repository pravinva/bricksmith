/**
 * Chat interface component for the architect conversation.
 */

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import type { ChatMessage } from '../types';

interface ChatProps {
  messages: ChatMessage[];
  onSendMessage: (message: string, imageBase64?: string, imageFilename?: string) => Promise<unknown>;
  isSending: boolean;
  isLoading: boolean;
  readyForOutput: boolean;
  onGenerateOutput: () => Promise<void>;
  onStartRefinement?: () => void;
  disabled?: boolean;
}

export function Chat({
  messages,
  onSendMessage,
  isSending,
  isLoading,
  readyForOutput,
  onGenerateOutput,
  onStartRefinement,
  disabled = false,
}: ChatProps) {
  const [input, setInput] = useState('');
  const [attachedImageBase64, setAttachedImageBase64] = useState<string | null>(null);
  const [attachedImageFilename, setAttachedImageFilename] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isSending || disabled) return;

    const message = input.trim();
    const imgBase64 = attachedImageBase64 ?? undefined;
    const imgFilename = attachedImageFilename ?? undefined;
    setInput('');
    setAttachedImageBase64(null);
    setAttachedImageFilename(null);
    await onSendMessage(message, imgBase64, imgFilename);
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type and size (max 10MB)
    const validTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      // Strip the data:image/...;base64, prefix
      const base64 = result.split(',')[1];
      setAttachedImageBase64(base64);
      setAttachedImageFilename(file.name);
    };
    reader.readAsDataURL(file);

    // Reset file input so the same file can be re-selected
    e.target.value = '';
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <p className="text-lg font-medium">Start a new conversation</p>
            <p className="text-sm mt-2">
              Describe your architecture problem to begin
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                {message.attachedImageBase64 && (
                  <div className="mb-2">
                    <img
                      src={`data:image/png;base64,${message.attachedImageBase64}`}
                      alt="Attached image"
                      className="rounded border border-white/30 max-h-48 w-auto"
                    />
                  </div>
                )}
                {message.imageUrl && (
                  <a
                    href={message.imageUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block mb-2"
                  >
                    <img
                      src={message.imageUrl}
                      alt="Generated diagram"
                      className="rounded border border-gray-200 w-full h-auto hover:opacity-90 transition-opacity"
                    />
                  </a>
                )}
                <div className={`prose prose-sm max-w-none ${message.role === 'user' ? 'prose-invert' : ''}`}>
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
                <div
                  className={`text-xs mt-2 ${
                    message.role === 'user' ? 'text-primary-200' : 'text-gray-400'
                  }`}
                >
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))
        )}

        {isSending && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-3">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce animation-delay-200"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce animation-delay-400"></div>
                </div>
                <span className="text-gray-500 text-sm">Thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Ready for output banner */}
      {readyForOutput && (
        <div className="bg-green-50 border-t border-green-200 px-4 py-3">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-800 font-medium">
                Architecture is ready!
              </p>
              <p className="text-green-600 text-sm">
                Generate a diagram or save the prompt
              </p>
            </div>
            <div className="flex gap-2">
              {onStartRefinement && (
                <button
                  onClick={onStartRefinement}
                  disabled={isSending || isLoading}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
                >
                  Generate &amp; Refine
                </button>
              )}
              <button
                onClick={onGenerateOutput}
                disabled={isSending || isLoading}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
              >
                Generate Output
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Input area */}
      <form onSubmit={handleSubmit} className="border-t p-4">
        {/* Image attachment preview */}
        {attachedImageBase64 && (
          <div className="mb-2 flex items-center gap-2">
            <img
              src={`data:image/png;base64,${attachedImageBase64}`}
              alt="Attachment preview"
              className="h-16 w-auto rounded border border-gray-300"
            />
            <span className="text-sm text-gray-500 truncate max-w-[200px]">
              {attachedImageFilename}
            </span>
            <button
              type="button"
              onClick={() => { setAttachedImageBase64(null); setAttachedImageFilename(null); }}
              className="text-gray-400 hover:text-red-500 text-lg leading-none"
              title="Remove attachment"
            >
              &times;
            </button>
          </div>
        )}
        <div className="flex space-x-2">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/png,image/jpeg,image/gif,image/webp"
            onChange={handleImageSelect}
            className="hidden"
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={disabled || isSending}
            className="px-3 py-2 text-gray-500 hover:text-primary-600 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            title="Attach image"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
            </svg>
          </button>
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={disabled ? 'Select or create a session to start' : 'Type your message...'}
            disabled={disabled || isSending}
            rows={2}
            className="flex-1 resize-none rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={!input.trim() || isSending || disabled}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
        <p className="text-xs text-gray-400 mt-2">
          Press Enter to send, Shift+Enter for new line
        </p>
      </form>
    </div>
  );
}
