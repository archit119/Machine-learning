import streamlit as st
import pandas as pd
from pandasql import sqldf
from model_logic import final_table
import calendar

st.title("Sales Variation")
st.write("This page allows users to analize and inspect charts based on their chosen input values:")

# this helps us write queries how we are used to doing
def query(sql):
        return sqldf(sql, globals())


# first chart : "Average Sales by Platform"
st.subheader("Average Sales by Platform")
platform_df = query(f"""
    SELECT platforms_count, AVG(first_year_sales_k) AS avg_sales
    FROM final_table
    GROUP BY platforms_count
    ORDER BY platforms_count
""") 
platform_df["platforms_count"] = platform_df["platforms_count"].astype(str)
st.bar_chart(platform_df, x="platforms_count", y="avg_sales")

# second chart : "Average Sales per Genre"
st.subheader("Average Sales per Genre")
genre_df = query(f"""
    SELECT genre, AVG(first_year_sales_k) AS avg_sales
    FROM final_table 
    GROUP BY Genre 
""")
genre_df["genre"] = genre_df["genre"].astype(str)
st.bar_chart(genre_df, x="genre", y="avg_sales")

# third chart : "Average Sales per Release Month"
st.subheader("Average Sales per Release Month")
month_df = query(f"""
    SELECT release_month, AVG(first_year_sales_k) AS avg_sales 
    FROM final_table
    GROUP BY release_month 
    ORDER BY release_month
""")
# we map the numbers 0-11 that we used for the months to the actually month names
month_map = {
        0: "Jan", 1: "Feb", 2: "Mar", 3:"Apr", 4: "May", 5: "Jun", 
        6: "Jul", 7: "Aug", 8:"Sept", 9: "Oct", 10: "Nov", 11: "Dec"
}

month_df["release_month"] = month_df["release_month"].map(month_map)
# Giving the chronological order
month_order = list(month_map.values())
month_df["release_month"] = pd.Categorical(month_df["release_month"], categories=month_order, ordered=True)

# Sort by the new categorical order
month_df = month_df.sort_values("release_month")
st.line_chart(month_df, x="release_month", y="avg_sales")


