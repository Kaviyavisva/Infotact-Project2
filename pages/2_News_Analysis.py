import streamlit as st
import pandas as pd
import plotly.express as px
import json
import sys
import html
from pathlib import Path

# Add src directories to system path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "src"))

from classifier import classify_article
from config import OUTPUT_FILE

st.set_page_config(
    page_title="Infotact - News Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom css for news dashboard
st.markdown("""
<style>
    /* Styling variables */
    :root {
        --primary-dark: #0b1329;
        --card-bg: rgba(30, 41, 59, 0.75);
        --glass-border: rgba(255, 255, 255, 0.08);
        --glow-high: 0 0 10px rgba(ef4444, 0.2);
        --glow-medium: 0 0 10px rgba(f97316, 0.2);
        --glow-low: 0 0 10px rgba(59, 130, 246, 0.2);
    }
    
    .stApp {
        background-color: var(--primary-dark);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Layout styling */
    .news-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
    }
    
    .page-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(to right, #60a5fa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 8px 0;
    }
    
    /* News Card */
    .news-card {
        background: var(--card-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .news-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.3);
    }
    
    .severity-high {
        border-left: 5px solid #ef4444;
    }
    
    .severity-medium {
        border-left: 5px solid #f97316;
    }
    
    .severity-low {
        border-left: 5px solid #3b82f6;
    }
    
    .card-meta {
        font-size: 0.8rem;
        color: #94a3b8;
        display: flex;
        gap: 15px;
        margin-bottom: 10px;
        align-items: center;
    }
    
    .card-title-link {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f8fafc !important;
        text-decoration: none !important;
        display: block;
        margin-bottom: 10px;
    }
    
    .card-title-link:hover {
        color: #60a5fa !important;
    }
    
    .card-preview {
        font-size: 0.925rem;
        color: #cbd5e1;
        line-height: 1.5;
        margin-bottom: 15px;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 6px;
        border: 1px solid transparent;
    }
    
    .badge-high {
        background-color: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border-color: rgba(239, 68, 68, 0.3);
    }
    
    .badge-medium {
        background-color: rgba(249, 115, 22, 0.15);
        color: #fb923c;
        border-color: rgba(249, 115, 22, 0.3);
    }
    
    .badge-low {
        background-color: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .badge-category {
        background-color: rgba(148, 163, 184, 0.1);
        color: #e2e8f0;
        border-color: rgba(148, 163, 184, 0.2);
    }
</style>
""", unsafe_allow_html=True)

import re

def clean_news_content(text):
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove markdown link placeholders: [Text](url) -> Text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove markdown header prefix matches
    text = re.sub(r'#+\s+', '', text)
    # Strip markdown symbols
    for char in ['*', '`', '_', '■']:
        text = text.replace(char, '')
    
    # Strip typical website head/menu remnants (like Resources Archives Subscribe)
    remnant_words = ["Subscribe Today", "Resources", "Archives", "Search", "Menu"]
    for word in remnant_words:
        text = re.sub(r'\b' + re.escape(word) + r'\b', '', text, flags=re.I)
        
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# Cache data loading
@st.cache_data
def load_and_classify_news():
    if not OUTPUT_FILE.exists():
        return pd.DataFrame()
        
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            articles = json.load(f)
            
        processed_articles = []
        for article in articles:
            title = article.get("title", "")
            content = article.get("content", "")
            
            # Perform classification & severity calculations
            category, severity = classify_article(title, content)
            
            cleaned_content = clean_news_content(content)
            
            refactored_item = {
                "title": title,
                "url": article.get("url", "#"),
                "source": article.get("source", "Unknown Source"),
                "publication_date": article.get("publication_date") or "N/A",
                "preview": cleaned_content[:250] + "..." if cleaned_content else "No content available.",
                "content": content or "",
                "category": category,
                "severity": severity,
                "score": article.get("score", 0.5)
            }
            processed_articles.append(refactored_item)
            
        return pd.DataFrame(processed_articles)
        
    except Exception as e:
        st.error(f"Error loading news file: {e}")
        return pd.DataFrame()

df = load_and_classify_news()

# HEADER
st.markdown("""
<div class="news-header">
    <h1 class="page-title">📊 News Analysis Board</h1>
    <p style="margin: 0; color: #94a3b8; font-weight: 300;">
        Real-time categorization, threat scoring, and analysis of active supply chain disruptions.
    </p>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("⚠️ No news articles available. Run `python src/news_fetcher.py` to fetch active logs first.")
else:
    # -----------------------------
    # Sidebar Filters
    # -----------------------------
    st.sidebar.header("🔍 Filter Dashboard")
    
    # 1. Search Bar
    search_query = st.sidebar.text_input("Search articles", "").strip().lower()
    
    # 2. Category multi-select
    all_categories = sorted(df["category"].unique())
    selected_categories = st.sidebar.multiselect(
        "Categories",
        options=all_categories,
        default=all_categories
    )
    
    # 3. Severity multi-select
    selected_severities = st.sidebar.multiselect(
        "Severity Tiers",
        options=["High", "Medium", "Low"],
        default=["High", "Medium", "Low"]
    )
    
    # 4. Source multi-select
    all_sources = sorted(df["source"].unique())
    selected_sources = st.sidebar.multiselect(
        "Publication Sources",
        options=all_sources,
        default=all_sources
    )
    
    # Apply filters
    filtered_df = df[
        df["category"].isin(selected_categories) &
        df["severity"].isin(selected_severities) &
        df["source"].isin(selected_sources)
    ]
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df["title"].str.lower().str.contains(search_query) |
            filtered_df["content"].str.lower().str.contains(search_query)
        ]
        
    # -----------------------------
    # Metric Summary Layer
    # -----------------------------
    st.write("### 📈 Operational Overview")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    total_loaded = len(filtered_df)
    high_count = len(filtered_df[filtered_df["severity"] == "High"])
    
    if not filtered_df.empty:
        top_category = filtered_df["category"].value_counts().idxmax()
        top_source = filtered_df["source"].value_counts().idxmax()
    else:
        top_category = "N/A"
        top_source = "N/A"
        
    with m_col1:
        st.metric(label="Articles Mapped", value=total_loaded)
    with m_col2:
        st.metric(label="High Threats", value=high_count, delta="Immediate Alert", delta_color="inverse")
    with m_col3:
        st.metric(label="Primary Disruption", value=top_category)
    with m_col4:
        st.metric(label="Key Source Feed", value=top_source)
        
    st.write("---")
    
    # -----------------------------
    # Visual Analytics Sections
    # -----------------------------
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.write("##### Disruption Distribution by Category")
        if not filtered_df.empty:
            cat_counts = filtered_df["category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Articles"]
            
            fig1 = px.pie(
                cat_counts, 
                values="Articles", 
                names="Category",
                color_discrete_sequence=px.colors.qualitative.Safe,
                hole=0.4
            )
            fig1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                height=300,
                margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No data selected to display category charts.")
            
    with col_chart2:
        st.write("##### Disruption Severity Breakdown")
        if not filtered_df.empty:
            sev_counts = filtered_df["severity"].value_counts().reindex(["High", "Medium", "Low"], fill_value=0).reset_index()
            sev_counts.columns = ["Severity", "Articles"]
            
            fig2 = px.bar(
                sev_counts,
                x="Severity",
                y="Articles",
                color="Severity",
                color_discrete_map={
                    "High": "#ef4444",
                    "Medium": "#f97316",
                    "Low": "#3b82f6"
                },
                category_orders={"Severity": ["High", "Medium", "Low"]}
            )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                height=300,
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(title=None),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data selected to display severity charts.")
            
    st.write("---")
    
    # -----------------------------
    # News Cards Mapped Panel
    # -----------------------------
    st.write("### 📇 Mapped Logistics Feeds")
    
    if filtered_df.empty:
        st.info("No news feeds match the selected filter configuration.")
    else:
        for idx, row in filtered_df.iterrows():
            severity_lower = row["severity"].lower()
            
            # Severity Badge selector
            badge_class = f"badge-{severity_lower}"
            
            # Escape strings to prevent HTML injection errors
            escaped_severity = html.escape(str(row['severity']))
            escaped_category = html.escape(str(row['category']))
            escaped_pub_date = html.escape(str(row['publication_date']))
            escaped_source = html.escape(str(row['source']))
            escaped_url = html.escape(str(row['url']))
            escaped_title = html.escape(str(row['title']))
            escaped_preview = html.escape(str(row['preview']))
            
            # Card element HTML construction
            st.markdown(f"""
            <div class="news-card severity-{severity_lower}">
                <div class="card-meta">
                    <span class="badge {badge_class}">{escaped_severity} Severity</span>
                    <span class="badge badge-category">{escaped_category}</span>
                    <span>🕒 {escaped_pub_date}</span>
                    <span>🔌 {escaped_source}</span>
                </div>
                <a class="card-title-link" href="{escaped_url}" target="_blank">{escaped_title}</a>
                <div class="card-preview">{escaped_preview}</div>
            </div>
            """, unsafe_allow_html=True)
