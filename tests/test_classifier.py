"""
Test script for classifier.py
"""

from src.news_fetcher import NewsFetcher
from src.data_processor import DataProcessor
from src.classifier import NewsClassifier


def main():
    fetcher = NewsFetcher()
    processor = DataProcessor()
    classifier = NewsClassifier()

    articles = fetcher.fetch_news()
    processed_articles = processor.process_articles(articles)

    print("\nClassified News Articles:\n")

    for i, article in enumerate(processed_articles, start=1):
        result = classifier.classify_article(article)

        print(f"Article {i}")
        print(f"Title     : {result.title}")
        print(f"Category  : {result.category}")
        print(f"Severity  : {result.severity}")
        print(f"Reason    : {result.reason}")
        print("-" * 60)


if __name__ == "__main__":
    main()