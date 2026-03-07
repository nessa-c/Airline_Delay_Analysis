import streamlit as st
import pandas as pd
import plotly.express as px

def julia_chart(df: pd.DataFrame) -> None:    
    col1, col2, col3 = st.columns(3)
    with col1:
        seasons = ["All"] + sorted(df["season"].dropna().unique())
        selected_season = st.selectbox("Season", seasons, key="julia_season")
    with col2:
        carriers = sorted(df["carrier_name"].dropna().unique())
        selected_carriers = st.multiselect("Carrier", carriers, default=carriers, key="julia_carriers")
    with col3:
        airport_list = sorted(df["airport_code"].dropna().unique())
        selected_airports = st.selectbox("Airport", airport_list, key="julia_airports")
    
    df_f = df.copy()
    if selected_season != "All":
        df_f = df_f[df_f["season"] == selected_season]
    if selected_carriers:
        df_f = df_f[df_f["carrier_name"].isin(selected_carriers)]
    if selected_airports:
        df_f = df_f[df_f["airport_code"] == selected_airports]
    
    k1, k2 = st.columns(2)
    avg_delay = df_f["avg_delay_min"].mean() if not df_f.empty else 0
    avg_rate = df_f["delay_rate"].mean() * 0.01 if not df_f.empty else 0

    with k1:
        st.metric("Average Delay (min)", f"{avg_delay:.2f}")
    with k2:
        st.metric("% Flights Delayed (>15 min)", f"{avg_rate:.1%}")
    
    st.divider()
    
    group_var = None
    if len(selected_carriers) > 1:
        group_var = "carrier_name"
    elif len(selected_airports) > 1:
        group_var = "airport_code"
    
    st.subheader("Average Delay Time Trend")
    if not df_f.empty:
        if group_var:
            df_trend = (df_f.groupby(["date", group_var])["avg_delay_min"]
                .mean().reset_index().sort_values("date"))
            fig = px.line(df_trend, x="date", y="avg_delay_min", color=group_var, markers=True)
        else:
            df_trend = (df_f.groupby("date")["avg_delay_min"]
                .mean().reset_index().sort_values("date"))
            fig = px.line(df_trend, x="date", y="avg_delay_min", markers=True)
        
        fig.update_layout(yaxis_title="Delay (min)", xaxis_title="", template="plotly_white")
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("No data available for selected filters.")
    
    st.divider()
    st.subheader("Percentage of Flights Delayed (>15 min)")
    if not df_f.empty:
        if group_var:
            df_trend_rate = (df_f.groupby(["date", group_var])["delay_rate"]
                .mean().reset_index().sort_values("date"))
            fig2 = px.line(df_trend_rate, x="date", y="delay_rate", color=group_var, markers=True)
        else:
            df_trend_rate = (df_f.groupby("date")["delay_rate"]
                .mean().reset_index().sort_values("date"))
            fig2 = px.line(df_trend_rate, x="date", y="delay_rate", markers=True)
        
        fig2.update_layout(yaxis_title="Percentage", xaxis_title="", template="plotly_white")
        fig2.update_yaxes(tickformat=".1%")
        st.plotly_chart(fig2, width='stretch')
    else:
        st.warning("No data available for selected filters.")
