import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import scipy.stats as stats
import streamlit as st

df = pd.read_csv('./csv/delays_transformed.csv')
df = df[(df['year'] <= 2019) & (df['year'] >= 2014)]

# Different way of de
airport_risk = df.groupby("airport_name_cleansed", as_index=False).agg(
    total_flights=("arr_flights", "sum"),
    total_delays=("arr_del15", "sum")
)
airport_risk = airport_risk[airport_risk['total_flights'] >= 100000]
airport_risk['delay_pct'] = airport_risk['total_delays'] / airport_risk['total_flights']
top10_airports = airport_risk.sort_values('delay_pct', ascending=False).head(10)['airport_name_cleansed'].tolist()

airport = st.selectbox("Select Airport", index=None, placeholder="Any Airport", options=top10_airports)
if airport is not None:
    airline = st.selectbox("Select Airline", index=None, placeholder="Any Airline", options=sorted(df[df['airport_name_cleansed'] == airport]['carrier_name'].unique()))
else:
    airline = st.selectbox("Select Airline", index=None, placeholder="Any Airline", options=df['carrier_name'].unique())
season = st.selectbox("Select Season", index=None, placeholder="All Year", options=['Winter (Dec-Feb)', 'Spring (Mar-May)', 'Summer (June-Aug)', 'Fall (Sept-Nov)'])

pie_df = df.copy()

if airport is not None:
    pie_df = pie_df[pie_df["airport_name_cleansed"].str.contains(airport, case=False, na=False)]
if airline is not None:
    pie_df = pie_df[pie_df["carrier_name"].str.contains(airline, case=False, na=False)]
if season is not None:
    if 'Winter' in season:
        pie_df = pie_df[pie_df["month"].isin([12, 1, 2])]
    elif 'Spring' in season:
        pie_df = pie_df[pie_df["month"].isin([3, 4, 5])]
    elif 'Summer' in season:
        pie_df = pie_df[pie_df["month"].isin([6, 7, 8])]
    elif 'Fall' in season:
        pie_df = pie_df[pie_df["month"].isin([9, 10, 11])]

pie_df = (pie_df.groupby("carrier_name", as_index=False)[["arr_flights", 'arr_del15', 'carrier_ct', 'weather_ct', 'nas_ct', 'security_ct', 'late_aircraft_ct']].sum())
pie_df.insert(1, 'on_time', pie_df['arr_flights'] - pie_df['arr_del15'])

total_flights = pie_df["arr_flights"].sum()

carrier_pct = pie_df["carrier_ct"].sum() / total_flights
weather_pct = pie_df["weather_ct"].sum() / total_flights
nas_pct = pie_df["nas_ct"].sum() / total_flights
security_pct = pie_df["security_ct"].sum() / total_flights
late_aircraft_pct = pie_df["late_aircraft_ct"].sum() / total_flights
on_time_pct = pie_df["on_time"].sum() / total_flights

labels = ["Carrier", "Weather", "NAS", "Security", "Late Aircraft"]
values = [carrier_pct, weather_pct, nas_pct, security_pct, late_aircraft_pct]

fig, ax = plt.subplots(figsize=(6,6))
ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=["red", "green", "blue", "yellow", "magenta"])
if airport is not None:
    if airline is not None:
        if season is not None:
            ax.set_title(f"Percentage of Historical Delays (2014-2019) at {airport} Airport with {airline} in {season}")
        else:
            ax.set_title(f"Percentage of Historical Delays (2014-2019) at {airport} Airport with {airline}")
    else:
        ax.set_title(f"Percentage of Historical Delays (2014-2019) at {airport} Airport")
else:
    if airline is not None:
        if season is not None:
            ax.set_title(f"Percentage of Historical Delays (2014-2019) for {airline} in {season}")
        else:
            ax.set_title(f"Percentage of Historical Delays (2014-2019) for {airline}")
    else:
        ax.set_title(f"Percentage of Historical Delays (2014-2019)")

st.pyplot(fig)