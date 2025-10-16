FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt gói cần thiết cho build torch, tránh lỗi pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy và cài requirements
COPY requirements.txt .

# Cài đặt PyTorch CPU-only và các thư viện khác
RUN pip install --no-cache-dir torch==2.4.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Copy mã nguồn
COPY src/ /app/src/

# Tạo user không root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Lệnh chạy chính
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
