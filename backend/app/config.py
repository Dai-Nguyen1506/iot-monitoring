"""
Cấu hình hệ thống - đọc từ biến môi trường hoặc file .env
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Cassandra
    cassandra_host: str = "127.0.0.1"
    cassandra_port: int = 9042
    cassandra_keyspace: str = "iot_monitoring"

    # Backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    debug: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
