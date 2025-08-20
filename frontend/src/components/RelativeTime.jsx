import React from 'react';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

// Extend dayjs with relative time plugin
dayjs.extend(relativeTime);

const RelativeTime = ({ date, className = '', showTooltip = true }) => {
  const dayjsDate = dayjs(date);
  const relative = dayjsDate.fromNow();
  const absolute = dayjsDate.format('MMM D, YYYY [at] h:mm A');

  if (showTooltip) {
    return (
      <time
        dateTime={dayjsDate.toISOString()}
        className={`text-gray-600 ${className}`}
        title={absolute}
        aria-label={`${relative} (${absolute})`}
      >
        {relative}
      </time>
    );
  }

  return (
    <time
      dateTime={dayjsDate.toISOString()}
      className={`text-gray-600 ${className}`}
      aria-label={absolute}
    >
      {relative}
    </time>
  );
};

export default RelativeTime;
