"""
classifier.py

Rule-based classifier for supply chain disruption news.
"""

from src.models import NewsArticle, ClassifiedArticle


class NewsClassifier:
    """
    Classifies news articles into disruption categories.
    """

    def classify_article(self, article: NewsArticle) -> ClassifiedArticle:

        text = f"{article.title} {article.snippet}".lower()

        category = "Safe"
        severity = "Low"
        reason = "No major supply chain disruption detected."

        if any(word in text for word in ["flood", "earthquake", "cyclone", "storm", "hurricane"]):
            category = "Natural Disaster"
            severity = "Critical"
            reason = "Natural disaster may disrupt logistics and transportation."

        elif any(word in text for word in ["strike", "workers", "union", "dockworkers"]):
            category = "Labor Strike"
            severity = "High"
            reason = "Labor strike may interrupt supply chain operations."

        elif any(word in text for word in ["war", "conflict", "sanction", "geopolitical"]):
            category = "Geopolitical Conflict"
            severity = "Critical"
            reason = "Geopolitical issues may impact global trade."

        elif any(word in text for word in ["delay", "shipping", "port", "freight"]):
            category = "Transportation Delay"
            severity = "Medium"
            reason = "Transportation disruptions may delay deliveries."

        return ClassifiedArticle(
            title=article.title,
            category=category,
            severity=severity,
            reason=reason
        )