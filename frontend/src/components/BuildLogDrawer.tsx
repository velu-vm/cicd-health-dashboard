import React from 'react';
import { Build } from '../services/api';
import { X, ExternalLink, GitBranch, Clock, User, Calendar, Hash, Activity } from 'lucide-react';

interface BuildLogDrawerProps {
  build: Build | null;
  isOpen: boolean;
  onClose: () => void;
}

const BuildLogDrawer: React.FC<BuildLogDrawerProps> = ({ build, isOpen, onClose }) => {
  if (!build) return null;

  const formatDuration = (seconds: number | null) => {
    if (!seconds) return 'N/A';
    if (seconds < 60) return `${seconds}s`;
    if (seconds < 3600) return `${Math.round(seconds / 60)}m`;
    return `${Math.round(seconds / 3600)}h`;
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const formatCommitSha = (sha: string | null) => {
    if (!sha) return 'N/A';
    return sha.substring(0, 8);
  };

  const getStatusChip = (status: string) => {
    const statusClasses = {
      success: 'status-chip status-success',
      failed: 'status-chip status-failed',
      running: 'status-chip status-running',
      queued: 'status-chip status-queued'
    };
    
    const statusText = {
      success: 'Success',
      failed: 'Failed',
      running: 'Running',
      queued: 'Queued'
    };
    
    return (
      <span className={statusClasses[status as keyof typeof statusClasses] || 'status-chip status-queued'}>
        {statusText[status as keyof typeof statusText] || status}
      </span>
    );
  };

  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={onClose}
        />
      )}
      
      {/* Drawer */}
      <div className={`fixed right-0 top-0 h-full w-full md:w-2/3 lg:w-1/2 bg-white shadow-2xl transform transition-transform duration-300 ease-in-out z-50 ${
        isOpen ? 'translate-x-0' : 'translate-x-full'
      }`}>
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <Activity className="w-6 h-6 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              Build #{build.external_id}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto h-full">
          {/* Build Summary */}
          <div className="mb-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Status and Basic Info */}
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  {getStatusChip(build.status)}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Provider</label>
                  <div className="flex items-center space-x-2">
                    <GitBranch className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{build.provider_name || 'Unknown'}</span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Branch</label>
                  <div className="flex items-center space-x-2">
                    <GitBranch className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{build.branch}</span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Commit SHA</label>
                  <div className="flex items-center space-x-2">
                    <Hash className="w-4 h-4 text-gray-400" />
                    <span className="font-mono text-gray-900">{formatCommitSha(build.commit_sha)}</span>
                  </div>
                </div>
              </div>
              
              {/* Timing and Duration */}
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Duration</label>
                  <div className="flex items-center space-x-2">
                    <Clock className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{formatDuration(build.duration_seconds)}</span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Started At</label>
                  <div className="flex items-center space-x-2">
                    <Calendar className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{formatDate(build.started_at)}</span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Finished At</label>
                  <div className="flex items-center space-x-2">
                    <Calendar className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{formatDate(build.finished_at)}</span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Triggered By</label>
                  <div className="flex items-center space-x-2">
                    <User className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{build.triggered_by || 'Unknown'}</span>
                  </div>
                </div>
              </div>
            </div>
            
            {/* External Link */}
            {build.url && (
              <div className="mt-6">
                <a
                  href={build.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-2 text-primary-600 hover:text-primary-800 font-medium"
                >
                  <ExternalLink className="w-4 h-4" />
                  <span>View in GitHub Actions</span>
                </a>
              </div>
            )}
          </div>

          {/* Raw Payload */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Raw Payload</h3>
            <div className="bg-gray-50 rounded-lg p-4 overflow-auto">
              <pre className="text-sm text-gray-800 whitespace-pre-wrap">
                {JSON.stringify(build.raw_payload, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default BuildLogDrawer;
