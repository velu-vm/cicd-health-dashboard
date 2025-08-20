import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, ExternalLink, GitBranch, Clock, User, Calendar, Hash, Activity, AlertCircle } from 'lucide-react';
import { apiService, Build } from '../services/api';

const BuildDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [build, setBuild] = useState<Build | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBuild = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        const buildData = await apiService.getBuild(parseInt(id));
        setBuild(buildData);
      } catch (err) {
        console.error('Failed to fetch build:', err);
        setError('Failed to load build details. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchBuild();
  }, [id]);

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

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading build details...</p>
        </div>
      </div>
    );
  }

  if (error || !build) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Build Not Found</h2>
          <p className="text-gray-600 mb-6">{error || 'The requested build could not be found.'}</p>
          <button
            onClick={() => navigate('/')}
            className="btn btn-primary"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/')}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              
              <div className="flex items-center space-x-3">
                <Activity className="w-8 h-8 text-primary-600" />
                <div>
                  <h1 className="text-xl font-semibold text-gray-900">
                    Build #{build.external_id}
                  </h1>
                  <p className="text-sm text-gray-500">
                    {build.provider_name || 'Unknown Provider'}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {getStatusChip(build.status)}
              
              {build.url && (
                <a
                  href={build.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-primary flex items-center space-x-2"
                >
                  <ExternalLink className="w-4 h-4" />
                  <span>View in GitHub</span>
                </a>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Build Information */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Info Card */}
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Build Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
            </div>

            {/* Raw Payload Card */}
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Raw Payload</h2>
              <div className="bg-gray-50 rounded-lg p-4 overflow-auto max-h-96">
                <pre className="text-sm text-gray-800 whitespace-pre-wrap">
                  {JSON.stringify(build.raw_payload, null, 2)}
                </pre>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Build ID Card */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Build Details</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Build ID</label>
                  <p className="text-sm text-gray-900 font-mono">#{build.external_id}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Internal ID</label>
                  <p className="text-sm text-gray-900 font-mono">{build.id}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Created At</label>
                  <p className="text-sm text-gray-900">{formatDate(build.created_at)}</p>
                </div>
              </div>
            </div>

            {/* Actions Card */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
              <div className="space-y-3">
                <button
                  onClick={() => navigate('/')}
                  className="w-full btn btn-secondary"
                >
                  Back to Dashboard
                </button>
                
                {build.url && (
                  <a
                    href={build.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full btn btn-primary flex items-center justify-center space-x-2"
                  >
                    <ExternalLink className="w-4 h-4" />
                    <span>View in GitHub</span>
                  </a>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default BuildDetails;
