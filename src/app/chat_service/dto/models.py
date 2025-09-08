from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
import uuid
import time

class ModelType(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"

class Message(BaseModel):
    role: ModelType
    content: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="User's question or message")
    session_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), description="Session ID for conversation tracking")
    max_tokens: Optional[int] = Field(default=200, ge=1, le=1000, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="Temperature for text generation")

    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: float = Field(default_factory=lambda: time.time())
    response_time: Optional[float] = None
    model_used: str = "custom-llama"

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_loaded: bool
    memory_usage: Optional[str] = None

class FeedbackRequest(BaseModel):
    chat_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    feedback_text: Optional[str] = Field(None, max_length=500, description="Optional feedback text")

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)



