import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, RefreshCw } from 'lucide-react';
import SummaryCards from '../components/SummaryCards';
import MetricsChart from '../components/MetricsChart';
import BuildsTable from '../components/BuildsTable';
import BuildLogDrawer from '../components/BuildLogDrawer';
import { apiService, MetricsSummary, Build } from '../services/api';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [builds, setBuilds] = useState<Build[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedBuild, setSelectedBuild] = useState<Build | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [metricsData, buildsData] = await Promise.all([
        apiService.getMetricsSummary(),
        apiService.getBuilds(50, 0)
      ]);
      
      setMetrics(metricsData);
      setBuilds(buildsData.builds);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      // Set mock data for development
      setMetrics({
        window_days: 7,
        success_rate: 0.85,
        failure_rate: 0.15,
        avg_build_time_seconds: 412.3,
        last_build_status: 'success',
        last_updated: new Date().toISOString()
      });
      setBuilds([]);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

  const handleBuildClick = (build: Build) => {
    setSelectedBuild(build);
    setDrawerOpen(true);
  };

  const closeDrawer = () => {
    setDrawerOpen(false);
    setSelectedBuild(null);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Activity className="w-8 h-8 text-primary-600" />
              <h1 className="text-2xl font-bold text-gray-900">
                CI/CD Health Dashboard
              </h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={handleRefresh}
                disabled={refreshing}
                className="btn btn-secondary flex items-center space-x-2"
              >
                <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
                <span>{refreshing ? 'Refreshing...' : 'Refresh'}</span>
              </button>
              
              <button
                onClick={() => navigate('/builds')}
                className="btn btn-primary"
              >
                View All Builds
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Summary Cards */}
        <SummaryCards metrics={metrics!} loading={loading} />
        
        {/* Metrics Chart */}
        <MetricsChart metrics={metrics!} loading={loading} />
        
        {/* Builds Table */}
        <BuildsTable 
          builds={builds} 
          loading={loading} 
          onBuildClick={handleBuildClick}
        />
      </main>

      {/* Build Log Drawer */}
      <BuildLogDrawer
        build={selectedBuild}
        isOpen={drawerOpen}
        onClose={closeDrawer}
      />
    </div>
  );
};

export default Dashboard;
