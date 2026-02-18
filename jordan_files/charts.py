import pandas as pd
import plotly.express as px
import streamlit as st


def plot_airport_delay_bar(df: pd.DataFrame) -> None:
    """Plotting median delay by airport."""
    if df.empty:
        st.info("No rows match your filters.")
        return
    x_val = 'airport_code'
    y_val = 'arr_delay'
    df_agg = (
        df.groupby([x_val], as_index=False)[y_val]
        .median()
        #.to_frame()
        #.reset_index()
    )
    fig = px.bar(
        df_agg,
        x=x_val,
        y=y_val,
        title=None
    )
    st.plotly_chart(fig, width='stretch')

def plot_response_hist(df: pd.DataFrame) -> None:
    """Plotting a simple histogram of response times."""
    if df.empty:
        st.info("No rows match your filters.")
        return

    fig = px.histogram(
        df,
        x="response_time_days",
        nbins=30,
        title=None,
    )
    st.plotly_chart(fig, width='stretch')


def plot_borough_bar(df: pd.DataFrame) -> None:
    """Plotting median response time by borough."""
    if df.empty:
        st.info("No rows match your filters.")
        return

    agg = (
        df.groupby("borough", as_index=False)["response_time_days"]
        .median()
        .rename(columns={"response_time_days": "median_response_days"})
        .sort_values("median_response_days", ascending=False)
    )

    fig = px.bar(
        agg,
        x="borough",
        y="median_response_days",
        title=None,
    )
    st.plotly_chart(fig, width='stretch')
