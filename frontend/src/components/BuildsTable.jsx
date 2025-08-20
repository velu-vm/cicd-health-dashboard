import React, { useState, useMemo } from 'react';
import { ExternalLink, Eye, GitBranch, Clock, User } from 'lucide-react';
import StatusChip from './StatusChip';
import RelativeTime from './RelativeTime';
import FilterBar from './FilterBar';
import LoadingSkeleton from './LoadingSkeleton';
import EmptyState from './EmptyState';
import BuildLogDrawer from './BuildLogDrawer';

const BuildsTable = ({ builds, loading, onBuildClick }) => {
  const [statusFilter, setStatusFilter] = useState('');
  const [branchFilter, setBranchFilter] = useState('');
  const [selectedBuild, setSelectedBuild] = useState(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  // Extract unique values for filters
  const availableStatuses = useMemo(() => {
    const statuses = [...new Set(builds.map(build => build.status))];
    return statuses.sort();
  }, [builds]);

  const availableBranches = useMemo(() => {
    const branches = [...new Set(builds.map(build => build.branch).filter(Boolean))];
    return branches.sort();
  }, [builds]);

  // Apply filters
  const filteredBuilds = useMemo(() => {
    return builds.filter(build => {
      const matchesStatus = !statusFilter || build.status === statusFilter;
      const matchesBranch = !branchFilter || build.branch === branchFilter;
      return matchesStatus && matchesBranch;
    });
  }, [builds, statusFilter, branchFilter]);

  const clearFilters = () => {
    setStatusFilter('');
    setBranchFilter('');
  };

  const openLogDrawer = (build) => {
    setSelectedBuild(build);
    setIsDrawerOpen(true);
  };

  const closeLogDrawer = () => {
    setIsDrawerOpen(false);
    setSelectedBuild(null);
  };

  const formatDuration = (seconds) => {
    if (!seconds) return '--';
    if (seconds < 60) return `${seconds}s`;
    if (seconds < 3600) return `${Math.round(seconds / 60)}m`;
    return `${Math.round(seconds / 3600)}h`;
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Recent Builds</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {[...Array(5)].map((_, i) => (
            <LoadingSkeleton key={i} type="table-row" />
          ))}
        </div>
      </div>
    );
  }

  if (builds.length === 0) {
    return (
      <EmptyState
        type="no-data"
        title="No Builds Available"
        message="There are no builds to display. Start a build or check your CI/CD configuration."
        action={{
          label: "Refresh",
          onClick: () => window.location.reload()
        }}
      />
    );
  }

  if (filteredBuilds.length === 0) {
    return (
      <div className="space-y-4">
        <FilterBar
          statusFilter={statusFilter}
          branchFilter={branchFilter}
          onStatusChange={setStatusFilter}
          onBranchChange={setBranchFilter}
          onClearFilters={clearFilters}
          availableStatuses={availableStatuses}
          availableBranches={availableBranches}
        />
        <EmptyState
          type="no-results"
          title="No Builds Match Filters"
          message="Try adjusting your filters to see more builds."
          action={{
            label: "Clear Filters",
            onClick: clearFilters
          }}
        />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Filter Bar */}
      <FilterBar
        statusFilter={statusFilter}
        branchFilter={branchFilter}
        onStatusChange={setStatusFilter}
        onBranchChange={setBranchFilter}
        onClearFilters={clearFilters}
        availableStatuses={availableStatuses}
        availableBranches={availableBranches}
      />

      {/* Builds Table */}
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            Recent Builds ({filteredBuilds.length})
          </h2>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Build ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Branch
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Duration
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Started
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredBuilds.map((build) => (
                <tr key={build.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <StatusChip status={build.status} size="sm" />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      #{build.external_id}
                    </div>
                    <div className="text-sm text-gray-500">
                      {build.provider_name || 'GitHub Actions'}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <GitBranch className="w-4 h-4 text-gray-400" />
                      <span className="text-sm text-gray-900">
                        {build.branch || 'main'}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-gray-400" />
                      <span className="text-sm text-gray-900">
                        {formatDuration(build.duration_seconds)}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      <RelativeTime date={build.started_at} />
                    </div>
                    <div className="text-sm text-gray-500">
                      {build.triggered_by || 'Unknown'}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => openLogDrawer(build)}
                        className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                        aria-label="View build logs"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      {build.url && (
                        <a
                          href={build.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                          aria-label="View build in external system"
                        >
                          <ExternalLink className="w-4 h-4" />
                        </a>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Build Log Drawer */}
      <BuildLogDrawer
        isOpen={isDrawerOpen}
        onClose={closeLogDrawer}
        build={selectedBuild}
      />
    </div>
  );
};

export default BuildsTable;
