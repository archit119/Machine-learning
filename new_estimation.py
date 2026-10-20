import streamlit as st
import featureEngineering


side_bar_title = st.sidebar.title("Input")

genre = st.sidebar.selectbox(
    
    "Genre",
    ("rpg", "shooter", "adventure","puzzle","strategy")
    
)
release_month = st.sidebar.slider(
    "Release Month",
    0,11
)


marketing_budget = st.sidebar.number_input("Marketing Budget")

price = st.sidebar.number_input("Price at Launch")

dev_time = st.sidebar.slider(
    "Dev Time in Month",
    0,11
)

is_franchise = st.sidebar.radio(
    "Is it a franchise",
    [":green[Yes]",":red[No]"]
)
