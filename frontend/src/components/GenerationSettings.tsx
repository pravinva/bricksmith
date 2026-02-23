/**
 * Collapsible generation settings panel for controlling image generation parameters.
 * Used by both RefinementPanel and ArchitectureViz.
 */

import { useState } from 'react';
import type { GenerationSettingsRequest } from '../types';
import { TEMPERATURE_PRESETS, IMAGE_SIZES, ASPECT_RATIOS } from '../types';

interface GenerationSettingsPanelProps {
  settings: GenerationSettingsRequest;
  onChange: (settings: GenerationSettingsRequest) => void;
  disabled?: boolean;
  showVariants?: boolean;
}

function buildSummary(settings: GenerationSettingsRequest): string {
  const parts: string[] = [];
  const preset = TEMPERATURE_PRESETS.find(p => p.value === settings.preset);
  parts.push(preset?.label || 'Balanced');
  parts.push(settings.image_size || '2K');
  parts.push(settings.aspect_ratio || '16:9');
  if (settings.num_variants && settings.num_variants > 1) {
    parts.push(`${settings.num_variants}x`);
  }
  return parts.join(' / ');
}

export function GenerationSettingsPanel({
  settings,
  onChange,
  disabled = false,
  showVariants = false,
}: GenerationSettingsPanelProps) {
  const [isOpen, setIsOpen] = useState(false);

  const update = (partial: Partial<GenerationSettingsRequest>) => {
    onChange({ ...settings, ...partial });
  };

  return (
    <div className="bg-white rounded-lg border">
      {/* Toggle header */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-3 py-2 flex items-center justify-between text-left hover:bg-gray-50 rounded-lg"
        disabled={disabled}
      >
        <div className="flex items-center gap-2">
          <svg
            className={`w-4 h-4 text-gray-400 transition-transform ${isOpen ? 'rotate-90' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
          <span className="text-sm font-medium text-gray-700">Generation settings</span>
        </div>
        <span className="text-xs text-gray-500">{buildSummary(settings)}</span>
      </button>

      {/* Expanded content */}
      {isOpen && (
        <div className="px-3 pb-3 space-y-3 border-t">
          {/* Temperature preset */}
          <div className="pt-3">
            <label className="block text-xs font-medium text-gray-600 mb-1">
              Temperature preset
            </label>
            <select
              value={settings.preset || 'balanced'}
              onChange={(e) => update({ preset: e.target.value })}
              disabled={disabled}
              className="w-full text-sm border border-gray-300 rounded px-2 py-1.5 focus:outline-none focus:ring-1 focus:ring-primary-500 disabled:opacity-50"
            >
              {TEMPERATURE_PRESETS.map((p) => (
                <option key={p.value} value={p.value}>
                  {p.label} (temp {p.temp})
                </option>
              ))}
            </select>
          </div>

          {/* Image size */}
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Image size</label>
            <div className="flex gap-1">
              {IMAGE_SIZES.map((size) => (
                <button
                  key={size}
                  type="button"
                  onClick={() => update({ image_size: size })}
                  disabled={disabled}
                  className={`flex-1 px-2 py-1 text-xs rounded border ${
                    (settings.image_size || '2K') === size
                      ? 'bg-primary-600 text-white border-primary-600'
                      : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50'
                  } disabled:opacity-50`}
                >
                  {size}
                </button>
              ))}
            </div>
          </div>

          {/* Aspect ratio */}
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Aspect ratio</label>
            <div className="flex gap-1 flex-wrap">
              {ASPECT_RATIOS.map((ratio) => (
                <button
                  key={ratio}
                  type="button"
                  onClick={() => update({ aspect_ratio: ratio })}
                  disabled={disabled}
                  className={`px-2 py-1 text-xs rounded border ${
                    (settings.aspect_ratio || '16:9') === ratio
                      ? 'bg-primary-600 text-white border-primary-600'
                      : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50'
                  } disabled:opacity-50`}
                >
                  {ratio}
                </button>
              ))}
            </div>
          </div>

          {/* Num variants */}
          {showVariants && (
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Variants: {settings.num_variants || 1}
              </label>
              <input
                type="range"
                min={1}
                max={8}
                value={settings.num_variants || 1}
                onChange={(e) => update({ num_variants: Number(e.target.value) })}
                disabled={disabled}
                className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600 disabled:opacity-50"
              />
              <div className="flex justify-between text-[10px] text-gray-400">
                <span>1</span>
                <span>8</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
