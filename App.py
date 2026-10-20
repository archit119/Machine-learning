import streamlit as st
import featureEngineering

sales_variation = st.Page("sales_variation.py", title="Sales Variation")
new_estimation_page = st.Page("new_estimation.py", title="New Estimation")
past_games_page = st.Page("past_games.py", title="Past Games")

pg = st.navigation([sales_variation,new_estimation_page, past_games_page],position="top")

pg.run()
