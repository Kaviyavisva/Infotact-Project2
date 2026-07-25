import streamlit as st
import pandas as pd
import plotly.express as px
import json
import sys
from pathlib import Path

import html

# Add src directories to system path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "src"))

from entity_extractor import extract_entities
from config import OUTPUT_FILE

st.set_page_config(
    page_title="Infotact - Entity Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom css for entity board
st.markdown("""
<style>
    .stApp {
        background-color: #0b1329;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    .entity-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
    }
    
    .page-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(to right, #60a5fa, #a5f3fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 8px 0;
    }
    
    /* Entity Group Card */
    .entity-group-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }
    
    .group-hdr {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 12px;
        color: #f8fafc;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .entity-item-badge {
        display: inline-block;
        background-color: rgba(59, 130, 246, 0.1);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.2);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.825rem;
        margin: 4px;
        font-weight: 500;
    }
    
    .entity-none-msg {
        font-style: italic;
        color: #64748b;
        font-size: 0.85rem;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Geolocation Coordinates Mapping Lookup for spatial maps
COORDINATES_MAP = {
    # Ports
    "Rotterdam Port": (51.9054, 4.3160),
    "Cat Lai Port": (10.7618, 106.7865),
    "Singapore Port": (1.2642, 103.8402),
    "Shanghai Port": (31.2304, 121.4737),
    "Shenzhen Port": (22.5431, 114.0579),
    "Ningbo Port": (29.8683, 121.5440),
    "Los Angeles Port": (33.7288, -118.2620),
    "Long Beach Port": (33.7701, -118.1937),
    "New York Port": (40.6974, -74.0261),
    "Suez Canal": (30.5852, 32.2654),
    "Dover Port": (51.1279, 1.3134),
    "Hamburg Port": (53.5458, 9.9644),
    "Felixstowe Port": (51.9566, 1.3168),
    "Mumbai Port": (18.9438, 72.8400),
    "Tokyo Port": (35.6186, 139.7758),
    "Busan Port": (35.1054, 129.0436),
    "Antwerp Port": (51.2612, 4.3857),
    "Houston Port": (29.7604, -95.3698),
    "Savannah Port": (32.0835, -81.0998),
    "Jebel Ali Port": (25.0112, 55.0617),
    "Oakland Port": (37.7958, -122.2875),
    "Seattle Port": (47.6062, -122.3321),
    "Tacoma Port": (47.2529, -122.4443),
    "Milford Haven Port": (51.7107, -5.0347),
    "Southampton Port": (50.9022, -1.3962),
    "Liverpool Port": (53.4084, -2.9916),
    "Cromarty Firth Port": (57.6934, -4.1374),
    "Swansea Port": (51.6214, -3.9436),
    "Newport Port": (51.5842, -2.9977),
    "Tyne Port": (55.0084, -1.4294),
    # Airports
    "Tan Son Nhat Airport": (10.8188, 106.6519),
    "Heathrow Airport": (51.4700, -0.4543),
    "JFK Airport": (40.6413, -73.7781),
    "LAX Airport": (33.9416, -118.4085),
    # Cities
    "Shanghai": (31.2304, 121.4737),
    "Shenzhen": (22.5431, 114.0579),
    "Beijing": (39.9042, 116.4074),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Ho Chi Minh City": (10.8231, 106.6297),
    "Hanoi": (21.0285, 105.8542),
    "Tokyo": (35.6762, 139.6503),
    "Seoul": (37.5665, 126.9780),
    "Singapore": (1.3521, 103.8198),
    "Rotterdam": (51.9244, 4.4777),
    "Dover": (51.1279, 1.3134),
    "Suez": (29.9668, 32.5498),
    "London": (51.5074, -0.1278),
    "Liverpool": (53.4084, -2.9916),
    "Southampton": (50.9022, -1.3962),
    "Santiago": (-33.4489, -70.6693),
}

# Cache entity extraction to avoid re-running Spacy on every load
@st.cache_data
def load_news_and_extract_entities():
    if not OUTPUT_FILE.exists():
        return [], []
        
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            articles = json.load(f)
            
        corpus_entities = []
        for idx, article in enumerate(articles):
            title = article.get("title", "")
            content = article.get("content", "")
            
            # Call our NER extractor
            ents = extract_entities(article)
            
            # Structure item detail
            item = {
                "id": idx,
                "title": title,
                "url": article.get("url", "#"),
                "source": article.get("source", "Unknown"),
                "entities": ents
            }
            corpus_entities.append(item)
            
        return articles, corpus_entities
        
    except Exception as e:
        st.error(f"Error extracting entities: {e}")
        return [], []

articles, extracted_corpus = load_news_and_extract_entities()

# HEADER
st.markdown("""
<div class="entity-header">
    <h1 class="page-title">🔍 Entity Extraction & Analytics</h1>
    <p style="margin: 0; color: #94a3b8; font-weight: 300;"> Mined Locations, Operators, Ports, and Shipping Channels from logistics news documents using SpaCy NER and Regex pipelines. </p>
</div>
""", unsafe_allow_html=True)

if not extracted_corpus:
    st.warning("⚠️ No news records available. Run `python src/news_fetcher.py` and refresh.")
else:
    # -----------------------------
    # Sidebar selectors
    # -----------------------------
    st.sidebar.header("🧭 Analytics View")
    view_type = st.sidebar.radio(
        "Select Analytics Scope",
        options=["Corpus Aggregates", "Single Article Mappings"]
    )
    
    # -----------------------------
    # Helper: Helper to render list of entities
    # -----------------------------
    def render_entity_section(title, icon, items):
        items_str = ""
        if not items:
            items_str = '<div class="entity-none-msg">None detected</div>'
        else:
            for item in items:
                items_str += f'<span class="entity-item-badge">{html.escape(str(item))}</span>'
                
        st.markdown(f"""
        <div class="entity-group-card">
            <div class="group-hdr"><span>{icon}</span> {title}</div>
            <div style="flex-wrap: wrap; display: flex;">
                {items_str}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # CORPUS VIEW TYPE
    # -----------------------------
    if view_type == "Corpus Aggregates":
        st.write("### 🌐 Global Entity Aggregation")
        st.write("Overview of all suppliers, countries, and logistics infrastructure extracted from our news feeds.")
        
        # Compile aggregate list counts
        all_countries = []
        all_cities = []
        all_ports = []
        all_airports = []
        all_suppliers = []
        all_plants = []
        all_routes = []
        
        for item in extracted_corpus:
            ents = item["entities"]
            all_countries.extend(ents.get("countries", []))
            all_cities.extend(ents.get("cities", []))
            all_ports.extend(ents.get("ports", []))
            all_airports.extend(ents.get("airports", []))
            all_suppliers.extend(ents.get("suppliers", []))
            all_plants.extend(ents.get("plants", []))
            all_routes.extend(ents.get("shipping_routes", []))
            
        # Metric Cards Rows
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        with col_m1:
            st.metric(label="Mined Suppliers", value=len(set(all_suppliers)))
        with col_m2:
            st.metric(label="Mined Ports", value=len(set(all_ports)))
        with col_m3:
            st.metric(label="Mined Airports", value=len(set(all_airports)))
        with col_m4:
            st.metric(label="Mined Countries", value=len(set(all_countries)))
        with col_m5:
            st.metric(label="Active Routes Mapped", value=len(set(all_routes)))
            
        st.write("---")
        
        # Grid layout for corpus metrics
        col_list1, col_list2 = st.columns(2)
        
        with col_list1:
            st.write("##### Top Mined Entities (Plotly Visualizations)")
            
            # Top Countries
            df_countries = pd.Series(all_countries).value_counts().reset_index()
            df_countries.columns = ["Country", "Mentions"]
            
            # Top Suppliers
            df_suppliers = pd.Series(all_suppliers).value_counts().reset_index()
            df_suppliers.columns = ["Supplier", "Mentions"]
            
            # Top Ports/Airports
            df_ports = pd.Series(all_ports + all_airports).value_counts().reset_index()
            df_ports.columns = ["Facility", "Mentions"]
            
            viz_option = st.selectbox(
                "Filter Chart Entity Type",
                options=["Top Suppliers", "Top Impacted Countries", "Top Hubs/Facilities"]
            )
            
            if viz_option == "Top Suppliers" and not df_suppliers.empty:
                fig = px.bar(df_suppliers.head(8), x="Mentions", y="Supplier", orientation="h", color="Mentions",
                             color_continuous_scale="deep")
                fig.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", height=320, margin=dict(t=10, b=10, l=10, r=10))
                st.plotly_chart(fig, use_container_width=True)
            elif viz_option == "Top Impacted Countries" and not df_countries.empty:
                fig = px.bar(df_countries.head(8), x="Mentions", y="Country", orientation="h", color="Mentions",
                             color_continuous_scale="viridis")
                fig.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", height=320, margin=dict(t=10, b=10, l=10, r=10))
                st.plotly_chart(fig, use_container_width=True)
            elif viz_option == "Top Hubs/Facilities" and not df_ports.empty:
                fig = px.bar(df_ports.head(8), x="Mentions", y="Facility", orientation="h", color="Mentions",
                             color_continuous_scale="bluered")
                fig.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", height=320, margin=dict(t=10, b=10, l=10, r=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No matching entity counts found to display charts.")
                
        with col_list2:
            st.write("##### Interactive Disruption Mapping Overlay")
            
            # Map coordinates resolution
            loc_mentions = pd.Series(all_ports + all_airports + all_cities).value_counts()
            
            map_data = []
            for loc_name, count in loc_mentions.items():
                if loc_name in COORDINATES_MAP:
                    lat, lon = COORDINATES_MAP[loc_name]
                    map_data.append({
                        "name": loc_name,
                        "latitude": lat,
                        "longitude": lon,
                        "mentions": count,
                        "size": min(10 + count * 8, 80) # scale sizes nicely
                    })
                    
            if map_data:
                map_df = pd.DataFrame(map_data)
                st.map(map_df, latitude="latitude", longitude="longitude", size="size")
                st.caption("ℹ️ Mapped log locations scaled by total incident mentions.")
            else:
                st.info("No recognizable locations have been extracted to match map coordinate files.")
                
        st.write("---")
        st.write("##### Mapped Entity Lists (Aggregated)")
        # Display tabs of Lists of Entities
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Suppliers & Plants", "Ports & Airports", "Countries & Cities", "Shipping Routes", "Full Summary"])
        
        with tab1:
            render_entity_section("Suppliers", "🏢", sorted(list(set(all_suppliers))))
            st.write("")
            render_entity_section("Manufacturing Plants", "🏭", sorted(list(set(all_plants))))
            
        with tab2:
            render_entity_section("Ports", "⚓", sorted(list(set(all_ports))))
            st.write("")
            render_entity_section("Airports", "✈️", sorted(list(set(all_airports))))
            
        with tab3:
            render_entity_section("Countries", "🌍", sorted(list(set(all_countries))))
            st.write("")
            render_entity_section("Cities", "🏙️", sorted(list(set(all_cities))))
            
        with tab4:
            render_entity_section("Shipping Routes", "🛣️", sorted(list(set(all_routes))))
            
        with tab5:
            col_x1, col_x2 = st.columns(2)
            with col_x1:
                st.write("**Aggregate Statistics Table**")
                stats = {
                    "Entity Category": ["Countries", "Cities", "Ports", "Airports", "Suppliers", "Plants", "Routes"],
                    "Unique Mined": [len(set(all_countries)), len(set(all_cities)), len(set(all_ports)), len(set(all_airports)), len(set(all_suppliers)), len(set(all_plants)), len(set(all_routes))],
                    "Total Mentions": [len(all_countries), len(all_cities), len(all_ports), len(all_airports), len(all_suppliers), len(all_plants), len(all_routes)]
                }
                st.table(pd.DataFrame(stats))
            with col_x2:
                st.write("**Help & Information**")
                st.info(
                    "This engine matches SpaCy Named Entities (GPE = Country/City, ORG = Suppliers/Plants) "
                    "with specialized rule-based regex patterns in `src/entity_extractor.py`. "
                    "Inferred relationships (e.g., matching a Plant to its Supplier name, aligning Cities "
                    "to Countries) are resolved dynamically to enhance logistics maps."
                )

    # -----------------------------
    # SINGLE ARTICLE VIEW TYPE
    # -----------------------------
    else:
        st.write("### 📄 News Article Entity Inspection")
        
        # Select box for single news article
        titles_list = [item["title"] for item in extracted_corpus]
        selected_title = st.selectbox(
            "Select News Article Feed",
            options=titles_list
        )
        
        # Resolve index
        chosen_article = next(x for x in extracted_corpus if x["title"] == selected_title)
        ents = chosen_article["entities"]
        
        st.markdown(f"**Source URL**: [Open Original Article Feed Link]({chosen_article['url']})")
        st.write("---")
        
        col_view1, col_view2 = st.columns([2, 1])
        
        with col_view1:
            st.write("##### Extracted Entities Cards")
            
            # Row 1
            col_r1a, col_r1b = st.columns(2)
            with col_r1a:
                render_entity_section("Countries", "🌍", ents.get("countries", []))
            with col_r1b:
                render_entity_section("Cities", "🏙️", ents.get("cities", []))
                
            # Row 2
            st.write("")
            col_r2a, col_r2b = st.columns(2)
            with col_r2a:
                render_entity_section("Ports", "⚓", ents.get("ports", []))
            with col_r2b:
                render_entity_section("Airports", "✈️", ents.get("airports", []))
                
            # Row 3
            st.write("")
            col_r3a, col_r3b = st.columns(2)
            with col_r3a:
                render_entity_section("Suppliers Mapped", "🏢", ents.get("suppliers", []))
            with col_r3b:
                render_entity_section("Manufacturing Plants", "🏭", ents.get("plants", []))
                
            # Row 4
            st.write("")
            render_entity_section("Shipping Routes Mapped", "🛣️", ents.get("shipping_routes", []))
            
        with col_view2:
            st.write("##### Article Geospatial Focus Map")
            
            # Compile Coordinates
            art_ports = ents.get("ports", [])
            art_airports = ents.get("airports", [])
            art_cities = ents.get("cities", [])
            
            art_locs = list(set(art_ports + art_airports + art_cities))
            
            map_data = []
            for loc in art_locs:
                if loc in COORDINATES_MAP:
                    lat, lon = COORDINATES_MAP[loc]
                    map_data.append({
                        "name": loc,
                        "latitude": lat,
                        "longitude": lon,
                        "size": 35
                    })
                    
            if map_data:
                map_df = pd.DataFrame(map_data)
                st.map(map_df, latitude="latitude", longitude="longitude", size="size")
                st.caption("📍 Coordinates pinpointed from article text locations.")
            else:
                st.info("No mapped coordinates recognized in this report. Showing global fallback.")
                # Show neutral default map centered at coordinates of major hubs
                fallback_df = pd.DataFrame([
                    {"latitude": 20.0, "longitude": 30.0, "size": 1}
                ])
                st.map(fallback_df, zoom=1)
                
            st.write("")
            st.write("**Article Text Preview**")
            # Pull clean content
            raw_article = next(x for x in articles if x.get("title") == selected_title)
            content_txt = raw_article.get("raw_content") or raw_article.get("content") or "No content preview available."
            escaped_content = html.escape(content_txt)
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 8px; font-size: 0.85rem; max-height: 250px; overflow-y: auto; color: #cbd5e1; line-height: 1.4;">
                {escaped_content}
            </div>
            """, unsafe_allow_html=True)
