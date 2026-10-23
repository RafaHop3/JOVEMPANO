import time
import feedparser
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/feeds", tags=["Feeds"])

# ──────────────────────────────────────────────────────────────────────────────
# RSS Sources for each category (Massively Diversified)
# ──────────────────────────────────────────────────────────────────────────────
FEED_SOURCES: dict[str, list[str]] = {
    "politica": [
        "https://g1.globo.com/rss/g1/politica/",
        "https://www.cnnbrasil.com.br/politica/feed/",
        "https://www.poder360.com.br/politica/feed/",
        "https://feeds.folha.uol.com.br/poder/rss091.xml",
        "https://noticias.r7.com/brasil/politica/feed.xml",
    ],
    "economia": [
        "https://g1.globo.com/rss/g1/economia/",
        "https://www.infomoney.com.br/feed/",
        "https://www.cnnbrasil.com.br/economia/feed/",
        "https://valor.globo.com/rss/valor/",
        "https://feeds.folha.uol.com.br/mercado/rss091.xml",
    ],
    "esportes": [
        "https://ge.globo.com/rss/ge/",
        "https://www.cnnbrasil.com.br/esportes/feed/",
        "https://noticias.r7.com/esportes/feed.xml",
        "https://feeds.folha.uol.com.br/esporte/rss091.xml",
        "https://www.gazetaesportiva.com/feed/",
    ],
    "tecnologia": [
        "https://g1.globo.com/rss/g1/tecnologia/",
        "https://olhardigital.com.br/rss",
        "https://www.cnnbrasil.com.br/tecnologia/feed/",
        "https://gizmodo.uol.com.br/feed/",
        "https://canaltech.com.br/rss/",
    ],
    "mundo": [
        "https://g1.globo.com/rss/g1/mundo/",
        "https://feeds.bbci.co.uk/portuguese/rss.xml",
        "https://www.cnnbrasil.com.br/internacional/feed/",
        "https://noticias.r7.com/internacional/feed.xml",
        "https://feeds.folha.uol.com.br/mundo/rss091.xml",
    ],
    "entretenimento": [
        "https://gshow.globo.com/rss/gshow/",
        "https://www.cnnbrasil.com.br/entretenimento/feed/",
        "https://noticias.r7.com/entretenimento/feed.xml",
        "https://feeds.folha.uol.com.br/ilustrada/rss091.xml",
        "https://f5.folha.uol.com.br/rss091.xml",
    ],
    "geral": [
        "https://g1.globo.com/rss/g1/",
        "https://rss.uol.com.br/feed/noticias.xml",
        "https://feeds.bbci.co.uk/portuguese/rss.xml",
        "https://www.cnnbrasil.com.br/feed/",
        "https://www.poder360.com.br/feed/",
        "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml",
        "https://noticias.r7.com/feed.xml",
    ],
}

CATEGORY_LABELS: dict[str, str] = {
    "politica":      "Política",
    "economia":      "Economia",
    "esportes":      "Esportes",
    "tecnologia":    "Tecnologia",
    "mundo":         "Mundo",
    "entretenimento":"Entretenimento",
    "geral":         "Geral",
}

# In-memory cache: { url: (timestamp, parsed_feed) }
_cache: dict[str, tuple[float, object]] = {}
CACHE_TTL = 120  # 2 minutes

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
def clean_html(html_text: str) -> str:
    """Strip HTML tags and return plain text snippet."""
    if not html_text:
        return ""
    text = BeautifulSoup(html_text, "html.parser").get_text(separator=" ", strip=True)
    return text[:300]


def extract_image(entry) -> str | None:
    """Try several common RSS image fields."""
    media = getattr(entry, "media_content", None)
    if media and isinstance(media, list) and media[0].get("url"):
        return media[0]["url"]
    thumb = getattr(entry, "media_thumbnail", None)
    if thumb and isinstance(thumb, list) and thumb[0].get("url"):
        return thumb[0]["url"]
    enclosures = getattr(entry, "enclosures", None)
    if enclosures and isinstance(enclosures, list) and enclosures[0].get("href"):
        return enclosures[0]["href"]
    # Look for <img> tags in summary or content
    for field in ("summary", "content"):
        val = getattr(entry, field, "")
        if isinstance(val, list) and val:
            val = val[0].get("value", "")
        if isinstance(val, str) and "<img" in val:
            soup = BeautifulSoup(val, "html.parser")
            tag = soup.find("img")
            if tag and tag.get("src"):
                return tag["src"]
    return None


def fetch_single_feed(url: str):
    """Fetch and parse one feed with in-memory caching."""
    now = time.time()
    if url in _cache:
        ts, data = _cache[url]
        if now - ts < CACHE_TTL:
            return data

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36 (JovemPano/2.1 RSS Reader)"
        ),
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=6)
        resp.raise_for_status()
        parsed = feedparser.parse(resp.content)
        _cache[url] = (now, parsed)
        return parsed
    except Exception as exc:
        print(f"[Feeds] Error fetching {url}: {exc}")
        return None

def get_sort_key(entry):
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        return time.mktime(parsed)
    return 0

POSITIVE_KEYWORDS = [
    "sustentabilidade", "avanço", "descoberta", "cura", "solidariedade", 
    "educação", "tecnologia", "meio ambiente", "direitos", "inclusão",
    "voluntariado", "recuperação", "crescimento", "ciência", "positivo",
    "esperança", "inovação"
]

def is_social_interest(title: str, summary: str) -> bool:
    text = (title + " " + summary).lower()
    return any(key in text for key in POSITIVE_KEYWORDS)


# ──────────────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/{category}")
def get_category_feed(category: str, limit: int = 15, page: int = 1):
    """
    Return parsed RSS articles for the given category slug.
    Implements an interleaving algorithm to ensure source diversity.
    """
    key = category.lower()
    is_positive = key in ["positive", "positivas"]
    
    if is_positive:
        urls = FEED_SOURCES["geral"]
        cat_display = "Boas Notícias"
    else:
        urls = FEED_SOURCES.get(key, FEED_SOURCES["geral"])
        cat_display = CATEGORY_LABELS.get(key, "Geral")

    # Fetch feeds concurrently
    feeds_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(urls), 6)) as executor:
        future_to_url = {executor.submit(fetch_single_feed, u): u for u in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            if data:
                feeds_data.append(data)

    # 1. Group valid entries by their source/feed title
    entries_by_source = {}
    for feed in feeds_data:
        source_title = clean_html(feed.feed.get("title", "Fonte Externa"))
        if not source_title or source_title == "Fonte Externa":
            source_title = "Notícias"
            
        entries = getattr(feed, "entries", [])
        if entries:
            # Sort entries within the same feed by date
            entries.sort(key=get_sort_key, reverse=True)
            for e in entries:
                e["_custom_source"] = source_title
            entries_by_source[source_title] = entries

    # 2. Interleave: Take 1st from each, then 2nd from each, etc.
    balanced_entries = []
    sources_list = list(entries_by_source.keys())
    max_per_source = max([len(el) for el in entries_by_source.values()]) if entries_by_source else 0

    for i in range(max_per_source):
        batch = []
        for s in sources_list:
            if i < len(entries_by_source[s]):
                batch.append(entries_by_source[s][i])
        
        # Sort each "layer" by date to maintain relative recency
        batch.sort(key=get_sort_key, reverse=True)
        balanced_entries.extend(batch)

    # 3. Process, Deduplicate and Clean
    articles = []
    seen_titles = set()
    
    for entry in balanced_entries:
        title = entry.get("title", "Sem título").strip()
        if not title or title in seen_titles:
            continue
            
        summary_clean = clean_html(entry.get("summary", ""))
        if is_positive and not is_social_interest(title, summary_clean):
            continue
        
        # Filtro de Imagem: Pula a notícia se não houver imagem
        image_url = extract_image(entry)
        if not image_url:
            continue
            
        seen_titles.add(title)
        articles.append({
            "id": entry.get("id") or entry.get("link", ""),
            "title": title,
            "summary": summary_clean,
            "image_url": image_url,
            "link": entry.get("link", ""),
            "published_at": entry.get("published") or entry.get("updated", ""),
            "source": entry.get("_custom_source", "Notícias"),
            "category": cat_display,
            "is_positive": is_positive,
        })

    # Injeção das novidades da Orbe Systems no topo da categoria Tecnologia
    if key == "tecnologia" and page == 1:
        try:
            from app.database import SessionLocal
            from app.models import News
            with SessionLocal() as db_session:
                orbe_news = db_session.query(News).filter(News.category.ilike("%tecnologia%")).order_by(News.id.desc()).limit(3).all()
                orbe_articles = []
                for on in orbe_news:
                    orbe_articles.append({
                        "id": f"orbe-{on.id}",
                        "title": f"[ORBE SYSTEMS] {on.title}",
                        "summary": clean_html(on.content)[:280],
                        "image_url": on.image_url or "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80",
                        "link": f"/news/{on.id}",
                        "published_at": on.created_at.isoformat() if on.created_at else "",
                        "source": "Orbe Systems Tech Radar",
                        "category": "Tecnologia",
                        "is_positive": False,
                    })
                articles = orbe_articles + articles
        except Exception as e:
            print(f"[Feeds] Erro ao injetar noticias Orbe Systems: {e}")

    # Pagination slice
    start_idx = (page - 1) * limit
    paginated_articles = articles[start_idx : start_idx + limit]

    return JSONResponse(
        content=paginated_articles,
        headers={"Cache-Control": "public, max-age=120"},
    )
