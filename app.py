"""
Bitcoin Macro Factor Dashboard - Enhanced Version
Clean, modular architecture with separated components

Features:
- 4-tab interface (Overview, Analysis, Signals, Comparison)
- Modular code structure for easy maintenance
- Real-time FRED data integration
- Trading signal analysis

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from monitor_enhanced import fetch_all_fred_data
from components import (
    render_sidebar,
    render_overview_tab,
    render_analysis_tab,
    render_signals_tab,
    render_comparison_tab
)

# Page configuration
st.set_page_config(
    page_title="Bitcoin Macro Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
    }
    .bullish { color: #00C853; font-weight: bold; }
    .bearish { color: #FF1744; font-weight: bold; }
    .neutral { color: #FFB300; font-weight: bold; }
    .big-number { font-size: 32px; font-weight: bold; }
    .indicator-name { font-size: 14px; color: #B0B0B0; }
    .change-positive { color: #00C853; }
    .change-negative { color: #FF1744; }
    </style>
""", unsafe_allow_html=True)


# --- DATA CACHING ---
@st.cache_data(ttl=3600 * 24)  # Cache for 24 hours
def load_all_data():
    """Load and cache all FRED data"""
    return fetch_all_fred_data()


# --- DATA FILTERING ---
def get_filtered_data(series_id, start_date, limit):
    """
    Filter cached data based on user input

    Args:
        series_id: FRED series identifier
        start_date: Filter start date
        limit: Maximum number of data points

    Returns:
        DataFrame: Filtered data with Date and Value columns
    """
    data = st.session_state.all_data.get(series_id, [])

    if not data:
        return pd.DataFrame({"Date": [], "Value": []})

    # Filter by date
    start_date_str = start_date.strftime("%Y-%m-%d")
    date_filtered_data = [
        item for item in data
        if item["Date"] >= start_date_str
    ]

    # Limit to most recent N values
    final_data = date_filtered_data[-limit:]

    # Convert to DataFrame
    df = pd.DataFrame(final_data, columns=["Date", "Value"])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df.dropna(subset=['Value'], inplace=True)

    return df


# --- INITIALIZE SESSION STATE ---
if "all_data" not in st.session_state:
    with st.spinner("📊 Loading historical FRED data... (First load may take a minute)"):
        st.session_state.all_data = load_all_data()
        st.session_state.last_refresh = pd.Timestamp.now()


# --- RENDER SIDEBAR ---
sidebar_settings = render_sidebar()

# Extract settings
start_date = sidebar_settings['start_date']
limit = sidebar_settings['limit']
show_table = sidebar_settings['show_table']
show_statistics = sidebar_settings['show_statistics']


# --- MAIN CONTENT ---
st.title("📈 Bitcoin Macro Factor Dashboard")
st.markdown("Monitor key macroeconomic indicators for Bitcoin trading signals")

# Tab navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🔍 Detailed Analysis",
    "🎯 Trading Signals",
    "📈 Comparison"
])

# --- RENDER TABS ---
with tab1:
    render_overview_tab(get_filtered_data, start_date, limit)

with tab2:
    render_analysis_tab(get_filtered_data, start_date, limit, show_table, show_statistics)

with tab3:
    render_signals_tab(st.session_state.all_data)

with tab4:
    render_comparison_tab(get_filtered_data, start_date, limit)

# Footer
st.markdown("---")
st.caption("Data source: Federal Reserve Economic Data FRED")
