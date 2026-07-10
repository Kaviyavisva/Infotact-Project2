"""
output_writer.py

Writes classified news articles to a JSON file.
"""

import json
import os

from src.config import OUTPUT_FILE


class OutputWriter:
    """
    Saves classified news articles to a JSON file.
    """

    def save_results(self, classified_articles):
        """
        Save classified articles.

        Args:
            classified_articles (list): List of ClassifiedArticle objects.
        """

        # Ensure output directory exists
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

        data = []

        for article in classified_articles:
            data.append({
                "title": article.title,
                "category": article.category,
                "severity": article.severity,
                "reason": article.reason
            })

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"\nResults saved to: {OUTPUT_FILE}")