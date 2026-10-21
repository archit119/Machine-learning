from joblib import load
import pandas as pd
import numpy as np
import featureEngineering as fe
import math

model = load("game_model_full.joblib")
columns = list(load("required_inputs.joblib"))
finalDrop = list(load("final_drop.joblib"))

dataset_path = "data-3.csv" 
df = pd.read_csv(dataset_path)

final_table = df.copy() # get the table
final_table.drop(columns=finalDrop, inplace=True)
# print(finalDrop)

table_for_dist = load("table_for_dist.joblib")

pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 90)
print(final_table.head(10).round(4).to_string())

pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 90)
print(table_for_dist.head(10).round(4).to_string())

def getInputs(genre, release_month, marketing, team_size, platform_count, multiplayer, franchise, publisher_sizes, launch_discount):
    # genre field
        genre_puzzle = 0
        genre_rpg = 0
        genre_shooter = 0
        genre_strategy = 0
    
        if(genre=='Puzzle'):
            genre_puzzle = 1
        elif(genre=='RPG'):
            genre_rpg=1
        elif(genre=='Shooter'):
            genre_shooter=1
        elif(genre=='Strategy'):
            genre_strategy=1
    
        # release month
        release_month_dict = {
            "January": 0,
            "February": 1,
            "March": 2,
            "April": 3,
            "May": 4,
            "June": 5,
            "July": 6,
            "August": 7,
            "September": 8,
            "October": 9,
            "November": 10,
            "December": 11,
        }
        release_month_mapped = release_month_dict[release_month]
    
        release_month_sin = np.sin(((release_month_mapped + 1)/12) * 2 * np.pi)
        release_month_cos = np.cos(((release_month_mapped + 1)/12) * 2 * np.pi)
    
        # marketing can be left as is
        # team_size can also be left as is
        # platform_count can be left as is
    
        # multiplayer
        is_multiplayer=0
        if('Yes' in multiplayer):
            is_multiplayer=1
    
        # is_franchise
        is_franchise=0
        if('Yes' in franchise):
            is_franchise=1
    
        # publisher size
        publisher_size_dict = {"Tiny": 0, "Small": 1, "Medium": 2, "Large": 3, "Giant": 4}
        publisher_size = publisher_size_dict[publisher_sizes]
    
        # launch discount
        launch_discount = launch_discount/100
    
        inputs = {
            'marketing_budget_usd': marketing,
            'team_size': team_size,
            'platforms_count': platform_count,
            'is_multiplayer': is_multiplayer,
            'is_franchise': is_franchise,
            'publisher_size': publisher_size,
            'launch_discount': launch_discount,
            'release_month_sin': release_month_sin,
            'release_month_cos': release_month_cos,
            'genre_puzzle': genre_puzzle,
            'genre_rpg': genre_rpg,
            'genre_shooter': genre_shooter,
            'genre_strategy': genre_strategy,
        }

        return inputs

def predict(genre, release_month, marketing, team_size, platform_count, multiplayer, franchise, publisher_sizes, launch_discount):
    inputs = getInputs(genre, release_month, marketing, team_size, platform_count, multiplayer, franchise, publisher_sizes, launch_discount)

    X_new = pd.DataFrame([inputs])[columns]         
    log_pred = model.predict(X_new)[0]               
    sales_k = np.expm1(log_pred)                     

    print(f"Predicted first-year sales: {sales_k:.1f}k")
    return sales_k


def getEuclaidenDistances(genre, release_month, marketing, team_size, platform_count, multiplayer, franchise, publisher_sizes, launch_discount):
    inputs = getInputs(genre, release_month, marketing, team_size, platform_count, multiplayer, franchise, publisher_sizes, launch_discount)

    scaler = model[0]  

    table_scaled = scaler.transform(table_for_dist[columns])
    input_scaled = scaler.transform(pd.DataFrame([inputs])[columns])

    distances = np.sqrt(((table_scaled - input_scaled) ** 2).sum(axis=1))

    table_with_dist = final_table.copy()
    table_with_dist["Distance"] = distances
    return table_with_dist.sort_values("Distance")