import streamlit as st

st.set_page_config(
    page_title="News Analysis",
    page_icon="📰",
    layout="wide"
)

st.title("📰 News Analysis")

st.markdown("""
## Module Overview

This module performs the complete Week 1 pipeline.

### Features

- 📰 Fetch latest logistics news
- ⚙️ Process retrieved articles
- 🤖 AI-based disruption classification
- 📊 Generate structured news output

The backend pipeline has already been completed successfully.
""")

st.success("✅ Week 1 Pipeline Ready")

st.info("The complete backend integration will be connected after Week 2.")