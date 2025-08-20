import React from 'react';
import { X, Copy, Check } from 'lucide-react';
import StatusChip from './StatusChip';
import RelativeTime from './RelativeTime';

const BuildLogDrawer = ({ isOpen, onClose, build }) => {
  const [copied, setCopied] = React.useState(false);

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy to clipboard:', err);
    }
  };

  if (!isOpen || !build) return null;

  const formatDuration = (seconds) => {
    if (!seconds) return 'N/A';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={onClose}
        aria-hidden="true"
      />
      
      {/* Drawer */}
      <div
        className={`fixed right-0 top-0 h-full w-full md:w-2/3 lg:w-1/2 bg-white shadow-xl z-50 transform transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="drawer-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <h2 id="drawer-title" className="text-lg font-semibold text-gray-900">
              Build #{build.external_id}
            </h2>
            <StatusChip status={build.status} size="sm" />
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Close drawer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="space-y-6">
            {/* Build Overview */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Build Overview</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Provider:</span>
                  <span className="ml-2 text-gray-900">{build.provider_name || 'GitHub Actions'}</span>
                </div>
                <div>
                  <span className="text-gray-500">Branch:</span>
                  <span className="ml-2 text-gray-900">{build.branch || 'main'}</span>
                </div>
                <div>
                  <span className="text-gray-500">Duration:</span>
                  <span className="ml-2 text-gray-900">{formatDuration(build.duration_seconds)}</span>
                </div>
                <div>
                  <span className="text-gray-500">Triggered by:</span>
                  <span className="ml-2 text-gray-900">{build.triggered_by || 'Unknown'}</span>
                </div>
                <div>
                  <span className="text-gray-500">Started:</span>
                  <span className="ml-2 text-gray-900">
                    <RelativeTime date={build.started_at} />
                  </span>
                </div>
                <div>
                  <span className="text-gray-500">Finished:</span>
                  <span className="ml-2 text-gray-900">
                    {build.finished_at ? (
                      <RelativeTime date={build.finished_at} />
                    ) : (
                      'Not finished'
                    )}
                  </span>
                </div>
              </div>
            </div>

            {/* Commit Information */}
            {build.commit_sha && (
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-700 mb-3">Commit Information</h3>
                <div className="flex items-center gap-2">
                  <span className="text-gray-500">SHA:</span>
                  <code className="bg-gray-200 px-2 py-1 rounded text-sm font-mono">
                    {build.commit_sha}
                  </code>
                  <button
                    onClick={() => copyToClipboard(build.commit_sha)}
                    className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                    aria-label="Copy commit SHA"
                  >
                    {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>
              </div>
            )}

            {/* External Link */}
            {build.url && (
              <div className="bg-blue-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-blue-700 mb-3">External Link</h3>
                <a
                  href={build.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 underline break-all"
                >
                  {build.url}
                </a>
              </div>
            )}

            {/* Raw Payload */}
            {build.raw_payload && (
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-sm font-medium text-gray-700">Raw Payload</h3>
                  <button
                    onClick={() => copyToClipboard(JSON.stringify(build.raw_payload, null, 2))}
                    className="flex items-center gap-2 px-3 py-1 text-sm text-gray-600 hover:text-gray-800 transition-colors border border-gray-300 rounded-md"
                    aria-label="Copy raw payload"
                  >
                    {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                    {copied ? 'Copied!' : 'Copy'}
                  </button>
                </div>
                <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                  <pre className="text-sm text-gray-100">
                    <code>{JSON.stringify(build.raw_payload, null, 2)}</code>
                  </pre>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default BuildLogDrawer;
