from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""

    def __init__(self, app, calls_per_minute: int = 60):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        current_time = datetime.now()

        # Clean old requests
        cutoff_time = current_time - timedelta(minutes=1)
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > cutoff_time
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.calls_per_minute:
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded", "detail": "Too many requests"}
            )

        # Add current request
        self.requests[client_ip].append(current_time)

        response = await call_next(request)
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Request logging middleware"""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url}")

        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} - {process_time:.4f}s - "
            f"{request.method} {request.url}"
        )

        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)

        return response
