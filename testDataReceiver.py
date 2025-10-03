import os
import sys
from dotenv import load_dotenv

# --- Check for Dependencies ---
try:
    # This should import the core batch function from your main monitor.py
    from monitor import fetch_all_fred_data
    # This should import your final list of IDs
    from seriesIds import FRED_SERIES_IDS 
except ImportError as e:
    print(f"Error: Could not import necessary components. Check your files.")
    print(f"Details: {e}")
    sys.exit(1)

# Load environment variables (API key)
load_dotenv()
FRED_API_KEY = os.getenv('FRED_API_KEY')

if not FRED_API_KEY:
    print("Error: FRED_API_KEY not found in .env file. Cannot run test.")
    sys.exit(1)

def run_batch_test():
    """
    Executes the fetch_all_fred_data function and prints a diagnostic summary
    of the retrieved data size for each indicator.
    """
    print("\n" + "="*50)
    print("        RUNNING FULL BATCH FETCH TEST      ")
    print("="*50)
    
    # Execute the function that calls the FRED API 10 times
    all_series_data = fetch_all_fred_data()
    
    # --- Print Summary Results ---
    print("\n--- Diagnostic Summary ---")
    
    failed_series = []
    
    # Iterate through the expected IDs and report the results
    for friendly_name, series_id in FRED_SERIES_IDS.items():
        data = all_series_data.get(series_id, [])
        data_count = len(data)
        
        if data_count > 0:
            print(f"✅ SUCCESS: {friendly_name:<20} ({series_id}): {data_count} observations")
            # Print last observation to confirm recent data
            print(f"            Last Date: {data[-1]['Date']}, Value: {data[-1]['Value']}")
        else:
            print(f"❌ FAILURE: {friendly_name:<20} ({series_id}): 0 observations")
            failed_series.append(friendly_name)

    print("\n" + "="*50)
    if not failed_series:
        print("        ALL 10 INDICATORS FETCHED SUCCESSFULLY      ")
    else:
        print(f"        WARNING: {len(failed_series)} SERIES FAILED TO LOAD      ")
        print(f"        Failed series: {', '.join(failed_series)}")
        
    print("="*50)

if __name__ == "__main__":
    run_batch_test()