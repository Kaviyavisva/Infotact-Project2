"""
data_processor.py

Processes and cleans fetched news articles.
"""

from src.models import NewsArticle


class DataProcessor:
    """
    Cleans and structures news articles.
    """

    def process_articles(self, articles):
        """
        Process fetched news articles.

        Args:
            articles (list): List of fetched news articles.

        Returns:
            list[NewsArticle]: List of processed news articles.
        """

        processed_articles = []

        for article in articles:

            title = article.get("title", "").strip()
            url = article.get("url", "").strip()
            snippet = article.get("snippet", "").strip()

            # Skip incomplete articles
            if title and snippet:
                processed_articles.append(
                    NewsArticle(
                        title=title,
                        url=url,
                        snippet=snippet
                    )
                )

        return processed_articles