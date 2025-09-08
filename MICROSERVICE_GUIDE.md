# QA Chatbot Microservice - Hướng dẫn từ A-Z

## 🎯 Microservice là gì?

**Microservice** là cách chia ứng dụng lớn thành nhiều service nhỏ, mỗi service:

- Chạy độc lập (có thể trên server khác nhau)
- Có chức năng riêng biệt
- Có database riêng
- Giao tiếp qua API
- Deploy riêng biệt

## 📊 So sánh Architecture

### Monolith (Kiểu cũ):

```
┌─────────────────────────────────────┐
│           ONE BIG APPLICATION        │
│  ┌─────────┬──────────┬───────────┐  │
│  │  Chat   │   User   │ Analytics │  │
│  │ Module  │ Module   │  Module   │  │
│  └─────────┴──────────┴───────────┘  │
│          ONE SHARED DATABASE         │
└─────────────────────────────────────┘
```

### Microservice (Kiểu mới):

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Chat Service│    │ User Service│    │Analytics Svc│
│     API     │    │     API     │    │     API     │
│     DB      │    │     DB      │    │     DB      │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌─────────────┐
                    │ API Gateway │
                    │(Entry Point)│
                    └─────────────┘
```

## 🏗️ BƯỚC 1: Thiết kế Chat Service Architecture

### 1.1 Layers (Tầng) trong service:

```
┌─────────────────────────────────────┐
│              API Layer              │  ← Nhận HTTP requests
│         (Controllers/Routes)        │
├─────────────────────────────────────┤
│            Service Layer            │  ← Business Logic
│        (ChatService, ModelSvc)      │
├─────────────────────────────────────┤
│             Data Layer              │  ← Database operations
│         (Repository/DAO)            │
├─────────────────────────────────────┤
│            Database                 │  ← Store data
│        (SQLite/PostgreSQL)          │
└─────────────────────────────────────┘
```

### 1.2 Components (Thành phần):

1. **API Layer**: Nhận request từ client
2. **Service Layer**: Xử lý logic nghiệp vụ
3. **Repository Layer**: Truy cập database
4. **Models**: Định nghĩa cấu trúc dữ liệu
5. **Configuration**: Cấu hình ứng dụng

## 📁 BƯỚC 2: Cấu trúc thư mục

```
chat-service/
├── app/                          # Main application
│   ├── main.py                  # Entry point (FastAPI app)
│   ├── core/                    # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py           # Settings (DB, API keys, etc.)
│   │   ├── logging_config.py   # Log configuration
│   │   └── middleware/
│   │       └── middleware.py   # Rate limiting, CORS, etc.
│   ├── api/                     # API Layer
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── chat.py     # Chat endpoints
│   ├── services/                # Service Layer (Business Logic)
│   │   ├── __init__.py
│   │   ├── chat_service.py     # Chat business logic
│   │   └── model_service.py    # AI model management
│   ├── repositories/            # Data Layer
│   │   ├── __init__.py
│   │   ├── chat_repository.py  # Chat data operations
│   │   └── base.py             # Base repository
│   ├── models/                  # Database Models
│   │   ├── __init__.py
│   │   ├── chat.py             # Chat database model
│   │   └── base.py             # Base model
│   ├── schemas/                 # Pydantic Schemas (DTO)
│   │   ├── __init__.py
│   │   ├── chat.py             # Chat request/response schemas
│   │   └── base.py             # Base schemas
│   └── db/                      # Database
│       ├── __init__.py
│       ├── session.py          # Database session
│       └── base.py             # Database base
├── tests/                       # Tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_services.py
│   └── conftest.py
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker container
├── docker-compose.yml          # Multi-container setup
├── .env.example                # Environment template
└── README.md                   # Documentation
```

## ⚙️ BƯỚC 3: Định nghĩa API Contracts

### 3.1 Chat API Endpoints:

```
POST   /api/v1/chat/message      # Gửi tin nhắn, nhận phản hồi
GET    /api/v1/chat/history      # Lấy lịch sử chat
DELETE /api/v1/chat/history      # Xóa lịch sử
POST   /api/v1/chat/feedback     # Gửi feedback
GET    /health                   # Health check
GET    /metrics                  # Metrics cho monitoring
```

### 3.2 Request/Response Schemas:

```json
// POST /api/v1/chat/message
{
  "message": "What is machine learning?",
  "session_id": "user123",
  "temperature": 0.7,
  "max_tokens": 150
}

// Response
{
  "response": "Machine learning is...",
  "session_id": "user123",
  "timestamp": "2025-09-08T10:30:00Z",
  "response_time": 1.25
}
```

## 🔧 BƯỚC 4: Implementation Steps

### 4.1 Setup Project Structure

### 4.2 Implement Database Models

### 4.3 Create Repository Layer

### 4.4 Build Service Layer

### 4.5 Develop API Layer

### 4.6 Add Middleware & Configuration

### 4.7 Write Tests

### 4.8 Containerize với Docker

### 4.9 Setup Monitoring

### 4.10 Deploy

## 🚀 BƯỚC 5: Scaling to Multiple Microservices

Sau khi Chat Service hoàn thành, có thể mở rộng:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Chat Service│    │ User Service│    │Auth Service │
│   Port 8001 │    │   Port 8002 │    │   Port 8003 │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌─────────────┐
                    │ API Gateway │
                    │   Port 80   │  ← Client requests
                    └─────────────┘
```

## 💡 Lợi ích của Microservice Architecture:

1. **Scalability**: Scale từng service riêng biệt
2. **Technology Freedom**: Mỗi service dùng tech stack khác nhau
3. **Team Independence**: Mỗi team phát triển service riêng
4. **Fault Isolation**: 1 service lỗi không làm sập toàn bộ
5. **Deployment Independence**: Deploy từng service riêng biệt

## ⚠️ Challenges:

1. **Complexity**: Phức tạp hơn monolith
2. **Network Latency**: Giao tiếp qua network
3. **Data Consistency**: Khó đảm bảo ACID
4. **Monitoring**: Cần monitor nhiều service
5. **Testing**: Test integration phức tạp hơn

---

**Kết luận**: Microservice phù hợp với ứng dụng lớn, nhiều team. Với dự án nhỏ, monolith có thể đơn giản hơn.
