"""
Entry point cho FastAPI application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import cassandra_client
from app.routers import ingest, history


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Quản lý lifecycle: connect/disconnect Cassandra."""
    cassandra_client.connect()
    yield
    cassandra_client.close()


app = FastAPI(
    title="IoT Monitoring API",
    description="Hệ thống giám sát IoT cảm biến môi trường",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware cho phép Frontend truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký routers
app.include_router(ingest.router, prefix="/api/v1", tags=["Ingest"])
app.include_router(history.router, prefix="/api/v1", tags=["History"])


@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "iot-monitoring-api"}
