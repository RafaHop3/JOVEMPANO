import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "JovemPano Minimal"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./jovempano.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "minimal-secret-key-change-later")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin")
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    class Config:
        env_file = ".env"

settings = Settings()
