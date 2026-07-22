"""
4_Supplier_Impact.py
--------------------
Supplier Impact Analysis Dashboard.

Displays:
- Supplier Risk Score
- Impact Level
- Supplier Risk
- Severity
- Disruption Category
- Supplier Information
- Uncertain Data Flag
- Analysis Timestamp

Uses:
    src/impact_analyzer.py

Author: Mugdha Sangaonkar
Role: Risk Analytics & Supplier Impact Dashboard Developer
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================================
# PROJECT ROOT SETUP
# =========================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# Import Week 2 impact analysis module
from src.impact_analyzer import analyze_impact


# =========================================================================
# PAGE CONFIGURATION
# =========================================================================

st.set_page_config(
    page_title="Supplier Impact Analysis",
    page_icon="📊",
    layout="wide",
)


# =========================================================================
# HELPER FUNCTION — SUPPLIER RISK
# =========================================================================

def get_supplier_risk(risk_score):
    """
    Convert risk score into supplier risk category.

    Risk Score:
    0-19   -> Low
    20-44  -> Moderate
    45-69  -> High
    70-100 -> Critical
    """

    if risk_score < 20:
        return "Low"

    elif risk_score < 45:
        return "Moderate"

    elif risk_score < 70:
        return "High"

    else:
        return "Critical"


# =========================================================================
# HELPER FUNCTION — RISK DESCRIPTION
# =========================================================================

def get_risk_description(supplier_risk):

    descriptions = {
        "Low": "Supplier impact is currently low. Normal monitoring is recommended.",

        "Moderate": (
            "Supplier may experience some disruption. "
            "Continue monitoring the situation."
        ),

        "High": (
            "Supplier has a high disruption risk. "
            "Consider contingency planning and alternative suppliers."
        ),

        "Critical": (
            "Supplier is at critical risk. "
            "Immediate mitigation and alternative sourcing may be required."
        ),
    }

    return descriptions.get(
        supplier_risk,
        "Risk information is unavailable."
    )


# =========================================================================
# PAGE TITLE
# =========================================================================

st.title("📊 Supplier Impact Analysis Dashboard")

st.write(
    "Analyze how disruption events may affect suppliers based on "
    "disruption category, severity, geographic location, and industry."
)


# =========================================================================
# SIDEBAR — DISRUPTION INPUT
# =========================================================================

st.sidebar.header("🔍 Disruption Information")


disruption_category = st.sidebar.selectbox(
    "Disruption Category",
    [
        "Natural Disaster",
        "Geopolitical Conflict",
        "Labor Strike",
        "Transportation Delay",
        "Safe / No Risk",
    ],
)


severity = st.sidebar.selectbox(
    "Severity Level",
    [
        "Low",
        "Medium",
        "High",
        "Critical",
    ],
)


# =========================================================================
# SIDEBAR — SUPPLIER INPUT
# =========================================================================

st.sidebar.header("🏭 Supplier Information")


supplier_id = st.sidebar.text_input(
    "Supplier ID",
    value="SUP-001",
    placeholder="Example: SUP-001",
)


location = st.sidebar.text_input(
    "Supplier Location",
    placeholder="Example: Red Sea region",
)


industry = st.sidebar.selectbox(
    "Supplier Industry",
    [
        "",
        "electronics",
        "automotive",
        "pharmaceuticals",
        "food",
        "textiles",
        "construction",
        "retail",
    ],
)


# =========================================================================
# ANALYZE BUTTON
# =========================================================================

analyze_button = st.sidebar.button(
    "🚀 Analyze Supplier Impact",
    use_container_width=True,
)


# =========================================================================
# RUN ANALYSIS
# =========================================================================

if analyze_button:

    # -------------------------------------------------------------
    # Prepare disruption input
    # Compatible with analyze_impact() from impact_analyzer.py
    # -------------------------------------------------------------

    disruption = {
        "category": disruption_category,
        "severity": severity,
    }


    # -------------------------------------------------------------
    # Prepare supplier input
    # -------------------------------------------------------------

    supplier = {
        "supplier_id": supplier_id,
        "location": location,
        "industry": industry,
    }


    # -------------------------------------------------------------
    # Validate basic supplier ID
    # -------------------------------------------------------------

    if not supplier_id.strip():

        st.warning(
            "Supplier ID is missing. The analysis will use 'unknown' "
            "as the supplier ID."
        )


    # -------------------------------------------------------------
    # Call Week 2 Impact Analyzer
    # -------------------------------------------------------------

    result = analyze_impact(
        disruption=disruption,
        supplier=supplier,
    )


    # =========================================================================
    # EXTRACT RESULTS
    # =========================================================================

    risk_score = result["risk_score"]

    impact_level = result["impact_level"]

    supplier_risk = get_supplier_risk(
        risk_score
    )

    result_severity = result["severity"]

    result_category = result["disruption_category"]

    result_supplier_id = result["supplier_id"]

    uncertain = result["flagged_uncertain"]

    analyzed_at = result["analyzed_at"]


    # =========================================================================
    # MAIN DASHBOARD
    # =========================================================================

    st.success(
        "Supplier impact analysis completed successfully."
    )


    st.subheader("📈 Supplier Risk Overview")


    # =========================================================================
    # METRICS
    # =========================================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            label="Risk Score",
            value=f"{risk_score}/100",
        )


    with col2:

        st.metric(
            label="Impact Level",
            value=impact_level,
        )


    with col3:

        st.metric(
            label="Supplier Risk",
            value=supplier_risk,
        )


    with col4:

        st.metric(
            label="Severity",
            value=result_severity,
        )


    st.divider()


    # =========================================================================
    # RISK SCORE VISUALIZATION
    # =========================================================================

    st.subheader("🎯 Risk Score Visualization")


    st.progress(
        min(max(int(risk_score), 0), 100)
    )


    st.write(
        f"**Current Risk Score:** {risk_score}/100"
    )


    # =========================================================================
    # RISK ANALYSIS DESCRIPTION
    # =========================================================================

    st.subheader("⚠️ Supplier Risk Assessment")


    st.info(
        get_risk_description(
            supplier_risk
        )
    )


    # =========================================================================
    # SUPPLIER DETAILS
    # =========================================================================

    st.subheader("🏭 Supplier & Disruption Details")


    details = pd.DataFrame(
        {
            "Field": [
                "Supplier ID",
                "Supplier Location",
                "Supplier Industry",
                "Disruption Category",
                "Severity",
                "Risk Score",
                "Impact Level",
                "Supplier Risk",
            ],

            "Value": [
                result_supplier_id,
                location if location else "Unknown",
                industry if industry else "Unknown",
                result_category,
                result_severity,
                risk_score,
                impact_level,
                supplier_risk,
            ],
        }
    )


    st.dataframe(
        details,
        use_container_width=True,
        hide_index=True,
    )


    # =========================================================================
    # ANALYTICS CHART
    # =========================================================================

    st.subheader("📊 Risk Analytics")


    chart_data = pd.DataFrame(
        {
            "Metric": [
                "Risk Score",
                "Impact Level Score",
                "Supplier Risk Score",
            ],

            "Score": [
                risk_score,

                # Convert impact level into visualization score
                {
                    "Minimal": 20,
                    "Moderate": 45,
                    "Significant": 70,
                    "Severe": 100,
                }.get(
                    impact_level,
                    0,
                ),

                # Convert supplier risk into visualization score
                {
                    "Low": 20,
                    "Moderate": 45,
                    "High": 70,
                    "Critical": 100,
                }.get(
                    supplier_risk,
                    0,
                ),
            ],
        }
    )


    st.bar_chart(
        chart_data.set_index("Metric")
    )


    # =========================================================================
    # CLASSIFICATION INFORMATION
    # =========================================================================

    st.subheader("📋 Analysis Summary")


    summary_col1, summary_col2 = st.columns(2)


    with summary_col1:

        st.write(
            f"**Disruption Category:** {result_category}"
        )

        st.write(
            f"**Severity:** {result_severity}"
        )

        st.write(
            f"**Impact Level:** {impact_level}"
        )


    with summary_col2:

        st.write(
            f"**Risk Score:** {risk_score}/100"
        )

        st.write(
            f"**Supplier Risk:** {supplier_risk}"
        )

        st.write(
            f"**Supplier ID:** {result_supplier_id}"
        )


    # =========================================================================
    # DATA QUALITY VALIDATION
    # =========================================================================

    st.subheader("✅ Risk Assessment Validation")


    if uncertain:

        st.warning(
            "The analysis contains incomplete or uncertain supplier "
            "information. The risk score should be interpreted with caution."
        )

    else:

        st.success(
            "All required disruption and supplier information was available. "
            "Risk assessment passed the input consistency check."
        )


    # =========================================================================
    # ANALYSIS TIMESTAMP
    # =========================================================================

    st.caption(
        f"Analysis completed at: {analyzed_at}"
    )


# =========================================================================
# INITIAL PAGE MESSAGE
# =========================================================================

else:

    st.info(
        "👈 Enter the disruption and supplier information in the sidebar, "
        "then click **Analyze Supplier Impact** to view the risk analysis."
    )


    st.markdown(
        """
        ### Dashboard Features

        This dashboard provides:

        - 📊 **Risk Score** — 0 to 100 supplier risk score
        - 🚦 **Impact Level** — Minimal, Moderate, Significant, or Severe
        - 🏭 **Supplier Risk** — Low, Moderate, High, or Critical
        - ⚠️ **Severity** — Low, Medium, High, or Critical
        - 🌍 **Geographic Location** — Supplier location
        - 🏢 **Industry** — Supplier industry sensitivity
        - ✅ **Validation** — Identifies incomplete or uncertain data
        - 📈 **Risk Analytics** — Visual representation of supplier risk
        """
    )
