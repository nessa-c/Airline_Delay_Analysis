import streamlit as st
import pandas as pd
import plotly.express as px

def nessa_chart(df: pd.DataFrame) -> None:    
    airport_risk = df.groupby("airport_name_cleansed").agg(
        total_flights=("arr_flights", "sum"),
        total_delays=("arr_del15", "sum")
    )
    airport_risk = airport_risk[airport_risk['total_flights'] >= 100000]
    airport_risk['delay_pct'] = airport_risk['total_delays'] / airport_risk['total_flights']
    top10_airports = airport_risk.sort_values('delay_pct', ascending=False).head(10).index.tolist()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        airport = st.selectbox("Airport", [None] + top10_airports, key="nessa_airport")
    with col2:
        airline_list = sorted(df['carrier_name'].unique()) if airport is None else sorted(df[df['airport_name_cleansed'] == airport]['carrier_name'].unique())
        airline = st.selectbox("Airline", [None] + airline_list, key="nessa_airline")
    with col3:
        season = st.selectbox("Season", [None, "Winter", "Spring", "Summer", "Fall"], key="nessa_season")
    
    pie_df = df.copy()
    if airport:
        pie_df = pie_df[pie_df["airport_name_cleansed"] == airport]
    if airline:
        pie_df = pie_df[pie_df["carrier_name"] == airline]
    
    if season:
        season_map = {"Winter": [12, 1, 2], "Spring": [3, 4, 5], "Summer": [6, 7, 8], "Fall": [9, 10, 11]}
        pie_df = pie_df[pie_df["month"].isin(season_map[season])]
    
    pie_df = pie_df.groupby("carrier_name")[["carrier_ct", "weather_ct", "nas_ct", "security_ct", "late_aircraft_ct"]].sum()
    total_flights = pie_df.sum(axis=1).sum()
    
    if total_flights > 0:
        values = [
            pie_df["carrier_ct"].sum() / total_flights,
            pie_df["weather_ct"].sum() / total_flights,
            pie_df["nas_ct"].sum() / total_flights,
            pie_df["security_ct"].sum() / total_flights,
            pie_df["late_aircraft_ct"].sum() / total_flights
        ]
        labels = ["Carrier", "Weather", "NAS", "Security", "Late Aircraft"]
        
        fig = px.pie(values=values, names=labels, category_orders={"names": labels}, color_discrete_sequence=px.colors.qualitative.Plotly_r)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(template="plotly_white", hoverlabel=dict(font_size=16))
        st.plotly_chart(fig, width='stretch')
        
        st.divider()
        col1, col2, col3, col4, col5 = st.columns(5)
        for col, label, val in zip([col1, col2, col3, col4, col5], labels, values):
            with col:
                st.metric(label, f"{val:.1%}")
    else:
        st.warning("No data available")