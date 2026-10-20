import streamlit as st
import numpy as np
import model_logic as ml

# stuff needed:
# genre
# release month
# marketting 
# team size
# platform count
# multiplayer or not
# is franchise
# publisher size
# launch discount

# ui stuff
side_bar_title = st.sidebar.title("Input")
with st.sidebar.form(key="sidebar form"):

    new_genre = st.selectbox(
        
        "Genre",
        ("RPG", "Shooter", "Adventure", "Puzzle", "Strategy")
        
    )
    new_release_month = st.selectbox(
        
        "Month",
        ("January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
        
    )

    new_marketing_budget = st.number_input("Marketing Budget", step=1)

    new_team_size = st.number_input("Team size", step=1)

    new_platform_count = st.number_input("Platform Count", step=1)

    new_multiplayer = st.radio(
        "Is it multiplayer?",
        [":green[Yes]",":red[No]"]
    )

    new_is_franchise = st.radio(
        "Is it a franchise",
        [":green[Yes]",":red[No]"]
    )

    new_publisher_size = st.selectbox(

        "Publisher Size",
        {"Tiny", "Small", "Medium", "Large", "Giant"}

    )

    new_launch_discount = st.slider(
        "Launch Discount (%)", 0, 60, 
    )

    submit_button = st.form_submit_button("Submit")


st.write("First Year Sales Prediction:")

if(submit_button):
    sales = ml.predict(new_genre, new_release_month, new_marketing_budget, new_team_size, new_platform_count, new_multiplayer, new_is_franchise, new_publisher_size, new_launch_discount)
    st.write(sales)

