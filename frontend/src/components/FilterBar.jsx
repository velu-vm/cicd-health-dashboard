import React from 'react';
import { Filter, X } from 'lucide-react';

const FilterBar = ({
  statusFilter,
  branchFilter,
  onStatusChange,
  onBranchChange,
  onClearFilters,
  availableStatuses,
  availableBranches,
  className = ''
}) => {
  const hasActiveFilters = statusFilter || branchFilter;

  return (
    <div className={`bg-white border border-gray-200 rounded-lg p-4 ${className}`}>
      <div className="flex items-center gap-4 mb-4">
        <div className="flex items-center gap-2 text-gray-700">
          <Filter className="w-4 h-4" />
          <span className="font-medium">Filters</span>
        </div>
        {hasActiveFilters && (
          <button
            onClick={onClearFilters}
            className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 transition-colors"
            aria-label="Clear all filters"
          >
            <X className="w-3 h-3" />
            Clear filters
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Status Filter */}
        <div>
          <label htmlFor="status-filter" className="block text-sm font-medium text-gray-700 mb-2">
            Status
          </label>
          <select
            id="status-filter"
            value={statusFilter}
            onChange={(e) => onStatusChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            aria-describedby="status-filter-help"
          >
            <option value="">All Statuses</option>
            {availableStatuses.map((status) => (
              <option key={status} value={status}>
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </option>
            ))}
          </select>
          <p id="status-filter-help" className="mt-1 text-xs text-gray-500">
            Filter builds by their current status
          </p>
        </div>

        {/* Branch Filter */}
        <div>
          <label htmlFor="branch-filter" className="block text-sm font-medium text-gray-700 mb-2">
            Branch
          </label>
          <select
            id="branch-filter"
            value={branchFilter}
            onChange={(e) => onBranchChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            aria-describedby="branch-filter-help"
          >
            <option value="">All Branches</option>
            {availableBranches.map((branch) => (
              <option key={branch} value={branch}>
                {branch}
              </option>
            ))}
          </select>
          <p id="branch-filter-help" className="mt-1 text-xs text-gray-500">
            Filter builds by git branch
          </p>
        </div>
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex flex-wrap gap-2">
            {statusFilter && (
              <span className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                Status: {statusFilter}
                <button
                  onClick={() => onStatusChange('')}
                  className="ml-1 hover:bg-blue-200 rounded-full p-0.5"
                  aria-label={`Remove status filter: ${statusFilter}`}
                >
                  <X className="w-3 h-3" />
                </button>
              </span>
            )}
            {branchFilter && (
              <span className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                Branch: {branchFilter}
                <button
                  onClick={() => onBranchChange('')}
                  className="ml-1 hover:bg-blue-200 rounded-full p-0.5"
                  aria-label={`Remove branch filter: ${branchFilter}`}
                >
                  <X className="w-3 h-3" />
                </button>
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterBar;
