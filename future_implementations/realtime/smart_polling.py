"""
Smart Polling Implementation - BACKUP PLAN
Update only when data is likely available (after market hours)

STATUS: Ready to deploy (copy to components/ when needed)
EFFORT: 2 hours
COST: Free
USE CASE: Daily trading dashboards, optimal API usage
"""

import streamlit as st
from datetime import datetime, time as dt_time, timedelta


def should_update_now():
    """
    Determine if we should fetch new data based on market hours

    Logic:
        - Daily indicators (S&P 500, etc.) update after market close (4 PM ET)
        - Don't update during market hours (data won't be there)
        - Update once per day after market close
        - Don't update on weekends

    Returns:
        bool: True if update is recommended
    """
    now = datetime.now()

    # Check if weekend
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False

    # Market hours: 9:30 AM - 4:00 PM ET
    # Data updates: After 4:00 PM ET
    market_close = dt_time(16, 0)  # 4:00 PM
    update_window_end = dt_time(23, 59)  # End of day

    current_time = now.time()

    # Only update after market close
    if market_close <= current_time <= update_window_end:
        return True

    return False


def setup_smart_update():
    """
    Smart update that only fetches when data is likely new

    Features:
        - Updates once per day after market close
        - Respects weekends (no updates)
        - Minimizes API calls
        - Shows status in sidebar

    Usage:
        # In app_enhanced.py, after loading data:
        from components.smart_polling import setup_smart_update
        setup_smart_update()
    """

    if should_update_now():
        # Check if we already updated today
        today = datetime.now().date()

        if 'last_update_date' not in st.session_state:
            st.session_state.last_update_date = None

        if st.session_state.last_update_date != today:
            st.sidebar.info("📥 Fetching today's market data...")
            st.cache_data.clear()
            st.session_state.last_update_date = today
            st.session_state.last_refresh = datetime.now()
            st.rerun()
        else:
            st.sidebar.success("✅ Already updated today")
    else:
        now = datetime.now()
        current_time = now.time()

        # Show helpful status message
        if now.weekday() >= 5:
            st.sidebar.caption("⏸️ Weekend - markets closed")
        elif current_time < dt_time(16, 0):
            next_update = datetime.combine(now.date(), dt_time(16, 0))
            hours_until = (next_update - now).total_seconds() / 3600
            st.sidebar.caption(f"⏸️ Market open - update at 4 PM ET ({hours_until:.1f}h)")
        else:
            st.sidebar.caption("✅ Using today's data")


def setup_configurable_polling(update_times=None):
    """
    Configurable polling at specific times

    Args:
        update_times: List of time objects when to update
                     Default: [4:00 PM, 9:00 AM] for market close and open

    Usage:
        from datetime import time
        setup_configurable_polling([
            time(9, 0),   # 9 AM
            time(16, 0),  # 4 PM
            time(20, 0)   # 8 PM
        ])
    """

    if update_times is None:
        update_times = [
            dt_time(9, 0),   # Morning update
            dt_time(16, 0),  # After market close
        ]

    now = datetime.now()
    current_time = now.time()

    # Find next update time
    next_update_time = None
    for update_time in sorted(update_times):
        if current_time < update_time:
            next_update_time = update_time
            break

    if next_update_time is None:
        # No more updates today, next is tomorrow's first update
        next_update_time = update_times[0]
        next_update = datetime.combine(now.date() + timedelta(days=1), next_update_time)
    else:
        next_update = datetime.combine(now.date(), next_update_time)

    # Check if we should update now
    for update_time in update_times:
        # Create a 5-minute window around each update time
        update_window_start = (datetime.combine(now.date(), update_time) - timedelta(minutes=2))
        update_window_end = (datetime.combine(now.date(), update_time) + timedelta(minutes=3))

        if update_window_start.time() <= current_time <= update_window_end.time():
            # Check if we already updated in this window
            update_key = f"updated_{update_time.hour}_{update_time.minute}"

            if not st.session_state.get(update_key, False):
                st.sidebar.info(f"📥 Scheduled update at {update_time.strftime('%I:%M %p')}")
                st.cache_data.clear()
                st.session_state[update_key] = True
                st.session_state.last_refresh = datetime.now()
                st.rerun()

    # Show next update time
    time_until = (next_update - now).total_seconds()
    hours = int(time_until / 3600)
    minutes = int((time_until % 3600) / 60)

    st.sidebar.caption(f"⏰ Next update: {next_update.strftime('%I:%M %p')} ({hours}h {minutes}m)")


# Example usage:
if __name__ == "__main__":
    st.title("Smart Polling Test")

    # Test smart update
    setup_smart_update()

    st.write(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"Day of week: {datetime.now().strftime('%A')}")

    if should_update_now():
        st.success("✅ Update window active")
    else:
        st.info("⏸️ Outside update window")
