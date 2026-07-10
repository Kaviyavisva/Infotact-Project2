"""
Test script for data_processor.py
"""

from src.news_fetcher import NewsFetcher
from src.data_processor import DataProcessor


def main():
    fetcher = NewsFetcher()
    processor = DataProcessor()

    articles = fetcher.fetch_news()
    processed_articles = processor.process_articles(articles)

    print(f"\nProcessed {len(processed_articles)} articles:\n")

    for i, article in enumerate(processed_articles, start=1):
        print(f"Article {i}")
        print(f"Title   : {article.title}")
        print(f"URL     : {article.url}")
        print(f"Snippet : {article.snippet}")
        print("-" * 60)


if __name__ == "__main__":
    main()