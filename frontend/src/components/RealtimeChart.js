import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

/**
 * RealtimeChart - Biểu đồ đường hiển thị đồng thời Temperature, Humidity, CO2
 */
function RealtimeChart({ data, loading }) {
  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: 60 }}>
        <div className="spinner"></div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: 300,
          color: 'var(--text-muted)',
          fontSize: '0.9rem',
        }}
      >
        Chọn thiết bị và khoảng thời gian để hiển thị biểu đồ
      </div>
    );
  }

  // Format dữ liệu cho Recharts
  const formattedData = data.map((item) => ({
    ...item,
    time: new Date(item.recorded_at).toLocaleTimeString('vi-VN'),
  }));

  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={formattedData}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
        <XAxis
          dataKey="time"
          stroke="var(--text-muted)"
          tick={{ fontSize: 12 }}
        />
        <YAxis stroke="var(--text-muted)" tick={{ fontSize: 12 }} />
        <Tooltip
          contentStyle={{
            backgroundColor: 'var(--bg-card)',
            border: '1px solid var(--border-color)',
            borderRadius: 8,
            color: 'var(--text-primary)',
          }}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="temperature"
          stroke="var(--chart-temperature)"
          strokeWidth={2}
          dot={false}
          name="🌡️ Temperature (°C)"
        />
        <Line
          type="monotone"
          dataKey="humidity"
          stroke="var(--chart-humidity)"
          strokeWidth={2}
          dot={false}
          name="💧 Humidity (%)"
        />
        <Line
          type="monotone"
          dataKey="co2"
          stroke="var(--chart-co2)"
          strokeWidth={2}
          dot={false}
          name="🌿 CO2 (ppm)"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default RealtimeChart;
