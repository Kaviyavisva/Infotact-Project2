"""
impact_analyzer.py

Analyzes disruption severity and assigns
risk score and impact level.
"""


class ImpactAnalyzer:

    def analyze(self, article):

        severity = article.severity.lower()
        category = article.category

        # ----------------------------
        # Base Risk Score from Severity
        # ----------------------------
        if severity == "critical":
            risk_score = 90
            impact = "Severe"

        elif severity == "high":
            risk_score = 70
            impact = "High"

        elif severity == "medium":
            risk_score = 45
            impact = "Moderate"

        else:
            risk_score = 20
            impact = "Low"

        # ----------------------------
        # Additional Risk based on Category
        # ----------------------------
        if category == "Natural Disaster":
            risk_score += 15

        elif category == "Geopolitical Conflict":
            risk_score += 10

        elif category == "Labor Strike":
            risk_score += 5

        elif category == "Transportation Delay":
            risk_score += 0

        # Maximum score should not exceed 100
        risk_score = min(risk_score, 100)

        return {

            "title": article.title,

            "category": article.category,

            "severity": article.severity,

            "reason": article.reason,

            "risk_score": risk_score,

            "impact": impact

        }