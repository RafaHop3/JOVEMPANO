from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import RawNews, GeneratedArticle
from app.services.llm_service import generate_article_from_raw

router = APIRouter(prefix="/articles", tags=["Articles Generation"])

@router.post("/generate/{raw_news_id}")
async def generate_article(raw_news_id: int, db: AsyncSession = Depends(get_db)):
    """
    Fetches raw news data, generates an article via LLM, and persists it as a draft.
    """
    result = await db.execute(select(RawNews).where(RawNews.id == raw_news_id))
    raw_news = result.scalars().first()
    
    if not raw_news:
        raise HTTPException(status_code=404, detail="Raw news not found")
        
    # Ensure there isn't an article already
    existing = await db.execute(select(GeneratedArticle).where(GeneratedArticle.raw_news_id == raw_news_id))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Article already generated for this news")
        
    try:
        article_data = await generate_article_from_raw(
            source=raw_news.source,
            title=raw_news.title,
            content=raw_news.content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {str(e)}")
        
    if not article_data:
         raise HTTPException(status_code=500, detail="LLM failed to return structured JSON")
         
    # Format the content nicely incorporating the JSON structure into the text block
    structured_content = f"**{article_data['subtitle']}**\n\n{article_data['content']}\n\n*Tags: {', '.join(article_data['tags'])}*\n*Fontes: {', '.join(article_data['sources'])}*"
    
    new_article = GeneratedArticle(
        raw_news_id=raw_news_id,
        title=article_data['title'],
        content=structured_content,
        status="draft"
    )
    
    db.add(new_article)
    await db.commit()
    await db.refresh(new_article)
    
    return {"message": "Article generated successfully", "article_id": new_article.id, "article_title": new_article.title}

@router.get("/")
async def get_articles(db: AsyncSession = Depends(get_db)):
    """
    Fetches all generated articles.
    """
    result = await db.execute(select(GeneratedArticle).order_by(GeneratedArticle.id.desc()).limit(20))
    articles = result.scalars().all()
    return articles
