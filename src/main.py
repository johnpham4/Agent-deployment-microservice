from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.api import Router as ChatRouter
from core.config import settings
from services.chat_service import chatService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.info("Starting QA Chatbot service...")

    # Load model if needed (uncomment để load model khi startup)
    # try:
    #     await chatService.load_model()
    #     logging.info("Model loaded on startup")
    # except Exception as e:
    #     logging.warning(f"Could not load model on startup: {e}")
    #     logging.info("Model will be loaded on first request")

    yield

    # Shutdown
    logging.info("Shutting down QA Chatbot service...")


app = FastAPI(
    title="QA Chatbot Service",
    description="AI-powered Q&A chatbot microservice",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ChatRouter, prefix="/api/v1/chat", tags=["chat"])

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
    logging.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
