/**
 * API Service - Giao tiếp với Backend FastAPI
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Truy vấn lịch sử dữ liệu cảm biến theo device_id và khoảng thời gian
 */
export const fetchHistory = async (deviceId, startTime, endTime) => {
  const response = await apiClient.get(`/api/v1/history/${deviceId}`, {
    params: {
      start: startTime,
      end: endTime,
    },
  });
  return response.data;
};

/**
 * Gửi yêu cầu kích hoạt simulation (nếu có endpoint)
 */
export const triggerSimulation = async () => {
  // TODO: Implement khi backend có endpoint điều khiển simulation
  console.log('Simulation triggered');
};

/**
 * Health check
 */
export const healthCheck = async () => {
  const response = await apiClient.get('/');
  return response.data;
};

export default apiClient;
