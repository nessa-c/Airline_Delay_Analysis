import streamlit as st
import pandas as pd
import plotly.express as px

def jordan_chart(df: pd.DataFrame) -> None:    
    airport_display = df['city'] + " (" + df['airport_code'] + ")"
    airline_list = ["All"] + sorted(df["carrier_name"].unique())
    airport_list = sorted(airport_display.unique().tolist())
    
    left, right = st.columns([1, 3])

    ## Render Filters
    with left:
        airline = st.selectbox("Airline", airline_list, index=0, key="jordan_airline")
        airport = st.multiselect("Airport", airport_list, key="jordan_airport")


        min_rt, max_rt = int(df["year"].min()), int(df["year"].max())
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
        view_mode_time = st.radio("View By:", ["Minutes", "Hours"], horizontal=True, key="view_mode_time")



    ## Apply Filters
    df_f = df.copy()
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
        col1, col2, col3, col4 = st.columns(4)
        if view_mode_time == "Minutes":
            col1.metric("Median Delay (min)", f"{df_f['arr_delay'].median():,.0f}" if not df_f.empty else "N/A")
            col2.metric("Average Delay (min)", f"{df_f['arr_delay'].mean():,.0f}" if not df_f.empty else "N/A")
        else:
            col1.metric("Median Delay (hours)", f"{df_f['arr_delay'].median()/60:,.1f}" if not df_f.empty else "N/A")
            col2.metric("Average Delay (hours)", f"{df_f['arr_delay'].mean()/60:,.1f}" if not df_f.empty else "N/A")

        col3.metric("Total Flights", f"{len(df_f):,}" if not df_f.empty else "0")

        if "arr_del15" in df_f.columns and not df_f.empty:
            delay_pct = (df_f["arr_del15"] == 1).sum() / len(df_f) * 100
            col4.metric("Delayed %", f"{delay_pct:.1f}%")
        else:
            col4.metric("Delayed %", "N/A")

        st.divider()

        ## Chart
        if not df_f.empty:
            agg = df_f.groupby("airport_code")["arr_delay"].median()

            y_name = "Median Delay (min)"
            title = "Median Delay (min) by Airport"
            y_value = agg.values

            if view_mode_time == "Hours":
                y_name = "Median Delay (hours)"
                title = "Median Delay (hours) by Airport"
                y_value = agg.values/60

            fig = px.bar(x=agg.index, y=y_value, labels={"x": "Airport", "y": y_name}, title=title, color=agg.index)
            fig.update_layout(template="plotly_white",
                              title={
                                  'y': 0.9,
                                  'x': 0.535,
                                  'xanchor': 'center',
                                  'yanchor': 'top'}
                              )
            st.plotly_chart(fig, width='stretch')

        if not df_f.empty:
            agg = df_f.groupby("airport_code")["arr_delay"].mean()

            y_name_mean = "Average Delay (min)"
            title = "Average Delay (min) by Airport"
            y_value = agg.values

            if view_mode_time == "Hours":
                y_name = "Average Delay (hours)"
                title = "Average Delay (hours) by Airport"
                y_value = agg.values / 60

            fig = px.bar(x=agg.index, y=y_value, labels={"x": "Airport", "y": y_name}, title=title, color=agg.index)
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