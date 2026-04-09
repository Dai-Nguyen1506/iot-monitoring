"""
Pydantic models cho dữ liệu cảm biến.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    """Model dữ liệu đầu vào từ cảm biến."""

    device_id: str = Field(..., description="Mã thiết bị cảm biến", examples=["sensor_001"])
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Thời điểm ghi nhận dữ liệu",
    )
    temperature: float = Field(..., description="Nhiệt độ (°C)", examples=[25.5])
    humidity: float = Field(..., description="Độ ẩm (%)", examples=[60.0])
    co2: float = Field(..., description="Nồng độ CO2 (ppm)", examples=[400.0])


class SensorReadingResponse(BaseModel):
    """Model dữ liệu trả về cho client."""

    device_id: str
    recorded_at: datetime
    temperature: float
    humidity: float
    co2: float
    status: str


class IngestResponse(BaseModel):
    """Response sau khi ingest dữ liệu."""

    success: bool
    message: str
    device_id: str
    recorded_at: datetime


class HistoryResponse(BaseModel):
    """Response truy vấn lịch sử."""

    device_id: str
    count: int
    query_time_ms: float
    readings: list[SensorReadingResponse]
