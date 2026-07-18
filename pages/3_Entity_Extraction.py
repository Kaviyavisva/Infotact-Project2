import streamlit as st
import json
import os

st.set_page_config(
    page_title="Entity Extraction",
    page_icon="📍",
    layout="wide"
)

st.title("📍 Entity Extraction")

OUTPUT_FILE = "output/classified_news.json"

if not os.path.exists(OUTPUT_FILE):
    st.warning("Please run the pipeline first.")
    st.stop()

with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
    reports = json.load(file)

st.success(f"Loaded {len(reports)} reports.")

for i, report in enumerate(reports, start=1):

    with st.expander(f"Article {i}: {report['Title']}"):

        entities = report.get("Entities", {})

        if not entities:
            st.info("No entities extracted.")
            continue

        cols = st.columns(2)

        keys = list(entities.keys())

        for index, key in enumerate(keys):

            values = entities[key]

            with cols[index % 2]:

                st.subheader(key.replace("_", " ").title())

                if values:
                    for value in values:
                        st.write(f"• {value}")
                else:
                    st.write("No entities found.")