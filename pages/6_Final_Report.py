import streamlit as st
import json
import os

st.set_page_config(
    page_title="Final Report",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Final Supply Chain Risk Report")

OUTPUT_FILE = "output/classified_news.json"

if not os.path.exists(OUTPUT_FILE):
    st.warning("Please run the pipeline first.")
    st.stop()

with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
    reports = json.load(file)

st.success(f"{len(reports)} reports generated.")

for i, report in enumerate(reports, start=1):

    with st.expander(f"Report {i}: {report['Title']}", expanded=(i == 1)):

        st.markdown("## Incident Summary")

        st.write(f"**Generated At:** {report['generated_at']}")
        st.write(f"**Title:** {report['Title']}")
        st.write(f"**Category:** {report['Category']}")
        st.write(f"**Severity:** {report['Severity']}")
        st.write(f"**Impact:** {report['Impact']}")
        st.write(f"**Risk Score:** {report['Risk Score']}")
        st.write(f"**Priority:** {report['Priority']}")
        st.write(f"**Estimated Recovery:** {report['Estimated Recovery']}")

        st.markdown("---")

        st.subheader("Reason")
        st.info(report["Reason"])

        st.subheader("Primary Action")
        st.success(report["Primary Action"])

        st.subheader("Recommendations")

        for rec in report["Recommendations"]:
            st.write(f"• {rec}")

        st.markdown("---")

        st.subheader("Extracted Entities")

        entities = report.get("Entities", {})

        if entities:
            for key, values in entities.items():
                if values:
                    st.write(f"**{key.replace('_', ' ').title()}**")
                    for value in values:
                        st.write(f"- {value}")

        st.download_button(
            label="📥 Download Report",
            data=json.dumps(report, indent=4),
            file_name=f"report_{i}.json",
            mime="application/json",
            key=f"download_{i}"
        )