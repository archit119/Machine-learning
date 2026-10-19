import pandasql as ps
import pandas as pd
from IPython.display import display
import numpy as np

# function query(sql) will help us write our SQL queries easily
def query(sql):
    return ps.sqldf(sql, globals())

dataset_path = "data-3.csv" 
df = pd.read_csv(dataset_path)

# log the data test
df['first_year_sales_k_log'] = np.log1p(df['first_year_sales_k'])

print()
print()

genre = query("""
SELECT genre, first_year_sales_k, first_year_sales_k_log
FROM df
""")
display(genre.groupby("genre").agg(["count", "mean", "median"]).round(2))

print()

genre = query("""
SELECT is_multiplayer, first_year_sales_k, first_year_sales_k_log
FROM df
""")
display(genre.groupby("is_multiplayer").agg(["count", "mean", "median"]).round(2))

print()

dev_time = query("""
SELECT
  CASE
    WHEN dev_time_months < 17 THEN 'A (6-16)'
    WHEN dev_time_months < 28 THEN 'B (17-27)'
    WHEN dev_time_months < 38 THEN 'C (28-37)'
    WHEN dev_time_months < 48 THEN 'D (38-47)'
    ELSE 'E (48-60)'
  END AS dev_time_band,
first_year_sales_k, first_year_sales_k_log
FROM df
""")
display(dev_time.groupby("dev_time_band").agg(["count", "mean", "median"]).round(2))

print()

team_size = query("""
SELECT
  CASE
    WHEN team_size < 78 THEN 'A (23-77)'
    WHEN team_size < 110 THEN 'B (78-109)'
    WHEN team_size < 136 THEN 'C (110-135)'
    WHEN team_size < 193 THEN 'D (136-192)'
    ELSE 'E (193-520)'
  END AS team_size_band,
first_year_sales_k, first_year_sales_k_log
FROM df
""")
display(team_size.groupby("team_size_band").agg(["count", "mean", "median"]).round(2))

print()

platforms = query("""
SELECT platforms_count, first_year_sales_k, first_year_sales_k_log
FROM df
""")
display(platforms.groupby("platforms_count").agg(["count", "mean", "median"]).round(2))

print()

price = query("""
SELECT launch_price_usd, first_year_sales_k, first_year_sales_k_log
FROM df
""")
display(price.groupby("launch_price_usd").agg(["count", "mean", "median"]).round(2))

print()

playtime = query("""
SELECT
  CASE
    WHEN median_playtime_hours < 7.5 THEN 'A (<7.5)'
    WHEN median_playtime_hours < 11.5 THEN 'B (7.5-11.5)'
    WHEN median_playtime_hours < 18 THEN 'C (11.5-18)'
    WHEN median_playtime_hours < 29 THEN 'D (18-29)'
    WHEN median_playtime_hours < 50 THEN 'E (29-50)'
    ELSE 'F (50+)'
  END AS playtime_band,
first_year_sales_k, first_year_sales_k_log
FROM df
""")
display(playtime.groupby("playtime_band").agg(["count", "mean", "median"]).round(2))

print()

publisher_size = query("""
SELECT
  CASE publisher_size
    WHEN 'tiny' THEN 'A tiny'
    WHEN 'small' THEN 'B small'
    WHEN 'medium' THEN 'C medium'
    WHEN 'large' THEN 'D large'
    ELSE 'E giant'
  END AS publisher_size_band,
first_year_sales_k, first_year_sales_k_log
FROM df
""")
display(publisher_size.groupby("publisher_size_band").agg(["count", "mean", "median"]).round(2))

print()
print()