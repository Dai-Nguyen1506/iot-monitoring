import React from 'react';

/**
 * PerformanceMonitor - Hiển thị thời gian phản hồi thực tế của truy vấn
 */
function PerformanceMonitor({ queryTime }) {
  const getStatusColor = (time) => {
    if (time === null) return 'var(--text-muted)';
    if (time < 50) return 'var(--accent-green)';
    if (time < 100) return 'var(--accent-orange)';
    return 'var(--accent-red)';
  };

  const getStatusText = (time) => {
    if (time === null) return 'Chưa có dữ liệu';
    if (time < 50) return '✅ Đạt mục tiêu (< 50ms)';
    if (time < 100) return '⚠️ Chấp nhận được';
    return '❌ Cần tối ưu';
  };

  return (
    <div>
      <div
        className="perf-value"
        style={{
          background: queryTime !== null
            ? `linear-gradient(135deg, ${getStatusColor(queryTime)}, var(--accent-blue))`
            : undefined,
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
        }}
      >
        {queryTime !== null ? queryTime.toFixed(2) : '--'}
        <span className="perf-unit">ms</span>
      </div>
      <p className="perf-label">{getStatusText(queryTime)}</p>
    </div>
  );
}

export default PerformanceMonitor;
