import streamlit as st
import pandas as pd

from src import julia_chart
from src import nessa_chart
from src import jordan_chart
from src import nessa_chart2

st.set_page_config(
    page_title="Airline Delay Causes",
    layout="wide",
)
tooltip_style = """
<style>
div[data-baseweb="tooltip"] {
  width: 12rem;
}
</style>
"""
st.markdown(tooltip_style,unsafe_allow_html=True)

st.title("Airline Delay Causes Dashboard")
st.caption("Airline Delay app for Filter & Fly")

st.markdown("""
    <style>
        .block-container {
            padding: 2rem 15%; 
        }        
    </style>
    """, unsafe_allow_html=True)

# Load data
df = pd.read_csv("data/delaydata_final.csv")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["About","Delay Trends", "Delay Causes", "Airport Analysis", "Delay Comparisons", "Data Table"])

with tab1:
    st.header("About This Dashboard")
    st.markdown("""
        This dashboard provides insights into airline delays, their causes, and trends over time. 
        Use the tabs to explore different aspects of the data:
        - **Delay Trends**: Analyze how average delays and delay rates have changed over time with various filters.
        - **Delay Causes**: See the breakdown of delay causes based on selected filters.
        - **Airport Analysis**: Explore delay patterns by airport and airline.
        - **Delay Comparisons**: Compare delay times across different airports and airlines.
        - **Data Table**: View the raw data used for analysis.
    """)

with tab2:
    st.header("Delay Trends")
    st.write("This tab will show delay trends over time with various filters.")
    julia_chart.julia_chart(df)

with tab3:
    st.header("Delay Causes")
    st.write("This tab will show delay causes breakdown.")
    nessa_chart.nessa_chart(df)

with tab4:
    st.header("Airport Analysis")
    st.write("This tab will allow analysis by airport and airline.")
    jordan_chart.jordan_chart(df)

with tab5:
    st.header("Delay Comparisons")
    st.write("This tab will allow comparison of delay times across different airports and airlines.")
    nessa_chart2.nessa_chart(df)

with tab6:
    st.header("Data Table")
    if not df.empty:
        st.dataframe(df, width='stretch')
    else:
        st.info("No data available")