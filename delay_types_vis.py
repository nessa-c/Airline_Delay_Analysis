import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import scipy.stats as stats
import streamlit as st

df = pd.read_csv('./csv/delays_reduced.csv')

airport = st.selectbox("Select Airport", options=df['airport_code'].unique())
airline = st.selectbox("Select Airline", options=df['carrier_name'].unique())
season = st.selectbox("Select Season", options=['Winter', 'Spring', 'Summer', 'Fall'])

pie_df = df.copy()

if airport is not None:
    pie_df = pie_df[pie_df["airport_code"].str.contains(airport, case=False, na=False)]
if airline is not None:
    pie_df = pie_df[pie_df["carrier_name"].str.contains(airline, case=False, na=False)]
if season is not None:
    if season == 'Winter':
        pie_df = pie_df[pie_df["month"].isin([12, 1, 2])]
    elif season == 'Spring':
        pie_df = pie_df[pie_df["month"].isin([3, 4, 5])]
    elif season == 'Summer':
        pie_df = pie_df[pie_df["month"].isin([6, 7, 8])]
    elif season == 'Fall':
        pie_df = pie_df[pie_df["month"].isin([9, 10, 11])]

pie_df = pie_df[(pie_df["year"] >= 2014) & (pie_df["year"] <= 2019)]

pie_df = (pie_df.groupby("carrier_name", as_index=False)[["arr_flights", 'arr_del15', 'carrier_ct', 'weather_ct', 'nas_ct', 'security_ct', 'late_aircraft_ct']].sum())

total_flights = pie_df["arr_flights"].sum()

if total_flights > 0:
    carrier_pct = pie_df["carrier_ct"].sum() / total_flights
    weather_pct = pie_df["weather_ct"].sum() / total_flights
    nas_pct = pie_df["nas_ct"].sum() / total_flights
    security_pct = pie_df["security_ct"].sum() / total_flights
    late_aircraft_pct = pie_df["late_aircraft_ct"].sum() / total_flights

    labels = ["Carrier", "Weather", "NAS", "Security", "Late Aircraft"]
    values = [carrier_pct, weather_pct, nas_pct, security_pct, late_aircraft_pct]

    fig, ax = plt.subplots(figsize=(7,7))
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90,
           colors=["red", "green", "blue", "yellow", "magenta"])
    ax.set_title("Percentage of Historical Delays")

    st.pyplot(fig)
else:
    st.write("No data available for this selection")