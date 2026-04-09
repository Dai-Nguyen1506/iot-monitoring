# BÁO CÁO CHI TIẾT ĐỀ TÀI

## Hệ thống giám sát IoT cảm biến môi trường

## 1. Giới thiệu tổng quan

Hệ thống hướng đến bài toán giám sát môi trường theo thời gian thực, tối ưu cho luồng dữ liệu lớn (Big Data) và khả năng truy vấn lịch sử độ trễ thấp.

- Mục tiêu chính:
  - Thu nhận dữ liệu liên tục từ nhiều thiết bị cảm biến.
  - Lưu trữ dữ liệu time-series ổn định, dễ mở rộng.
  - Truy vấn lịch sử nhanh với độ trễ cực thấp.
- Công nghệ cốt lõi:
  - Backend: Python + FastAPI
  - Database: Apache Cassandra
  - Frontend: React/HTML
- Chỉ tiêu hiệu năng:
  - Thời gian phản hồi truy vấn lịch sử: < 50ms
- Quy mô giả lập:
  - 1,000 thiết bị hoạt động đồng thời

## 2. Kiến trúc hệ thống (System Architecture)

Hệ thống được thiết kế theo 4 lớp để đảm bảo dễ mở rộng, dễ vận hành và dễ tối ưu hiệu năng:

1. Lớp Cảm biến (Simulators)
   - Script Python giả lập 1,000 thiết bị gửi dữ liệu JSON.
   - Giao thức giao tiếp: HTTP hoặc MQTT.
   - Mỗi bản tin gồm: device_id, timestamp, temperature, humidity, co2.

2. Lớp API (Backend)
   - Sử dụng FastAPI tiếp nhận dữ liệu từ lớp cảm biến.
   - Xử lý validation, chuẩn hóa và ghi dữ liệu vào Cassandra.
   - Cung cấp API truy vấn lịch sử cho Dashboard.

3. Lớp Lưu trữ (Database)
   - Apache Cassandra được sử dụng làm kho dữ liệu time-series.
   - Tối ưu schema theo hướng query-first để đảm bảo truy vấn nhanh.

4. Lớp Hiển thị (Frontend)
   - Dashboard cập nhật dữ liệu theo thời gian thực.
   - Công cụ tìm kiếm lịch sử theo device và khoảng thời gian.
   - Hiển thị thông tin hiệu năng hệ thống.

## 3. Thiết kế dữ liệu (Data Modeling - Query-first)

### 3.1 Câu hỏi truy vấn trung tâm

Schema được thiết kế để tối ưu cho câu hỏi:

Lấy toàn bộ dữ liệu của thiết bị X trong khoảng thời gian Y.

### 3.2 CQL khởi tạo

```sql
CREATE KEYSPACE iot_monitoring
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE sensor_readings (
    device_id text,
    recorded_at timestamp,
    temperature float,
    humidity float,
    co2 float,
    status text,
    PRIMARY KEY (device_id, recorded_at)
) WITH CLUSTERING ORDER BY (recorded_at DESC);
```

### 3.3 Giải thích thiết kế

- `device_id` (Partition Key):
  - Gom dữ liệu của từng thiết bị vào cùng partition.
  - Tối ưu cho truy vấn theo một thiết bị cụ thể.
- `recorded_at` (Clustering Key):
  - Sắp xếp dữ liệu theo thời gian.
  - Cấu hình `DESC` giúp lấy dữ liệu mới nhất nhanh hơn.
- `status`:
  - Đánh dấu trạng thái bản ghi: `normal`, `warning`, `error`.
  - Hỗ trợ cảnh báo và phân tích lỗi.

## 4. Chi tiết các tính năng API

### 4.1 API tiếp nhận dữ liệu (Data Ingestion)

- Endpoint: `POST /api/v1/ingest`
- Nhiệm vụ:
  - Nhận dữ liệu từ thiết bị cảm biến.
  - Kiểm tra định dạng và ràng buộc dữ liệu.
  - Ghi nhanh vào Cassandra.
- Kỹ thuật tối ưu:
  - Sử dụng `async/await` để xử lý bất đồng bộ.
  - Sử dụng Prepared Statements để tăng throughput ghi.

### 4.2 API truy vấn lịch sử (Query API)

- Endpoint: `GET /api/v1/history/{device_id}?start=...&end=...`
- Nhiệm vụ:
  - Trả về danh sách số đo của một thiết bị trong khoảng thời gian.
- Cam kết hiệu năng:
  - Tốc độ phản hồi mục tiêu < 50ms.
  - Đạt được nhờ schema query-first và partition key phù hợp.

## 5. Giao diện Dashboard (Figma Design Reference)

Dashboard gồm các thành phần chính sau:

1. Real-time Multi-channel Chart
   - Biểu đồ đường hiển thị đồng thời:
     - Nhiệt độ
     - Độ ẩm
     - CO2

2. Bộ lọc tra cứu
   - Ô nhập `device_id`.
   - Bộ chọn khoảng thời gian (`start`, `end`).

3. Performance Monitor
   - Hiển thị thời gian phản hồi thực tế của truy vấn.
   - Ví dụ: `Query time: 12ms`.

4. Simulation Control
   - Nút bấm: `Giả lập 1000 cảm biến`.
   - Kích hoạt script gửi dữ liệu ảo để test tải.

## 6. Tính năng nâng cao: Batch Analytics

Một worker Python chạy định kỳ để quét dữ liệu trong Cassandra và phát hiện bất thường.

### 6.1 Các quy tắc phát hiện lỗi

1. Giá trị đột biến (Outliers)
   - Sử dụng Z-score hoặc ngưỡng cứng.
   - Ví dụ ngưỡng cứng: `temperature > 100`.
   - Công thức:

$$
z = \frac{x - \mu}{\sigma}
$$

Nếu $z > 3$, giá trị được xem là bất thường.

2. Chuỗi null kéo dài
   - Trong 10 bản ghi liên tiếp, nếu có hơn 5 bản ghi null thì đánh dấu cảnh báo.

3. Giá trị âm bất hợp lý
   - Phát hiện các giá trị không hợp lý như:
     - `humidity < 0`
     - `co2 < 0`

### 6.2 Hành động sau phát hiện

- Tự động cập nhật cột `status` thành `warning`.
- Đẩy `device_id` vào danh sách cảnh báo trên Dashboard.

## 7. Kế hoạch triển khai (Roadmap)

| Giai đoạn | Nội dung công việc |
|---|---|
| Giai đoạn 1 | Cài đặt Cassandra, thiết kế schema theo query-first |
| Giai đoạn 2 | Xây dựng FastAPI cho ingest và query |
| Giai đoạn 3 | Viết script giả lập 1000 cảm biến và đo hiệu năng |
| Giai đoạn 4 | Phát triển frontend (React) + biểu đồ thời gian thực |
| Giai đoạn 5 | Hoàn thiện worker Batch Analytics phát hiện lỗi |

## 8. Tiêu chí đánh giá thành công

- Hệ thống ingest ổn định với tải giả lập 1,000 thiết bị.
- Truy vấn lịch sử theo `device_id` trong mức < 50ms (mục tiêu).
- Dashboard cập nhật dữ liệu theo thời gian thực, hiển thị đầy đủ cảnh báo.
- Batch Analytics phát hiện được bất thường và cập nhật trạng thái chính xác.

## 9. Kết luận

Đề tài hướng đến một nền tảng giám sát IoT có tính ứng dụng cao, kết hợp:

- Khả năng thu nhận dữ liệu lớn theo thời gian thực.
- Lưu trữ time-series tối ưu truy vấn lịch sử.
- Giao diện trực quan cho vận hành và theo dõi hiệu năng.
- Cơ chế phát hiện bất thường tự động để nâng cao độ tin cậy hệ thống.

Kiến trúc này phù hợp để mở rộng cho các bài toán Smart Factory, Smart Building và Smart City trong thực tế.
