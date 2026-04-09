"""
Router: Tiếp nhận dữ liệu cảm biến (Data Ingestion).
Endpoint: POST /api/v1/ingest
"""

from fastapi import APIRouter, HTTPException
from app.models.sensor import SensorReading, IngestResponse
from app.services.ingest_service import ingest_reading

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
async def ingest_sensor_data(reading: SensorReading):
    """
    Nhận dữ liệu từ thiết bị cảm biến.
    - Kiểm tra định dạng và ràng buộc dữ liệu.
    - Ghi nhanh vào Cassandra sử dụng Prepared Statements.
    """
    try:
        result = await ingest_reading(reading)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingest failed: {str(e)}")
