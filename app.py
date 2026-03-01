import streamlit as st
import pandas as pd
import plotly.express as px


def main() -> None:
    st.set_page_config(
        page_title="Airline Delay Dashboard",
        layout="wide"
    )

    # Add CSS for wider margins
    st.markdown("""
        <style>
            .block-container {
                padding: 1rem 15%; 
            }        
        </style>
        """, unsafe_allow_html=True)
    
    st.title("🛫 Airline Delay Analysis Dashboard")
    st.markdown("---")

    df = pd.read_csv("data/delaydata_final.csv")

    tab1, tab2, tab3 = st.tabs(["Delay Trends", "Delay Causes", "Airport Analysis"])

# Tab 1: Delay Trends
with tab1:
    st.header("Delay Trends")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        seasons = ["All"] + sorted(df_julia["season"].dropna().unique())
        selected_season = st.selectbox("Season", seasons, key="julia_season")
    with col2:
        carriers = sorted(df_julia["carrier_name"].dropna().unique())
        selected_carriers = st.multiselect("Carrier", carriers, key="julia_carriers")
    with col3:
        airport_list = sorted(df_julia["airport_code"].dropna().unique())
        selected_airports = st.multiselect("Airport", airport_list, key="julia_airports")
    
    df_julia_f = df_julia.copy()
    if selected_season != "All":
        df_julia_f = df_julia_f[df_julia_f["season"] == selected_season]
    if selected_carriers:
        df_julia_f = df_julia_f[df_julia_f["carrier_name"].isin(selected_carriers)]
    if selected_airports:
        df_julia_f = df_julia_f[df_julia_f["airport_code"].isin(selected_airports)]
    
    k1, k2 = st.columns(2)
    avg_delay = df_julia_f["avg_delay_min"].mean() if not df_julia_f.empty else 0
    avg_rate = df_julia_f["delay_rate"].mean() if not df_julia_f.empty else 0
    with k1:
        st.metric("Average Delay (min)", f"{avg_delay:.2f}")
    with k2:
        st.metric("Delay Rate", f"{avg_rate:.1%}")
    
    st.divider()
    
    group_var = None
    if len(selected_carriers) > 1:
        group_var = "carrier_name"
    elif len(selected_airports) > 1:
        group_var = "airport_code"
    
    st.subheader("Average Delay Trend")
    if not df_julia_f.empty:
        if group_var:
            df_trend = (df_julia_f.groupby(["date", group_var])["avg_delay_min"]
                .mean().reset_index().sort_values("date"))
            fig = px.line(df_trend, x="date", y="avg_delay_min", color=group_var, markers=True)
        else:
            df_trend = (df_julia_f.groupby("date")["avg_delay_min"]
                .mean().reset_index().sort_values("date"))
            fig = px.line(df_trend, x="date", y="avg_delay_min", markers=True)
        
        fig.update_layout(yaxis_title="Delay (min)", xaxis_title="", template="plotly_white")
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("No data available for selected filters.")
    
    st.divider()
    st.subheader("Delay Rate Trend")
    if not df_julia_f.empty:
        if group_var:
            df_trend_rate = (df_julia_f.groupby(["date", group_var])["delay_rate"]
                .mean().reset_index().sort_values("date"))
            fig2 = px.line(df_trend_rate, x="date", y="delay_rate", color=group_var, markers=True)
        else:
            df_trend_rate = (df_julia_f.groupby("date")["delay_rate"]
                .mean().reset_index().sort_values("date"))
            fig2 = px.line(df_trend_rate, x="date", y="delay_rate", markers=True)
        
        fig2.update_layout(yaxis_title="Rate", xaxis_title="", template="plotly_white")
        fig2.update_yaxes(tickformat=".1%")
        st.plotly_chart(fig2, width='stretch')
    else:
        st.warning("No data available for selected filters.")

# Tab 2: Delay Causes
with tab2:
    st.header("Delay Causes Breakdown")
    
    airport_risk = df_nessa.groupby("airport_name_cleansed").agg(
        total_flights=("arr_flights", "sum"),
        total_delays=("arr_del15", "sum")
    )
    airport_risk = airport_risk[airport_risk['total_flights'] >= 100000]
    airport_risk['delay_pct'] = airport_risk['total_delays'] / airport_risk['total_flights']
    top10_airports = airport_risk.sort_values('delay_pct', ascending=False).head(10).index.tolist()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        airport_nessa = st.selectbox("Airport", [None] + top10_airports, key="nessa_airport")
    with col2:
        airline_list = sorted(df_nessa['carrier_name'].unique()) if airport_nessa is None else sorted(df_nessa[df_nessa['airport_name_cleansed'] == airport_nessa]['carrier_name'].unique())
        airline_nessa = st.selectbox("Airline", [None] + airline_list, key="nessa_airline")
    with col3:
        season_nessa = st.selectbox("Season", [None, "Winter", "Spring", "Summer", "Fall"], key="nessa_season")
    
    pie_df = df_nessa.copy()
    if airport_nessa:
        pie_df = pie_df[pie_df["airport_name_cleansed"] == airport_nessa]
    if airline_nessa:
        pie_df = pie_df[pie_df["carrier_name"] == airline_nessa]
    
    if season_nessa:
        season_map = {"Winter": [12, 1, 2], "Spring": [3, 4, 5], "Summer": [6, 7, 8], "Fall": [9, 10, 11]}
        pie_df = pie_df[pie_df["month"].isin(season_map[season_nessa])]
    
    pie_df = pie_df.groupby("carrier_name")[["arr_flights", "carrier_ct", "weather_ct", "nas_ct", "security_ct", "late_aircraft_ct"]].sum()
    total_flights = pie_df["arr_flights"].sum()
    
    if total_flights > 0:
        values = [
            pie_df["carrier_ct"].sum() / total_flights,
            pie_df["weather_ct"].sum() / total_flights,
            pie_df["nas_ct"].sum() / total_flights,
            pie_df["security_ct"].sum() / total_flights,
            pie_df["late_aircraft_ct"].sum() / total_flights
        ]
        labels = ["Carrier", "Weather", "NAS", "Security", "Late Aircraft"]
        
        fig = px.pie(values=values, names=labels, color_discrete_sequence=["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, width='stretch')
        
        st.divider()
        col1, col2, col3, col4, col5 = st.columns(5)
        for col, label, val in zip([col1, col2, col3, col4, col5], labels, values):
            with col:
                st.metric(label, f"{val:.1%}")
    else:
        st.warning("No data available")

with tab3:
    st.header("Airport Analysis")
    
    airport_display = df_jordan['city'] + " (" + df_jordan['airport_code'] + ")"
    airline_list = ["All"] + sorted(df_jordan["carrier_name"].unique())
    airport_list = sorted(airport_display.unique().tolist())
    
    left, right = st.columns([1, 3])

    ## Render Filters
    with left:
        airline = st.selectbox("Airline", airline_list, index=0, key="jordan_airline")
        airport = st.multiselect("Airport", airport_list, key="jordan_airport")


        min_rt, max_rt = int(df_jordan["year"].min()), int(df_jordan["year"].max())
        rt_range = st.slider(
            "Years",
            min_value=min_rt,
            max_value=max_rt,
            value=(min_rt, max_rt),
            step=1,
        )

        month_range = st.select_slider(
            "Months",
            options=[
                "1-Jan",
                "2-Feb",
                "3-Mar",
                "4-Apr",
                "5-May",
                "6-Jun",
                "7-Jul",
                "8-Aug",
                "9-Sep",
                "10-Oct",
                "11-Nov",
                "12-Dec",
            ],
            value=("1-Jan", "12-Dec")
        )

    ## Apply Filters
    df_f = df_jordan.copy()
    df_f["airport_display"] = df_f['city'] + " (" + df_f['airport_code'] + ")"
    if airline != "All":
        df_f = df_f[df_f["carrier_name"] == airline]

    #### Apply airport multiselect filter
    if len(airport) != 0:
        df_f = df_f[df_f["airport_display"].isin(airport)]
    else:
        df_f = df_f.copy()

    #### Apply year slider filter
    lo, hi = rt_range
    df_f = df_f[(df_f["year"] >= lo) & (df_f["year"] <= hi)]

    #### Apply month slider filter
    lo_month, hi_month = month_range
    lo_int = int(lo_month.split("-")[0])
    hi_int = int(hi_month.split("-")[0])
    df_f = df_f[(df_f["month"] >= lo_int) & (df_f["month"] <= hi_int)]

    with right:
        ## KPI
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Delay (min)", f"{df_f['arr_delay'].mean():.1f}" if not df_f.empty else "N/A")
        col2.metric("Total Flights", f"{len(df_f):,}" if not df_f.empty else "0")
        if "arr_del15" in df_f.columns and not df_f.empty:
            delay_pct = (df_f["arr_del15"] == 1).sum() / len(df_f) * 100
            col3.metric("Delayed %", f"{delay_pct:.1f}%")
        else:
            col3.metric("Delayed %", "N/A")
        
        st.divider()

        ## Chart
        if not df_f.empty:
            agg = df_f.groupby("airport_code")["arr_delay"].median().head(10)
            fig = px.bar(x=agg.index, y=agg.values, labels={"x": "Airport", "y": "Median Delay (min)"}, title="Median Delay (min) by Airport")
            fig.update_layout(template="plotly_white",
                              title={
                                  'y': 0.9,
                                  'x': 0.535,
                                  'xanchor': 'center',
                                  'yanchor': 'top'}
                              )
            st.plotly_chart(fig, width='stretch')
    
    st.divider()
    st.subheader("Data")
    if not df_f.empty:
        st.dataframe(df_f, width='stretch')
    else:
        st.info("No data available")

if __name__ == "__main__":
    main()
    st.markdown(
        """
        **Design Note**  
        This dashboard provides data analysts to explore airline delay patterns with different filters and visualizations.
        The layout is designed to be clean and intuitive, with interactive elements that allow users to dive into into specific aspects of the data.
        """
    )