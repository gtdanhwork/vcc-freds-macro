"""
Data freshness monitoring component
Shows when data was last updated and FRED update frequencies
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# FRED update frequencies for each indicator
FRED_UPDATE_FREQUENCIES = {
    's&p500': {'freq': 'Daily', 'days': 1, 'source': 'Market data'},
    'fed_rate': {'freq': 'Daily', 'days': 1, 'source': 'Federal Reserve'},
    'dxy': {'freq': 'Daily', 'days': 1, 'source': 'Market data'},
    'geopolitial_risk': {'freq': 'Daily', 'days': 1, 'source': 'CBOE (VIX)'},
    'fed_balance_sheet': {'freq': 'Weekly', 'days': 7, 'source': 'Federal Reserve'},
    'cpi': {'freq': 'Monthly', 'days': 30, 'source': 'Bureau of Labor Statistics'},
    'unemployment': {'freq': 'Monthly', 'days': 30, 'source': 'Bureau of Labor Statistics'},
    'consumer_confidence': {'freq': 'Monthly', 'days': 30, 'source': 'University of Michigan'},
    'gdp': {'freq': 'Quarterly', 'days': 90, 'source': 'Bureau of Economic Analysis'},
    'national_debt': {'freq': 'Quarterly', 'days': 90, 'source': 'US Treasury'}
}


def get_data_age(df):
    """
    Calculate how old the latest data point is

    Args:
        df: DataFrame with Date column

    Returns:
        tuple: (latest_date, days_old, is_stale)
    """
    if df.empty:
        return None, None, True

    latest_date = pd.to_datetime(df['Date'].iloc[-1])
    days_old = (datetime.now() - latest_date).days
    is_stale = days_old > 7  # Consider stale if > 7 days old

    return latest_date, days_old, is_stale


def render_data_freshness_badge(indicator_key, df):
    """
    Display a small badge showing data freshness

    Args:
        indicator_key: Indicator identifier
        df: DataFrame with data
    """
    latest_date, days_old, is_stale = get_data_age(df)

    if latest_date is None:
        st.caption("⚠️ No data")
        return

    freq_info = FRED_UPDATE_FREQUENCIES.get(indicator_key, {'freq': 'Unknown', 'days': 1})

    # Color code based on freshness
    if days_old == 0:
        color = "🟢"
        status = "Today"
    elif days_old <= freq_info['days']:
        color = "🟢"
        status = f"{days_old}d ago"
    elif days_old <= freq_info['days'] * 2:
        color = "🟡"
        status = f"{days_old}d ago"
    else:
        color = "🔴"
        status = f"{days_old}d ago"

    st.caption(f"{color} {status} | {freq_info['freq']} updates")


def render_cache_status():
    """
    Display cache status in sidebar
    Shows when data was last refreshed
    """
    if "last_refresh" in st.session_state:
        last_refresh = st.session_state.last_refresh
        now = pd.Timestamp.now()
        time_since_refresh = now - last_refresh

        hours = int(time_since_refresh.total_seconds() / 3600)
        minutes = int((time_since_refresh.total_seconds() % 3600) / 60)

        # Cache expires after 24 hours
        cache_expires_in = timedelta(hours=24) - time_since_refresh
        hours_left = int(cache_expires_in.total_seconds() / 3600)

        st.markdown("---")
        st.subheader("📊 Data Status")

        # Last refresh
        if hours == 0:
            st.success(f"✅ Refreshed {minutes} min ago")
        else:
            st.info(f"🔄 Refreshed {hours}h {minutes}m ago")

        # Cache expiry
        if hours_left <= 1:
            st.warning(f"⏰ Cache expires in {hours_left}h")
        else:
            st.caption(f"Cache expires in {hours_left}h")

        # Next auto-refresh
        next_refresh = last_refresh + timedelta(hours=24)
        st.caption(f"Next auto-refresh: {next_refresh.strftime('%Y-%m-%d %H:%M')}")


def render_update_frequency_info():
    """
    Display information about FRED update frequencies
    """
    with st.expander("ℹ️ Data Update Frequencies"):
        st.markdown("""
        **How often does data update?**

        Your dashboard caches data for **24 hours**. FRED sources update at different frequencies:

        **Daily Updates:**
        - S&P 500, Fed Rate, Dollar Index (DXY), VIX

        **Weekly Updates:**
        - Fed Balance Sheet (Thursdays)

        **Monthly Updates:**
        - CPI, Unemployment, Consumer Confidence

        **Quarterly Updates:**
        - GDP, National Debt

        💡 **Tip**: Click "🔄 Refresh Data" to manually fetch latest data before cache expires.
        """)

        # Show latest data dates for all indicators
        st.markdown("**Latest Data Dates:**")

        if "all_data" in st.session_state:
            from seriesIds import FRED_SERIES_IDS
            from config import INDICATOR_METADATA

            data_freshness = []

            for indicator_key, series_id in FRED_SERIES_IDS.items():
                data = st.session_state.all_data.get(series_id, [])
                if data:
                    latest_date = data[-1]['Date']
                    metadata = INDICATOR_METADATA.get(indicator_key, {})
                    freq_info = FRED_UPDATE_FREQUENCIES.get(indicator_key, {})

                    data_freshness.append({
                        'Indicator': metadata.get('name', indicator_key),
                        'Latest Date': latest_date,
                        'Frequency': freq_info.get('freq', 'Unknown')
                    })

            if data_freshness:
                df_fresh = pd.DataFrame(data_freshness)
                st.dataframe(df_fresh, width="stretch", hide_index=True)


def render_realtime_disclaimer():
    """
    Display disclaimer about real-time data
    """
    st.info("""
    ℹ️ **Data Freshness Notice**

    - Dashboard caches data for **24 hours**
    - FRED updates vary by indicator (daily/weekly/monthly/quarterly)
    - This is **not real-time** data
    - Use "🔄 Refresh Data" button to manually update
    """)
