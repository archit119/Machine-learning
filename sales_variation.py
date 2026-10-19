import streamlit as st
import pandas as pd
import featureEngineering
st.title("Sales Variation")
st.write("This page allows users to analize and inspect charts based on their chosen input values:")

st.subheader("Average Sales by Platform")
st.write("")
st.bar_chart(featureEngineering.df_encoded)


st.write("")
st.subheader("Average Sales per Genre")
st.write("")

st.subheader("Average Sales per Release Month")
st.write("")

st.subheader("Review vs Scale")
st.write("")

