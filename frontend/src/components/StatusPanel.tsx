/**
 * Status panel showing current architecture state and available logos.
 */

import type { ArchitectureState } from '../types';

interface StatusPanelProps {
  architecture: ArchitectureState;
  availableLogos: string[];
  sessionStatus: string;
  turnCount: number;
  readyForOutput: boolean;
}

export function StatusPanel({
  architecture,
  availableLogos,
  sessionStatus,
  turnCount,
  readyForOutput,
}: StatusPanelProps) {
  const { components, connections } = architecture;

  return (
    <div className="space-y-4">
      {/* Session status */}
      <div className="bg-white rounded-lg border p-4">
        <h3 className="font-medium text-gray-900 mb-3">Session Status</h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-500">Status:</span>
            <span
              className={`font-medium ${
                sessionStatus === 'completed'
                  ? 'text-green-600'
                  : 'text-blue-600'
              }`}
            >
              {sessionStatus}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Turns:</span>
            <span className="font-medium">{turnCount}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Ready for output:</span>
            <span className={readyForOutput ? 'text-green-600' : 'text-gray-400'}>
              {readyForOutput ? 'Yes' : 'Not yet'}
            </span>
          </div>
        </div>
      </div>

      {/* Components */}
      <div className="bg-white rounded-lg border p-4">
        <h3 className="font-medium text-gray-900 mb-3">
          Components ({components.length})
        </h3>
        {components.length === 0 ? (
          <p className="text-sm text-gray-400">No components defined yet</p>
        ) : (
          <ul className="space-y-2">
            {components.map((comp) => (
              <li
                key={comp.id}
                className="flex items-start justify-between text-sm"
              >
                <div>
                  <span className="font-medium text-gray-900">{comp.label}</span>
                  <span className="ml-2 px-1.5 py-0.5 text-xs bg-gray-100 rounded">
                    {comp.type}
                  </span>
                </div>
                {comp.logo_name && (
                  <span className="text-xs text-primary-600">
                    {comp.logo_name}
                  </span>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Connections */}
      <div className="bg-white rounded-lg border p-4">
        <h3 className="font-medium text-gray-900 mb-3">
          Connections ({connections.length})
        </h3>
        {connections.length === 0 ? (
          <p className="text-sm text-gray-400">No connections defined yet</p>
        ) : (
          <ul className="space-y-1">
            {connections.map((conn, idx) => (
              <li key={idx} className="text-sm text-gray-600">
                <span className="font-medium">{conn.from_id}</span>
                <span className="mx-2 text-gray-400">→</span>
                <span className="font-medium">{conn.to_id}</span>
                {conn.label && (
                  <span className="ml-2 text-gray-400">({conn.label})</span>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Available logos */}
      <div className="bg-white rounded-lg border p-4">
        <h3 className="font-medium text-gray-900 mb-3">
          Available Logos ({availableLogos.length})
        </h3>
        {availableLogos.length === 0 ? (
          <p className="text-sm text-gray-400">No logos loaded</p>
        ) : (
          <div className="flex flex-wrap gap-1">
            {availableLogos.map((logo) => (
              <span
                key={logo}
                className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
              >
                {logo}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
