from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import RawNews
from app.schemas import RawNews as RawNewsSchema

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/", response_model=list[RawNewsSchema])
async def get_news(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RawNews).offset(skip).limit(limit))
    return result.scalars().all()
