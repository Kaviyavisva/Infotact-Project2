import streamlit as st

from src.pipeline import SupplyChainPipeline

from components.metrics import show_metrics
from components.news_cards import show_news_cards

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
- 📍 Identifies affected regions and suppliers *(Week 2)*
- 📈 Estimates supplier impact *(Week 2)*
- 💡 Generates mitigation recommendations *(Week 2)*
- 📄 Produces comprehensive risk reports *(Week 2)*
""")

st.success("✅ Week 1 completed successfully | 🚧 Week 2 integration in progress")

st.divider()

# ------------------------------
# Project Status
# ------------------------------
st.subheader("📊 Project Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Sprint", "Week 2")

with col2:
    st.metric("Overall Progress", "50%")

with col3:
    st.metric("Application Status", "🟢 Active")

# ------------------------------
# Module Progress
# ------------------------------
st.subheader("📌 Module Progress")

progress = {
    "News Fetcher": "✅ Completed",
    "Data Processor": "✅ Completed",
    "Risk Classifier": "✅ Completed",
    "Entity Extraction": "🚧 In Progress",
    "Supplier Impact": "🚧 In Progress",
    "Recommendations": "🚧 In Progress",
    "Final Report": "🚧 In Progress"
}

for module, status in progress.items():
    st.write(f"**{module}** : {status}")

# ------------------------------
# Overall Project Progress
# ------------------------------
st.subheader("📈 Overall Project Progress")

progress_percentage = 50

st.progress(progress_percentage / 100)

st.write(f"**Project Completion:** {progress_percentage}%")

# ------------------------------
# Development Team
# ------------------------------
st.subheader("👥 Development Team")

team_data = {
    "Kaviyashri Viswanathan": "Integration Coordinator & Risk Analysis",
    "Abhishek Sangani": "Entity Extraction",
    "Mugdha Sangaonkar": "Supplier Impact Analysis",
    "Adhiraj Singh Shekhawat": "Recommendation & Report Generation"
}

for member, role in team_data.items():
    st.write(f"**{member}** — {role}")
# ------------------------------
# System Workflow
# ------------------------------

st.divider()

st.subheader("🔄 System Workflow")

st.markdown("""
```text
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
Entity Extraction (Week 2)
          │
          ▼
Supplier Impact Analysis (Week 2)
          │
          ▼
Recommendation Engine (Week 2)
          │
          ▼
Final Risk Report""")



# ✅ Step 5 – Add Project Highlights


st.subheader("⭐ Project Highlights")

col1, col2 = st.columns(2)

with col1:
    st.success("✅ AI-powered disruption classification")
    st.success("✅ Modular pipeline architecture")
    st.success("✅ Streamlit web interface")

with col2:
    st.info("🚧 Entity Extraction")
    st.info("🚧 Supplier Impact Analysis")
    st.info("🚧 Recommendation Engine")
# ------------------------------
# Upcoming Modules
# ------------------------------
st.divider()

st.subheader("📍 Entity Extraction")
st.info("This module will be integrated in Week 2.")

st.subheader("📈 Supplier Impact Analysis")
st.info("This module will be integrated in Week 2.")

st.subheader("💡 Mitigation Recommendation")
st.info("This module will be integrated in Week 2.")

st.subheader("📄 Final Risk Report")
st.info("This module will be integrated in Week 2.")

st.divider()

st.caption(
    "Autonomous Supply Chain Disruption Monitor | "
    "InfoTact Solutions Internship | Week 2 Development"
)