import pandas as pd
import streamlit as st

from src.charts import plot_airport_delay_bar
from src.charts import plot_response_hist, plot_borough_bar


def header_metrics(df: pd.DataFrame) -> None:
    """Rendering header metrics. Placeholder values are intentional."""
    c1, c2, c3 = st.columns(3)

    # TODO (IN-CLASS): Replace these placeholders with real metrics from df
    # Suggestions:
    # - Total complaints (len(df))
    # - Median response time
    # - % from Web vs Phone vs App (pick one)
    risk = df['arr_del15'] / df['arr_flights']
    with c1:
        st.metric("Risk", "TODO")
    with c2:
        st.metric("Airport Delay Medians", "TODO")
    with c3:
        st.metric("Most Common Delay", "TODO")


def body_layout_tabs(df: pd.DataFrame) -> None:
    """Tabs layout with 3 default tabs."""
    t1, t2, t3 = st.tabs(["By Airport", "To Do", "To Do"])

    with t1:
        st.subheader("Median Delay Minutes by Airport")
        plot_airport_delay_bar(df)


    with t2:
        st.subheader("Median Response Time by Borough")
        #plot_borough_bar(df)


    with t3:
        st.subheader("Filtered Rows")
        #st.dataframe(df, width='stretch', height=480)

