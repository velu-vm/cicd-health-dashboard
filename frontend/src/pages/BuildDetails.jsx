import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, ExternalLink, Clock, GitBranch, User, Calendar } from 'lucide-react';
import { apiService } from '../services/api';
import StatusChip from '../components/StatusChip';
import RelativeTime from '../components/RelativeTime';
import LoadingSkeleton from '../components/LoadingSkeleton';
import EmptyState from '../components/EmptyState';

const BuildDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [build, setBuild] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBuild = async () => {
      try {
        setLoading(true);
        setError(null);
        const buildData = await apiService.getBuild(id);
        setBuild(buildData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch build details');
        console.error('Error fetching build:', err);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchBuild();
    }
  }, [id]);

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

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <LoadingSkeleton type="card" />
        </div>
      </div>
    );
  }

  if (error || !build) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <EmptyState
            type="error"
            title="Failed to Load Build Details"
            message={error || 'Build not found'}
            action={{
              label: 'Go Back',
              onClick: () => navigate('/')
            }}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </button>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Build #{build.external_id}
              </h1>
              <p className="text-gray-600 mt-1">
                {build.provider_name || 'GitHub Actions'} • {build.branch || 'main'}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <StatusChip status={build.status} size="lg" />
              {build.url && (
                <a
                  href={build.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                  View Build
                </a>
              )}
            </div>
          </div>
        </div>

        {/* Build Information Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Status */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <StatusChip status={build.status} size="sm" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Status</p>
                <p className="text-lg font-semibold text-gray-900 capitalize">
                  {build.status}
                </p>
              </div>
            </div>
          </div>

          {/* Duration */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Clock className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Duration</p>
                <p className="text-lg font-semibold text-gray-900">
                  {formatDuration(build.duration_seconds)}
                </p>
              </div>
            </div>
          </div>

          {/* Branch */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <GitBranch className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Branch</p>
                <p className="text-lg font-semibold text-gray-900">
                  {build.branch || 'main'}
                </p>
              </div>
            </div>
          </div>

          {/* Triggered By */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <User className="w-5 h-5 text-orange-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Triggered By</p>
                <p className="text-lg font-semibold text-gray-900">
                  {build.triggered_by || 'Unknown'}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Build Details */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Build Details</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-medium text-gray-600 mb-2">Started At</h3>
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-gray-400" />
                <RelativeTime date={build.started_at} />
              </div>
              <p className="text-sm text-gray-500 mt-1">
                {formatDate(build.started_at)}
              </p>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-600 mb-2">Finished At</h3>
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-gray-400" />
                {build.finished_at ? (
                  <RelativeTime date={build.finished_at} />
                ) : (
                  <span className="text-gray-500">Not finished</span>
                )}
              </div>
              <p className="text-sm text-gray-500 mt-1">
                {formatDate(build.finished_at)}
              </p>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-600 mb-2">Commit SHA</h3>
              <p className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">
                {build.commit_sha ? build.commit_sha.substring(0, 8) : 'N/A'}
              </p>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-600 mb-2">Provider</h3>
              <p className="text-sm text-gray-900">
                {build.provider_name || 'GitHub Actions'}
              </p>
            </div>
          </div>
        </div>

        {/* Raw Payload */}
        {build.raw_payload && (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Raw Payload</h2>
            <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm">
              <code>{JSON.stringify(build.raw_payload, null, 2)}</code>
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default BuildDetails;
