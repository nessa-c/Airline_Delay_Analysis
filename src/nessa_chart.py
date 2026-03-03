import streamlit as st
import pandas as pd
import plotly.express as px

def nessa_chart(df: pd.DataFrame) -> None:
    df = df.copy()

    df["airport_display"] = df['city'] + " (" + df['airport_code'] + ")"

    airport_risk = df.copy()
    airport_risk = airport_risk.groupby("airport_display").agg(
        total_flights=("arr_flights", "sum"),
        total_delays=("arr_del15", "sum")
    )
    airport_risk = airport_risk[airport_risk['total_flights'] >= 100000]
    airport_risk['delay_pct'] = airport_risk['total_delays'] / airport_risk['total_flights']
    top10_airports = airport_risk.sort_values('delay_pct', ascending=False).head(10).index.tolist()
        
    left, right = st.columns([1, 3])

    with left:
        airport = st.selectbox("Airport", [None] + top10_airports)
        airline_list = sorted(df['carrier_name'].unique()) if airport is None else sorted(df[df['airport_display'] == airport]['carrier_name'].unique())
        airline = st.selectbox("Airline", [None] + airline_list)
        season = st.selectbox("Season", [None, "Winter", "Spring", "Summer", "Fall"], placeholder="All Year Round")
        all_flights = st.checkbox("Include On-Time Flights", value=False)

    pie_df = df.copy()
    if airport:
        pie_df = pie_df[pie_df["airport_display"] == airport]
    if airline:
        pie_df = pie_df[pie_df["carrier_name"] == airline]
    if season:
        pie_df = pie_df[pie_df["season"] == season]
    if all_flights:
        pie_df["on_time_ct"] = pie_df["arr_flights"] - pie_df["arr_del15"]

    counts = ["carrier_ct", "weather_ct", "nas_ct", "security_ct", "late_aircraft_ct"]
    labels = ["Carrier", "Weather", "NAS", "Security", "Late Aircraft"]
    if all_flights:
        counts.append("on_time_ct")
        labels.append("On-Time")

    pie_df = pie_df.groupby("carrier_name")[counts].sum()
    total_flights = pie_df.sum(axis=1).sum()

    with right:
        if total_flights > 0:
            values = [pie_df[col].sum() / total_flights for col in counts]
        else:
            values = [0] * len(counts)

        cols = st.columns(len(labels))
        help_texts = {
            "Carrier": "Flights delayed due to airline-related issues (e.g., crew delays, maintenance, equipment problems).",
            "Weather": "Flights delayed because of significant weather conditions (e.g., thunderstorms, snow, fog).",
            "NAS": "Flights delayed due to National Airspace System issues (e.g., air traffic control, heavy traffic volume, systems issues).",
            "Security": "Flights delayed due to security-related factors (e.g., screening issues, security breaches).",
            "Late Aircraft": "Flights delayed because the aircraft arrived late from a previous flight.",
            "On-Time": "Flights not affected by delays",
        }

        flight_counts = {}

        for label, col in zip(labels, counts):
            flight_counts[label] = int(pie_df[col].sum())

        for col_obj, label, val in zip(cols, labels, values):
            with col_obj:
                st.metric(
                    label,
                    f"{val:.1%}",
                    help=help_texts[label],
                    height="stretch",
                )
                st.caption(f"{flight_counts[label]:,} flights")


        if total_flights > 0 and any(v != 0 for v in values):
            title = []
            if airline:
                airline_name = airline.rstrip(" Inc.")
                title.append(airline_name + " ")
            else:
                title.append("")
            if airport:
                airport_code = airport.split("(")[-1].rstrip(")")
                title.append(" at " + airport_code)
            else:
                title.append("")
            if season: 
                title.append(" in " + season + "")
            else:
                title.append("")

            if title[0] == "" and title[1] == "" and title[2] == "":
                title = "Delay Cause Breakdown"
            else:
                title = title[0] + "Delays" + title[1] + title[2]

            fig = px.pie(
                title=title + f" ({int(total_flights):,} flights)",
                values=values,
                names=labels,
                category_orders={"names": labels},
                color_discrete_sequence=px.colors.qualitative.Plotly_r,
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(template="plotly_white", title={'x': 0.42, 'y': 0.9, 'xanchor': 'center', 'yanchor': 'top', 'font': {'size': 18}})
            st.plotly_chart(fig, width="stretch")
        else:
            st.warning("No data available")

