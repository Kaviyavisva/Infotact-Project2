"""
Test script for news_fetcher.py
"""

from src.news_fetcher import NewsFetcher


def main():
    fetcher = NewsFetcher()

    articles = fetcher.fetch_news()

    if not articles:
        print("No articles found.")
        return

    print(f"\nRetrieved {len(articles)} articles:\n")

    for i, article in enumerate(articles, start=1):
        print(f"Article {i}")
        print(f"Title   : {article['title']}")
        print(f"URL     : {article['url']}")
        print(f"Snippet : {article['snippet']}")
        print("-" * 60)


if __name__ == "__main__":
    main()