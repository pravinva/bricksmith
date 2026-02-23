/**
 * Architecture visualization component showing generated diagram images.
 */

import { useState } from 'react';
import type { GenerationSettingsRequest } from '../types';
import { GenerationSettingsPanel } from './GenerationSettings';

interface ArchitectureVizProps {
  imageUrl?: string;
  imageUrls?: string[];
  isGenerating?: boolean;
  onRequestGenerate?: (settings?: GenerationSettingsRequest) => void;
  className?: string;
}

export function ArchitectureViz({
  imageUrl,
  imageUrls = [],
  isGenerating = false,
  onRequestGenerate,
  className = ''
}: ArchitectureVizProps) {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [genSettings, setGenSettings] = useState<GenerationSettingsRequest>({
    preset: 'balanced',
    image_size: '2K',
    aspect_ratio: '16:9',
    num_variants: 1,
  });

  return (
    <>
      <div className={`bg-white rounded-lg border ${className}`}>
        <div className="border-b px-4 py-2 flex items-center justify-between">
          <div>
            <h3 className="font-medium text-gray-900">Architecture Diagram</h3>
            <p className="text-xs text-gray-500">
              {imageUrl ? 'Generated diagram' : 'No diagram generated yet'}
            </p>
          </div>
          {imageUrl && (
            <button
              onClick={() => setIsFullscreen(true)}
              className="p-1 text-gray-400 hover:text-gray-600"
              title="View fullscreen"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
              </svg>
            </button>
          )}
        </div>

        {/* Generation settings */}
        {onRequestGenerate && (
          <div className="px-4 pt-3">
            <GenerationSettingsPanel
              settings={genSettings}
              onChange={setGenSettings}
              disabled={isGenerating}
              showVariants
            />
          </div>
        )}

        <div className="p-4">
          {isGenerating ? (
            <div className="flex flex-col items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
              <p className="text-gray-500">Generating diagram...</p>
            </div>
          ) : imageUrls.length > 1 ? (
            <div className="grid grid-cols-2 gap-2">
              {imageUrls.map((url, idx) => (
                <div
                  key={url}
                  className="relative rounded overflow-hidden border cursor-pointer hover:ring-2 hover:ring-primary-400"
                  onClick={() => setIsFullscreen(true)}
                >
                  <img src={url} alt={`Variant ${idx + 1}`} className="w-full h-auto" />
                  <span className="absolute top-1 left-1 bg-black/60 text-white text-[10px] px-1.5 py-0.5 rounded">
                    V{idx + 1}
                  </span>
                </div>
              ))}
            </div>
          ) : imageUrl ? (
            <div className="relative">
              <img
                src={imageUrl}
                alt="Architecture diagram"
                className="w-full h-auto rounded cursor-pointer hover:opacity-90 transition-opacity"
                onClick={() => setIsFullscreen(true)}
              />
            </div>
          ) : (
            <div className="text-gray-400 text-center py-12">
              <svg
                className="w-16 h-16 mx-auto mb-3 text-gray-300"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <p className="mb-4">Diagram will appear here after generation</p>
              {onRequestGenerate && (
                <button
                  onClick={() => onRequestGenerate(genSettings)}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm"
                >
                  Generate Preview
                </button>
              )}
            </div>
          )}

          {/* Regenerate button when image already exists */}
          {(imageUrl || imageUrls.length > 0) && onRequestGenerate && !isGenerating && (
            <div className="mt-3 text-center">
              <button
                onClick={() => onRequestGenerate(genSettings)}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm"
              >
                Generate Preview
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Fullscreen modal */}
      {isFullscreen && imageUrl && (
        <div
          className="fixed inset-0 z-50 bg-black bg-opacity-90 flex items-center justify-center p-4"
          onClick={() => setIsFullscreen(false)}
        >
          <button
            onClick={() => setIsFullscreen(false)}
            className="absolute top-4 right-4 text-white hover:text-gray-300"
          >
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <img
            src={imageUrl}
            alt="Architecture diagram"
            className="max-w-full max-h-full object-contain"
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      )}
    </>
  );
}
