import streamlit as st
import pandas as pd
import json
import time
from src.pipeline import SupplyChainPipeline

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Autonomous Supply Chain Disruption Monitor",
    page_icon="🚛",
    layout="wide"
)

# ------------------------------
# Header
# ------------------------------
st.title("🚛 Autonomous Supply Chain Disruption Monitor")

st.caption("AI-powered Logistics Risk Intelligence Platform")

st.markdown("""
### Welcome!

This dashboard provides real-time monitoring of global logistics and supply chain disruptions.

The platform automatically:

- 📰 Collects the latest logistics news
- 🤖 Classifies disruption risks using AI
- 📍 Identifies affected regions and suppliers
- 📈 Estimates supplier impact
- 💡 Generates mitigation recommendations
- 📄 Produces comprehensive risk reports
""")

st.success("✅ Week 3 Dashboard Integration Completed")

st.divider()

# ------------------------------
# Run Pipeline
# ------------------------------
st.subheader("🚀 Run Supply Chain Pipeline")

if st.button("▶ Run Supply Chain Pipeline"):

    with st.spinner("Running Supply Chain Pipeline..."):
        start_time = time.time()

        pipeline = SupplyChainPipeline()
        reports = pipeline.run()

        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

    st.success(
        f"✅ Pipeline completed successfully! Generated {len(reports)} reports."
    )

    st.info(f"⏱ Pipeline Execution Time: {execution_time} seconds")

    # ------------------------------
    # Download JSON Report
    # ------------------------------
    json_data = json.dumps(reports, indent=4)

    st.download_button(
        label="📥 Download JSON Report",
        data=json_data,
        file_name="classified_news.json",
        mime="application/json"
    )

    st.divider()

    # ------------------------------
    # Pipeline Execution Status
    # ------------------------------
    st.subheader("⚙️ Pipeline Execution Status")

    status = {
        "📰 News Collection": "✅ Completed",
        "🧹 Data Processing": "✅ Completed",
        "🤖 Risk Classification": "✅ Completed",
        "📍 Entity Extraction": "✅ Completed",
        "📈 Supplier Impact Analysis": "✅ Completed",
        "💡 Recommendation Generation": "✅ Completed",
        "📄 Report Generation": "✅ Completed",
        "💾 Results Saved": "✅ Completed"
    }

    for stage, result in status.items():
        st.write(f"**{stage}** — {result}")

    st.divider()

    # ------------------------------
    # Dashboard Summary
    # ------------------------------
    st.subheader("📊 Dashboard Summary")

    total_articles = len(reports)

    high = sum(
        1 for r in reports
        if r["Severity"] == "High"
    )

    medium = sum(
        1 for r in reports
        if r["Severity"] == "Medium"
    )

    low = sum(
        1 for r in reports
        if r["Severity"] == "Low"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Articles", total_articles)
    col2.metric("High Risk", high)
    col3.metric("Medium Risk", medium)
    col4.metric("Low Risk", low)

    highest_score = max(report["Risk Score"] for report in reports)

    latest_run = reports[0]["generated_at"]

    col5, col6 = st.columns(2)

    col5.metric("Highest Risk Score", highest_score)

    col6.metric("Latest Run", latest_run)

    st.divider()

    # ------------------------------
    # Risk Distribution
    # ------------------------------
    st.subheader("📈 Risk Distribution")

    chart_df = pd.DataFrame({
        "Severity": ["High", "Medium", "Low"],
        "Articles": [high, medium, low]
    })

    st.bar_chart(chart_df.set_index("Severity"))

    st.divider()

    # ------------------------------
    # Category Distribution
    # ------------------------------
    st.subheader("📊 Disruption Categories")

    category_counts = {}

    for report in reports:

        category = report["Category"]

        category_counts[category] = category_counts.get(category, 0) + 1

    category_df = pd.DataFrame(
        {
            "Category": category_counts.keys(),
            "Articles": category_counts.values()
        }
    )

    st.bar_chart(category_df.set_index("Category"))

    st.divider()

    # ------------------------------
    # Reports
    # ------------------------------
    st.header("📋 Supply Chain Disruption Reports")

    selected_severity = st.selectbox(
        "Filter by Severity",
        ["All", "High", "Medium", "Low"]
    )

    if selected_severity == "All":
        filtered_reports = reports
    else:
        filtered_reports = [
            report for report in reports
            if report["Severity"] == selected_severity
        ]

    if len(filtered_reports) == 0:
        st.warning("No reports found for the selected severity.")

    for i, report in enumerate(filtered_reports, start=1):
        with st.expander(f"📄 Article {i}: {report['Title']}"):

            st.subheader("📄 Report Summary")

            st.write("**Category:**", report["Category"])
            st.write("**Severity:**", report["Severity"])

            risk_score = report["Risk Score"]

            st.write("**Risk Score:**", risk_score)

            st.progress(risk_score / 100)

            st.caption(f"{risk_score}% Risk Level")

            st.write("**Impact:**", report["Impact"])
            st.write("**Priority:**", report["Priority"])
            st.write("**Estimated Recovery:**", report["Estimated Recovery"])
            st.write("**Reason:**", report["Reason"])

            st.success(f"🚀 Primary Action: {report['Primary Action']}")

            st.subheader("💡 Recommendations")

            for recommendation in report["Recommendations"]:
                st.write(f"• {recommendation}")

            st.subheader("📍 Extracted Entities")

            entities = report.get("Entities", {})

            has_entities = False

            for key, values in entities.items():
                if values:
                    has_entities = True
                    st.write(
                        f"**{key.replace('_', ' ').title()}** : "
                        f"{', '.join(values)}"
                    )

            if not has_entities:
                st.info("No entities detected for this article.")

            st.divider()

# ------------------------------
# Project Status
# ------------------------------
st.divider()

st.subheader("📊 Project Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Sprint", "Week 3")

with col2:
    st.metric("Overall Progress", "75%")

with col3:
    st.metric("Application Status", "🟢 Active")

# ------------------------------
# Development Team
# ------------------------------
st.divider()

st.subheader("👥 Development Team")

team_data = {
    "Kaviyashri Viswanathan": "Dashboard Integration Coordinator & System Validation",
    "Abhishek Sangani": "Entity Extraction",
    "Mugdha Sangaonkar": "Supplier Impact Analysis",
    "Adhiraj Singh Shekhawat": "Recommendation Engine & Report Generation"
}

for member, role in team_data.items():
    st.write(f"**{member}** — {role}")

# ------------------------------
# Project Highlights
# ------------------------------
st.divider()

st.subheader("⭐ Project Highlights")

col1, col2 = st.columns(2)

with col1:
    st.success("✅ Automated News Collection")
    st.success("✅ AI Risk Classification")
    st.success("✅ Interactive Dashboard")

with col2:
    st.info("📍 Entity Extraction")
    st.info("📈 Supplier Impact Analysis")
    st.info("💡 Recommendation Generation")

# ------------------------------
# System Workflow
# ------------------------------
st.divider()

st.subheader("🔄 System Workflow")

st.code(
"""
Latest Logistics News
        │
        ▼
News Fetcher
        │
        ▼
Data Processor
        │
        ▼
Risk Classifier
        │
        ▼
Entity Extraction
        │
        ▼
Supplier Impact Analysis
        │
        ▼
Recommendation Engine
        │
        ▼
Risk Report Generation
        │
        ▼
Dashboard Visualization
""",
language="text"
)

# ------------------------------
# Footer
# ------------------------------
st.divider()

st.caption(
    "🚛 Autonomous Supply Chain Disruption Monitor | "
    "InfoTact Solutions Internship | Week 3 Dashboard Integration"
)