import React from 'react';
import { Inbox, Search, AlertCircle } from 'lucide-react';

const EmptyState = ({ type, title, message, action, className = '' }) => {
  const getIcon = () => {
    switch (type) {
      case 'no-data':
        return <Inbox className="w-12 h-12 text-gray-400" />;
      case 'no-results':
        return <Search className="w-12 h-12 text-gray-400" />;
      case 'error':
        return <AlertCircle className="w-12 h-12 text-red-400" />;
      default:
        return <Inbox className="w-12 h-12 text-gray-400" />;
    }
  };

  const getContainerClasses = () => {
    const baseClasses = 'text-center py-12 px-6';
    if (type === 'error') {
      return `${baseClasses} bg-red-50 border border-red-200 rounded-lg`;
    }
    return `${baseClasses} bg-gray-50 border border-gray-200 rounded-lg`;
  };

  return (
    <div className={`${getContainerClasses()} ${className}`}>
      <div className="flex justify-center mb-4">
        {getIcon()}
      </div>
      <h3 className={`text-lg font-medium mb-2 ${
        type === 'error' ? 'text-red-800' : 'text-gray-900'
      }`}>
        {title}
      </h3>
      <p className={`text-sm mb-6 ${
        type === 'error' ? 'text-red-700' : 'text-gray-600'
      }`}>
        {message}
      </p>
      {action && (
        <button
          onClick={action.onClick}
          className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors ${
            type === 'error'
              ? 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
              : 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500'
          }`}
        >
          {action.label}
        </button>
      )}
    </div>
  );
};

export default EmptyState;
