import streamlit as st
import json
import logging
from src.report_generator import ReportGenerator, ReportError, StructuredReport
from src.recommendation_engine import DisruptionContext
from src.utils.logger import get_logger

logger = get_logger("streamlit_ui_report")

st.set_page_config(page_title="Final Mitigation Report", page_icon="📄", layout="wide")

@st.cache_resource
def get_report_generator():
    return ReportGenerator()

def render_report_ui(report: StructuredReport):
    """Helper function to render the report visually before download."""
    st.markdown("### 📋 Incident Summary")
    st.info(report.incident_summary)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Affected Supplier", report.affected_supplier)
    col2.metric("Affected Region", report.affected_region)
    col3.metric("Risk Score", f"{report.risk_score} / 10.0")
    
    col4, col5, col6 = st.columns(3)
    col4.metric("Disruption Type", report.disruption_type)
    col5.metric("Impact Level", report.impact_level)
    col6.metric("Generated At", report.timestamp[:19].replace("T", " "))
    
    st.markdown("---")
    st.markdown("### 🛠️ Approved Mitigation Protocol")
    
    for idx, rec in enumerate(report.mitigation_recommendations, start=1):
        with st.container(border=True):
            st.markdown(f"**{idx}. {rec.action}** *(Priority: {rec.priority})*")
            st.caption(f"Estimated Time: {rec.estimated_time} | Expected Benefit: {rec.expected_benefit}")

# ==========================================
# Main Validation & Logic
# ==========================================
st.title("📄 Final Mitigation Report Export")

if "recommendations" not in st.session_state or not st.session_state.recommendations:
    st.warning("⚠️ No active recommendations found. Please go to **5 - Recommendations** and generate a mitigation plan first.")
    logger.warning("User attempted to view report without active recommendations.")
    st.stop()

recs = st.session_state.recommendations
raw_context = st.session_state.current_context

# Validate context
if not raw_context or "affected_supplier" not in raw_context or "affected_location" not in raw_context:
    st.error("⚠️ Invalid disruption context detected. Missing supplier or location data.")
    logger.error("Missing required supplier/location data in session state.")
    st.stop()

st.markdown("Review the structured mitigation report below and export it for downstream AI agent ingestion or distribution.")

report_gen = get_report_generator()

try:
    # 1. Build the Pydantic Context object required by the backend
    context_obj = DisruptionContext(**raw_context)
    
    # 2. Generate Report (This is fast, but in a heavy system we'd use @st.cache_data)
    with st.spinner("Compiling structured report..."):
        report = report_gen.generate_report(context=context_obj, recommendations=recs)
    
    logger.info("Successfully generated structured report for UI display.")
    
    # 3. Render Visual UI
    render_report_ui(report)
    
    # 4. Export Options
    st.markdown("---")
    st.subheader("💾 Export Report")
    st.markdown("Download the standard JSON payload. This payload is strictly formatted for consumption by LLMs and LangGraph endpoints.")
    
    # Generate JSON strings
    pretty_json = report_gen.export_to_json(report, pretty=True)
    compact_json = report_gen.export_to_json(report, pretty=False)
    
    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(
            label="⬇️ Download Pretty JSON",
            data=pretty_json,
            file_name=f"mitigation_report_{report.affected_supplier.replace(' ', '_')}.json",
            mime="application/json",
            type="primary",
            use_container_width=True
        )
    with dl_col2:
        st.download_button(
            label="⬇️ Download Compact JSON",
            data=compact_json,
            file_name=f"mitigation_report_{report.affected_supplier.replace(' ', '_')}_compact.json",
            mime="application/json",
            use_container_width=True
        )

except ReportError as e:
    st.error(f"❌ Failed to generate report: {e}")
    logger.error(f"Report generation failed: {e}")
except Exception as e:
    st.error("❌ An unexpected error occurred while compiling the JSON report.")
    logger.error(f"Unexpected JSON export failure: {e}")
