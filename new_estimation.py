import streamlit as st
import numpy as np
import model_logic as ml
import pandas as pd
import random
import altair as alt
import model_stats as ms

# stuff needed:
# genre
# release month
# marketting 
# team size
# platform count
# multiplayer or not
# is franchise
# publisher size
# launch discount

def monthConverter(monthNumber):
    release_month_dict = {
        0: "January",
        1: "February",
        2: "March",
        3: "April",
        4: "May",
        5: "June",
        6: "July",
        7: "August",
        8: "September",
        9: "October",
        10: "November",
        11: "December",
    }
    return release_month_dict[monthNumber]


def differentMonths(new_genre, new_marketing_budget, new_team_size, new_platform_count, new_multiplayer, new_is_franchise, new_publisher_size, new_launch_discount):
    monthSales = []
    for i in range(12):
        monthSales.append(ml.predict(new_genre, monthConverter(i), new_marketing_budget, new_team_size, new_platform_count, new_multiplayer, new_is_franchise, new_publisher_size, new_launch_discount))

    return monthSales

# ui stuff
side_bar_title = st.sidebar.title("Game Details")
st.set_page_config(layout="wide")
with st.sidebar.form(key="sidebar form"):

    new_genre = st.selectbox(
        
        "Genre",
        ("RPG", "Shooter", "Adventure", "Puzzle", "Strategy")
        
    )
    new_release_month = st.selectbox(
        
        "Month",
        ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
        
    )

    new_marketing_budget = st.number_input("Marketing Budget (USD)", step=1)

    new_team_size = st.number_input("Team size", min_value=1, step=1)

    new_platform_count = st.number_input("Platform Count", min_value=1, step=1)

    new_multiplayer = st.radio(
        "Is it multiplayer?",
        [":green[Yes]",":red[No]"]
    )

    new_is_franchise = st.radio(
        "Is it a franchise",
        [":green[Yes]",":red[No]"]
    )

    new_publisher_size = st.selectbox(

        "Publisher Size",
        {"Tiny", "Small", "Medium", "Large", "Giant"}

    )

    new_launch_discount = st.number_input(
        "Launch Discount (%)", min_value=0, max_value=100, 
    )

    submit_button = st.form_submit_button("Submit")



gameNames = ["Clair Obscur: Expedition 33", "The Last of Us Part I", "Detroit: Become Human", "Cyberpunk: 2077", "Hollow Knight", "Celeste", "Resident Evil: Requiem", "Marvel's Spiderman", "Pragmata", "God of War (2018)"]

if(submit_button):
    st.subheader("First-year sales estimate")
    sales = ml.predict(new_genre, new_release_month, new_marketing_budget, new_team_size, new_platform_count, new_multiplayer, new_is_franchise, new_publisher_size, new_launch_discount)
    formatted_sales = f"{sales:.1f}k"
    # we got a rmse of 0.59
    # using log conversions you end up with 1.75 value
    low, high = sales / 1.75, sales * 1.75
 
    c1, c2 = st.columns(2)
    c1.metric("Predicted first-year sales", f"{sales:.1f}k copies", border=True)
    c2.metric("Likely range", f"{low:.0f}k – {high:.0f}k", border=True)

    distTable = ml.getEuclaidenDistances(new_genre, new_release_month, new_marketing_budget, new_team_size, new_platform_count, new_multiplayer, new_is_franchise, new_publisher_size, new_launch_discount)
    distTable_sorted = distTable.sort_values(by='Distance', ascending=True).head(3)
    pd.set_option('display.width', 200)
    pd.set_option('display.max_colwidth', 90)
    print(distTable_sorted.round(4).to_string())

    st.subheader("Most similar past games")
    cols = st.columns(3)
    names = random.sample(gameNames, 3)

    i = 0
    for col, (_, game) in zip(cols, distTable_sorted.iterrows()):
        with col.container(border=True):
            st.markdown(
                f"""
                <div style="font-size: 0.8rem; color: #A8AEBD;">{game['genre'].upper()} · {monthConverter(game['release_month'])}</div>
                <div style="font-size: 1.1rem; font-weight: 600; margin-top: 4px;">{names[i]}</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #FF4B4B; margin: 4px 0;">{game['first_year_sales_k']:.1f}k copies</div>
                <div style="font-size: 0.8rem; color: #A8AEBD; margin-bottom: 20px;">
                    Marketing ${game['marketing_budget_usd']:,.0f} · {'Franchise' if game['is_franchise'] else 'New IP'}
                </div>
                """,
                unsafe_allow_html=True,
            )
        i += 1

    monthSales = differentMonths(new_genre, new_marketing_budget, new_team_size, new_platform_count, new_multiplayer, new_is_franchise, new_publisher_size, new_launch_discount)
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    print("Month Sales", len(monthSales))
    monthDf = pd.DataFrame(
        {"Month": months,
        "Predicted sales (k)": monthSales}
    )
    pd.set_option('display.width', 200)
    pd.set_option('display.max_colwidth', 90)
    print(monthDf.round(4).to_string())

    # st.line_chart(monthDf, x="Month", y="Predicted sales (k)")
    st.subheader("Predicted sales by release month")
    chart = alt.Chart(monthDf).mark_bar().encode(
        x=alt.X("Month", sort=None),
        y=alt.Y("Predicted sales (k)"),
        tooltip=[
            alt.Tooltip("Month"),
            alt.Tooltip("Predicted sales (k)", format=".1f"),
        ],
    )

    st.altair_chart(chart, width='stretch')

    ms.displayStats()

