import streamlit as st


def show_news_cards(results):
    """
    Display classified news articles.
    """

    st.divider()

    st.subheader("📰 Classified News")

    for i, article in enumerate(results, start=1):

        with st.expander(f"📰 Article {i}: {article.title}"):

            st.write(f"**Category:** {article.category}")
            st.write(f"**Severity:** {article.severity}")
            st.write(f"**Reason:** {article.reason}")