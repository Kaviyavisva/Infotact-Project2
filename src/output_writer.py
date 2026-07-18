"""
output_writer.py

Writes final supply chain risk reports to a JSON file.
"""

import json
import os

from src.config import OUTPUT_FILE


class OutputWriter:
    """
    Saves final reports to a JSON file.
    """

    def save_results(self, reports):

        # Ensure output directory exists
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(reports, file, indent=4)

        print(f"\nResults saved to: {OUTPUT_FILE}")