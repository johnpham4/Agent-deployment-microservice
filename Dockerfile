# Use official Python image with CUDA support if needed
# FROM  pytorch/pytorch:2.8.0-cuda12.6-cudnn9-runtime
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

COPY src/ /app/src/

RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]