"""
report_generator.py

Generates a structured supply chain
risk assessment report.
"""

from datetime import datetime


class ReportGenerator:

    def generate(self, data):

        report = {

            "generated_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

            "Title": data["title"],

            "Category": data["category"],

            "Severity": data["severity"],

            "Risk Score": data["risk_score"],

            "Impact": data["impact"],

            "Priority": data["priority"],

            "Estimated Recovery": data["estimated_recovery"],

            "Reason": data["reason"],

            "Primary Action": data["recommended_action"],

            "Recommendations": data["recommendations"],

            # Entity information
            "Entities": data.get("entities", {})

        }

        return report

    def display(self, report):

        print("=" * 65)

        print("        SUPPLY CHAIN DISRUPTION REPORT")

        print("=" * 65)

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

        print("\nRecommended Actions")

        print("-" * 65)

        for i, rec in enumerate(report["Recommendations"], start=1):
            print(f"{i}. {rec}")

        entities = report.get("Entities", {})

        if entities:

            print("\nExtracted Entities")

            print("-" * 65)

            for key, values in entities.items():

                if values:

                    print(f"{key.title():20}: {', '.join(values)}")

        print("=" * 65)