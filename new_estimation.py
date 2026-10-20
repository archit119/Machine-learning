import streamlit as st
import numpy as np
import model
import math

side_bar_title = st.sidebar.title("Input")
with st.sidebar.form(key="sidebar form"):

    new_genre = st.selectbox(
        
        "Genre",
        ("rpg", "shooter", "adventure","puzzle","strategy")
        
    )
    new_release_month = st.slider(
        "Release Month",
        0,11
    )


    new_marketing_budget = st.number_input("Marketing Budget")

    new_price = st.number_input("Price at Launch")

    new_dev_time = st.slider(
        "Dev Time in Month",
        0,11
    )

    new_is_franchise = st.radio(
        "Is it a franchise",
        [":green[Yes]",":red[No]"]
    )

    submit_button = st.form_submit_button("Submit")


st.write("First Year Sales Prediction:")