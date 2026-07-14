"""
data_processor.py

Processes and cleans fetched news articles.
"""

import re
from src.models import NewsArticle


class DataProcessor:
    """
    Cleans and structures news articles.
    """

    def clean_text(self, text):
        """
        Clean and normalize article text.
        """

        if not text:
            return ""

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        # Remove HTML tags
        text = re.sub(r"<.*?>", "", text)

        return text.strip()

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

            title = self.clean_text(article.get("title", ""))
            url = article.get("url", "").strip()
            snippet = self.clean_text(article.get("snippet", ""))
            source = article.get("source", "").strip()

            # Skip incomplete articles
            if title and snippet and url:
                processed_articles.append(
                    NewsArticle(
                        title=title,
                        url=url,
                        source=source,
                        snippet=snippet
                    )
                )

        return processed_articles