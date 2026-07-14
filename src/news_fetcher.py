"""
news_fetcher.py

Fetches recent logistics and supply chain news using DDGS.
"""

from ddgs import DDGS
from urllib.parse import urlparse
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

    def remove_duplicates(self, articles):
        """
        Remove duplicate news articles based on URL.
        """
        unique_articles = []
        seen_urls = set()

        for article in articles:
            url = article.get("url", "").strip()

            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)

        return unique_articles

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
                url = result.get("href", "")

                articles.append(
                    {
                        "title": result.get("title", ""),
                        "url": url,
                        "source": urlparse(url).netloc if url else "",
                        "snippet": result.get("body", "")
                    }
                )

            self.logger.info(f"Successfully fetched {len(articles)} articles.")

            articles = self.remove_duplicates(articles)

            self.logger.info(f"{len(articles)} unique articles collected.")

            return articles

        except Exception as e:
            self.logger.error(f"Error fetching news: {e}")
            return []