# QA Chatbot Microservice

Microservice AI-powered Q&A chatbot sử dụng mô hình LLaMA được fine-tune.

## Tính năng chính

- **AI Chat Generation**: Tạo phản hồi thông minh cho câu hỏi người dùng
- **Session Management**: Quản lý phiên trò chuyện
- **Chat History**: Lưu trữ và truy xuất lịch sử chat
- **User Feedback**: Thu thập phản hồi từ người dùng
- **Analytics**: Thống kê sử dụng service
- **Health Monitoring**: Giám sát tình trạng service và model
- **Rate Limiting**: Giới hạn số lượng request
- **Logging**: Ghi log chi tiết cho debugging

## Cấu trúc dự án

```
src/app/
├── main.py                    # Entry point của ứng dụng
├── core/                      # Core configurations
│   ├── config.py             # Application settings
│   ├── logging_config.py     # Logging configuration
│   └── middleware/
│       └── middleware.py     # Custom middleware
├── chat_service/             # Chat service module
│   ├── api/
│   │   └── api.py           # API endpoints
│   ├── dto/
│   │   └── models.py        # Pydantic models
│   ├── services/
│   │   ├── model_service.py # Model management
│   │   └── chat_service.py  # Business logic
│   └── db/
│       └── database.py      # Database models & connection
└── tests/                    # Unit tests
    └── test_api.py
```

## API Endpoints

### Chat Endpoints

- `POST /api/v1/chat/generate` - Tạo phản hồi chat
- `GET /api/v1/chat/history/{session_id}` - Lấy lịch sử chat
- `POST /api/v1/chat/feedback` - Gửi feedback
- `GET /api/v1/chat/analytics` - Xem thống kê

### System Endpoints

- `GET /health` - Health check
- `GET /api/v1/chat/model/info` - Thông tin model
- `POST /api/v1/chat/model/load` - Load/reload model

## Cài đặt và chạy

### 1. Sử dụng Docker (Khuyến nghị)

```bash
# Build và chạy với Docker Compose
cd src
docker-compose up --build

# Hoặc chạy riêng lẻ
docker build -t qa-chatbot .
docker run -p 8000:8000 qa-chatbot
```

### 2. Chạy trực tiếp

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
cd src/app
python main.py
```

## Configuration

Tạo file `.env` từ `.env.example` và cập nhật các giá trị:

```bash
cp .env.example .env
```

Các cấu hình quan trọng:

- `MODEL_PATH`: Đường dẫn đến model đã fine-tune
- `DATABASE_URL`: Chuỗi kết nối database
- `MAX_TOKENS`: Số token tối đa cho mỗi response
- `RATE_LIMIT_PER_MINUTE`: Giới hạn request mỗi phút

## Sử dụng API

### Gửi chat message

```bash
curl -X POST "http://localhost:8000/api/v1/chat/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is machine learning?",
    "session_id": "user123",
    "max_tokens": 150,
    "temperature": 0.7
  }'
```

### Lấy lịch sử chat

```bash
curl "http://localhost:8000/api/v1/chat/history/user123"
```

### Health check

```bash
curl "http://localhost:8000/health"
```

## Testing

```bash
# Chạy tests
cd src/app
python -m pytest tests/ -v

# Chạy test với coverage
pytest tests/ --cov=. --cov-report=html
```

## Monitoring và Logging

- Logs được lưu trong thư mục `logs/`
- Health check endpoint: `/health`
- Metrics endpoint (nếu enabled): `:9090/metrics`

## Deployment

### Production Checklist

- [ ] Cập nhật `SECRET_KEY` trong production
- [ ] Sử dụng PostgreSQL thay vì SQLite
- [ ] Enable Redis cho caching
- [ ] Cấu hình reverse proxy (nginx)
- [ ] Setup monitoring (Prometheus + Grafana)
- [ ] Cấu hình backup database

### Kubernetes Deployment

```yaml
# Xem file k8s-deployment.yaml (sẽ tạo nếu cần)
```

## Troubleshooting

### Lỗi thường gặp

1. **Model không load được**

   - Kiểm tra `MODEL_PATH` có đúng không
   - Đảm bảo có đủ RAM/VRAM
   - Xem log để biết chi tiết lỗi

2. **Database connection error**

   - Kiểm tra `DATABASE_URL`
   - Đảm bảo database service đang chạy

3. **Rate limit errors**
   - Điều chỉnh `RATE_LIMIT_PER_MINUTE`
   - Implement caching để giảm số request

## Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License
