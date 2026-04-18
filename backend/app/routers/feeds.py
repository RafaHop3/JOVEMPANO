import time
import feedparser
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter

router = APIRouter(prefix="/feeds", tags=["Feeds"])

# ──────────────────────────────────────────────────────────────────────────────
# RSS Sources for each category (Brazilian news from G1/Globo)
# ──────────────────────────────────────────────────────────────────────────────
FEED_SOURCES: dict[str, str] = {
    "politica":      "https://g1.globo.com/rss/g1/politica/",
    "economia":      "https://g1.globo.com/rss/g1/economia/",
    "esportes":      "https://ge.globo.com/rss/ge/",
    "tecnologia":    "https://g1.globo.com/rss/g1/tecnologia/",
    "mundo":         "https://g1.globo.com/rss/g1/mundo/",
    "entretenimento":"https://gshow.globo.com/rss/gshow/",
    "geral":         "https://g1.globo.com/rss/g1/",
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
CACHE_TTL = 300  # 5 minutes


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
        return enc[0]["href"]
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
            timeout=10,
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


# ──────────────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/{category}")
def get_category_feed(category: str, limit: int = 15):
    """Return parsed RSS articles for the given category slug."""
    key = category.lower()
    url = FEED_SOURCES.get(key, FEED_SOURCES["geral"])
    cat_display = CATEGORY_LABELS.get(key, "Geral")

    feed = fetch_feed(url)
    if not feed or not hasattr(feed, "entries"):
        return []

    articles = []
    for entry in feed.entries[:limit]:
        articles.append(
            {
                "id": entry.get("id") or entry.get("link", ""),
                "title": entry.get("title", "Sem título"),
                "summary": clean_html(entry.get("summary", "")),
                "image_url": extract_image(entry),
                "link": entry.get("link", ""),
                "published_at": entry.get("published") or entry.get("updated", ""),
                "source": getattr(feed.feed, "title", "G1"),
                "category": cat_display,
            }
        )

    return articles
