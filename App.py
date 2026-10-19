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


marketing_budget_sidebar=st.sidebar.number_input("Marketing Budget")

price_sidebar=st.sidebar.number_input("Price at Launch")

dev_time_sidebar = st.sidebar.slider(
    "Dev Time in Month",
    0,11
)

is_franchise_sidebar = st.sidebar.radio(
    "Is it a franchise",
    [":green[Yes]",":red[No]"]
)


pg.run()
