"""
Cấu hình cho Simulator.
"""

# API Backend endpoint
API_URL = "http://localhost:8000/api/v1/ingest"

# Số lượng thiết bị giả lập
DEVICE_COUNT = 1000

# Khoảng cách gửi dữ liệu (giây)
SEND_INTERVAL = 1.0

# Giới hạn giá trị cảm biến
TEMPERATURE_RANGE = (15.0, 45.0)
HUMIDITY_RANGE = (20.0, 90.0)
CO2_RANGE = (300.0, 1500.0)

# Xác suất tạo dữ liệu bất thường (để test Batch Analytics)
ANOMALY_PROBABILITY = 0.02
