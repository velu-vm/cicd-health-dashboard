import React from 'react';

const StatusChip = ({ status, size = 'md', className = '' }) => {
  const getStatusConfig = (status) => {
    switch (status.toLowerCase()) {
      case 'success':
        return {
          label: 'Success',
          bgColor: 'bg-green-100',
          textColor: 'text-green-800',
          borderColor: 'border-green-200',
          icon: '✅'
        };
      case 'failed':
        return {
          label: 'Failed',
          bgColor: 'bg-red-100',
          textColor: 'text-red-800',
          borderColor: 'border-red-200',
          icon: '❌'
        };
      case 'running':
        return {
          label: 'Running',
          bgColor: 'bg-amber-100',
          textColor: 'text-amber-800',
          borderColor: 'border-amber-200',
          icon: '🔄'
        };
      case 'queued':
        return {
          label: 'Queued',
          bgColor: 'bg-gray-100',
          textColor: 'text-gray-800',
          borderColor: 'border-gray-200',
          icon: '⏳'
        };
      default:
        return {
          label: 'Unknown',
          bgColor: 'bg-gray-100',
          textColor: 'text-gray-800',
          borderColor: 'border-gray-200',
          icon: '❓'
        };
    }
  };

  const getSizeClasses = (size) => {
    switch (size) {
      case 'sm':
        return 'px-2 py-1 text-xs';
      case 'lg':
        return 'px-4 py-2 text-base';
      default:
        return 'px-3 py-1.5 text-sm';
    }
  };

  const config = getStatusConfig(status);
  const sizeClasses = getSizeClasses(size);

  return (
    <span
      className={`
        inline-flex items-center gap-1.5 font-medium rounded-full border
        ${config.bgColor} ${config.textColor} ${config.borderColor}
        ${sizeClasses} ${className}
      `}
      role="status"
      aria-label={`Build status: ${config.label}`}
    >
      <span className="text-xs" aria-hidden="true">
        {config.icon}
      </span>
      {config.label}
    </span>
  );
};

export default StatusChip;
