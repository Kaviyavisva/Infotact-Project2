import streamlit as st

st.set_page_config(
    page_title="Disruption Monitoring Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🌍 Autonomous Disruption Monitoring Agent")
    st.markdown("---")
    
    st.markdown("""
    ### Welcome to the Disruption Monitoring Dashboard!
    
    This interface integrates with the backend AI recommendation engine and report generator 
    to provide real-time mitigation strategies for supply chain disruptions.
    
    **Navigation:**
    - 👈 Use the sidebar to navigate to **5 - Recommendations** to simulate a disruption and view mitigation protocols.
    - 👈 Navigate to **6 - Final Report** to export the structured JSON report.
    """)
    
    st.info("Ensure you generate recommendations first before attempting to export the Final Report.", icon="ℹ️")
    
if __name__ == "__main__":
    main()
