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



from joblib import load
import pandas as pd
import numpy as np

model = load("game_model_full.joblib")
columns = list(load("required_inputs.joblib"))

inputs = {
    'marketing_budget_usd': 500000,
    'team_size': 120,
    'platforms_count': 2,
    'is_multiplayer': 1,
    'is_franchise': 0,
    'publisher_size': 2,
    'launch_discount': 0.2,
    'release_month_sin': 0.5,
    'release_month_cos': 0.866,
    'genre_puzzle': 0,
    'genre_rpg': 1,
    'genre_shooter': 0,
    'genre_strategy': 0,
}

X_new = pd.DataFrame([inputs])[columns]         
log_pred = model.predict(X_new)[0]               
sales_k = np.expm1(log_pred)                     

print(f"Predicted first-year sales: {sales_k:.1f}k")

