import streamlit as st
import json
import os

st.set_page_config(
    page_title="Supplier Impact",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Supplier Impact Assessment")

OUTPUT_FILE = "output/classified_news.json"

if not os.path.exists(OUTPUT_FILE):
    st.warning("Please run the pipeline first.")
    st.stop()

with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
    reports = json.load(file)

st.success(f"Loaded {len(reports)} reports.")

for i, report in enumerate(reports, start=1):

    with st.expander(f"Article {i}: {report['Title']}"):

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Impact Level", report["Impact"])
            st.metric("Risk Score", report["Risk Score"])

        with col2:
            st.metric("Priority", report["Priority"])
            st.metric("Recovery Time", report["Estimated Recovery"])

        st.write("### Risk Assessment")
        st.info(report["Reason"])
        st.success(f"Report Status: {report['Status']}")

        entities = report.get("Entities", {})

        suppliers = entities.get("suppliers", [])

        if suppliers:
            st.write("### Affected Suppliers")

            for supplier in suppliers:
                st.write(f"• {supplier}")
        else:
            st.write("### Affected Suppliers")
            st.write("No supplier identified.")