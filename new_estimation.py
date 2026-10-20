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