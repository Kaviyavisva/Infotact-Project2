import streamlit as st


def show_sidebar():
    """
    Display the application sidebar.
    """

    st.sidebar.title("Navigation")

    st.sidebar.success("Week 1 ✅ Completed")
    st.sidebar.info("Week 2 🚧 In Progress")

    st.sidebar.markdown("---")

    st.sidebar.write("### Pipeline")

    st.sidebar.write("✅ News Fetcher")
    st.sidebar.write("✅ Data Processor")
    st.sidebar.write("✅ Risk Classifier")
    st.sidebar.write("🚧 Entity Extraction")
    st.sidebar.write("🚧 Impact Analysis")
    st.sidebar.write("🚧 Recommendation Engine")