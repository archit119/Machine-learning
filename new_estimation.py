import streamlit as st
from streamlit_option_menu import option_menu

import streamlit as st

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