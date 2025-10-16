"""
Custom Prometheus metrics for the FastAPI application
"""
from prometheus_client import Counter, Histogram, Gauge, Info
import psutil
import time
from typing import Dict, Any

# Request metrics
chat_requests_total = Counter(
    'chat_requests_total',
    'Total number of chat requests',
    ['method', 'endpoint', 'status_code']
)

chat_request_duration = Histogram(
    'chat_request_duration_seconds',
    'Time spent processing chat requests',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0]
)

# Model metrics
model_load_duration = Histogram(
    'model_load_duration_seconds',
    'Time spent loading the model',
    buckets=[1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0]
)

model_inference_duration = Histogram(
    'model_inference_duration_seconds',
    'Time spent on model inference',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

model_loaded = Gauge(
    'model_loaded',
    'Whether the model is currently loaded (1) or not (0)'
)

# Token metrics
tokens_generated_total = Counter(
    'tokens_generated_total',
    'Total number of tokens generated'
)

tokens_per_request = Histogram(
    'tokens_per_request',
    'Number of tokens generated per request',
    buckets=[10, 50, 100, 200, 500, 1000, 2000]
)

# System metrics
memory_usage_bytes = Gauge(
    'memory_usage_bytes',
    'Current memory usage in bytes'
)

cpu_usage_percent = Gauge(
    'cpu_usage_percent',
    'Current CPU usage percentage'
)

# Error metrics
errors_total = Counter(
    'errors_total',
    'Total number of errors',
    ['error_type', 'endpoint']
)

# Health metrics
health_check_duration = Histogram(
    'health_check_duration_seconds',
    'Time spent on health checks',
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0]
)

# Application info
app_info = Info('app_info', 'Application information')

# MLflow metrics
mlflow_experiments_total = Gauge(
    'mlflow_experiments_total',
    'Total number of MLflow experiments'
)

mlflow_runs_total = Gauge(
    'mlflow_runs_total',
    'Total number of MLflow runs'
)

# Connection metrics
active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

# Custom business metrics
chat_sessions_active = Gauge(
    'chat_sessions_active',
    'Number of active chat sessions'
)

chat_response_quality = Histogram(
    'chat_response_quality_score',
    'Quality score of chat responses',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

def update_system_metrics():
    """Update system resource metrics"""
    try:
        # Memory usage
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_usage_bytes.set(memory_info.rss)
        
        # CPU usage
        cpu_percent = process.cpu_percent()
        cpu_usage_percent.set(cpu_percent)
        
    except Exception as e:
        print(f"Error updating system metrics: {e}")

def record_chat_request(method: str, endpoint: str, status_code: int, duration: float):
    """Record chat request metrics"""
    chat_requests_total.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
    chat_request_duration.labels(method=method, endpoint=endpoint).observe(duration)

def record_model_inference(duration: float, tokens_generated: int = 0):
    """Record model inference metrics"""
    model_inference_duration.observe(duration)
    if tokens_generated > 0:
        tokens_generated_total.inc(tokens_generated)
        tokens_per_request.observe(tokens_generated)

def record_error(error_type: str, endpoint: str):
    """Record error metrics"""
    errors_total.labels(error_type=error_type, endpoint=endpoint).inc()

def set_model_status(loaded: bool):
    """Set model loading status"""
    model_loaded.set(1 if loaded else 0)

def set_app_info(version: str, python_version: str, environment: str):
    """Set application information"""
    app_info.info({
        'version': version,
        'python_version': python_version,
        'environment': environment,
        'build_time': str(int(time.time()))
    })