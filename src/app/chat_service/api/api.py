from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging
import time
from typing import Optional

# Import models và services
from chat_service.dto.models import ChatRequest, ChatResponse, ErrorResponse
from chat_service.services.chat_service import chatService
from core.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# Tạo router
router = APIRouter()

@router.post("/generate", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def generate_chat_response(request: ChatRequest):
    """
    Generate AI response for user message
    """
    try:
        start_time = time.time()

        # Validate model is loaded
        if not chatService.is_model_loaded():
            logger.warning("Model not loaded, attempting to load...")
            try:
                await chatService.load_model()
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="AI model is not available. Please try again later."
                )

        # Generate response using the service
        try:
            ai_response = chatService.generate_response(
                user_input=request.message,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate response. Please try again."
            )

        response_time = time.time() - start_time

        # Return response (không save database)
        return ChatResponse(
            response=ai_response,
            session_id=request.session_id,
            response_time=response_time,
            model_used="custom-llama",
            timestamp=time.time()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in generate_chat_response: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_usage_mb = memory_info.rss / 1024 / 1024

        return {
            "status": "healthy",
            "service": "chat-service",
            "version": "1.0.0",
            "model_loaded": chatService.is_model_loaded(),
            "memory_usage_mb": round(memory_usage_mb, 2),
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
        }

@router.post("/model/load")
async def load_model(model_path: Optional[str] = None):
    """
    Load or reload the AI model
    """
    try:
        logger.info(f"Loading model from path: {model_path or settings.MODEL_PATH}")
        await chatService.load_model(model_path)

        return {
            "success": True,
            "message": "Model loaded successfully",
            "model_path": model_path or settings.MODEL_PATH,
        }

    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load model: {str(e)}"
        )

@router.get("/model/status")
async def get_model_status():
    """
    Get model status and information
    """
    try:
        return {
            "model_loaded": chatService.is_model_loaded(),
            "model_path": settings.MODEL_PATH,
            "device": chatService.device if hasattr(chatService, 'device') else "unknown",
        }
    except Exception as e:
        logger.error(f"Error getting model status: {e}")
        return {
            "error": str(e),
            "timestamp": time.time()
        }

# Export router
Router = router

