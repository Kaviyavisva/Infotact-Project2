"""
config.py

Central configuration file for the Supply Chain Disruption Monitoring project.
Modify project settings here instead of hardcoding values.
"""

# Search Configuration
SEARCH_QUERY = (
    "recent supply chain disruptions OR port strike "
    "OR logistics disruption OR shipping delay"
)

MAX_RESULTS = 5

# Classification Categories
CATEGORIES = [
    "Natural Disaster",
    "Labor Strike",
    "Geopolitical Conflict",
    "Transportation Delay",
    "Safe"
]

# Severity Levels
SEVERITY_LEVELS = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

# Output File
OUTPUT_FILE = "output/classified_news.json"