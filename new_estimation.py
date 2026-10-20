import streamlit as st
import featureEngineering


side_bar_title = st.sidebar.title("Input")
with st.sidebar.form(key="sidebar form"):

    genre = st.selectbox(
        
        "Genre",
        ("rpg", "shooter", "adventure","puzzle","strategy")
        
    )
    release_month = st.slider(
        "Release Month",
        0,11
    )


    marketing_budget = st.number_input("Marketing Budget")

    price = st.number_input("Price at Launch")

    dev_time = st.slider(
        "Dev Time in Month",
        0,11
    )

    is_franchise = st.radio(
        "Is it a franchise",
        [":green[Yes]",":red[No]"]
    )

    submit_button = st.form_submit_button("Submit")


st.write("First Year Sales Prediction:")