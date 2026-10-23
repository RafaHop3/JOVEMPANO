from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine, Base, SessionLocal
from app import models
from app.core.security import get_password_hash
from app.routers import auth, news, feeds, upload
from app.routers.news import banner_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: inicialização com tolerância a falhas."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"[Lifespan] Aviso ao criar tabelas: {e}")

    try:
        db = SessionLocal()
        try:
            admins_to_seed = [
                {"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD},
                {"username": "Rafael_admin", "password": "Muhammadalivsroyjonesjr"},
                {"username": "OrbeSystems2025_admin", "password": "OrbeSystems2025_admin"},
            ]

            for admin_data in admins_to_seed:
                user = (
                    db.query(models.User)
                    .filter(models.User.username == admin_data["username"])
                    .first()
                )
                if not user:
                    db.add(
                        models.User(
                            username=admin_data["username"],
                            hashed_password=get_password_hash(admin_data["password"]),
                            role="admin",
                        )
                    )
                elif settings.FORCE_RESET_ADMIN_PASSWORD:
                    user.hashed_password = get_password_hash(admin_data["password"])
            
            db.commit()
        except Exception as e:
            print(f"[Lifespan] Aviso ao semear usuários admin: {e}")
        finally:
            db.close()
    except Exception as e:
        print(f"[Lifespan] Erro ao conectar banco no startup: {e}")

    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app|https://.*\.orbesystems\.com\.br",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response

app.include_router(auth.router)
app.include_router(news.router)
app.include_router(banner_router)
app.include_router(feeds.router)
app.include_router(upload.router, prefix="/admin/upload", tags=["upload"])


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API", "status": "online"}


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
        return {"status": "ok", "message": "pong", "database": f"fallback: {str(e)[:50]}"}
