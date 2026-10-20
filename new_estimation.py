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






from joblib import load
import pandas as pd
import numpy as np

model = load("game_model_full.joblib")
columns = list(load("required_inputs.joblib"))


new_release_month_sin = np.sin(((new_release_month + 1)/12) * 2 * np.pi)
new_release_month_cos = np.cos(((new_release_month + 1)/12) * 2 * np.pi)

if(new_is_franchise == 'Yes'): is_franchise = 1
else: is_franchise = 0

genre_puzzle = 0
genre_rpg = 0
genre_shooter = 0,
genre_strategy = 0
genre_adventure = 0

if new_genre == 'puzzle':
    genre_puzzle = 1
elif new_genre == 'strategy':
    genre_strategy = 1
elif new_genre == 'rpg':
    genre_rpg = 1
elif new_genre == 'adventure':
    genre_adventure = 1
else: genre_shooter = 1
inputs = {
    'marketing_budget_usd': new_marketing_budget,
    'team_size': 120,
    'platforms_count': 2,
    'is_multiplayer': 1,
    'is_franchise': is_franchise,
    'publisher_size': 2,
    'launch_discount': 0.2,
    'release_month_sin': new_release_month_sin,
    'release_month_cos': new_release_month_cos,
    'genre_puzzle': genre_puzzle,
    'genre_rpg': genre_rpg,
    'genre_shooter': genre_shooter,
    'genre_strategy': genre_strategy,
    'genre_adventure': genre_adventure
}

X_new = pd.DataFrame([inputs])[columns]         
log_pred = model.predict(X_new)[0]               
sales_k = np.expm1(log_pred)                     

print(f"Predicted first-year sales: {sales_k:.1f}k")

st.write(f"Predicted first-year sales: {sales_k:.1f} k")