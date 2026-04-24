import time
import feedparser
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/feeds", tags=["Feeds"])

# ──────────────────────────────────────────────────────────────────────────────
# RSS Sources for each category (Diversified Sources)
# ──────────────────────────────────────────────────────────────────────────────
FEED_SOURCES: dict[str, list[str]] = {
    "politica": [
        "https://g1.globo.com/rss/g1/politica/",
        "https://www.cnnbrasil.com.br/politica/feed/",
    ],
    "economia": [
        "https://g1.globo.com/rss/g1/economia/",
        "https://www.infomoney.com.br/feed/",
        "https://www.cnnbrasil.com.br/economia/feed/",
    ],
    "esportes": [
        "https://ge.globo.com/rss/ge/",
        "https://www.cnnbrasil.com.br/esportes/feed/",
    ],
    "tecnologia": [
        "https://g1.globo.com/rss/g1/tecnologia/",
        "https://olhardigital.com.br/rss",
    ],
    "mundo": [
        "https://g1.globo.com/rss/g1/mundo/",
        "https://feeds.bbci.co.uk/portuguese/rss.xml",
        "https://www.cnnbrasil.com.br/internacional/feed/",
    ],
    "entretenimento": [
        "https://gshow.globo.com/rss/gshow/",
        "https://www.cnnbrasil.com.br/entretenimento/feed/",
    ],
    "geral": [
        "https://g1.globo.com/rss/g1/",
        "https://rss.uol.com.br/feed/noticias.xml",
        "https://feeds.bbci.co.uk/portuguese/rss.xml",
        "https://www.cnnbrasil.com.br/feed/",
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
CACHE_TTL = 120  # 2 minutes — equilíbrio entre frescor e carga nos provedores RSS


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
    # media:content
    media = getattr(entry, "media_content", None)
    if media and isinstance(media, list) and media[0].get("url"):
        return media[0]["url"]
    # media:thumbnail
    thumb = getattr(entry, "media_thumbnail", None)
    if thumb and isinstance(thumb, list) and thumb[0].get("url"):
        return thumb[0]["url"]
    # enclosures
    enc = getattr(entry, "enclosures", None)
    if enc and enc[0].get("href"):
        # Sometimes CNN/UOL puts images in enclosures
        if "image" in enc[0].get("type", "") or enc[0]["href"].endswith((".jpg", ".png", ".webp")):
            return enc[0]["href"]
    # check for image embedded in summary/content if no direct tag exists
    content = getattr(entry, "content", None)
    if content and isinstance(content, list) and content[0].get("value"):
        soup = BeautifulSoup(content[0]["value"], "html.parser")
        img = soup.find("img")
        if img and img.get("src"):
            return img["src"]
    
    # Check summary as fallback
    summary = entry.get("summary", "")
    if "<img" in summary:
        soup = BeautifulSoup(summary, "html.parser")
        img = soup.find("img")
        if img and img.get("src"):
            return img["src"]

    return None


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
            timeout=8,
            headers={"User-Agent": "JovemPano/2.0 RSS Reader (+https://jovempano.vercel.app)"},
        )
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        _cache[url] = (now, feed)
        return feed
    except Exception as exc:
        print(f"[feeds] Error fetching {url}: {exc}")
        # Return stale cache if available
        if url in _cache:
            return _cache[url][1]
        return None

def get_sort_key(entry):
    """Safely get a sortable timestamp from an RSS entry."""
    # published_parsed or updated_parsed is a time.struct_time
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        return time.mktime(parsed)
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/{category}")
def get_category_feed(category: str, limit: int = 15):
    """Return parsed RSS articles for the given category slug, merged from multiple sources."""
    key = category.lower()
    urls = FEED_SOURCES.get(key, FEED_SOURCES["geral"])
    cat_display = CATEGORY_LABELS.get(key, "Geral")

    # Fetch feeds concurrently
    feeds_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_feed, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            feed = future.result()
            if feed and hasattr(feed, "entries"):
                feeds_data.append(feed)

    if not feeds_data:
        return JSONResponse(
            content=[],
            headers={"Cache-Control": "public, max-age=60"},
        )

    # Merge entries from all feeds
    all_entries = []
    for feed in feeds_data:
        source_title = getattr(feed.feed, "title", "Notícias")
        # Clean up source names
        if "G1" in source_title: source_title = "G1"
        elif "CNN" in source_title: source_title = "CNN Brasil"
        elif "UOL" in source_title: source_title = "UOL"
        elif "BBC" in source_title: source_title = "BBC News"
        elif "InfoMoney" in source_title: source_title = "InfoMoney"
        elif "Olhar Digital" in source_title: source_title = "Olhar Digital"

        for entry in feed.entries[:20]:  # take top 20 from each to avoid massive sorting
            entry["_custom_source"] = source_title
            all_entries.append(entry)

    # Sort merged entries by date (newest first)
    all_entries.sort(key=get_sort_key, reverse=True)

    articles = []
    # Deduplicate by title to avoid the same news from different feeds
    seen_titles = set()

    for entry in all_entries:
        if len(articles) >= limit:
            break
            
        title = entry.get("title", "Sem título").strip()
        if not title or title in seen_titles:
            continue
            
        seen_titles.add(title)

        articles.append(
            {
                "id": entry.get("id") or entry.get("link", ""),
                "title": title,
                "summary": clean_html(entry.get("summary", "")),
                "image_url": extract_image(entry),
                "link": entry.get("link", ""),
                "published_at": entry.get("published") or entry.get("updated", ""),
                "source": entry.get("_custom_source", "Notícias"),
                "category": cat_display,
            }
        )

    return JSONResponse(
        content=articles,
        headers={"Cache-Control": "public, max-age=120"},
    )
