"""
recommendation_engine.py

Generates intelligent mitigation recommendations
based on disruption category, severity,
risk score and impact level.
"""


class RecommendationEngine:

    def __init__(self):

        self.rules = {

            "Transportation Delay": [
                "Use alternate transportation routes.",
                "Notify logistics partners immediately.",
                "Track shipment status every 2 hours.",
                "Increase inventory buffer at destination."
            ],

            "Natural Disaster": [
                "Shift sourcing to alternate suppliers.",
                "Increase safety stock.",
                "Delay non-critical shipments.",
                "Monitor weather forecasts continuously."
            ],

            "Labor Strike": [
                "Redirect cargo through alternate ports.",
                "Coordinate with third-party logistics providers.",
                "Communicate delivery delays to customers.",
                "Increase warehouse inventory."
            ],

            "Geopolitical Conflict": [
                "Suspend shipments through affected regions.",
                "Source materials from alternate countries.",
                "Review customs and trade regulations.",
                "Activate emergency procurement plan."
            ]
        }

    def _calculate_priority(self, risk_score):

        if risk_score >= 85:
            return "Critical"

        elif risk_score >= 70:
            return "High"

        elif risk_score >= 40:
            return "Medium"

        else:
            return "Low"

    def generate(self, impact_data):

        category = impact_data["category"]

        risk_score = impact_data["risk_score"]

        recommendations = self.rules.get(
            category,
            ["Continue monitoring the situation."]
        )

        # Recommendation details
        impact_data["recommendations"] = recommendations

        impact_data["priority"] = self._calculate_priority(risk_score)

        impact_data["recommended_action"] = recommendations[0]

        impact_data["estimated_recovery"] = {

            "Critical": "5-7 Days",
            "High": "3-5 Days",
            "Medium": "1-2 Days",
            "Low": "Within 24 Hours"

        }[impact_data["priority"]]

        # Preserve entities if present
        if "entities" not in impact_data:
            impact_data["entities"] = {}

        return impact_data