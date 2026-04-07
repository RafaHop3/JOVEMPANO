from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import News, User, HeroBanner
from app.schemas import NewsCreate, NewsOut, HeroBannerCreate, HeroBannerOut
from app.core.security import get_current_user
from typing import List

router = APIRouter(prefix="/news", tags=["News"])

@router.post("/", response_model=NewsOut)
def create_news(news: NewsCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_news = News(title=news.title, content=news.content, image_url=news.image_url, category=news.category)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@router.get("/", response_model=List[NewsOut])
def get_news(db: Session = Depends(get_db)):
    return db.query(News).order_by(News.id.desc()).all()

@router.delete("/{news_id}", status_code=204)
def delete_news(news_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(News).filter(News.id == news_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Notícia não encontrada.")
    db.delete(item)
    db.commit()

# --- Hero Banners ---
banner_router = APIRouter(prefix="/banners", tags=["Banners"])

@banner_router.get("/", response_model=List[HeroBannerOut])
def get_banners(db: Session = Depends(get_db)):
    return db.query(HeroBanner).order_by(HeroBanner.id.desc()).all()

@banner_router.post("/", response_model=HeroBannerOut)
def create_banner(banner: HeroBannerCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_banner = HeroBanner(**banner.dict())
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return db_banner
