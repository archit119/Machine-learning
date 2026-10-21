import streamlit as st
from joblib import load


@st.cache_data
def load_stats():
    return load("model_stats.joblib")


def stat_card(col, label, value, caption):
    with col.container(border=True):
        st.markdown(
            f"""
            <div style="font-size: 0.8rem; color: #A8AEBD;">{label}</div>
            <div style="font-size: 2rem; font-weight: 700; color: #FF4B4B; margin: 4px 0;">{value}</div>
            <div style="font-size: 0.8rem; color: #A8AEBD; margin-bottom: 10px;">{caption}</div>
            """,
            unsafe_allow_html=True,
        )

def displayStats():
    stats = load_stats()

    st.subheader("Model statistics")
    st.caption("All numbers are from 5-fold cross-validation: every game was predicted by a model that never saw it.")

    c1, c2, c3 = st.columns(3)

    stat_card(c1, "Accuracy (R²)",
            f"{stats['r2_mean']:.2f}",
            f"The model explains about {stats['r2_mean']:.0%} of the differences in first-year sales between games.")

    stat_card(c2, "Typical error (RMSE)",
            f"{stats['rmse_mean']:.2f}",
            "Average prediction error, measured on the log scale of sales.")

    stat_card(c3, "Typical error in sales",
            f"×/÷ {stats['error_factor']:.2f}",
            f"Actual sales are usually within {stats['error_factor']:.2f}× above or below the prediction.")

    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

    with st.expander("How to read these numbers"):
        st.markdown(
            f"""
            - **R²** runs from 0 to 1. 0 means no better than always guessing the average; 1 means perfect predictions.
            - **RMSE** is measured on the log of sales, because sales are very skewed (a few games sell far more than the rest).
            - **×/÷ {stats['error_factor']:.2f}** is the RMSE converted back to real sales (e^RMSE).
            For example, a prediction of 100k typically means actual sales between
            {100 / stats['error_factor']:.0f}k and {100 * stats['error_factor']:.0f}k.
            """
        )