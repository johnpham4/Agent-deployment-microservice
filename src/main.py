from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from loguru import logger
from contextlib import asynccontextmanager
import os
import sys
from prometheus_fastapi_instrumentator import Instrumentator


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .api import Router as ChatRouter
from .chat_service import chatService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    logger.info("Starting QA Chatbot service...")

    # Load model if needed (uncomment để load model khi startup)
    # try:
    #     await chatService.load_model()
    #     logger.info("Model loaded on startup")
    # except Exception as e:
    #     logger.warning(f"Could not load model on startup: {e}")
    #     logger.info("Model will be loaded on first request")

    yield

    # Shutdown
    logger.info("Shutting down QA Chatbot service...")


app = FastAPI(
    title="QA Chatbot Service",
    description="AI-powered Q&A chatbot microservice",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

Instrumentator().instrument(app).expose(app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(ChatRouter, prefix="/api/v1/chat", tags=["chat"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "qa-chatbot"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "QA Chatbot Service",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=False,
        log_level="info"
    )


