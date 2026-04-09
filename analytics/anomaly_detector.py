"""
Batch Analytics: Phát hiện bất thường trong dữ liệu cảm biến.

Các quy tắc phát hiện lỗi:
1. Giá trị đột biến (Outliers) - Z-score > 3
2. Chuỗi null kéo dài - >5 null trong 10 bản ghi liên tiếp
3. Giá trị âm bất hợp lý - humidity < 0, co2 < 0
"""

import math
from cassandra.cluster import Cluster


# Ngưỡng cứng phát hiện bất thường
THRESHOLDS = {
    "temperature_max": 100.0,
    "humidity_min": 0.0,
    "co2_min": 0.0,
    "z_score_limit": 3.0,
}


def calculate_z_score(value: float, mean: float, std: float) -> float:
    """
    Tính Z-score cho một giá trị.
    z = (x - μ) / σ
    """
    if std == 0:
        return 0.0
    return (value - mean) / std


def detect_outliers(values: list[float]) -> list[int]:
    """Phát hiện index các giá trị đột biến bằng Z-score."""
    if len(values) < 2:
        return []

    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std = math.sqrt(variance)

    outlier_indices = []
    for i, v in enumerate(values):
        z = calculate_z_score(v, mean, std)
        if abs(z) > THRESHOLDS["z_score_limit"]:
            outlier_indices.append(i)

    return outlier_indices


def detect_null_streaks(values: list, window_size: int = 10, threshold: int = 5) -> bool:
    """Phát hiện chuỗi null kéo dài trong dữ liệu."""
    if len(values) < window_size:
        return False

    for i in range(len(values) - window_size + 1):
        window = values[i : i + window_size]
        null_count = sum(1 for v in window if v is None)
        if null_count > threshold:
            return True

    return False


def detect_negative_values(humidity: float, co2: float) -> bool:
    """Phát hiện giá trị âm bất hợp lý."""
    return humidity < THRESHOLDS["humidity_min"] or co2 < THRESHOLDS["co2_min"]


def analyze_device(session, device_id: str, limit: int = 100):
    """
    Phân tích dữ liệu của một thiết bị.
    Trả về danh sách các bất thường được phát hiện.
    """
    rows = session.execute(
        f"SELECT * FROM sensor_readings WHERE device_id = '{device_id}' LIMIT {limit}"
    )
    readings = list(rows)

    if not readings:
        return []

    anomalies = []

    # 1. Kiểm tra giá trị âm bất hợp lý
    for r in readings:
        if detect_negative_values(r.humidity, r.co2):
            anomalies.append({
                "device_id": device_id,
                "recorded_at": r.recorded_at,
                "type": "negative_value",
                "detail": f"humidity={r.humidity}, co2={r.co2}",
            })

    # 2. Kiểm tra đột biến bằng Z-score
    temperatures = [r.temperature for r in readings if r.temperature is not None]
    outlier_indices = detect_outliers(temperatures)
    for idx in outlier_indices:
        r = readings[idx]
        anomalies.append({
            "device_id": device_id,
            "recorded_at": r.recorded_at,
            "type": "outlier",
            "detail": f"temperature={r.temperature}",
        })

    # 3. Kiểm tra ngưỡng cứng
    for r in readings:
        if r.temperature is not None and r.temperature > THRESHOLDS["temperature_max"]:
            anomalies.append({
                "device_id": device_id,
                "recorded_at": r.recorded_at,
                "type": "threshold_exceeded",
                "detail": f"temperature={r.temperature} > {THRESHOLDS['temperature_max']}",
            })

    return anomalies


def update_status_to_warning(session, device_id: str, recorded_at):
    """Cập nhật status thành 'warning' cho bản ghi bất thường."""
    session.execute(
        """
        UPDATE sensor_readings SET status = 'warning'
        WHERE device_id = %s AND recorded_at = %s
        """,
        (device_id, recorded_at),
    )
