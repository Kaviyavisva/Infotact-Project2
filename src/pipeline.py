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

        # -----------------------------
        # Step 1 : Fetch News
        # -----------------------------
        try:
            articles = self.fetcher.fetch_news()
            print("✅ News Fetcher Completed")
        except Exception as e:
            print(f"❌ News Fetcher Failed: {e}")
            return []

        # -----------------------------
        # Step 2 : Process News
        # -----------------------------
        try:
            processed_articles = self.processor.process_articles(articles)
            print("✅ Data Processor Completed")
        except Exception as e:
            print(f"❌ Data Processor Failed: {e}")
            return []

        final_reports = []

        # -----------------------------
        # Step 3 onwards
        # -----------------------------
        for article in processed_articles:

            try:

                # Risk Classification
                classified = self.classifier.classify_article(article)
                print("✅ Risk Classification Completed")

                # Entity Extraction
                entity_input = {
                    "title": article.title,
                    "content": article.snippet,
                    "category": classified.category,
                    "severity": classified.severity,
                    "reason": classified.reason
                }

                entities = extract_entities(entity_input)
                print("✅ Entity Extraction Completed")

                # Supplier Impact Analysis
                impact = self.impact_analyzer.analyze(classified)
                print("✅ Supplier Impact Analysis Completed")

                # Attach entities
                impact["entities"] = entities

                # Recommendation Engine
                recommendation = self.recommendation_engine.generate(impact)
                print("✅ Recommendation Engine Completed")

                # Attach entities again
                recommendation["entities"] = entities

                # Report Generation
                report = self.report_generator.generate(recommendation)
                print("✅ Report Generation Completed")

                final_reports.append(report)

            except Exception as e:
                print(f"❌ Error processing article: {article.title}")
                print(f"Reason: {e}")
                continue

        # -----------------------------
        # Save Results
        # -----------------------------
        try:
            self.output_writer.save_results(final_reports)
            print("✅ Results Saved Successfully")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")

        return final_reports