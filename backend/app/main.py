from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine, Base, SessionLocal
from app import models
from app.core.security import get_password_hash
from app.routers import auth, news, feeds
from app.routers.news import banner_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: create tables and seed default admin on startup."""
    # ── Startup ──────────────────────────────────────────────────────────────
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            hashed = get_password_hash(settings.ADMIN_PASSWORD)
            db.add(models.User(username="admin", hashed_password=hashed, role="admin"))
            db.commit()
    finally:
        db.close()

    yield  # ── Application runs here ─────────────────────────────────────────
    # ── Shutdown (nothing required) ───────────────────────────────────────────


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

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
app.include_router(feeds.router)


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}


@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}
