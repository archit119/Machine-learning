import streamlit as st
import pandas as pd
from pandasql import sqldf
st.title("Sales Variation")
st.write("This page allows users to analize and inspect charts based on their chosen input values:")

st.subheader("Average Sales by Platform")
st.write("")
platform_df = query(f"""
    SELECT platforms_count, AVG(first_year_sales_k) AS avg_sales
    FROM final_copy_table
    WHERE genre = '{genre}'
    GROUP BY platforms_count
    ORDER BY platforms_count
""") 
platform_df["platforms_count"] = platform_df["platforms_count"].astype(str)
st.bar_chart(platform_df, x="platform_count", y="avg_sales")


st.write("")
st.subheader("Average Sales per Genre")
st.write("")

st.subheader("Average Sales per Release Month")
st.write("")

st.subheader("Review vs Scale")
st.write("")

