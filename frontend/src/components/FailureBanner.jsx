import React from 'react';
import { AlertTriangle, X } from 'lucide-react';

const FailureBanner = ({ isVisible, onDismiss, className = '' }) => {
  if (!isVisible) return null;

  return (
    <div className={`bg-red-50 border border-red-200 rounded-lg p-4 ${className}`} role="alert" aria-live="polite">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          <AlertTriangle className="w-5 h-5 text-red-400" aria-hidden="true" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-medium text-red-800">
            Build Failure Detected
          </h3>
          <p className="mt-1 text-sm text-red-700">
            The most recent build has failed. Check the build details below for more information.
          </p>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="flex-shrink-0 p-1 text-red-400 hover:text-red-600 transition-colors"
            aria-label="Dismiss failure banner"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
};

export default FailureBanner;
