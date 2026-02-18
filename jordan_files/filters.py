import pandas as pd
import streamlit as st


def render_filters(df: pd.DataFrame) -> dict:
    """Rendering filter widgets and returning the chosen values."""
    st.sidebar.header("Filters")

    airport_name = df['city'] + " (" + df['airport_code'] + ")"
    airline_list = ["All"] + sorted(df["carrier_name"].unique().tolist())
    airport_list = ["All"] + sorted(airport_name.unique().tolist())
    #complaint_types = sorted(df["complaint_type"].unique().tolist())

    airline = st.sidebar.selectbox("Airline", airline_list, index=0)
    airport = st.sidebar.selectbox("Airport", airport_list, index=0)

    #complaint = st.sidebar.selectbox("Complaint Type", ["All"] + complaint_types, index=0)

    # Response time slider
    min_rt, max_rt = int(df["month"].min()), int(df["month"].max())
    rt_range = st.sidebar.slider(
        "Months",
        min_value=0,
        max_value=max_rt,
        value=(0, max_rt),
        step=1,
    )

    # TODO (IN-CLASS): Add a checkbox toggle to cap outliers (e.g., at 99th percentile)
    cap_outliers = st.sidebar.checkbox("Cap extreme response times", value=False)

    return {
        "airline": airline,
        "airport": airport,
        #"complaint": complaint,
        "rt_range": rt_range,
        "cap_outliers": cap_outliers,
    }


def apply_filters(df: pd.DataFrame, selections: dict) -> pd.DataFrame:
    """Applying filter selections to the dataframe."""
    out = df.copy()

    if selections["airline"] != "All":
        airline = 'carrier_name'
        out = out[out[airline] == selections["airline"]]

    if selections["airport"] != "All":
        airport_name = out['city'] + " (" + out['airport_code'] + ")"
        out = out[airport_name == selections["airport"]]

   # if selections["complaint"] != "All":
        #out = out[out["complaint_type"] == selections["complaint"]]

    lo, hi = selections["rt_range"]
    out = out[(out["month"] >= lo) & (out["month"] <= hi)]

    return out.reset_index(drop=True)
