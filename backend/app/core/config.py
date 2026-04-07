import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "JovemPano Minimal"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./jovempano.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "minimal-secret-key-change-later")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin")
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173", 
        "http://127.0.0.1:5173", 
        "http://localhost:5174", 
        "http://localhost:5175",
        "https://jovem-pano.vercel.app",
        "https://jovempano.vercel.app",
        "https://jovempano.render.com",
        "https://jovempano-backend.onrender.com"
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Permite adicionar origens via string separada por vírgula no ENV
        extra_origins = os.getenv("EXTRA_CORS_ORIGINS", "")
        if extra_origins:
            self.CORS_ORIGINS.extend([origin.strip() for origin in extra_origins.split(",")])
        
        frontend_url = os.getenv("FRONTEND_URL", "")
        if frontend_url and frontend_url not in self.CORS_ORIGINS:
            self.CORS_ORIGINS.append(frontend_url)
    
    class Config:
        env_file = ".env"

settings = Settings()
