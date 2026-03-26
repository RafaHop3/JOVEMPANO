from fastapi import FastAPI
from app.core.config import settings
from app.database import engine, Base
# Import models to ensure tables are created when calling create_all
from app import models
from app.routers import news, tasks_router, generator_router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(news.router)
app.include_router(tasks_router.router)
app.include_router(generator_router.router)

@app.on_event("startup")
async def startup_event():
    # Note: In production, consider using Alembic for migrations instead of create_all.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}
