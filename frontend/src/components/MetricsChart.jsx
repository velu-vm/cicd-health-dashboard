import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { apiService } from '../services/api';
import LoadingSkeleton from './LoadingSkeleton';
import { BarChart3, TrendingUp } from 'lucide-react';

const MetricsChart = ({ metrics, loading }) => {
  const [chartData, setChartData] = useState([]);
  const [chartType, setChartType] = useState('bar');
  const [dataLoading, setDataLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch and aggregate build data for chart
  const fetchChartData = async () => {
    try {
      setDataLoading(true);
      setError(null);
      
      // Fetch builds from the last 7 days
      const buildsResponse = await apiService.getBuilds(500, 0);
      const builds = buildsResponse.builds;
      
      // Filter builds from last 7 days
      const sevenDaysAgo = new Date();
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
      
      const recentBuilds = builds.filter(build => 
        build.started_at && new Date(build.started_at) >= sevenDaysAgo
      );
      
      // Aggregate by day
      const aggregatedData = {};
      
      // Initialize last 7 days
      for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        const dateKey = date.toISOString().split('T')[0];
        aggregatedData[dateKey] = {
          date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          success: 0,
          failed: 0,
          running: 0,
          queued: 0
        };
      }
      
      // Count builds by status and date
      recentBuilds.forEach(build => {
        if (build.started_at) {
          const buildDate = new Date(build.started_at).toISOString().split('T')[0];
          if (aggregatedData[buildDate]) {
            switch (build.status.toLowerCase()) {
              case 'success':
                aggregatedData[buildDate].success++;
                break;
              case 'failed':
                aggregatedData[buildDate].failed++;
                break;
              case 'running':
                aggregatedData[buildDate].running++;
                break;
              case 'queued':
                aggregatedData[buildDate].queued++;
                break;
              default:
                // Count unknown statuses as failed for visibility
                aggregatedData[buildDate].failed++;
                break;
            }
          }
        }
      });
      
      // Convert to array and sort by date
      const chartDataArray = Object.values(aggregatedData).sort((a, b) => {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        return dateA.getTime() - dateB.getTime();
      });
      
      setChartData(chartDataArray);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch chart data');
      console.error('Error fetching chart data:', err);
    } finally {
      setDataLoading(false);
    }
  };

  useEffect(() => {
    if (!loading && metrics) {
      fetchChartData();
    }
  }, [loading, metrics]);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-md shadow-lg text-sm">
          <p className="font-semibold text-gray-900 mb-1">{label}</p>
          {payload.map((entry, index) => (
            <p key={`item-${index}`} style={{ color: entry.color }}>
              {`${entry.name}: ${entry.value}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  if (loading || dataLoading) {
    return <LoadingSkeleton type="chart" className="mb-8" />;
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <div className="text-center">
          <p className="text-red-600 mb-4">Failed to load chart data: {error}</p>
          <button
            onClick={fetchChartData}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!chartData || chartData.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <div className="text-center">
          <p className="text-gray-500">No chart data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
      {/* Header with chart type toggle */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900">Build Activity (Last 7 Days)</h2>
        <div className="flex items-center gap-4">
          {/* Chart Type Toggle */}
          <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setChartType('bar')}
              className={`p-2 rounded-md transition-colors ${
                chartType === 'bar' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              aria-label="Switch to bar chart"
            >
              <BarChart3 className="w-4 h-4" />
            </button>
            <button
              onClick={() => setChartType('line')}
              className={`p-2 rounded-md transition-colors ${
                chartType === 'line' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              aria-label="Switch to line chart"
            >
              <TrendingUp className="w-4 h-4" />
            </button>
          </div>
          
          {/* Legend */}
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-500 rounded"></div>
              <span>Success</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-red-500 rounded"></div>
              <span>Failed</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-amber-500 rounded"></div>
              <span>Running</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-gray-500 rounded"></div>
              <span>Queued</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Chart Container */}
      <div className="h-80" role="img" aria-label={`Build activity ${chartType} chart showing success and failure counts over the last 7 days`}>
        <ResponsiveContainer width="100%" height="100%">
          {chartType === 'bar' ? (
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis 
                dataKey="date" 
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={false}
              />
              <YAxis 
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                tickFormatter={(value) => `${value}`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Bar 
                dataKey="success" 
                fill="#10b981" 
                radius={[4, 4, 0, 0]}
                name="Success"
              />
              <Bar 
                dataKey="failed" 
                fill="#ef4444" 
                radius={[4, 4, 0, 0]}
                name="Failed"
              />
              <Bar 
                dataKey="running" 
                fill="#f59e0b" 
                radius={[4, 4, 0, 0]}
                name="Running"
              />
              <Bar 
                dataKey="queued" 
                fill="#6b7280" 
                radius={[4, 4, 0, 0]}
                name="Queued"
              />
            </BarChart>
          ) : (
            <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis 
                dataKey="date" 
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={false}
              />
              <YAxis 
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                tickFormatter={(value) => `${value}`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="success" 
                stroke="#10b981" 
                strokeWidth={2}
                dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
                name="Success"
              />
              <Line 
                type="monotone" 
                dataKey="failed" 
                stroke="#ef4444" 
                strokeWidth={2}
                dot={{ fill: '#ef4444', strokeWidth: 2, r: 4 }}
                name="Failed"
              />
              <Line 
                type="monotone" 
                dataKey="running" 
                stroke="#f59e0b" 
                strokeWidth={2}
                dot={{ fill: '#f59e0b', strokeWidth: 2, r: 4 }}
                name="Running"
              />
              <Line 
                type="monotone" 
                dataKey="queued" 
                stroke="#6b7280" 
                strokeWidth={2}
                dot={{ fill: '#6b7280', strokeWidth: 2, r: 4 }}
                name="Queued"
              />
            </LineChart>
          )}
        </ResponsiveContainer>
      </div>
      
      {/* Data Source Info */}
      <div className="mt-4 text-center">
        <p className="text-xs text-gray-500">
          Chart data aggregated from {chartData.reduce((sum, day) => sum + day.success + day.failed + day.running + day.queued, 0)} builds over the last 7 days
        </p>
        <p className="text-xs text-gray-400 mt-1">
          Toggle between bar and line chart views
        </p>
      </div>
    </div>
  );
};

export default MetricsChart;
