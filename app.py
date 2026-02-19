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

# Add CSS for wider margins
st.markdown("""
    <style>
        .main {
            max-width: 80%;
        }
        .block-container {
            padding: 1rem 15%; 
        }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------
# Load Data (Cached)
# ---------------------------------
@st.cache_data(show_spinner=False)
def load_data_jordan():
    """Load Jordan's reduced delays data"""
    return pd.read_csv("csv/delays_reduced.csv")

@st.cache_data(show_spinner=False)
def load_data_julia():
    """Load Julia's updated delays data with trend analysis"""
    df = pd.read_csv("csv/delays_updated.csv")
    
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

@st.cache_data(show_spinner=False)
def load_data_nessa():
    """Load Nessa's transformed data for delay cause analysis"""
    df = pd.read_csv("csv/delays_transformed.csv")
    df = df[(df['year'] <= 2019) & (df['year'] >= 2014)]
    return df

# Load all datasets
df_jordan = load_data_jordan()
df_julia = load_data_julia()
df_nessa = load_data_nessa()

# ---------------------------------
# Page Title and Navigation
# ---------------------------------
st.title("🛫 Comprehensive Airline Delay Analysis Dashboard")
st.markdown("---")

# Create tabs for each team's analysis
tab1, tab2, tab3 = st.tabs(["Delay Trends (Julia)", "Delay Causes (Nessa)", "Airport Analysis (Jordan)"])

# =================================
# TAB 1: JULIA'S DELAY TRENDS ANALYSIS
# =================================
with tab1:
    st.header("Trend Analysis of Average Delay Minutes and Delay Rate")
    st.caption("Interactive analysis comparing delay severity and frequency across carriers and airports")
    
    # Filters for Julia's section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        seasons = ["All"] + sorted(df_julia["season"].dropna().unique())
        selected_season = st.selectbox("Season", seasons, key="julia_season")
    
    with col2:
        carriers = sorted(df_julia["carrier_name"].dropna().unique())
        selected_carriers = st.multiselect(
            "Carrier Name",
            carriers,
            default=[],
            key="julia_carriers"
        )
    
    with col3:
        airports = sorted(df_julia["airport_code"].dropna().unique())
        selected_airports = st.multiselect(
            "Airport",
            airports,
            default=[],
            key="julia_airports"
        )
    
    # Apply filters
    df_julia_f = df_julia.copy()
    
    if selected_season != "All":
        df_julia_f = df_julia_f[df_julia_f["season"] == selected_season]
    
    if selected_carriers:
        df_julia_f = df_julia_f[df_julia_f["carrier_name"].isin(selected_carriers)]
    
    if selected_airports:
        df_julia_f = df_julia_f[df_julia_f["airport_code"].isin(selected_airports)]
    
    # KPI Section
    k1, k2 = st.columns(2)
    
    avg_delay = df_julia_f["avg_delay_min"].mean() if not df_julia_f.empty else 0
    avg_rate = df_julia_f["delay_rate"].mean() if not df_julia_f.empty else 0
    
    with k1:
        st.metric("Average Delay (minutes)", f"{avg_delay:.2f}")
    
    with k2:
        st.metric("Delay Rate", f"{avg_rate:.1%}")
    
    st.divider()
    
    # Smart grouping logic
    group_var = None
    if len(selected_carriers) > 1:
        group_var = "carrier_name"
    elif len(selected_airports) > 1:
        group_var = "airport_code"
    
    # Average delay trend
    st.subheader("Trend of Average Delay Minutes")
    
    if not df_julia_f.empty:
        if group_var:
            df_trend = (
                df_julia_f.groupby(["date", group_var])["avg_delay_min"]
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
                df_julia_f.groupby("date")["avg_delay_min"]
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
            template="plotly_white",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("No data available for selected filters.")
    
    st.divider()
    
    # Delay rate trend
    st.subheader("Trend of Delay Rate")
    
    if not df_julia_f.empty:
        if group_var:
            df_trend_rate = (
                df_julia_f.groupby(["date", group_var])["delay_rate"]
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
                df_julia_f.groupby("date")["delay_rate"]
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
            template="plotly_white",
            hovermode="x unified"
        )
        
        fig2.update_yaxes(tickformat=".1%")
        
        st.plotly_chart(fig2, width='stretch')
    else:
        st.warning("No data available for selected filters.")
    
    st.divider()
    st.markdown(
        """
        **Design Note:**  
        This section enables airline analysts to compare delay severity (avg delay minutes) 
        and delay frequency (delay rate) across carriers and airports.  
        Multi-line comparison automatically activates when multiple entities are selected.
        """
    )

# =================================
# TAB 2: NESSA'S DELAY CAUSES ANALYSIS
# =================================
with tab2:
    st.header("Delay Causes Breakdown Analysis")
    st.caption("Analyze the distribution of delay causes: Carrier, Weather, NAS, Security, and Late Aircraft")
    
    # Get top 10 airports by delay percentage
    airport_risk = df_nessa.groupby("airport_name_cleansed", as_index=False).agg(
        total_flights=("arr_flights", "sum"),
        total_delays=("arr_del15", "sum")
    )
    airport_risk = airport_risk[airport_risk['total_flights'] >= 100000]
    airport_risk['delay_pct'] = airport_risk['total_delays'] / airport_risk['total_flights']
    top10_airports = airport_risk.sort_values('delay_pct', ascending=False).head(10)['airport_name_cleansed'].tolist()
    
    # Filters for Nessa's section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        airport_nessa = st.selectbox(
            "Select Airport",
            index=None,
            placeholder="Any Airport",
            options=top10_airports,
            key="nessa_airport"
        )
    
    with col2:
        if airport_nessa is not None:
            airline_options = sorted(df_nessa[df_nessa['airport_name_cleansed'] == airport_nessa]['carrier_name'].unique())
        else:
            airline_options = sorted(df_nessa['carrier_name'].unique())
        
        airline_nessa = st.selectbox(
            "Select Airline",
            index=None,
            placeholder="Any Airline",
            options=airline_options,
            key="nessa_airline"
        )
    
    with col3:
        season_nessa = st.selectbox(
            "Select Season",
            index=None,
            placeholder="All Year",
            options=['Winter (Dec-Feb)', 'Spring (Mar-May)', 'Summer (June-Aug)', 'Fall (Sept-Nov)'],
            key="nessa_season"
        )
    
    # Apply filters
    pie_df = df_nessa.copy()
    
    if airport_nessa is not None:
        pie_df = pie_df[pie_df["airport_name_cleansed"].str.contains(airport_nessa, case=False, na=False)]
    
    if airline_nessa is not None:
        pie_df = pie_df[pie_df["carrier_name"].str.contains(airline_nessa, case=False, na=False)]
    
    if season_nessa is not None:
        if 'Winter' in season_nessa:
            pie_df = pie_df[pie_df["month"].isin([12, 1, 2])]
        elif 'Spring' in season_nessa:
            pie_df = pie_df[pie_df["month"].isin([3, 4, 5])]
        elif 'Summer' in season_nessa:
            pie_df = pie_df[pie_df["month"].isin([6, 7, 8])]
        elif 'Fall' in season_nessa:
            pie_df = pie_df[pie_df["month"].isin([9, 10, 11])]
    
    # Aggregate data
    pie_df = (pie_df.groupby("carrier_name", as_index=False)[["arr_flights", 'arr_del15', 'carrier_ct', 'weather_ct', 'nas_ct', 'security_ct', 'late_aircraft_ct']].sum())
    pie_df.insert(1, 'on_time', pie_df['arr_flights'] - pie_df['arr_del15'])
    
    total_flights = pie_df["arr_flights"].sum()
    
    if total_flights > 0:
        carrier_pct = pie_df["carrier_ct"].sum() / total_flights
        weather_pct = pie_df["weather_ct"].sum() / total_flights
        nas_pct = pie_df["nas_ct"].sum() / total_flights
        security_pct = pie_df["security_ct"].sum() / total_flights
        late_aircraft_pct = pie_df["late_aircraft_ct"].sum() / total_flights
        
        labels = ["Carrier", "Weather", "NAS", "Security", "Late Aircraft"]
        values = [carrier_pct, weather_pct, nas_pct, security_pct, late_aircraft_pct]
        
        # Build title
        title_parts = ["Delay Causes (2014-2019)"]
        if airport_nessa is not None:
            title_parts.append(f"at {airport_nessa}")
        if airline_nessa is not None:
            title_parts.append(f"with {airline_nessa}")
        if season_nessa is not None:
            title_parts.append(f"in {season_nessa}")
        
        fig = px.pie(
            values=values,
            names=labels,
            title=" ".join(title_parts),
            color_discrete_sequence=["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"]
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(template="plotly_white", hovermode="closest")
        
        st.plotly_chart(fig, width='stretch')
        
        # Display summary statistics
        st.divider()
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Carrier Delays", f"{carrier_pct:.1%}")
        with col2:
            st.metric("Weather Delays", f"{weather_pct:.1%}")
        with col3:
            st.metric("NAS Delays", f"{nas_pct:.1%}")
        with col4:
            st.metric("Security Delays", f"{security_pct:.1%}")
        with col5:
            st.metric("Late Aircraft", f"{late_aircraft_pct:.1%}")
    else:
        st.warning("No data available for selected filters.")

# =================================
# TAB 3: JORDAN'S AIRPORT ANALYSIS
# =================================
with tab3:
    st.header("Airport Delay Analysis")
    st.caption("Filter and analyze delay patterns by airport and airline")
    
    # Create airport name display
    airport_name_display = df_jordan['city'] + " (" + df_jordan['airport_code'] + ")"
    airline_list_j = ["All"] + sorted(df_jordan["carrier_name"].unique().tolist())
    airport_list_j = ["All"] + sorted(airport_name_display.unique().tolist())
    
    # Create left and right columns for layout
    left_col, right_col = st.columns([1, 3])
    
    # Filters for Jordan's section (on left)
    with left_col:
        st.subheader("Filters")
        
        airline_j = st.selectbox(
            "Airline",
            airline_list_j,
            index=0,
            key="jordan_airline"
        )
        
        airport_j = st.selectbox(
            "Airport",
            airport_list_j,
            index=0,
            key="jordan_airport"
        )
        
        # Response time slider
        min_rt, max_rt = int(df_jordan["month"].min()), int(df_jordan["month"].max())
        rt_range = st.slider(
            "Months",
            min_value=min_rt,
            max_value=max_rt,
            value=(min_rt, max_rt),
            step=1,
            key="jordan_months"
        )
    
    # Apply filters
    df_jordan_f = df_jordan.copy()
    
    if airline_j != "All":
        df_jordan_f = df_jordan_f[df_jordan_f["carrier_name"] == airline_j]
    
    if airport_j != "All":
        airport_name_display_f = df_jordan_f['city'] + " (" + df_jordan_f['airport_code'] + ")"
        df_jordan_f = df_jordan_f[airport_name_display_f == airport_j]
    
    lo, hi = rt_range
    df_jordan_f = df_jordan_f[(df_jordan_f["month"] >= lo) & (df_jordan_f["month"] <= hi)]
    
    # Display visualizations on right
    with right_col:
        # Display key metrics
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if not df_jordan_f.empty:
                avg_arr_delay = df_jordan_f["arr_delay"].mean()
                st.metric("Average Arrival Delay (min)", f"{avg_arr_delay:.1f}")
            else:
                st.metric("Average Arrival Delay (min)", "N/A")
        
        with col2:
            if not df_jordan_f.empty:
                total_flights = len(df_jordan_f)
                st.metric("Total Flights", f"{total_flights:,}")
            else:
                st.metric("Total Flights", "0")
        
        with col3:
            if not df_jordan_f.empty and "arr_del15" in df_jordan_f.columns:
                delay_count = (df_jordan_f["arr_del15"] == 1).sum()
                delay_pct = (delay_count / len(df_jordan_f)) * 100 if len(df_jordan_f) > 0 else 0
                st.metric("Flights Delayed (>15min)", f"{delay_pct:.1f}%")
            else:
                st.metric("Flights Delayed (>15min)", "N/A")
        
        st.divider()
        
        # Median delay by airport chart
        st.subheader("Median Arrival Delay by Airport")
        
        if not df_jordan_f.empty:
            df_agg = df_jordan_f.groupby("airport_code", as_index=False)["arr_delay"].median()
            
            fig = px.bar(
                df_agg,
                x="airport_code",
                y="arr_delay",
                title=None,
                labels={"airport_code": "Airport", "arr_delay": "Median Delay (minutes)"}
            )
            
            fig.update_layout(
                template="plotly_white",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No rows match your filters.")
    
    st.divider()
    
    # Data table (full width)
    st.subheader("Filtered Data")
    
    if not df_jordan_f.empty:
        st.dataframe(df_jordan_f, width='stretch', height=400)
    else:
        st.info("No data to display for the selected filters.")
