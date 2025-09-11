from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "QA Chatbot Service"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "localhost"
    PORT: int = 8000

    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Model settings
    MODEL_PATH: str = "../merged_model"  # Must be set in .env file
    MAX_TOKENS: int = 200
    TEMPERATURE: float = 0.7
    TOP_P: float = 1.0

    # Database settings
    # DATABASE_URL: str = "sqlite:///./chat_history.db"


    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"


    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    CHAT_TEMPLATE: str = """{% for message in messages %}
                    {% if message['role'] == 'system' %}{{ '<|system|>\n' + message['content'] + eos_token }}
                    {% elif message['role'] == 'user' %}{{ '<|user|>\n' + message['content'] + eos_token }}
                    {% elif message['role'] == 'assistant' %}{{ '<|assistant|>\n' + message['content'] + eos_token }}
                    {% endif %}
                    {% if loop.last and add_generation_prompt %}{{ '<|assistant|>' }}
                    {% endif %}
                    {% endfor %}"""

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields


settings = Settings()
