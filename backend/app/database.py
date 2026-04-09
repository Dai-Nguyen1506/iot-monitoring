"""
Kết nối và quản lý session Cassandra.
Sử dụng Prepared Statements để tối ưu throughput.
"""

from cassandra.cluster import Cluster
from cassandra.query import PreparedStatement
from app.config import settings


class CassandraClient:
    """Quản lý kết nối tới Apache Cassandra."""

    def __init__(self):
        self.cluster = None
        self.session = None
        self._prepared_insert = None
        self._prepared_query = None

    def connect(self):
        """Thiết lập kết nối tới Cassandra cluster."""
        self.cluster = Cluster(
            [settings.cassandra_host],
            port=settings.cassandra_port,
        )
        self.session = self.cluster.connect(settings.cassandra_keyspace)
        self._prepare_statements()
        print(f"✅ Connected to Cassandra at {settings.cassandra_host}:{settings.cassandra_port}")

    def _prepare_statements(self):
        """Chuẩn bị Prepared Statements để tăng hiệu năng."""
        self._prepared_insert = self.session.prepare(
            """
            INSERT INTO sensor_readings (device_id, recorded_at, temperature, humidity, co2, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """
        )

        self._prepared_query = self.session.prepare(
            """
            SELECT device_id, recorded_at, temperature, humidity, co2, status
            FROM sensor_readings
            WHERE device_id = ? AND recorded_at >= ? AND recorded_at <= ?
            """
        )

    @property
    def insert_statement(self) -> PreparedStatement:
        return self._prepared_insert

    @property
    def query_statement(self) -> PreparedStatement:
        return self._prepared_query

    def close(self):
        """Đóng kết nối."""
        if self.cluster:
            self.cluster.shutdown()
            print("🔌 Cassandra connection closed.")


# Singleton instance
cassandra_client = CassandraClient()
