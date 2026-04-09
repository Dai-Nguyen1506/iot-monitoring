-- ============================================
-- IoT Monitoring - Cassandra Schema
-- Thiết kế theo Query-first approach
-- ============================================

-- Tạo Keyspace
CREATE KEYSPACE IF NOT EXISTS iot_monitoring
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE iot_monitoring;

-- Bảng chính: sensor_readings
-- Partition Key: device_id (gom dữ liệu theo thiết bị)
-- Clustering Key: recorded_at DESC (sắp xếp theo thời gian mới nhất)
CREATE TABLE IF NOT EXISTS sensor_readings (
    device_id text,
    recorded_at timestamp,
    temperature float,
    humidity float,
    co2 float,
    status text,
    PRIMARY KEY (device_id, recorded_at)
) WITH CLUSTERING ORDER BY (recorded_at DESC);
