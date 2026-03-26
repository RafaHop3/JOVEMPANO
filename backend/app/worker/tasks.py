import asyncio
from sqlalchemy.future import select
from celery.utils.log import get_task_logger

from app.worker.celery_app import celery_app
from app.spiders.rss_parser import fetch_rss_feed
from app.database import AsyncSessionLocal
from app.models import RawNews

logger = get_task_logger(__name__)

# List of feeds to monitor
RSS_FEEDS = [
    {"url": "https://www12.senado.leg.br/noticias/feed/noticias", "source": "Senado Federal"},
    {"url": "https://www.camara.leg.br/noticias/rss", "source": "Câmara dos Deputados"},
    {"url": "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml", "source": "Agência Brasil"},
    {"url": "https://portal.stf.jus.br/rss/noticia.asp", "source": "Supremo Tribunal Federal (STF)"},
    {"url": "https://g1.globo.com/rss/g1/politica/", "source": "G1 Política"},
]

async def save_news_to_db(news_items):
    async with AsyncSessionLocal() as session:
        for item in news_items:
            # Check if url already exists
            stmt = select(RawNews).where(RawNews.url == item['url'])
            result = await session.execute(stmt)
            exists = result.scalars().first()
            if not exists:
                new_article = RawNews(
                    source=item['source'],
                    title=item['title'],
                    url=item['url'],
                    content=item['content'],
                    author=item['author']
                )
                session.add(new_article)
        await session.commit()

@celery_app.task(name="fetch_all_rss_feeds")
def fetch_all_rss_feeds():
    logger.info("Starting RSS feed collection...")
    all_news = []
    for feed in RSS_FEEDS:
        logger.info(f"Fetching from {feed['source']}")
        news = fetch_rss_feed(feed['url'], feed['source'])
        all_news.extend(news)
        
    logger.info(f"Total news collected: {len(all_news)}. Saving to database...")
    # Getting loop because celery runs sync by default
    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_news_to_db(all_news))
    
    logger.info("RSS feed collection completed.")
    return {"status": "success", "count": len(all_news)}
