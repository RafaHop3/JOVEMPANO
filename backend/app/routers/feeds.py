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
    enc = getattr(entry, "enclosures", None)
    if enc and enc[0].get("href"):
        if "image" in enc[0].get("type", "") or enc[0]["href"].endswith((".jpg", ".png", ".webp")):
            return enc[0]["href"]
    content = getattr(entry, "content", None)
    if content and isinstance(content, list) and content[0].get("value"):
        soup = BeautifulSoup(content[0]["value"], "html.parser")
        img = soup.find("img")
        if img and img.get("src"):
            return img["src"]
    summary = entry.get("summary", "")
    if "<img" in summary:
        soup = BeautifulSoup(summary, "html.parser")
        img = soup.find("img")
        if img and img.get("src"):
            return img["src"]
    return None


import logging
logger = logging.getLogger(__name__)

def fetch_feed(url: str) -> object | None:
    """Fetch and parse an RSS feed, with simple in-memory cache."""
    now = time.time()
    if url in _cache:
        cached_ts, cached_feed = _cache[url]
        if now - cached_ts < CACHE_TTL:
            return cached_feed

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8"
            },
        )
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        if not feed.entries:
             logger.warning(f"[feeds] No entries found for {url}")
        _cache[url] = (now, feed)
        return feed
    except Exception as exc:
        logger.error(f"[feeds] Error fetching {url}: {str(exc)}")
        if url in _cache:
            return _cache[url][1]
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_url = {executor.submit(fetch_feed, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            feed = future.result()
            if feed and hasattr(feed, "entries"):
                feeds_data.append(feed)

    if not feeds_data:
        return JSONResponse(content=[], headers={"Cache-Control": "public, max-age=60"})

    # 1. Group entries by source
    entries_by_source: dict[str, list] = {}
    for feed in feeds_data:
        source_title = getattr(feed.feed, "title", "Notícias")
        if "G1" in source_title: source_title = "G1"
        elif "CNN" in source_title: source_title = "CNN Brasil"
        elif "UOL" in source_title: source_title = "UOL"
        elif "BBC" in source_title: source_title = "BBC News"
        elif "InfoMoney" in source_title: source_title = "InfoMoney"
        elif "Olhar Digital" in source_title: source_title = "Olhar Digital"
        elif "Folha" in source_title: source_title = "Folha de S.Paulo"
        elif "Poder360" in source_title: source_title = "Poder360"
        elif "Estadão" in source_title: source_title = "Estadão"
        elif "Valor" in source_title: source_title = "Valor Econômico"
        elif "R7" in source_title: source_title = "R7 Notícias"
        elif "Gizmodo" in source_title: source_title = "Gizmodo"
        elif "Canaltech" in source_title: source_title = "Canaltech"
        elif "Gazeta" in source_title: source_title = "Gazeta Esportiva"

        source_entries = sorted(feed.entries[:30], key=get_sort_key, reverse=True)
        for e in source_entries:
            e["_custom_source"] = source_title
        entries_by_source[source_title] = source_entries

    # 2. Interleaving Algorithm (The Balance Engine)
    balanced_entries = []
    max_per_source = 40
    sources_list = sorted(list(entries_by_source.keys()))
    
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

    # Pagination slice
    start_idx = (page - 1) * limit
    paginated_articles = articles[start_idx : start_idx + limit]

    return JSONResponse(
        content=paginated_articles,
        headers={"Cache-Control": "public, max-age=120"},
    )
