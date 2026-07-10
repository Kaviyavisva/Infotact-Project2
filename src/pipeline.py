"""
pipeline.py

Integrates the complete Week 1 workflow.
"""

from src.news_fetcher import NewsFetcher
from src.data_processor import DataProcessor
from src.classifier import NewsClassifier
from src.output_writer import OutputWriter


class SupplyChainPipeline:
    """
    Complete Week 1 Supply Chain Disruption Monitoring Pipeline.
    """

    def __init__(self):
        self.fetcher = NewsFetcher()
        self.processor = DataProcessor()
        self.classifier = NewsClassifier()
        self.output_writer = OutputWriter()

    def run(self):
        """
        Execute the complete pipeline.

        Returns:
            list: Classified news articles.
        """

        # Step 1: Fetch news
        articles = self.fetcher.fetch_news()

        # Step 2: Process news
        processed_articles = self.processor.process_articles(articles)

        # Step 3: Classify news
        classified_articles = []

        for article in processed_articles:
            result = self.classifier.classify_article(article)
            classified_articles.append(result)

        # Step 4: Save results
        self.output_writer.save_results(classified_articles)

        return classified_articles