"""
Scheduler: Chạy worker Batch Analytics định kỳ.
Quét toàn bộ dữ liệu trong Cassandra và phát hiện bất thường.
"""

import time
from cassandra.cluster import Cluster
from anomaly_detector import analyze_device, update_status_to_warning


# Cấu hình
CASSANDRA_HOST = "127.0.0.1"
CASSANDRA_PORT = 9042
CASSANDRA_KEYSPACE = "iot_monitoring"
SCAN_INTERVAL_SECONDS = 60  # Quét mỗi 60 giây


def get_all_device_ids(session) -> list[str]:
    """Lấy danh sách tất cả device_id duy nhất."""
    rows = session.execute("SELECT DISTINCT device_id FROM sensor_readings")
    return [row.device_id for row in rows]


def run_analytics_cycle(session):
    """Chạy một chu kỳ phân tích bất thường."""
    device_ids = get_all_device_ids(session)
    print(f"🔍 Scanning {len(device_ids)} devices...")

    total_anomalies = 0

    for device_id in device_ids:
        anomalies = analyze_device(session, device_id)

        for anomaly in anomalies:
            print(
                f"  ⚠️ [{anomaly['type']}] {anomaly['device_id']} "
                f"at {anomaly['recorded_at']}: {anomaly['detail']}"
            )
            # Cập nhật status thành warning
            update_status_to_warning(
                session, anomaly["device_id"], anomaly["recorded_at"]
            )

        total_anomalies += len(anomalies)

    print(f"✅ Cycle complete: {total_anomalies} anomalies detected and flagged.")
    return total_anomalies


def main():
    """Entry point cho Batch Analytics scheduler."""
    print("🚀 Starting Batch Analytics Worker")
    print(f"📊 Cassandra: {CASSANDRA_HOST}:{CASSANDRA_PORT}/{CASSANDRA_KEYSPACE}")
    print(f"⏱️  Scan interval: {SCAN_INTERVAL_SECONDS}s")
    print("-" * 50)

    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect(CASSANDRA_KEYSPACE)

    try:
        while True:
            run_analytics_cycle(session)
            time.sleep(SCAN_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n🛑 Analytics worker stopped.")
    finally:
        cluster.shutdown()


if __name__ == "__main__":
    main()
