import React, { useState } from 'react';
import RealtimeChart from './RealtimeChart';
import HistoryFilter from './HistoryFilter';
import PerformanceMonitor from './PerformanceMonitor';
import SimulationControl from './SimulationControl';
import { fetchHistory } from '../services/api';

/**
 * Dashboard - Component chính chứa toàn bộ các widget
 */
function Dashboard() {
  const [chartData, setChartData] = useState([]);
  const [queryTime, setQueryTime] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (deviceId, startTime, endTime) => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchHistory(deviceId, startTime, endTime);
      setChartData(result.readings || []);
      setQueryTime(result.query_time_ms);
    } catch (err) {
      setError(err.message || 'Lỗi khi truy vấn dữ liệu');
      setChartData([]);
      setQueryTime(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="dashboard">
      {/* Biểu đồ Real-time */}
      <div className="card chart-card">
        <div className="card-title">
          <span className="icon">📊</span>
          Real-time Multi-channel Chart
        </div>
        <RealtimeChart data={chartData} loading={loading} />
        {error && (
          <p style={{ color: 'var(--accent-red)', marginTop: 12, fontSize: '0.85rem' }}>
            ⚠️ {error}
          </p>
        )}
      </div>

      {/* Bộ lọc tra cứu */}
      <div className="card">
        <div className="card-title">
          <span className="icon">🔍</span>
          Bộ lọc tra cứu
        </div>
        <HistoryFilter onSearch={handleSearch} loading={loading} />
      </div>

      {/* Performance Monitor */}
      <div className="card">
        <div className="card-title">
          <span className="icon">⚡</span>
          Performance Monitor
        </div>
        <PerformanceMonitor queryTime={queryTime} />
      </div>

      {/* Simulation Control */}
      <div className="card" style={{ gridColumn: '1 / -1' }}>
        <div className="card-title">
          <span className="icon">🎮</span>
          Simulation Control
        </div>
        <SimulationControl />
      </div>
    </main>
  );
}

export default Dashboard;
