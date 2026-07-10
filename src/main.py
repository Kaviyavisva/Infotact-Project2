"""
main.py

Entry point for the Autonomous Supply Chain Disruption Monitoring Agent.
"""

from src.pipeline import SupplyChainPipeline


def main():
    """
    Run the complete Week 1 pipeline.
    """

    pipeline = SupplyChainPipeline()

    results = pipeline.run()

    print("\n========== SUPPLY CHAIN DISRUPTION REPORT ==========\n")

    if not results:
        print("No news articles found.")
        return

    for i, result in enumerate(results, start=1):
        print(f"Article {i}")
        print(f"Title     : {result.title}")
        print(f"Category  : {result.category}")
        print(f"Severity  : {result.severity}")
        print(f"Reason    : {result.reason}")
        print("-" * 70)


if __name__ == "__main__":
    main()