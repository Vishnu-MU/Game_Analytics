import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sql_queries import queries  # Created a separate file for SQL queries

st.set_page_config(page_title="Tennis Rankings Explorer", layout="wide")

# Database Connection Setup
engine = create_engine("mysql+pymysql://root:Joker%40212814@localhost:3306/tennis_db")

@st.cache_data
def load_data():
    rankings_df = pd.read_sql("SELECT * FROM rankings", engine)
    competitor_df = pd.read_sql("SELECT * FROM competitor", engine)
    venues_df = pd.read_sql("SELECT * FROM venues", engine)
    complexes_df = pd.read_sql("SELECT * FROM complexes", engine)
    categories_df = pd.read_sql("SELECT * FROM categories", engine)
    competitions_df = pd.read_sql("SELECT * FROM competitions", engine)
    return rankings_df, competitor_df, venues_df, complexes_df, categories_df, competitions_df

# Load all required data
rankings_df, competitor_df, venues_df, complexes_df, categories_df, competitions_df = load_data()

# Merge rankings with competitor details
rankings_df = rankings_df.merge(competitor_df, on="competitor_id", how="left")

# SQL Query Runner
def get_data(query):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

# -------------------------------
# App Tabs
# -------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎾 Tennis Dashboard Overview",
    "🔍 Search & Filter Competitors",
    "👤 Competitor & Country Analysis",
    "🏟️ Complexes & Venues Explorer",
    "📋 SQL Query Results"
])

# -------------------------------
# Tab 1: Dashboard Overview
# -------------------------------
with tab1:
    st.title("🎾 Tennis Dashboard Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", competitor_df.shape[0])
    col2.metric("Countries Represented", competitor_df['country'].nunique())
    col3.metric("Highest Points", rankings_df['points'].max())

    # Top 5 countries by total points
    top_countries = rankings_df.groupby("country")["points"].sum().reset_index()
    top_countries = top_countries.sort_values(by="points", ascending=False).head(5)
    st.markdown("### 🌍 Top 5 Countries")
    st.dataframe(top_countries, use_container_width=True)

    # Top 5 players by rank
    st.markdown("### 🥇 Top 5 Players by Rank")
    top_5 = rankings_df.sort_values(by="rank").head(5)
    st.dataframe(top_5[["rank", "name", "country", "points"]], use_container_width=True)

# -------------------------------
# Tab 2: Search & Filter Competitors
# -------------------------------
with tab2:
    st.title("🔍 Search & Filter Competitors")

    rank_range = st.slider("Filter by Rank", int(rankings_df["rank"].min()), int(rankings_df["rank"].max()), (1, 50))
    selected_countries = st.multiselect("Select Countries", sorted(rankings_df["country"].dropna().unique()))

    filtered_df = rankings_df.copy()
    filtered_df = filtered_df[
        (filtered_df["rank"] >= rank_range[0]) &
        (filtered_df["rank"] <= rank_range[1])
    ]
    if selected_countries:
        filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

    st.markdown("### 📋 Filtered Competitors")
    st.dataframe(filtered_df[["rank", "name", "country", "points", "competitions_played", "movement"]], use_container_width=True)

# -------------------------------
# Tab 3: Competitor Details & Country Analysis
# -------------------------------
with tab3:
    st.title("👤 Competitor Details Viewer")
    selected_name = st.selectbox("Select a Competitor", sorted(rankings_df["name"].dropna().unique()))
    selected_data = rankings_df[rankings_df["name"] == selected_name].iloc[0]
    st.write(f"**Name**: {selected_data['name']}")
    st.write(f"**Rank**: {selected_data['rank']}")
    st.write(f"**Movement**: {selected_data['movement']}")
    st.write(f"**Competitions Played**: {selected_data['competitions_played']}")
    st.write(f"**Country**: {selected_data['country']}")

    st.markdown("### 🌍 Country-Wise Analysis")
    country_summary = rankings_df.groupby("country").agg({
        "competitor_id": "count",
        "points": "sum"
    }).rename(columns={"competitor_id": "Competitors", "points": "Total Points"}).reset_index()
    st.dataframe(country_summary, use_container_width=True)

# -------------------------------
# Tab 4: Venues & Complexes
# -------------------------------
with tab4:
    st.title("🏟️ Complexes & Venues Explorer")

    # Merge venues with complex details
    merged_df = venues_df.merge(complexes_df, on="complex_id", how="left")

    # Country filter
    selected_country = st.selectbox("🌍 Select Country", sorted(merged_df["country_name"].unique()))
    filtered_df = merged_df[merged_df["country_name"] == selected_country]

    # Show merged venue & complex data
    st.write(f"### 📍 Complexes & Venues in {selected_country}")
    st.dataframe(filtered_df[[
        "complex_name", "venue_name", "city_name", "timezone", "complex_id"
    ]], use_container_width=True)

# -------------------------------
# Tab 5: SQL Query Results
# -------------------------------
with tab5:
    st.title("📋 SQL Query Results")

    # Sub-tabs for each SQL query category
    category_tabs = st.tabs(list(queries.keys()))

    for (category_name, category_queries), sub_tab in zip(queries.items(), category_tabs):
        with sub_tab:
            st.subheader(f"{category_name}")
            for query_title, query in category_queries.items():
                with st.expander(query_title):
                    st.code(query.strip(), language="sql")
                    if st.button(f"▶️ Run: {query_title}", key=query_title):
                        result = get_data(query)
                        st.dataframe(result, use_container_width=True)
