import streamlit as st

st.set_page_config(
    page_title="Supplier Impact",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Supplier Impact Analysis")

st.markdown("""
## Module Overview

This module evaluates how disruptions affect suppliers.

### Analysis Parameters

- Disruption Category
- Severity Level
- Geographic Location
- Industry Affected

### Impact Levels

- 🟢 Minimal
- 🟡 Moderate
- 🟠 Significant
- 🔴 Severe
""")

st.info("🚧 Waiting for Week 2 Integration")