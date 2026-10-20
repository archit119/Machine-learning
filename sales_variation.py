import streamlit as st
import pandas as pd
from pandasql import sqldf
st.title("Sales Variation")
st.write("This page allows users to analize and inspect charts based on their chosen input values:")
@st.cache_data
def load_data():
        data = pd.read_csv("data-3.csv")
        return data[data["dev_budget_usd"] <=3400000]
final_copy_table = load_data()

def query(sql):
        return sqldf(sql,globals())


genre = st.sidebar.selectbox("Genre", sorted(final_copy_table["genre"].unique()))
st.subheader("Average Sales by Platform")
platform_df = query(f"""
    SELECT platforms_count, AVG(first_year_sales_k) AS avg_sales
    FROM final_copy_table
    WHERE genre = '{genre}'
    GROUP BY platforms_count
    ORDER BY platforms_count
""") 
platform_df["platforms_count"] = platform_df["platforms_count"].astype(str)
st.bar_chart(platform_df, x="platforms_count", y="avg_sales")


st.subheader("Average Sales per Genre")
month = st.sidebar.slider("Release month", 0, 11, 0)
score = st.sidebar.slider("Score", 0, 100, 0)
genre_df = query(f"""
    SELECT genre, AVG(first_year_sales_k) As avg_sales
    FROM final_copy_table
    WHERE release_month = {month} And metacritic >= {score}
    GROUP BY Genre 
""")
genre_df["genre"] = genre_df["genre"].astype(str)
st.bar_chart(genre_df, x="genre", y="avg_sales")

st.subheader("Average Sales per Release Month")
month_df = query(f"""
    SELECT release_month, AVG(first_year_sales_k) As avg_sales 
    FROM final_copy_table
    WHERE genre = '{genre}' AND metacritic >= {score}
    GROUP BY release_month 
    ORDER BY release_month;
""")
month_df["release_month"] = month_df["release_month"]
st.line_chart(month_df, x="release_month", y="avg_sales")

multiplayer = st.sidebar.radio("Multiplayer", ["Yes", "No"])
st.subheader("Review vs Scale")
review_df = query(f"""
    SELECT metacritic, first_year_sales_k
    FROM final_copy_table
    WHERE genre = '{genre}' And is_multiplayer = {multiplayer};

""")
review_df["metacritic"] = review_df["metacritic"]
st.scatter_chart(review_df, x="metacritic", y="avg_sales")

