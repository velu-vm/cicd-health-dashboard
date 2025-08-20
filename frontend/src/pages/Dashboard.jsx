import React, { useState, useEffect } from 'react';
import { RefreshCw, AlertTriangle } from 'lucide-react';
import { apiService } from '../services/api';
import SummaryCards from '../components/SummaryCards';
import MetricsChart from '../components/MetricsChart';
import BuildsTable from '../components/BuildsTable';
import BuildLogDrawer from '../components/BuildLogDrawer';
import FailureBanner from '../components/FailureBanner';
import LoadingSkeleton from '../components/LoadingSkeleton';

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [builds, setBuilds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedBuild, setSelectedBuild] = useState(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [showFailureBanner, setShowFailureBanner] = useState(true);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [metricsData, buildsData] = await Promise.all([
        apiService.getMetricsSummary(),
        apiService.getBuilds()
      ]);
      
      setMetrics(metricsData);
      setBuilds(buildsData.builds);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleBuildClick = (build) => {
    setSelectedBuild(build);
    setIsDrawerOpen(true);
  };

  const closeDrawer = () => {
    setIsDrawerOpen(false);
    setSelectedBuild(null);
  };

  const dismissFailureBanner = () => {
    setShowFailureBanner(false);
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <AlertTriangle className="w-12 h-12 text-red-400 mx-auto mb-4" />
            <h1 className="text-xl font-semibold text-red-800 mb-2">Failed to Load Dashboard</h1>
            <p className="text-red-700 mb-4">{error}</p>
            <button
              onClick={fetchData}
              className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold text-gray-900">CI/CD Health Dashboard</h1>
            <button
              onClick={fetchData}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              aria-label="Refresh dashboard data"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>
          
          {/* Failure Banner */}
          {metrics && metrics.last_build_status === 'failed' && showFailureBanner && (
            <FailureBanner
              isVisible={true}
              onDismiss={dismissFailureBanner}
              className="mb-6"
            />
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <LoadingSkeleton key={i} type="summary-card" />
              ))}
            </div>
            <LoadingSkeleton type="chart" />
            <LoadingSkeleton type="table-row" />
          </div>
        )}

        {/* Dashboard Content */}
        {!loading && metrics && (
          <>
            {/* Summary Cards */}
            <div className="mb-8">
              <SummaryCards metrics={metrics} />
            </div>

            {/* Metrics Chart */}
            <div className="mb-8">
              <MetricsChart metrics={metrics} loading={loading} />
            </div>

            {/* Builds Table */}
            <div className="mb-8">
              <BuildsTable 
                builds={builds} 
                onBuildClick={handleBuildClick}
                loading={loading}
              />
            </div>
          </>
        )}

        {/* Build Log Drawer */}
        <BuildLogDrawer
          isOpen={isDrawerOpen}
          onClose={closeDrawer}
          build={selectedBuild}
        />
      </div>
    </div>
  );
};

export default Dashboard;
