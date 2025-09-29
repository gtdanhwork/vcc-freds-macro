import streamlit as st
import pandas as pd
import pandas_datareader.data as web
import datetime
import os

# --- Static Configuration for Dates and Series ---
# NOTE: This key MUST be set as an environment variable (FRED_API_KEY)
FRED_API_KEY = os.environ.get("FRED_API_KEY") 
SERIES_ID = "SP500"  # S&P 500 Index

# STATIC DATES (Updated to a static, two-month period in 2025)
STATIC_START_DATE = datetime.datetime(2025, 9, 1) 
STATIC_END_DATE = datetime.datetime(2025, 11, 1) 

# Default Y-Axis Limits 
DEFAULT_PRICE_MAX = 7000 
DEFAULT_PRICE_MIN = 4000

def fetch_and_process_fred_data(series_id, start_date, end_date):
    """
    Fetches economic data from FRED for the specified series ID and date range.
    The resulting DataFrame is optimized for Streamlit's line_chart, with Date as index.
    """
    if not FRED_API_KEY:
        # This case is handled in main(), but defensive return here is good.
        return pd.DataFrame() 

    st.info(f"Fetching data for **{series_id}** from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
    
    try:
        # Use pandas_datareader to fetch the time series data
        df = web.DataReader(series_id, 'fred', start=start_date, end=end_date)
        
        # Drop any rows with missing data (NaN)
        df = df.dropna()
        
        # Rename the column based on the series ID for the chart legend
        df.columns = [f'{series_id} Value']
        
        return df
    
    except Exception as e:
        # Displaying the full exception to the user helps with debugging
        st.error(f"❌ **Data Fetch Error:** Failed to retrieve data for {series_id}.")
        st.caption("Common reasons include a network issue, an incorrect API key, or a rate limit being hit.")
        st.exception(e) # Streamlit displays the detailed traceback
        return pd.DataFrame()


def main():
    """Streamlit application main function."""
    st.set_page_config(layout="wide")
    st.title(f"FRED Economic Data Visualization: {SERIES_ID}")
    
    # --- API Key Check & Troubleshooting ---
    if not FRED_API_KEY:
        st.error("🚨 **CRITICAL ERROR: FRED_API_KEY is not set.**")
        st.markdown("""
        **Please follow these steps to resolve the error:**
        1.  Go to the [FRED website] to get your free API key.
        2.  Set the key as an environment variable in your terminal before running the script:
            * **Linux/macOS:** `export FRED_API_KEY="YOUR_KEY_HERE"`
            * **Windows (CMD):** `set FRED_API_KEY="YOUR_KEY_HERE"`
            * **Windows (PowerShell):** `$env:FRED_API_KEY="YOUR_KEY_HERE"`
        3.  Run the application again: `streamlit run fred_sp500_app.py`
        """)
        return 

    # Determine the static dates used for the API call
    start_dt = STATIC_START_DATE
    end_dt = STATIC_END_DATE

    st.markdown(f"""
        Data Period: **{start_dt.strftime('%Y-%m-%d')}** to **{end_dt.strftime('%Y-%m-%d')}**. (Exactly two months in 2025)
    """)

    # --- Sidebar Inputs: Chart Configuration (Y-Axis) ---
    st.sidebar.header("Chart Y-Axis Limits")
    
    y_min = st.sidebar.number_input(
        "Minimum Value (Y-Axis)",
        value=DEFAULT_PRICE_MIN, 
        step=100
    )
    
    y_max = st.sidebar.number_input(
        "Maximum Value (Y-Axis)",
        value=DEFAULT_PRICE_MAX, 
        step=100
    )
    
    if y_min >= y_max:
        st.sidebar.error("Minimum value must be less than Maximum value.")
        return

    # --- Data Fetching ---
    data_df = fetch_and_process_fred_data(SERIES_ID, start_dt, end_dt)
    
    if data_df.empty:
        # This warning is displayed if data fetching failed but the API key was present.
        st.warning(f"Could not retrieve data for {SERIES_ID}. Check the console for the full exception details.")
        return

    # --- Visualization ---
    st.header(f"Line Graph: {SERIES_ID} Index Value")
    
    st.line_chart(
        data_df, 
        use_container_width=True,
        y_min=y_min,
        y_max=y_max
    )
    
    st.subheader("Raw Data (Sorted by Value: Highest to Lowest)")
    
    # --- NEW SORTING LOGIC ---
    # 1. Get the name of the value column dynamically
    value_column_name = data_df.columns[0]
    
    # 2. Sort the DataFrame by the value column in descending order
    sorted_df = data_df.sort_values(by=value_column_name, ascending=False)
    
    # 3. Display the sorted DataFrame
    st.dataframe(sorted_df.head(10)) 
    # --- END NEW SORTING LOGIC ---

if __name__ == '__main__':
    main()
