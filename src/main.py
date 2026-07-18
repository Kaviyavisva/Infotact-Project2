"""
main.py

Entry point for the Autonomous Supply Chain
Disruption Monitoring Agent.
"""

from src.pipeline import SupplyChainPipeline


def main():

    pipeline = SupplyChainPipeline()

    reports = pipeline.run()

    print("\n========== SUPPLY CHAIN DISRUPTION REPORT ==========\n")

    if not reports:
        print("No reports generated.")
        return

    for i, report in enumerate(reports, start=1):

        print(f"Article {i}")

        print(f"Generated At       : {report['generated_at']}")
        print(f"Title              : {report['Title']}")
        print(f"Category           : {report['Category']}")
        print(f"Severity           : {report['Severity']}")
        print(f"Risk Score         : {report['Risk Score']}")
        print(f"Impact             : {report['Impact']}")
        print(f"Priority           : {report['Priority']}")
        print(f"Recovery Time      : {report['Estimated Recovery']}")
        print(f"Primary Action     : {report['Primary Action']}")
        print(f"Reason             : {report['Reason']}")

        print("\nRecommendations:")

        for rec in report["Recommendations"]:
            print(f"  • {rec}")

        entities = report.get("Entities", {})

        if entities:

            print("\nExtracted Entities:")

            for key, values in entities.items():

                if values:
                    print(f"  {key.title():18}: {', '.join(values)}")

        print("-" * 70)


if __name__ == "__main__":
    main()