from IPython.display import display
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.feature_selection import mutual_info_regression
import random

#Modify the path according to where the file is in your filesystem
dataset_path = "data-3.csv" 

df = pd.read_csv(dataset_path)

# drop the outliers
# just gonna comment this out for now, because apparently spearman correlation doesent get affected by outliers
# final_copy_table = df.copy()
# rowsToDrop = []
# for i, row in final_copy_table.iterrows():
#     if row["dev_budget_usd"] > 3400000:
#         rowsToDrop.append(i)
# final_copy_table.drop(rowsToDrop, inplace=True)
# print(final_copy_table)

# encode the data
df_encoded = df.copy()

# first we change the studio from tiny-large to 0-4 (because here it increases so spearman correlation can make a link)
df_encoded["publisher_size"] = df_encoded["publisher_size"].map(
    {"tiny": 0, "small": 1, "medium": 2, "large": 3, "giant": 4})

# month cycle is cyclic, because 11 comes right after 0, we must somehow signify this
# we decided to use sin / cos because its a cyclic graph
# explained in the document the logic and the formula
df_encoded['release_month_sin'] = np.sin(((df_encoded['release_month'] + 1)/12) * 2 * np.pi)
df_encoded['release_month_cos'] = np.cos(((df_encoded['release_month'] + 1)/12) * 2 * np.pi)
df_encoded.drop(columns='release_month', inplace=True)

# Leakage check
# explained in the document
invalidColumns = ['metacritic', 'user_score', 'reviews_at_launch', 'median_playtime_hours']
df_encoded.drop(columns=invalidColumns, inplace=True)

df_encoded = pd.get_dummies(df_encoded, dtype=int, drop_first=True)

# getter function to be used by other scripts
def getTable():
    return df_encoded


if __name__ == "__main__":
    # here we get the correlation
    df_corr = df_encoded.corr('spearman')
    df_corr.info()

    # split data into X and y
    X = df_encoded.drop(columns='first_year_sales_k')
    y = np.log1p(df_encoded['first_year_sales_k']) # log transformed sales

    # display mutual inclusion 8 times with 8 different seeds
    for i in range(5):
        print("Attempt ", i)

        # a noise baseline
        # we need this because mutual inclusion can technically give completely unrelated fields a tiny positive score
        # this acts as a baseline, a field thats complete rubbish
        # we can see how much this gives us
        X['random_noise'] = np.random.default_rng(i).normal(size=len(X))
        X_sample = X.sample(frac=0.8, random_state=i)
        y_sample = y.loc[X_sample.index]

        # mutual info check
        discrete_cols = ['platforms_count', 'is_multiplayer', 'is_franchise', 'release_month_sin', 'release_month_cos', 'genre_puzzle', 'genre_rpg', 'genre_shooter', 'genre_strategy']
        discrete = X_sample.columns.isin(discrete_cols)

        mi = mutual_info_regression(X_sample, y_sample, discrete_features=discrete, random_state=i)
        mi = pd.Series(mi, index=X_sample.columns).sort_values(ascending=False)
        display(mi)
        print()
        print()

# display correlation graph
# fig, ax = plt.subplots(figsize=(15,10))
# sns.heatmap(df_corr, ax=ax)
# plt.title("Spearman Rank Correlation Heatmap")
# plt.show()

