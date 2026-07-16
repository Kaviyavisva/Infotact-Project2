import streamlit as st

st.set_page_config(
    page_title="Final Report",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Final Risk Report")

st.markdown("""
## Module Overview

This module generates the final supply chain disruption report.

### Report Contents

- 📰 Classified News
- 📍 Extracted Entities
- 📈 Supplier Impact
- 💡 Mitigation Recommendations
- 📊 Risk Summary

Reports will be available in structured JSON format and will support future dashboard integration.
""")

st.info("🚧 Waiting for Week 2 Integration")