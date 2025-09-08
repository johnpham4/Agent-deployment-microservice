# QA Chatbot API Documentation

## 🚀 Cách chạy API

### Sử dụng script (khuyến nghị):

```bash
# Windows
start_server.bat

# Linux/Mac
chmod +x start_server.sh
./start_server.sh
```

### Chạy trực tiếp:

```bash
cd src/app
python main.py
```

API sẽ chạy tại: **http://localhost:8000**

## 📋 API Endpoints

### 1. Health Check

```http
GET /api/v1/chat/health
```

**Response:**

```json
{
  "status": "healthy",
  "service": "chat-service",
  "version": "1.0.0",
  "model_loaded": true,
  "memory_usage_mb": 1024.5,
  "timestamp": 1694123456.789
}
```

### 2. Chat Generation (Main endpoint)

```http
POST /api/v1/chat/generate
```

**Request Body:**

```json
{
  "message": "What is the SQL query to get all users?",
  "session_id": "optional-session-id",
  "max_tokens": 150,
  "temperature": 0.7
}
```

**Response:**

```json
{
  "response": "SELECT * FROM users;",
  "session_id": "abc123-def456-789",
  "timestamp": 1694123456.789,
  "response_time": 1.25,
  "model_used": "custom-llama"
}
```

### 3. Model Management

#### Load Model

```http
POST /api/v1/chat/model/load
```

**Optional Body:**

```json
{
  "model_path": "/custom/path/to/model"
}
```

#### Model Status

```http
GET /api/v1/chat/model/status
```

**Response:**

```json
{
  "model_loaded": true,
  "model_path": "/app/merged_model",
  "device": "cuda",
  "timestamp": 1694123456.789
}
```

### 4. Chat History

```http
GET /api/v1/chat/history/{session_id}?limit=50
```

### 5. Analytics

```http
GET /api/v1/chat/analytics?days=7
```

## 🧪 Test API

### Sử dụng test script:

```bash
python test_api.py
```

### Sử dụng curl:

```bash
# Health check
curl http://localhost:8000/api/v1/chat/health

# Chat generation
curl -X POST http://localhost:8000/api/v1/chat/generate \
  -H "Content-Type: application/json" \
  -d '{
    "message": "SELECT all users from database",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

### Sử dụng Python requests:

```python
import requests

# Chat với API
response = requests.post(
    "http://localhost:8000/api/v1/chat/generate",
    json={
        "message": "How to create a table in SQL?",
        "max_tokens": 150,
        "temperature": 0.7
    }
)

result = response.json()
print(f"AI Response: {result['response']}")
```

## 📊 API Documentation

Khi server chạy, truy cập:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## ⚙️ Configuration

API sử dụng config từ `core/config.py`:

```python
# Model settings
MODEL_PATH = "/app/merged_model"  # Đường dẫn model
MAX_TOKENS = 200                 # Max tokens mặc định
TEMPERATURE = 0.7                # Temperature mặc định

# Chat template
CHAT_TEMPLATE = "..."            # Template cho chat
```

## 🔧 Troubleshooting

### Lỗi thường gặp:

1. **Model not loaded**

   ```
   HTTP 503: AI model is not available
   ```

   - Kiểm tra MODEL_PATH có đúng không
   - Gọi endpoint `/api/v1/chat/model/load` để load model

2. **Out of memory**

   ```
   CUDA out of memory
   ```

   - Giảm max_tokens
   - Sử dụng CPU thay vì GPU

3. **Import errors**
   ```
   ModuleNotFoundError: No module named 'xxx'
   ```
   - Cài đặt dependencies: `pip install -r requirements.txt`

### Debug:

1. Kiểm tra logs trong terminal
2. Test từng endpoint riêng biệt
3. Kiểm tra model files có tồn tại không

## 🚀 Deployment

### Docker:

```bash
docker build -t qa-chatbot .
docker run -p 8000:8000 qa-chatbot
```

### Production:

```bash
# Sử dụng Gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📈 Monitoring

- Memory usage: `/api/v1/chat/health`
- Response times: Included in chat responses
- Analytics: `/api/v1/chat/analytics`

## 🔐 Security Notes

- Trong production, cấu hình CORS origins cụ thể
- Thêm authentication nếu cần
- Rate limiting đã được implement trong middleware
- Validate input để tránh injection attacks
