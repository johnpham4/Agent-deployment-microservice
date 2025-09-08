from fastapi import BaseModel, Field
from datetime import datetime
from enum import Enum
import uuid
from typing import Optional, List, Dict, Any

class Modeltype(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"

class MessageDTO(BaseModel):
    Role: Modeltype
    Content: str
    Created_at: datetime = Field(default_factory=datetime.now)

class ChatResponseDTO(BaseModel):
    Role: Modeltype
    Content: str
    Created_at: datetime = Field(default_factory=datetime.now)

class HealthResponseDTO(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_loaded: bool
    memory_usage: Optional[str] = None

class ErrorResponseDTO(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

