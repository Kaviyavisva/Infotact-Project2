import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Welcome")

st.markdown("""
## Autonomous Supply Chain Disruption Monitoring Agent

Welcome to the AI-powered Supply Chain Risk Monitoring Dashboard.

This application monitors global logistics news, detects supply chain disruptions,
analyzes supplier impact, and provides mitigation recommendations.

### Project Modules

- 📰 News Analysis
- 📍 Entity Extraction
- 📈 Supplier Impact Analysis
- 💡 Mitigation Recommendation
- 📄 Final Risk Report

Use the navigation panel on the left to explore each module.
""")

st.success("Project Status: 🚧 Week 2 Development in Progress")