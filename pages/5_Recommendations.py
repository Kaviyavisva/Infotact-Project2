import streamlit as st
import json
import os

st.set_page_config(
    page_title="Recommendations",
    page_icon="💡",
    layout="wide"
)

st.title("💡 AI Mitigation Recommendations")

OUTPUT_FILE = "output/classified_news.json"

if not os.path.exists(OUTPUT_FILE):
    st.warning("Please run the pipeline first.")
    st.stop()

with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
    reports = json.load(file)

st.success(f"Loaded {len(reports)} reports.")

for i, report in enumerate(reports, start=1):

    with st.expander(f"Article {i}: {report['Title']}"):

        st.subheader("Primary Recommendation")

        st.success(report["Primary Action"])

        st.subheader("Priority")

        priority = report["Priority"]

        if priority == "Critical":
            st.error(priority)

        elif priority == "High":
            st.warning(priority)

        elif priority == "Medium":
            st.info(priority)

        else:
            st.success(priority)

        st.subheader("Recommended Actions")

        for j, rec in enumerate(report["Recommendations"], start=1):
            st.write(f"{j}. {rec}")

        st.subheader("Estimated Recovery")

        st.metric("Recovery Time", report["Estimated Recovery"])