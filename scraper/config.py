"""
Configuration file for the banking sentiment monitoring scraper
"""

# Brands to monitor
BRANDS = [
    "HBL",
    "Habib Bank",
    "Meezan Bank",
    "Bank Alfalah"
]

# News sources to scrape
NEWS_SOURCES = {
    "dawn": {
        "base_url": "https://www.dawn.com",
        "search_url": "https://www.dawn.com/search?query=",
        "name": "Dawn"
    },
    "tribune": {
        "base_url": "https://tribune.com.pk",
        "search_url": "https://tribune.com.pk/search?q=",
        "name": "Express Tribune"
    },
    "thenews": {
        "base_url": "https://www.thenews.com.pk",
        "search_url": "https://www.thenews.com.pk/search/",
        "name": "The News International"
    },
    "brecorder": {
        "base_url": "https://www.brecorder.com",
        "search_url": "https://www.brecorder.com/search?q=",
        "name": "Business Recorder"
    }
}

# Scraping settings
SCRAPE_SETTINGS = {
    "delay_between_requests": 3,  # seconds
    "max_articles_per_brand": 100,
    "timeout": 30,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Date range (last 3 months)
from datetime import datetime, timedelta

END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=90)

# Database settings (we'll use SQLite initially)
DATABASE = {
    "type": "sqlite",
    "path": "../data/raw/articles.db"
}

# Output paths
OUTPUT_PATHS = {
    "raw_data": "../data/raw/",
    "processed_data": "../data/processed/",
    "logs": "../logs/"
}