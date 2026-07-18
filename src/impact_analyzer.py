"""
impact_analyzer.py

Analyzes disruption severity and assigns
risk score and impact level.
"""


class ImpactAnalyzer:

    def analyze(self, article):

        severity = article.severity.lower()

        if severity == "critical":
            risk_score = 95
            impact = "Severe"

        elif severity == "high":
            risk_score = 75
            impact = "High"

        elif severity == "medium":
            risk_score = 50
            impact = "Moderate"

        else:
            risk_score = 20
            impact = "Low"

        return {

            "title": article.title,

            "category": article.category,

            "severity": article.severity,

            "reason": article.reason,

            "risk_score": risk_score,

            "impact": impact

        }