import streamlit as st
import pandas as pd 
import pandasql as ps
from model_logic import final_table 

st.title("Past Games")

df = final_table

# genre = st.session_state.get("genre", "rpg")
# publisher = st.session_state.get("publisher", "medium")
# score = st.session_state.get("score", 0)
# months = st.session_state.get("months", (0, 11))

# filters = f"""
# Where genre = '{genre}'
#     AND publisher_size = '{publisher}'
#     AND release_month BETWEEN {months[0]} AND {months[1]}
# """
def run(sql):
    return ps.sqldf(sql, {"df": df})

top10 = run(f"""
SELECT first_year_sales_k
FROM df
ORDER BY first_year_sales_k DESC
Limit 10;
""")

DBSs = run(f"""
SELECT marketing_budget_usd, first_year_sales_k
FROM df;
""")

if DBSs.empty: 
    st.warning("No games match these filters.")
else:
    left, right = st.columns(2)
    with left:
        st.subheader("Top 10 best selling games")
        st.bar_chart(top10)
        st.caption("Each bar is one game. Height = first year sales (thousands of copies). Bars are ranked best to worst, left to right")
    with right:
        st.subheader("Marketing budget vs sales")
        st.scatter_chart(DBSs, x="marketing_budget_usd", y="first_year_sales_k")



