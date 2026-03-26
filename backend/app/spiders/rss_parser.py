import feedparser
from bs4 import BeautifulSoup
import requests
from typing import List, Dict

def fetch_rss_feed(feed_url: str, source_name: str) -> List[Dict]:
    """
    Fetches an RSS feed and returns a list of dictionaries with the extracted news data.
    """
    feed = feedparser.parse(feed_url)
    news_items = []
    
    for entry in feed.entries:
        # Extract basic info
        title = entry.get('title', 'Sem Título')
        url = entry.get('link', '')
        author = entry.get('author', None)
        
        # Try to parse published date; fallback to none if not present
        # Extract content: some feeds use 'content', others 'summary'
        raw_content = ''
        if 'content' in entry:
            raw_content = entry['content'][0]['value']
        elif 'summary' in entry:
            raw_content = entry['summary']
            
        # Clean HTML content with BeautifulSoup
        soup = BeautifulSoup(raw_content, 'html.parser')
        clean_content = soup.get_text(separator='\n').strip()
        
        # In case the content is empty, maybe we need to fetch the URL directly
        if not clean_content and url:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    page_soup = BeautifulSoup(response.content, 'html.parser')
                    # Very generic content extraction, specific sources need specific selectors
                    paragraphs = page_soup.find_all('p')
                    clean_content = '\n'.join([p.get_text() for p in paragraphs])
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                
        if clean_content:
            news_items.append({
                "source": source_name,
                "title": title,
                "url": url,
                "content": clean_content,
                "author": author,
            })
            
    return news_items
