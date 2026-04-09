"""
Service: Xử lý logic truy vấn lịch sử dữ liệu cảm biến.
Đo thời gian phản hồi để hiển thị trên Dashboard.
"""

import asyncio
import time
from datetime import datetime
from app.database import cassandra_client
from app.models.sensor import HistoryResponse, SensorReadingResponse


async def query_history(
    device_id: str, start: datetime, end: datetime
) -> HistoryResponse:
    """Truy vấn lịch sử dữ liệu của một thiết bị trong khoảng thời gian."""
    loop = asyncio.get_event_loop()

    # Đo thời gian truy vấn
    start_time = time.perf_counter()

    rows = await loop.run_in_executor(
        None,
        cassandra_client.session.execute,
        cassandra_client.query_statement,
        (device_id, start, end),
    )

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    # Chuyển đổi kết quả thành response models
    readings = [
        SensorReadingResponse(
            device_id=row.device_id,
            recorded_at=row.recorded_at,
            temperature=row.temperature,
            humidity=row.humidity,
            co2=row.co2,
            status=row.status,
        )
        for row in rows
    ]

    return HistoryResponse(
        device_id=device_id,
        count=len(readings),
        query_time_ms=round(elapsed_ms, 2),
        readings=readings,
    )
