import React from 'react';

const LoadingSkeleton = ({ type, className = '' }) => {
  const renderSkeleton = () => {
    switch (type) {
      case 'card':
        return (
          <div className="bg-white rounded-lg border border-gray-200 p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
            <div className="h-3 bg-gray-200 rounded w-2/3"></div>
          </div>
        );
      
      case 'table-row':
        return (
          <div className="animate-pulse">
            <div className="h-16 bg-white border-b border-gray-200 flex items-center px-6">
              <div className="h-4 bg-gray-200 rounded w-16 mr-4"></div>
              <div className="h-6 bg-gray-200 rounded w-20 mr-4"></div>
              <div className="h-4 bg-gray-200 rounded w-24 mr-4"></div>
              <div className="h-4 bg-gray-200 rounded w-20 mr-4"></div>
              <div className="h-4 bg-gray-200 rounded w-16 mr-4"></div>
              <div className="h-4 bg-gray-200 rounded w-20"></div>
            </div>
          </div>
        );
      
      case 'summary-card':
        return (
          <div className="bg-white rounded-lg border border-gray-200 p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-3"></div>
            <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
            <div className="h-3 bg-gray-200 rounded w-2/3"></div>
          </div>
        );
      
      case 'chart':
        return (
          <div className="bg-white rounded-lg border border-gray-200 p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/3 mb-6"></div>
            <div className="flex items-end justify-between h-32">
              {[...Array(7)].map((_, i) => (
                <div key={i} className="w-8 bg-gray-200 rounded-t" style={{ height: `${Math.random() * 60 + 20}%` }}></div>
              ))}
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className={className}>
      {renderSkeleton()}
    </div>
  );
};

export default LoadingSkeleton;
