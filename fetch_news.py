#!/usr/bin/env python3
"""
Real news fetcher using NewsAPI and RSS feeds with sample data fallback
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import logging
import time
import random
import json
from xml.etree import ElementTree as ET
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAPIFetcher:
    """Fetch news from NewsAPI (requires API key)"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
    
    def fetch_headlines(self, sources="bbc-news,cnn,reuters", language="en", page_size=20):
        """Fetch headlines from NewsAPI"""
        if not self.api_key:
            logger.warning("❌ No NewsAPI key found")
            return []
        
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'sources': sources,
                'language': language,
                'pageSize': page_size,
                'apiKey': self.api_key
            }
            
            logger.info(f"📡 Fetching from NewsAPI: {sources}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            headlines = []
            
            if data['status'] == 'ok':
                for article in data['articles']:
                    if article['title'] and article['title'] != '[Removed]':
                        headlines.append({
                            "title": article['title'],
                            "publishedAt": article['publishedAt'],
                            "source": article['source']['name'],
                            "url": article.get('url', ''),
                            "description": article.get('description', '')
                        })
                
                logger.info(f"✅ Fetched {len(headlines)} headlines from NewsAPI")
                return headlines
            
        except Exception as e:
            logger.error(f"❌ NewsAPI fetch failed: {e}")
            return []
    
    def fetch_everything(self, query="technology OR business", language="en", page_size=20):
        """Fetch everything from NewsAPI with query"""
        if not self.api_key:
            return []
        
        try:
            url = f"{self.base_url}/everything"
            yesterday = (datetime.now() - timedelta(days=1)).isoformat()
            
            params = {
                'q': query,
                'language': language,
                'pageSize': page_size,
                'from': yesterday,
                'sortBy': 'publishedAt',
                'apiKey': self.api_key
            }
            
            logger.info(f"📡 Searching NewsAPI: {query}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            headlines = []
            
            if data['status'] == 'ok':
                for article in data['articles']:
                    if article['title'] and article['title'] != '[Removed]':
                        headlines.append({
                            "title": article['title'],
                            "publishedAt": article['publishedAt'],
                            "source": article['source']['name'],
                            "url": article.get('url', ''),
                            "description": article.get('description', '')
                        })
                
                logger.info(f"✅ Found {len(headlines)} articles from NewsAPI")
                return headlines
            
        except Exception as e:
            logger.error(f"❌ NewsAPI search failed: {e}")
            return []

class RSSFetcher:
    """Fetch news from RSS feeds"""
    
    def fetch_from_rss(self, rss_url, source_name):
        """Fetch headlines from RSS feed"""
        try:
            logger.info(f"📡 Fetching RSS: {source_name}")
            response = requests.get(rss_url, timeout=10)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            headlines = []
            
            # Handle different RSS formats
            items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')
            
            for item in items[:10]:  # Limit to 10 items
                title = None
                pub_date = datetime.now().isoformat()
                link = ""
                description = ""
                
                # Try different title formats
                title_elem = item.find('title') or item.find('.//{http://www.w3.org/2005/Atom}title')
                if title_elem is not None:
                    title = title_elem.text
                
                # Try to get publication date
                pub_elem = item.find('pubDate') or item.find('.//{http://www.w3.org/2005/Atom}updated')
                if pub_elem is not None:
                    pub_date = pub_elem.text
                
                # Try to get link
                link_elem = item.find('link') or item.find('.//{http://www.w3.org/2005/Atom}link')
                if link_elem is not None:
                    link = link_elem.text or link_elem.get('href', '')
                
                # Try to get description
                desc_elem = item.find('description') or item.find('.//{http://www.w3.org/2005/Atom}summary')
                if desc_elem is not None:
                    description = desc_elem.text or ""
                
                if title:
                    headlines.append({
                        "title": title.strip(),
                        "publishedAt": pub_date,
                        "source": source_name,
                        "url": link,
                        "description": description[:200] + "..." if len(description) > 200 else description
                    })
            
            logger.info(f"✅ Fetched {len(headlines)} headlines from {source_name}")
            return headlines
            
        except Exception as e:
            logger.error(f"❌ RSS fetch failed for {source_name}: {e}")
            return []

# Sample data removed for production deployment

def fetch_news_simple():
    """Main function to fetch news from multiple sources"""
    
    logger.info("🚀 Starting news fetch from multiple sources...")
    all_headlines = []
    
    # Method 1: Try NewsAPI (best quality, requires API key)
    newsapi = NewsAPIFetcher()
    if newsapi.api_key:
        headlines = newsapi.fetch_headlines()
        if headlines:
            all_headlines.extend(headlines)
        
        # Also try search for more diverse content
        search_headlines = newsapi.fetch_everything("business OR technology OR health")
        if search_headlines:
            all_headlines.extend(search_headlines[:10])  # Limit search results
    
    # Method 2: Try RSS feeds (free, but less reliable)
    if len(all_headlines) < 5:  # If we don't have enough headlines
        rss_fetcher = RSSFetcher()
        rss_sources = [
            ("https://feeds.bbci.co.uk/news/rss.xml", "BBC News"),
            ("https://feeds.reuters.com/reuters/topNews", "Reuters"),
            ("https://rss.cnn.com/rss/edition.rss", "CNN")
        ]
        
        for rss_url, source_name in rss_sources:
            headlines = rss_fetcher.fetch_from_rss(rss_url, source_name)
            all_headlines.extend(headlines)
            if len(all_headlines) >= 15:  # Stop if we have enough
                break
            time.sleep(1)  # Be respectful with requests
    
    # Method 3: Error if no real data sources work
    if len(all_headlines) < 3:
        logger.error("❌ Failed to fetch news from any real source. Please check:")
        logger.error("   1. Internet connection")
        logger.error("   2. NewsAPI key in .env file") 
        logger.error("   3. RSS feed availability")
        return None
    
    if not all_headlines:
        logger.error("❌ No headlines found from any source")
        return None
    
    # Remove duplicates and limit results
    seen_titles = set()
    unique_headlines = []
    for headline in all_headlines:
        title_lower = headline['title'].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_headlines.append(headline)
        if len(unique_headlines) >= 20:  # Limit to 20 headlines
            break
    
    df = pd.DataFrame(unique_headlines)
    
    # Save to raw directory
    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = f"data/raw/headlines_{timestamp}.csv"
    df.to_csv(out_path, index=False)
    
    logger.info(f"✅ Saved {len(df)} unique headlines → {out_path}")
    
    # Show source breakdown
    source_counts = df['source'].value_counts()
    logger.info("📊 Headlines by source:")
    for source, count in source_counts.items():
        logger.info(f"   • {source}: {count}")
    
    # Show preview
    logger.info("📰 Latest headlines:")
    for i, row in df.head(5).iterrows():
        source_icon = "🌐"
        logger.info(f"   {source_icon} {row['title'][:70]}...")
    
    return df

if __name__ == "__main__":
    fetch_news_simple()