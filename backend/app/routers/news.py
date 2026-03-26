from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import News, User
from app.schemas import NewsCreate, NewsOut
from app.core.security import get_current_user

router = APIRouter(prefix="/news", tags=["News"])

@router.post("/", response_model=NewsOut)
def create_news(news: NewsCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_news = News(title=news.title, content=news.content)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@router.get("/", response_model=list[NewsOut])
def get_news(db: Session = Depends(get_db)):
    return db.query(News).order_by(News.id.desc()).all()
