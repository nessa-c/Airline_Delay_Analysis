import streamlit as st
import pandas as pd
import plotly.express as px

def nessa_chart2(df: pd.DataFrame) -> None:
    delays = ["carrier_delay", "weather_delay", "nas_delay", "security_delay", "late_aircraft_delay"]
    labels = ["Carrier", "Weather", "NAS", "Security", "Late Aircraft"]

    df = df.copy()
    df["airport_display"] = df["city"] + " (" + df["airport_code"] + ")"

    left, right = st.columns([1, 3])

    with left:
        airport = st.multiselect("Airport", sorted(df["airport_display"].unique()), placeholder="All Airports")
        filtered = df[df["airport_display"].isin(airport)] if airport else df
        airline = st.multiselect("Airline", sorted(filtered["carrier_name"].unique()), placeholder="All Airlines")
        delay_type = st.multiselect("Delay Type", labels, placeholder="All Delay Types")
        view_mode = st.radio("View By:", ["Airline", "Airport"], horizontal=True, key="view_mode")

    dot_df = df.copy()
    if airport: dot_df = dot_df[dot_df["airport_display"].isin(airport)]
    if airline: dot_df = dot_df[dot_df["carrier_name"].isin(airline)]

    kpi_df = dot_df.copy()
    delay_map = dict(zip(labels, delays))
    if delay_type:
        for label, col in delay_map.items():
            if label not in delay_type:
                dot_df[col] = 0

    y_col = "carrier_name" if view_mode == "Airline" else "airport_display"
    scatter_df = dot_df.groupby(y_col, as_index=False)[delays].sum()
    scatter_df["delays"] = scatter_df[delays].sum(axis=1)
    scatter_df = scatter_df.sort_values("delays", ascending=True)
    help_texts = {
        "Carrier": "Flights delayed due to airline-related issues (e.g., crew delays, maintenance, equipment problems).",
        "Weather": "Flights delayed because of significant weather conditions (e.g., thunderstorms, snow, fog).",
        "NAS": "Flights delayed due to National Airspace System issues (e.g., air traffic control, heavy traffic volume, systems issues).",
        "Security": "Flights delayed due to security-related factors (e.g., screening issues, security breaches).",
        "Late Aircraft": "Flights delayed because the aircraft arrived late from a previous flight.",
    }
    with right:
        cols = st.columns(len(labels))
        for col_obj, label in zip(cols, labels):
            total = int(kpi_df[delay_map[label]].sum())
            with col_obj:
                st.metric(
                    label=f"{label} Delays",
                    value=f"{total/1_000_000:.1f}M" if total >= 1_000_000 else f"{total/1_000:.1f}K" if total >= 1_000 else f"{total:,}",
                    help=help_texts[label]
                )
                st.markdown(
                    f"""
                    <div style='margin-top:-2rem; font-size:14px; color:gray;'>total minutes</div>
                    """,
                    unsafe_allow_html=True
                )
        if scatter_df.empty:
            st.warning("No data available for this selection.")
            return
        delay_label_map = dict(zip(delays, labels))

        melt_df = (
            scatter_df
            .melt(id_vars=[y_col], value_vars=delays, var_name="delay_type", value_name="delay_minutes")
            .assign(delay_type=lambda x: x["delay_type"].map(delay_label_map))
            .query("delay_minutes > 0")
        )

        fig = px.scatter(
            melt_df, x="delay_minutes", y=y_col,
            color="delay_type", symbol="delay_type", hover_name=y_col,
            labels={"delay_minutes": "Delay Time (Minutes)", "delay_type": "Delay Type"},
            category_orders={"delay_type": labels},
            color_discrete_sequence=px.colors.qualitative.Plotly_r
        )
        fig.update_traces(marker=dict(size=18, line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'))
        fig.update_layout(yaxis_title=view_mode, height=500)
        

        st.plotly_chart(fig, width="stretch")