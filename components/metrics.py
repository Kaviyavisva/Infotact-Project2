import streamlit as st


def show_metrics(results):
    """
    Display dashboard metrics.
    """

    total_articles = len(results)

    high_count = sum(
        1 for article in results
        if article.severity.lower() == "high"
    )

    medium_count = sum(
        1 for article in results
        if article.severity.lower() == "medium"
    )

    low_count = sum(
        1 for article in results
        if article.severity.lower() == "low"
    )

    critical_count = sum(
        1 for article in results
        if article.severity.lower() == "critical"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("📰 Articles", total_articles)
    col2.metric("🔴 Critical", critical_count)
    col3.metric("🟠 High", high_count)
    col4.metric("🟡 Medium", medium_count)
    col5.metric("🟢 Low", low_count)