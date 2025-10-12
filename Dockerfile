# Use official Python image with CUDA support if needed
# FROM  pytorch/pytorch:2.8.0-cuda12.6-cudnn9-runtime
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04
# FROM python:3.11-slim

# Cài đặt Python và pip
RUN apt-get update && apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache/pip

COPY src/ /app/src/

# Tạo user không root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]