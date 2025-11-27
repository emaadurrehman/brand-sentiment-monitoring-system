"""
Main web scraper for banking news articles
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
from loguru import logger
import config

class BankingNewsScraper:
    """Scraper for banking-related news articles"""
    
    def __init__(self):
        """Initialize the scraper with Chrome options"""
        logger.info("Initializing Banking News Scraper...")
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={config.SCRAPE_SETTINGS["user_agent"]}')
        
        # Initialize driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        self.articles = []
        logger.success("Scraper initialized successfully")
    
    def scrape_dawn(self, brand):
        """Scrape articles from Dawn.com"""
        logger.info(f"Scraping Dawn for: {brand}")
        
        try:
            search_url = f"{config.NEWS_SOURCES['dawn']['search_url']}{brand}"
            self.driver.get(search_url)
            time.sleep(config.SCRAPE_SETTINGS['delay_between_requests'])
            
            # Get page source and parse
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Find article elements (you'll need to inspect Dawn's HTML structure)
            articles = soup.find_all('article', class_='story')  # Example selector
            
            for article in articles[:config.SCRAPE_SETTINGS['max_articles_per_brand']]:
                try:
                    title = article.find('h2').text.strip() if article.find('h2') else 'N/A'
                    link = article.find('a')['href'] if article.find('a') else 'N/A'
                    
                    # Make sure link is absolute
                    if link.startswith('/'):
                        link = config.NEWS_SOURCES['dawn']['base_url'] + link
                    
                    date_elem = article.find('span', class_='timestamp')
                    date = date_elem.text.strip() if date_elem else 'N/A'
                    
                    # Get article snippet/summary
                    snippet = article.find('div', class_='story__excerpt').text.strip() if article.find('div', class_='story__excerpt') else 'N/A'
                    
                    article_data = {
                        'brand': brand,
                        'source': 'Dawn',
                        'title': title,
                        'url': link,
                        'snippet': snippet,
                        'date': date,
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    self.articles.append(article_data)
                    logger.debug(f"Scraped: {title[:50]}...")
                    
                except Exception as e:
                    logger.warning(f"Error parsing article: {e}")
                    continue
            
            logger.success(f"Scraped {len(articles)} articles from Dawn for {brand}")
            
        except Exception as e:
            logger.error(f"Error scraping Dawn for {brand}: {e}")
    
    def scrape_tribune(self, brand):
        """Scrape articles from Express Tribune"""
        logger.info(f"Scraping Express Tribune for: {brand}")
        # Similar structure to scrape_dawn
        # We'll implement this after testing Dawn
        pass
    
    def scrape_all_brands(self):
        """Scrape all brands from all sources"""
        logger.info("Starting full scrape for all brands...")
        
        for brand in config.BRANDS:
            logger.info(f"\n{'='*50}")
            logger.info(f"Scraping articles for: {brand}")
            logger.info(f"{'='*50}")
            
            # Scrape from each source
            self.scrape_dawn(brand)
            time.sleep(config.SCRAPE_SETTINGS['delay_between_requests'])
            
            # Add other sources later
            # self.scrape_tribune(brand)
            # self.scrape_thenews(brand)
        
        logger.success(f"Total articles scraped: {len(self.articles)}")
    
    def save_to_csv(self, filename=None):
        """Save scraped articles to CSV"""
        if not filename:
            filename = f"../data/raw/articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df = pd.DataFrame(self.articles)
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.success(f"Saved {len(self.articles)} articles to {filename}")
        
        return filename
    
    def close(self):
        """Close the browser"""
        self.driver.quit()
        logger.info("Browser closed")

def main():
    """Main execution function"""
    logger.info("Starting Banking Sentiment Monitoring Scraper")
    
    scraper = BankingNewsScraper()
    
    try:
        # Scrape articles
        scraper.scrape_all_brands()
        
        # Save results
        scraper.save_to_csv()
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
    
    finally:
        scraper.close()
    
    logger.info("Scraping completed!")

if __name__ == "__main__":
    main()