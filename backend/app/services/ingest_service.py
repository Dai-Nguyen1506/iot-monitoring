"""
Service: Xử lý logic ghi dữ liệu cảm biến vào Cassandra.
Sử dụng async/await và Prepared Statements.
"""

import asyncio
from app.database import cassandra_client
from app.models.sensor import SensorReading, IngestResponse


def _determine_status(reading: SensorReading) -> str:
    """Xác định trạng thái dữ liệu dựa trên ngưỡng."""
    # Phát hiện giá trị bất thường
    if reading.temperature > 100 or reading.humidity < 0 or reading.co2 < 0:
        return "error"
    if reading.temperature > 50 or reading.humidity > 95 or reading.co2 > 2000:
        return "warning"
    return "normal"


async def ingest_reading(reading: SensorReading) -> IngestResponse:
    """Ghi một bản ghi cảm biến vào Cassandra."""
    status = _determine_status(reading)

    # Chạy Cassandra query trong thread pool (vì cassandra-driver là sync)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        cassandra_client.session.execute,
        cassandra_client.insert_statement,
        (
            reading.device_id,
            reading.timestamp,
            reading.temperature,
            reading.humidity,
            reading.co2,
            status,
        ),
    )

    return IngestResponse(
        success=True,
        message="Data ingested successfully",
        device_id=reading.device_id,
        recorded_at=reading.timestamp,
    )
