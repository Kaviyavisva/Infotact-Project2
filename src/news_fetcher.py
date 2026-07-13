import json
from urllib.parse import urlparse

from tavily import TavilyClient

from config import (
    TAVILY_API_KEY,
    SEARCH_QUERY,
    MAX_RESULTS,
    OUTPUT_FILE
)
from logger import logger
from utils import remove_duplicates, validate


class NewsFetcher:
    def __init__(self):
        self.client = TavilyClient(api_key=TAVILY_API_KEY)

    def fetch_news(self):
        """
        Fetch latest logistics and supply chain news using Tavily.
        """

        try:
            response = self.client.search(
                query=SEARCH_QUERY,
                topic="news",
                search_depth="advanced",
                max_results=MAX_RESULTS,
                include_answer=False,
                include_raw_content=True,
            )

            logger.info("News fetched successfully.")

            return response.get("results", [])

        except Exception as e:
            logger.error(f"Tavily API Error: {e}")
            return []

    def process_news(self):
        """
        Clean and structure the fetched news.
        """

        articles = self.fetch_news()
        processed = []

        for article in articles:

            url = article.get("url", "")

            item = {
                "title": article.get("title"),
                "url": url,
                "source": urlparse(url).netloc,
                "publication_date": article.get("published_date"),
                "content": article.get("raw_content") or article.get("content"),
                "score": article.get("score"),
            }

            if validate(item):
                processed.append(item)

        processed = remove_duplicates(processed)

        logger.info(f"{len(processed)} valid articles processed.")

        return processed

    def save_news(self, articles):
        """
        Save processed news to JSON.
        """

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(
                articles,
                file,
                indent=4,
                ensure_ascii=False,
            )

        logger.info(f"{len(articles)} articles saved to {OUTPUT_FILE}")

    def run(self):
        """
        Execute complete workflow.
        """

        articles = self.process_news()

        self.save_news(articles)

        return articles


def main():
    fetcher = NewsFetcher()

    news = fetcher.run()

    print(f"Fetched {len(news)} articles successfully.")

    if news:
        print("\nSample Article:\n")
        print(f"Title : {news[0]['title']}")
        print(f"Source: {news[0]['source']}")
        print(f"URL   : {news[0]['url']}")


if __name__ == "__main__":
    main()