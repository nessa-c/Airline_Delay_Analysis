import streamlit as st
import pandas as pd

from src import julia_chart
from src import nessa_chart
from src import jordan_chart

def main() -> None:
    st.set_page_config(
        page_title="Airline Delay Causes",
        layout="wide",
    )

    st.title("Airline Delay Causes Dashboard")
    st.caption("Airline Delay app for Filter & Fly")

    st.markdown("""
        <style>
            .block-container {
                padding: 1rem 15%; 
            }        
        </style>
        """, unsafe_allow_html=True)
    
    # Load data
    df = pd.read_csv("data/delaydata_final.csv")

    tab1, tab2, tab3 = st.tabs(["Delay Trends", "Delay Causes", "Airport Analysis"])

    with tab1:
        st.header("Delay Trends")
        st.write("This tab will show delay trends over time with various filters.")
        julia_chart.julia_chart(df)

    with tab2:
        st.header("Delay Causes")
        st.write("This tab will show delay causes breakdown.")
        nessa_chart.nessa_chart(df)

    with tab3:
        st.header("Airport Analysis")
        st.write("This tab will allow analysis by airport and airline.")
        jordan_chart.jordan_chart(df)

if __name__ == "__main__":
    main()