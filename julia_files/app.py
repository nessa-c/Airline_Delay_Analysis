import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="Airline Delay Dashboard",
    layout="wide"
)

st.title("Airline Delay Dashboard")
st.caption(
    "Interactive trend analysis of average delay minutes and delay rate."
)

st.divider()

# ---------------------------------
# Load Data
# ---------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("../csv/delays_updated.csv")

    # Create date column if year/month exist
    if "year" in df.columns and "month" in df.columns:
        df["date"] = pd.to_datetime(
            df["year"].astype(str) + "-" + df["month"].astype(str) + "-01"
        )

    # Create delay_rate if not already created
    if "delay_rate" not in df.columns:
        df["delay_rate"] = df.apply(
            lambda x: x["arr_del15"] / x["arr_flights"]
            if x["arr_flights"] > 0 else 0,
            axis=1
        )

    return df

df = load_data()

# ---------------------------------
# Filters
# ---------------------------------
st.subheader("Filters")

c1, c2, c3 = st.columns(3)

with c1:
    seasons = ["All"] + sorted(df["season"].dropna().unique())
    selected_season = st.selectbox("Season", seasons)

with c2:
    carriers = sorted(df["carrier_name"].dropna().unique())
    selected_carriers = st.multiselect(
        "Carrier Name",
        carriers,
        default=[]
    )

with c3:
    airports = sorted(df["airport_code"].dropna().unique())
    selected_airports = st.multiselect(
        "Airport",
        airports,
        default=[]
    )

st.divider()

# ---------------------------------
# Apply Filters
# ---------------------------------
df_f = df.copy()

if selected_season != "All":
    df_f = df_f[df_f["season"] == selected_season]

if selected_carriers:
    df_f = df_f[df_f["carrier_name"].isin(selected_carriers)]

if selected_airports:
    df_f = df_f[df_f["airport_code"].isin(selected_airports)]

# ---------------------------------
# KPI Section
# ---------------------------------
k1, k2 = st.columns(2)

avg_delay = df_f["avg_delay_min"].mean() if not df_f.empty else 0
avg_rate = df_f["delay_rate"].mean() if not df_f.empty else 0

with k1:
    st.metric("Average Delay (minutes)", f"{avg_delay:.2f}")

with k2:
    st.metric("Delay Rate", f"{avg_rate:.1%}")

st.divider()

# ---------------------------------
# SMART GROUPING LOGIC
# ---------------------------------
group_var = None

if len(selected_carriers) > 1:
    group_var = "carrier_name"
elif len(selected_airports) > 1:
    group_var = "airport_code"

# ---------------------------------
# AVG DELAY TREND
# ---------------------------------
st.subheader("Trend of Average Delay Minutes")

if not df_f.empty:

    if group_var:
        df_trend = (
            df_f.groupby(["date", group_var])["avg_delay_min"]
            .mean()
            .reset_index()
            .sort_values("date")
        )

        fig = px.line(
            df_trend,
            x="date",
            y="avg_delay_min",
            color=group_var,
            markers=True
        )

    else:
        df_trend = (
            df_f.groupby("date")["avg_delay_min"]
            .mean()
            .reset_index()
            .sort_values("date")
        )

        fig = px.line(
            df_trend,
            x="date",
            y="avg_delay_min",
            markers=True
        )

    fig.update_layout(
        yaxis_title="Average Delay (minutes)",
        xaxis_title="Date",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No data available for selected filters.")

st.divider()

# ---------------------------------
# DELAY RATE TREND
# ---------------------------------
st.subheader("Trend of Delay Rate")

if not df_f.empty:

    if group_var:
        df_trend_rate = (
            df_f.groupby(["date", group_var])["delay_rate"]
            .mean()
            .reset_index()
            .sort_values("date")
        )

        fig2 = px.line(
            df_trend_rate,
            x="date",
            y="delay_rate",
            color=group_var,
            markers=True
        )

    else:
        df_trend_rate = (
            df_f.groupby("date")["delay_rate"]
            .mean()
            .reset_index()
            .sort_values("date")
        )

        fig2 = px.line(
            df_trend_rate,
            x="date",
            y="delay_rate",
            markers=True
        )

    fig2.update_layout(
        yaxis_title="Delay Rate",
        xaxis_title="Date",
        template="plotly_white"
    )

    fig2.update_yaxes(tickformat=".1%")

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("No data available for selected filters.")

# ---------------------------------
# Footer
# ---------------------------------
st.divider()
st.markdown(
    """
    **Design Note:**  
    This dashboard enables airline analysts to compare delay severity (avg delay minutes) 
    and delay frequency (delay rate) across carriers and airports.  
    Multi-line comparison automatically activates when multiple entities are selected.
    """
)