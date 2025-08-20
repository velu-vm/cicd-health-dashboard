import React from 'react';
import { TrendingUp, TrendingDown, Clock, Activity } from 'lucide-react';
import StatusChip from './StatusChip';

const SummaryCards = ({ metrics }) => {
  if (!metrics) return null;

  const cards = [
    {
      title: 'Success Rate',
      value: `${(metrics.success_rate * 100).toFixed(1)}%`,
      change: metrics.success_rate >= 0.8 ? 'positive' : 'negative',
      icon: TrendingUp,
      color: 'bg-green-50',
      textColor: 'text-green-600',
      borderColor: 'border-green-200'
    },
    {
      title: 'Failure Rate',
      value: `${(metrics.failure_rate * 100).toFixed(1)}%`,
      change: metrics.failure_rate <= 0.2 ? 'positive' : 'negative',
      icon: TrendingDown,
      color: 'bg-red-50',
      textColor: 'text-red-600',
      borderColor: 'border-red-200'
    },
    {
      title: 'Avg Build Time',
      value: metrics.avg_build_time_seconds ? `${Math.round(metrics.avg_build_time_seconds / 60)}m` : 'N/A',
      change: 'neutral',
      icon: Clock,
      color: 'bg-blue-50',
      textColor: 'text-blue-600',
      borderColor: 'border-blue-200'
    },
    {
      title: 'Last Build Status',
      value: metrics.last_build_status || 'Unknown',
      change: metrics.last_build_status === 'success' ? 'positive' : 'negative',
      icon: Activity,
      color: 'bg-purple-50',
      textColor: 'text-purple-600',
      borderColor: 'border-purple-200',
      customValue: <StatusChip status={metrics.last_build_status || 'unknown'} size="sm" />
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => (
        <div
          key={index}
          className={`${card.color} border ${card.borderColor} rounded-lg p-6`}
        >
          <div className="flex items-center justify-between mb-4">
            <div className={`p-2 rounded-lg ${card.color} ${card.textColor}`}>
              <card.icon className="w-5 h-5" />
            </div>
            <div className={`text-sm font-medium ${
              card.change === 'positive' ? 'text-green-600' :
              card.change === 'negative' ? 'text-red-600' : 'text-gray-600'
            }`}>
              {card.change === 'positive' ? 'Good' :
               card.change === 'negative' ? 'Needs Attention' : 'Stable'}
            </div>
          </div>
          
          <h3 className="text-sm font-medium text-gray-600 mb-2">
            {card.title}
          </h3>
          
          <div className="text-2xl font-bold text-gray-900">
            {card.customValue || card.value}
          </div>
          
          {card.title === 'Last Build Status' && metrics.last_build_status && (
            <p className="text-xs text-gray-500 mt-2">
              Last updated: {new Date(metrics.last_updated).toLocaleString()}
            </p>
          )}
        </div>
      ))}
    </div>
  );
};

export default SummaryCards;
