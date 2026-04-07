from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine, Base, SessionLocal
from app import models
from app.core.security import get_password_hash
from app.routers import auth, news
from app.routers.news import banner_router
app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(news.router)
app.include_router(banner_router)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    
    # Create default admin if it doesn't exist
    db = SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            hashed = get_password_hash(settings.ADMIN_PASSWORD)
            db.add(models.User(username="admin", hashed_password=hashed, role="admin"))
            db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}
