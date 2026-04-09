"""
Router: Truy vấn lịch sử dữ liệu cảm biến.
Endpoint: GET /api/v1/history/{device_id}
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from app.models.sensor import HistoryResponse
from app.services.query_service import query_history

router = APIRouter()


@router.get("/history/{device_id}", response_model=HistoryResponse)
async def get_device_history(
    device_id: str,
    start: datetime = Query(..., description="Thời gian bắt đầu (ISO 8601)"),
    end: datetime = Query(..., description="Thời gian kết thúc (ISO 8601)"),
):
    """
    Truy vấn lịch sử dữ liệu của một thiết bị trong khoảng thời gian.
    Cam kết hiệu năng: < 50ms nhờ schema query-first.
    """
    try:
        result = await query_history(device_id, start, end)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
