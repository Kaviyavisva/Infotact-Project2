"""
pipeline.py

Complete Supply Chain Disruption Monitoring Pipeline
with Impact Analysis, Recommendations and Report Generation.
"""

from src.news_fetcher import NewsFetcher
from src.data_processor import DataProcessor
from src.classifier import NewsClassifier
from src.entity_extractor import extract_entities
from src.impact_analyzer import ImpactAnalyzer
from src.recommendation_engine import RecommendationEngine
from src.report_generator import ReportGenerator
from src.output_writer import OutputWriter


class SupplyChainPipeline:

    def __init__(self):

        self.fetcher = NewsFetcher()
        self.processor = DataProcessor()
        self.classifier = NewsClassifier()
        self.impact_analyzer = ImpactAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        self.report_generator = ReportGenerator()
        self.output_writer = OutputWriter()

    def run(self):

        # Step 1
        articles = self.fetcher.fetch_news()

        # Step 2
        processed_articles = self.processor.process_articles(articles)

        final_reports = []

        # Step 3 onwards
        for article in processed_articles:

            # Classify the article
            classified = self.classifier.classify_article(article)

            # Extract entities
            entity_input = {
                "title": classified.title,
                "content": "",
                "category": classified.category,
                "severity": classified.severity,
                "reason": classified.reason
            }

            entities = extract_entities(entity_input)

            # Analyze impact
            impact = self.impact_analyzer.analyze(classified)

            # Attach extracted entities
            impact["entities"] = entities

            # Generate recommendations
            recommendation = self.recommendation_engine.generate(impact)

            # Generate report
            report = self.report_generator.generate(recommendation)

            final_reports.append(report)

        # Save reports
        self.output_writer.save_results(final_reports)

        return final_reports