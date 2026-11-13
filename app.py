# %%
import os
import pandas as pd
import config
import psycopg2
import numpy as np
import time
import plotly.express as px

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

import streamlit as st

#st.session_state.rank_tier = 

df = pd.DataFrame()

# def filter_general(column_string,column_value,df):
#     df_filtered = df[df[column_string] == column_value]
#     return df_filtered

def filter_general(column_string, column_value, df):
    #If not column value is not a list
    if not isinstance(column_value, list):
        column_value = [column_value]

    # List of column values if list
    if column_string == "rank_tier":
        column_value = [list_of_ranks.index(rank)+1 for rank in column_value]
        if isinstance(column_value, list):
            if len(column_value) > 1:
                df = df.groupby("hero_id").agg({
                "localized_name": "first",
                "rank_tier": "first",
                "appearances": "sum",
                "wins": "sum",
                "timestamp": "first"
                }).reset_index()

                total_matches = df["appearances"].sum()
                df["appearance_rate"] = (df["appearances"] / total_matches * 100)

                df["win_rate"] = (df["wins"] / df["appearances"] * 100)

    #st.code(df)

    df_filtered = df[df[column_string].isin(column_value)]

    df_sorted = df_filtered.sort_values(by="win_rate", ascending=False)

    return df_sorted

def filter_UI(ranks,weeks):
    col1, col2 = st.columns(2)

    with col1:
        st.session_state.rank_tier = st.segmented_control(
        "",
        options=ranks,
        default="All",
        key="navigation",
        selection_mode="single"
        )

        if st.session_state.rank_tier is None:
            st.session_state.rank_tier = list_of_ranks
        if st.session_state.rank_tier == "All":
            st.session_state.rank_tier = list_of_ranks

    with col2:
        st.session_state.timestamp = st.selectbox(
            "",
            weeks
        )

def filter_main():
    filter_UI(list_of_ranks,list_of_timestamps)
    
    df_filtered = filter_general("timestamp",st.session_state.timestamp,df)
    df_filtered = filter_general("rank_tier",st.session_state.rank_tier,df_filtered)

    st.code(st.session_state.rank_tier)

    return df_filtered

print(config.START_TIME_)

# Load environment variables
load_dotenv()

# Retrieve Neon connection URL
@st.cache_data(ttl=600)
def database_connection():
    DATABASE_URL = os.getenv("DATABASE_READ_URL")

    if not DATABASE_URL:
        raise ValueError("DATABASE_READ_URL not found in .env")

    # Create database connection
    engine = create_engine(DATABASE_URL)

    try:
        # Read data from Neon
        with engine.connect() as conn:

            print("Connected user:",
                conn.execute(text("SELECT current_user")).scalar())

            df = pd.read_sql(
                text("SELECT * FROM hero_stats"),
                conn
            )

            print("\nRetrieved data:")
            #print(df.head())

            print("\nNumber of rows retrieved:", len(df))

    except Exception as e:
        print("Database connection failed:", e)

    finally:
        engine.dispose()

    return df

df = database_connection()
################################ DATAFRAME

#FIND UNIQUE WEEKS
list_of_timestamps = df["timestamp"].unique().tolist()
list_of_timestamps.sort(reverse=True)

#List of ranks
list_of_ranks = ["Herald","Guardian","Crusader","Archon","Legend","Ancient","Divine","All"]

#STATS SUMMARY
matches_analysed = int(df['appearances'].sum()/10)

max_idx_wr = df["win_rate"].idxmax()
highest_hero_wr = df.loc[max_idx_wr, "localized_name"]

max_idx_appear = df["appearances"].idxmax()
highest_hero_appear = df.loc[max_idx_appear, "localized_name"]



################################ START OF STREAMLIT CODE ####################

st.set_page_config(
    page_title="Dota 2 Weekly",
    page_icon="🎮",
    layout="wide"
)

# Sidebar
st.sidebar.title("🎮 Dota 2 Weekly")
st.sidebar.write("Data Analytics Dashboard")

st.sidebar.divider()

#### NAVIGATION PANEL
pages = [
    "Trending Heroes",
    "Hero Statistics",
    "Cluster Diagram",
    "Data Overview",
    "Pipeline Monitoring"
]

for page in pages:
    if st.sidebar.button(page, use_container_width=True):
        st.session_state.page = page

if "page" not in st.session_state:
    st.session_state.page = "Trending Heroes"

##### Main page

################# HERO STATS
if st.session_state.page == "Trending Heroes":
    st.title("Trending Heroes")

if st.session_state.page == "Hero Statistics":
    st.title("Hero Statistics")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Matches analysed", matches_analysed)

    with col2:
        st.metric("Highest winrate", highest_hero_wr)

    with col3:
        st.metric("Most played", highest_hero_appear)

    st.divider()

    st.subheader("Weekly Ranked Statistics")

    df_filtered = filter_main()

    #df_filtered = df[df["timestamp"] == st.session_state.timestamp]

    st.dataframe(
        df_filtered.drop(columns=["hero_id","timestamp"]),
        column_order=[
        "Rank",
        "localized_name",
        "appearances",
        "appearance_rate",
        "wins",
        "win_rate"
        ],
        use_container_width=True,
        hide_index=True,
        height="content",
        column_config={
            "Rank": st.column_config.TextColumn("Rank"),
            "localized_name": st.column_config.TextColumn("Hero"),
            "appearances": st.column_config.NumberColumn("Appearance"),
            "appearance_rate": st.column_config.NumberColumn("Appearance rate",
                format="%.2f%%"),
            "wins": st.column_config.NumberColumn("Wins"),
            "win_rate": st.column_config.NumberColumn(
                "Win Rate (%)",
                format="%.2f%%"
            )
        }
    )

################### CLUSTER CODE
elif st.session_state.page == "Cluster Diagram":

    st.title("Cluster Diagram")

    st.divider()

    st.subheader("Weekly Ranked Cluster")

    df_filtered = filter_main()

    fig = px.scatter(
        df_filtered,
        x="appearance_rate",
        y="win_rate",
        hover_name="localized_name",
        title="Hero Pick Rate vs Win Rate",
        labels={
            "appearance_rate": "Appearance Rate (%)",
            "win_rate": "Win Rate (%)",
            "matches_played": "Matches Played"
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == "Data Overview":
    st.title("Data Overview")

elif st.session_state.page == "Pipeline Monitoring":
    st.title("Pipeline Monitoring")


# %%
