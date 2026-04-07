import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "JovemPano Minimal"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./jovempano.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "minimal-secret-key-change-later")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # Base origins
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173", 
        "http://127.0.0.1:5173", 
        "http://localhost:5174", 
        "http://localhost:5175",
        "https://jovempano.vercel.app",
        "https://jovempano-backend.onrender.com"
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Permite adicionar origens extras via ENV
        extra = os.getenv("EXTRA_CORS_ORIGINS", "")
        if extra:
            self.CORS_ORIGINS.extend([o.strip() for o in extra.split(",") if o.strip()])
        
        # Garante que a URL do frontend esteja presente
        front = os.getenv("FRONTEND_URL", "")
        if front and front not in self.CORS_ORIGINS:
            self.CORS_ORIGINS.append(front)
    
    class Config:
        env_file = ".env"

settings = Settings()
