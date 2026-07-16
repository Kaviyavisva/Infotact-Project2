import streamlit as st

st.set_page_config(
    page_title="Entity Extraction",
    page_icon="📍",
    layout="wide"
)

st.title("📍 Entity Extraction")

st.markdown("""
## Module Overview

This module extracts important logistics entities from classified news articles.

### Entities Extracted

- 🌍 Countries
- 🏙 Cities
- 🚢 Ports
- ✈ Airports
- 🏭 Manufacturing Plants
- 🚛 Suppliers
- 🛣 Shipping Routes

The extracted entities will be used for supplier impact analysis.
""")

st.info("🚧 Waiting for Week 2 Integration")