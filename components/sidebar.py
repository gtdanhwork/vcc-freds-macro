"""
Sidebar components for dashboard controls
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from config import TIME_PERIODS


def render_sidebar():
    """
    Render the sidebar with all controls

    Returns:
        dict: Dictionary containing all sidebar settings
            - start_date: Selected start date
            - limit: Max data points
            - show_table: Boolean for table display
            - show_statistics: Boolean for statistics display
    """
    with st.sidebar:
        st.header("⚙️ Settings")

        # Refresh button
        if st.button("🔄 Refresh Data", width="stretch"):
            st.cache_data.clear()
            st.rerun()

        st.markdown("---")

        # Time period selection
        st.subheader("📅 Time Period")
        period_preset = st.selectbox(
            "Quick Select",
            list(TIME_PERIODS.keys()),
            index=2  # Default to "Last 6 Months"
        )

        if period_preset != 'Custom':
            days = TIME_PERIODS[period_preset]
            default_start_date = date.today() - timedelta(days=days)
        else:
            default_start_date = date.today() - timedelta(days=365)

        start_date = st.date_input(
            "Start Date",
            value=default_start_date,
            max_value=date.today()
        )

        limit = st.number_input(
            "Max Data Points",
            min_value=10,
            max_value=10000,
            value=500,
            step=50
        )

        st.markdown("---")

        # Display options
        st.subheader("🎨 Display Options")
        show_table = st.checkbox("Show Data Table", value=False)
        show_statistics = st.checkbox("Show Statistics", value=True)

        # Import data monitor here to show cache status
        from .data_monitor import render_cache_status, render_update_frequency_info

        # Cache status
        render_cache_status()

        # Update frequency information
        render_update_frequency_info()

    return {
        'start_date': start_date,
        'limit': limit,
        'show_table': show_table,
        'show_statistics': show_statistics
    }


def render_filter_info(start_date, limit, data_count):
    """
    Display information about current filters

    Args:
        start_date: Filter start date
        limit: Max data points limit
        data_count: Actual number of data points loaded
    """
    st.caption(f"📅 Showing data from {start_date.strftime('%Y-%m-%d')} | 📊 {data_count} data points loaded (limit: {limit})")
