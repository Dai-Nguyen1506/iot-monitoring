# 🌐 IoT Monitoring System

Hệ thống giám sát IoT cảm biến môi trường theo thời gian thực.

## 📋 Tổng quan

Hệ thống hướng đến bài toán giám sát môi trường theo thời gian thực, tối ưu cho luồng dữ liệu lớn (Big Data) và khả năng truy vấn lịch sử độ trễ thấp.

### Công nghệ cốt lõi
- **Backend:** Python + FastAPI
- **Database:** Apache Cassandra
- **Frontend:** React
- **Simulators:** Python scripts

### Chỉ tiêu hiệu năng
- Thời gian phản hồi truy vấn lịch sử: **< 50ms**
- Quy mô giả lập: **1,000 thiết bị** hoạt động đồng thời

## 🏗️ Kiến trúc hệ thống

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Simulators  │────▶│   FastAPI     │────▶│  Cassandra   │◀────│   Batch      │
│  (1000 devices)│    │   Backend    │     │  (Time-series)│    │   Analytics  │
└──────────────┘     └──────┬───────┘     └──────────────┘     └──────────────┘
                            │
                     ┌──────▼───────┐
                     │   React      │
                     │   Dashboard  │
                     └──────────────┘
```

## 📁 Cấu trúc thư mục

```
iot-monitoring/
├── backend/                  # Backend FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # Entry point FastAPI
│   │   ├── config.py         # Cấu hình (Cassandra, env)
│   │   ├── database.py       # Kết nối Cassandra
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── sensor.py     # Pydantic models
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── ingest.py     # POST /api/v1/ingest
│   │   │   └── history.py    # GET /api/v1/history/{device_id}
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── ingest_service.py
│   │       └── query_service.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # Frontend React Dashboard
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── index.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── components/
│   │   │   ├── Dashboard.js
│   │   │   ├── RealtimeChart.js
│   │   │   ├── HistoryFilter.js
│   │   │   ├── PerformanceMonitor.js
│   │   │   └── SimulationControl.js
│   │   └── services/
│   │       └── api.js
│   ├── package.json
│   └── Dockerfile
├── simulator/                # Script giả lập cảm biến
│   ├── __init__.py
│   ├── sensor_simulator.py
│   └── config.py
├── analytics/                # Batch Analytics worker
│   ├── __init__.py
│   ├── anomaly_detector.py
│   └── scheduler.py
├── scripts/                  # Scripts tiện ích
│   └── init_cassandra.cql
├── docs/                     # Tài liệu dự án
│   └── project.md
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Hướng dẫn cài đặt

### Yêu cầu
- Python 3.10+
- Node.js 18+
- Apache Cassandra 4.x (hoặc Docker)

### 1. Khởi động Cassandra
```bash
docker-compose up -d cassandra
```

### 2. Khởi tạo Database
```bash
docker exec -it cassandra cqlsh -f /scripts/init_cassandra.cql
```

### 3. Chạy Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Chạy Frontend
```bash
cd frontend
npm install
npm start
```

### 5. Chạy Simulator
```bash
cd simulator
python sensor_simulator.py
```

## 📡 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|--------|
| `POST` | `/api/v1/ingest` | Tiếp nhận dữ liệu cảm biến |
| `GET` | `/api/v1/history/{device_id}?start=...&end=...` | Truy vấn lịch sử theo thiết bị |

## 📄 License

MIT