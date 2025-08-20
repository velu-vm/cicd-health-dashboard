import React from 'react';
import { MetricsSummary } from '../services/api';
import { 
  CheckCircle, 
  XCircle, 
  Clock, 
  Activity,
  TrendingUp,
  TrendingDown
} from 'lucide-react';

interface SummaryCardsProps {
  metrics: MetricsSummary;
  loading?: boolean;
}

const SummaryCards: React.FC<SummaryCardsProps> = ({ metrics, loading = false }) => {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="card animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    );
  }

  const formatPercentage = (value: number) => `${(value * 100).toFixed(1)}%`;
  const formatDuration = (seconds: number | null) => {
    if (!seconds) return 'N/A';
    if (seconds < 60) return `${seconds}s`;
    if (seconds < 3600) return `${Math.round(seconds / 60)}m`;
    return `${Math.round(seconds / 3600)}h`;
  };

  const getStatusColor = (status: string | null) => {
    if (!status) return 'text-gray-500';
    switch (status.toLowerCase()) {
      case 'success': return 'text-success-600';
      case 'failed': return 'text-danger-600';
      case 'running': return 'text-warning-600';
      case 'queued': return 'text-gray-600';
      default: return 'text-gray-500';
    }
  };

  const getStatusIcon = (status: string | null) => {
    if (!status) return <Activity className="w-5 h-5" />;
    switch (status.toLowerCase()) {
      case 'success': return <CheckCircle className="w-5 h-5" />;
      case 'failed': return <XCircle className="w-5 h-5" />;
      case 'running': return <Clock className="w-5 h-5" />;
      case 'queued': return <Clock className="w-5 h-5" />;
      default: return <Activity className="w-5 h-5" />;
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {/* Success Rate */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600">Success Rate</p>
            <p className="text-2xl font-bold text-success-600">
              {formatPercentage(metrics.success_rate)}
            </p>
          </div>
          <div className="p-3 bg-success-100 rounded-full">
            <TrendingUp className="w-6 h-6 text-success-600" />
          </div>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Last {metrics.window_days} days
        </p>
      </div>

      {/* Failure Rate */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600">Failure Rate</p>
            <p className="text-2xl font-bold text-danger-600">
              {formatPercentage(metrics.failure_rate)}
            </p>
          </div>
          <div className="p-3 bg-danger-100 rounded-full">
            <TrendingDown className="w-6 h-6 text-danger-600" />
          </div>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Last {metrics.window_days} days
        </p>
      </div>

      {/* Average Build Time */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600">Avg Build Time</p>
            <p className="text-2xl font-bold text-primary-600">
              {formatDuration(metrics.avg_build_time_seconds)}
            </p>
          </div>
          <div className="p-3 bg-primary-100 rounded-full">
            <Clock className="w-6 h-6 text-primary-600" />
          </div>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Completed builds only
        </p>
      </div>

      {/* Last Build Status */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600">Last Build</p>
            <p className={`text-2xl font-bold ${getStatusColor(metrics.last_build_status)}`}>
              {metrics.last_build_status || 'N/A'}
            </p>
          </div>
          <div className={`p-3 rounded-full ${
            metrics.last_build_status === 'success' ? 'bg-success-100' :
            metrics.last_build_status === 'failed' ? 'bg-danger-100' :
            metrics.last_build_status === 'running' ? 'bg-warning-100' :
            'bg-gray-100'
          }`}>
            {getStatusIcon(metrics.last_build_status)}
          </div>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Most recent
        </p>
      </div>
    </div>
  );
};

export default SummaryCards;
