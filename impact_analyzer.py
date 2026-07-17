"""
impact_analyzer.py
--------------------
Supplier Impact Analysis & Risk Scoring module.

Takes the output of classifier.py (category, severity) plus supplier
context (location, industry) and produces a risk score + impact level
for downstream recommendation modules.

Responsibilities covered here:
1. Analyze how disruptions affect suppliers.
2. Estimate disruption impact using category, severity, location, industry.
3. Design a supplier risk scoring mechanism.
4. Assign impact levels (Minimal, Moderate, Significant, Severe).
5. Handle uncertain or incomplete disruption information.
6. Improve consistency of impact scoring.
7. Format impact analysis for downstream recommendation modules.

Author: Mugdha Sangaonkar
Role: Supplier Impact Analysis & Risk Scoring Developer
"""

import re
from datetime import datetime, timezone

# =========================================================================
# FIXED SCORING TABLES — keep these consistent across every run
# (this is what "improves consistency of impact scoring" — Responsibility 6)
# =========================================================================

# Base weight per disruption category (0-10 scale, higher = more disruptive)
CATEGORY_WEIGHTS = {
    "Natural Disaster": 9,
    "Geopolitical Conflict": 8,
    "Labor Strike": 6,
    "Transportation Delay": 5,
    "Safe / No Risk": 0,
}

# Severity multiplier
SEVERITY_WEIGHTS = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4,
}

# Industry vulnerability factor — how sensitive an industry is to
# supply chain disruptions in general (0.5 - 1.5 range)
INDUSTRY_SENSITIVITY = {
    "electronics": 1.4,
    "automotive": 1.3,
    "pharmaceuticals": 1.3,
    "food": 1.2,
    "textiles": 1.0,
    "construction": 0.9,
    "retail": 0.8,
    "default": 1.0,
}

# High-risk regions get a location multiplier boost (extend as needed)
HIGH_RISK_REGIONS = {
    "middle east": 1.3,
    "red sea": 1.4,
    "south china sea": 1.2,
    "eastern europe": 1.2,
    "horn of africa": 1.3,
}
DEFAULT_LOCATION_MULTIPLIER = 1.0

IMPACT_LEVELS = ["Minimal", "Moderate", "Significant", "Severe"]


# =========================================================================
# STEP 1 — INPUT NORMALIZATION / INCOMPLETE DATA HANDLING
# =========================================================================
def normalize_input(disruption: dict, supplier: dict) -> dict:
    """
    Cleans and fills in missing fields from the classifier output and
    supplier profile. Flags the record as uncertain if key fields are
    missing so the score can be treated with caution downstream.
    """
    uncertain = False

    category = disruption.get("category")
    if category not in CATEGORY_WEIGHTS:
        uncertain = True
        category = "Transportation Delay"  # neutral mid-risk default

    severity = disruption.get("severity")
    if severity not in SEVERITY_WEIGHTS:
        uncertain = True
        severity = "Medium"  # neutral default

    location = (supplier.get("location") or "").strip().lower()
    if not location:
        uncertain = True

    industry = (supplier.get("industry") or "").strip().lower()
    if not industry or industry not in INDUSTRY_SENSITIVITY:
        if industry:  # given but not recognized
            uncertain = True
        industry = "default"

    return {
        "category": category,
        "severity": severity,
        "location": location,
        "industry": industry,
        "supplier_id": supplier.get("supplier_id", "unknown"),
        "uncertain_input": uncertain,
    }


# =========================================================================
# STEP 2 — RISK SCORING MECHANISM
# =========================================================================
def _location_multiplier(location: str) -> float:
    """Returns a multiplier if the supplier's location matches a known
    high-risk region (substring match keeps this flexible)."""
    for region, mult in HIGH_RISK_REGIONS.items():
        if region in location:
            return mult
    return DEFAULT_LOCATION_MULTIPLIER


def calculate_risk_score(normalized: dict) -> float:
    """
    Combines category weight, severity multiplier, location multiplier,
    and industry sensitivity into a single 0-100 risk score.

    Formula:
        raw = category_weight * severity_multiplier
        adjusted = raw * location_multiplier * industry_sensitivity
        score = min(adjusted scaled to 0-100, 100)
    """
    category_weight = CATEGORY_WEIGHTS[normalized["category"]]
    severity_mult = SEVERITY_WEIGHTS[normalized["severity"]]
    location_mult = _location_multiplier(normalized["location"])
    industry_mult = INDUSTRY_SENSITIVITY[normalized["industry"]]

    raw_score = category_weight * severity_mult  # max 9*4 = 36
    adjusted_score = raw_score * location_mult * industry_mult

    # Scale so max theoretical value (~36 * 1.4 * 1.4 ≈ 70.6) maps near 100
    scaled_score = (adjusted_score / 70.6) * 100
    return round(min(scaled_score, 100.0), 2)


# =========================================================================
# STEP 3 — IMPACT LEVEL MAPPING
# =========================================================================
def score_to_impact_level(score: float) -> str:
    """Maps a 0-100 risk score to a fixed impact level bucket."""
    if score < 20:
        return "Minimal"
    elif score < 45:
        return "Moderate"
    elif score < 70:
        return "Significant"
    else:
        return "Severe"


# =========================================================================
# STEP 4 — FORMAT OUTPUT for downstream recommendation module
# =========================================================================
def format_output(
    supplier_id: str,
    category: str,
    severity: str,
    risk_score: float,
    impact_level: str,
    uncertain_input: bool,
) -> dict:
    """
    Standard schema the recommendation module should expect.
    Keep keys stable — other modules depend on this shape.
    """
    return {
        "supplier_id": supplier_id,
        "disruption_category": category,
        "severity": severity,
        "risk_score": risk_score,
        "impact_level": impact_level,
        "flagged_uncertain": uncertain_input,
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
    }


# =========================================================================
# MAIN ENTRY POINT — single supplier analysis
# =========================================================================
def analyze_impact(disruption: dict, supplier: dict) -> dict:
    """
    disruption: dict like {"category": "...", "severity": "..."}
                (this is exactly the shape classifier.py's format_output() returns)
    supplier:   dict like {"supplier_id": "...", "location": "...", "industry": "..."}
    """
    normalized = normalize_input(disruption, supplier)
    risk_score = calculate_risk_score(normalized)
    impact_level = score_to_impact_level(risk_score)

    return format_output(
        supplier_id=normalized["supplier_id"],
        category=normalized["category"],
        severity=normalized["severity"],
        risk_score=risk_score,
        impact_level=impact_level,
        uncertain_input=normalized["uncertain_input"],
    )


# =========================================================================
# BATCH ANALYSIS — for pipeline use across many suppliers
# =========================================================================
def analyze_batch(disruption: dict, suppliers: list) -> list:
    """
    Analyze the same disruption event across multiple suppliers.
    suppliers: list of dicts like
        [{"supplier_id": "S1", "location": "...", "industry": "..."}, ...]
    """
    return [analyze_impact(disruption, supplier) for supplier in suppliers]


# =========================================================================
# QUICK MANUAL TEST (no external dependencies needed)
# =========================================================================
if __name__ == "__main__":
    # Simulated classifier.py output (Week 1 module's output feeds this)
    sample_disruption = {
        "category": "Natural Disaster",
        "severity": "High",
    }

    sample_suppliers = [
        {"supplier_id": "SUP-001", "location": "Red Sea region", "industry": "electronics"},
        {"supplier_id": "SUP-002", "location": "Ohio, USA", "industry": "retail"},
        {"supplier_id": "SUP-003", "location": "", "industry": ""},  # incomplete data test
    ]

    results = analyze_batch(sample_disruption, sample_suppliers)
    for r in results:
        print(r)