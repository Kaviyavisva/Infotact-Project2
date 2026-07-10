"""
news_fetcher.py

Fetches recent logistics and supply chain news using DDGS.
"""

from ddgs import DDGS

from src.config import SEARCH_QUERY, MAX_RESULTS
from src.logger import setup_logger


class NewsFetcher:
    """
    Fetches logistics-related news articles.
    """

    def __init__(self):
        """
        Initialize the news fetcher.
        """
        self.search_engine = DDGS()
        self.logger = setup_logger()

    def fetch_news(self):
        """
        Fetch recent logistics news.

        Returns:
            list: List of news articles.
        """

        articles = []

        try:
            self.logger.info("Fetching latest logistics news...")

            results = self.search_engine.text(
                SEARCH_QUERY,
                max_results=MAX_RESULTS
            )

            for result in results:
                articles.append(
                    {
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", "")
                    }
                )

            self.logger.info(f"Successfully fetched {len(articles)} articles.")

            return articles

        except Exception as e:
            self.logger.error(f"Error fetching news: {e}")
            return []