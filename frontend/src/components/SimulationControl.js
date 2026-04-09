import React, { useState } from 'react';

/**
 * SimulationControl - Nút điều khiển giả lập 1000 cảm biến
 */
function SimulationControl() {
  const [isRunning, setIsRunning] = useState(false);

  const handleToggle = () => {
    setIsRunning(!isRunning);
    // TODO: Kết nối với backend hoặc WebSocket để điều khiển simulator
  };

  return (
    <div>
      <p style={{ color: 'var(--text-secondary)', marginBottom: 16, fontSize: '0.9rem' }}>
        Kích hoạt script giả lập để gửi dữ liệu từ 1,000 thiết bị cảm biến ảo.
      </p>

      <button
        className={`btn ${isRunning ? 'btn-danger' : 'btn-success'}`}
        onClick={handleToggle}
      >
        {isRunning ? '⏹️ Dừng giả lập' : '🚀 Giả lập 1000 cảm biến'}
      </button>

      <div className={`sim-status ${isRunning ? 'active' : 'inactive'}`}>
        <span>{isRunning ? '🟢' : '⚪'}</span>
        <span>
          {isRunning
            ? 'Đang gửi dữ liệu từ 1,000 thiết bị...'
            : 'Simulator chưa hoạt động'}
        </span>
      </div>
    </div>
  );
}

export default SimulationControl;
