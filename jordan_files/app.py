import streamlit as st
import pandas as pd

from data import load_data
from filters import render_filters, apply_filters
from charts import plot_airport_delay_bar
from layouts import header_metrics, body_layout_tabs


# -----------------------------
# IMT 561 Streamlit Airline Delay Analysis
# -----------------------------
#
#
#
#


def main() -> None:
    st.set_page_config(
        page_title="Airline Delay Causes",
        layout="wide",
    )

    st.title("Airline Delay Causes Dashboard")
    st.caption("Airline Delay app for Filter & Fly")

    # ✅ Data loading (cached)
    #df = load_data("data/sample.csv")
    df = load_data('../csv/delays_reduced.csv')


    # -------------------------
    # Filters (sidebar by default)
    # -------------------------
    # render_filters returns a dictionary of user selections
    selections = render_filters(df)

    # apply_filters returns a filtered dataframe based on selections
    df_f = apply_filters(df, selections)

    # -------------------------
    # Header metrics
    # -------------------------
    header_metrics(df_f)

    st.divider()

    # -------------------------
    # Main body
    # -------------------------
    # Tabs layout by default (3 tabs)
    tab_choice = st.radio(
        "Choose a layout for the body (lab demo uses tabs; assignment can remix):",
        ["Tabs", "Two Columns"],
        horizontal=True,
    )

    if tab_choice == "Tabs":
        body_layout_tabs(df_f)
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Median Delay Minutes by Airport")
            plot_airport_delay_bar(df_f)

        with col2:
            st.subheader("Filtered Rows")
            st.dataframe(df_f, width='stretch', height=420)


if __name__ == "__main__":
    main()
