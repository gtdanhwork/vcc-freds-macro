"""
Auto-Refresh Implementation - BACKUP PLAN
Simple auto-refresh every N minutes

STATUS: Ready to deploy (copy to components/ when needed)
EFFORT: 30 minutes
COST: Free
USE CASE: Internal dashboards, 5-15 minute updates
"""

import streamlit as st
from datetime import datetime, timedelta


def setup_auto_refresh(interval_seconds=300):
    """
    Auto-refresh the dashboard every N seconds

    Args:
        interval_seconds: Refresh interval (default 300 = 5 minutes)

    Usage:
        # In app_enhanced.py, after loading data:
        from components.auto_refresh import setup_auto_refresh
        setup_auto_refresh(interval_seconds=300)  # 5 minutes

    WARNING:
        - Hits FRED API more frequently
        - May reach rate limits with many users
        - Full page reload (resets user state)
    """

    # Method 1: JavaScript auto-reload (simple but loses state)
    st.markdown(f"""
    <script>
        // Auto-reload every {interval_seconds} seconds
        setTimeout(function() {{
            window.location.reload();
        }}, {interval_seconds * 1000});
    </script>
    """, unsafe_allow_html=True)

    # Show countdown in sidebar
    if 'refresh_start_time' not in st.session_state:
        st.session_state.refresh_start_time = datetime.now()

    elapsed = (datetime.now() - st.session_state.refresh_start_time).total_seconds()
    remaining = max(0, interval_seconds - elapsed)

    minutes = int(remaining / 60)
    seconds = int(remaining % 60)

    st.sidebar.caption(f"🔄 Auto-refresh in {minutes}m {seconds}s")


def setup_smart_auto_refresh(interval_seconds=300):
    """
    Smarter auto-refresh using Streamlit rerun (preserves state)

    Args:
        interval_seconds: Refresh interval

    Pros:
        - Doesn't lose user's current state
        - Smoother UX than full page reload

    Cons:
        - More complex
        - Still hits API frequently
    """

    # Initialize last refresh time
    if 'last_auto_refresh' not in st.session_state:
        st.session_state.last_auto_refresh = datetime.now()

    # Check if it's time to refresh
    time_since_refresh = (datetime.now() - st.session_state.last_auto_refresh).total_seconds()

    if time_since_refresh >= interval_seconds:
        # Clear cache and refresh
        st.cache_data.clear()
        st.session_state.last_auto_refresh = datetime.now()
        st.rerun()

    # Show countdown
    remaining = interval_seconds - time_since_refresh
    minutes = int(remaining / 60)
    seconds = int(remaining % 60)

    st.sidebar.caption(f"🔄 Next update in {minutes}m {seconds}s")

    # Important: Add small sleep to prevent CPU spinning
    import time
    time.sleep(1)


# Example usage:
if __name__ == "__main__":
    st.title("Auto-Refresh Test")

    # Test auto-refresh
    setup_auto_refresh(interval_seconds=60)  # 1 minute for testing

    st.write(f"Current time: {datetime.now().strftime('%H:%M:%S')}")
    st.write("Page will auto-refresh in 60 seconds")
