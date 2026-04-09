import React, { useState } from 'react';

/**
 * HistoryFilter - Bộ lọc tra cứu lịch sử theo device_id và khoảng thời gian
 */
function HistoryFilter({ onSearch, loading }) {
  const [deviceId, setDeviceId] = useState('sensor_0001');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (deviceId && startTime && endTime) {
      onSearch(deviceId, startTime, endTime);
    }
  };

  return (
    <form className="filter-section" onSubmit={handleSubmit}>
      <div className="filter-group">
        <label htmlFor="device-id">Device ID</label>
        <input
          id="device-id"
          type="text"
          placeholder="sensor_0001"
          value={deviceId}
          onChange={(e) => setDeviceId(e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label htmlFor="start-time">Start Time</label>
        <input
          id="start-time"
          type="datetime-local"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label htmlFor="end-time">End Time</label>
        <input
          id="end-time"
          type="datetime-local"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
        />
      </div>

      <button
        type="submit"
        className="btn btn-primary"
        disabled={loading || !deviceId || !startTime || !endTime}
      >
        {loading ? (
          <>
            <div className="spinner"></div>
            Đang tải...
          </>
        ) : (
          '🔍 Tra cứu'
        )}
      </button>
    </form>
  );
}

export default HistoryFilter;
