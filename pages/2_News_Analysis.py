import streamlit as st
import json
import os

st.set_page_config(
    page_title="News Analysis",
    page_icon="📰",
    layout="wide"
)

st.title("📰 News Analysis")

st.markdown("### Classified Supply Chain Disruption News")

OUTPUT_FILE = "output/classified_news.json"

if not os.path.exists(OUTPUT_FILE):
    st.warning("No classified news found. Please run the pipeline first.")
    st.stop()

with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
    reports = json.load(file)

st.success(f"Loaded {len(reports)} reports.")

for i, report in enumerate(reports, start=1):
    with st.expander(f"📰 Article {i}: {report['Title']}"):

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Category", report["Category"])

        with col2:
            st.metric("Severity", report["Severity"])

        st.metric("Risk Score", report["Risk Score"])

        col3, col4 = st.columns(2)

        with col3:
            st.metric("Priority", report["Priority"])

        with col4:
            st.metric("Recommendations", report["Recommendation Count"])

        st.success(f"Status: {report['Status']}")

        st.write("### Reason")
        st.write(report["Reason"])

        st.write("### Primary Action")
        st.success(report["Primary Action"])

        st.write("### Recommendations")
        for rec in report["Recommendations"]:
            st.write("• " + rec)