from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = int(os.getenv("PORT", "8000"))
    environment: str = "development"

    # CORS Configuration
    frontend_url: str = "http://localhost:3000"

    # Redis Configuration
    redis_url: Optional[str] = None

    # Security
    secret_key: str = "development_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Rate Limiting
    rate_limit_per_minute: int = 30

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()