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
        # Lista de usuários com permissão de Admin (você pode adicionar quantos quiser aqui)
        admins = [
            {"username": "rafael_admin", "password": "Muhammadalivsroyjonesjr"},
            # Para adicionar outro, basta descomentar e preencher a linha abaixo:
            # {"username": "nome_do_admin", "password": "senha_do_admin"},
        ]
        
        for admin_data in admins:
            user = db.query(models.User).filter(models.User.username == admin_data["username"]).first()
            if not user:
                hashed = get_password_hash(admin_data["password"])
                db.add(models.User(username=admin_data["username"], hashed_password=hashed, role="admin"))
                db.commit()
            else:
                # Força a atualização da senha caso ela mude nesta lista
                user.hashed_password = get_password_hash(admin_data["password"])
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


from sqlalchemy.sql import text
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

@app.get("/ping")
def ping(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "pong", "database": "connected"}
    except Exception as e:
        # In a real app we might log the exception `e`
        return {"status": "error", "message": "pong", "database": "disconnected"}
