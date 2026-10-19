import streamlit as st
import featureEngineering

sales_variation = st.Page("sales_variation.py", title="Sales Variation")
new_estimation_page = st.Page("new_estimation.py", title="New Estrimation")
past_games_page = st.Page("past_games.py", title="Past Games")

pg = st.navigation([sales_variation,new_estimation_page, past_games_page],position="top")


side_bar_title = st.sidebar.title("Input")

genre_sidebar = st.sidebar.selectbox(
    
    "Genre",
    ("rpg", "shooter", "adventure","puzzle","strategy")
    
)
release_month_sidebar = st.sidebar.slider(
    "Release Month",
    0,11
)

metacritic_sidebar = st.sidebar.slider(
    "Metacritic Score",
    0,100
)

multiplayer_sidebar = st.sidebar.radio(
        "Multiplayer",
        ["Yes", "No"]
)

publisher_size_sidebar = st.sidebar.selectbox(
    
    "Publisher Size",
    ("tiny", "small", "medium","large","giant")
    
)

pg.run()
