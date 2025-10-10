"""
Enhanced monitoring module with restored signal analysis
Builds on the original monitor.py with trading signal logic
"""

import os
import requests
import pandas as pd
import json
from datetime import date
from dotenv import load_dotenv
from seriesIds import FRED_SERIES_IDS
from utils import calculate_signal, aggregate_signals, calculate_statistics

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
FRED_API_KEY = os.getenv('FRED_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# --- TELEGRAM SUPPORT FUNCTIONS ---

def send_telegram_message(message):
    """Sends a message to your Telegram bot."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not configured")
        return None

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, json=payload)
        print("Telegram message sent!")
        return response.json()
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return None

# --- FRED DATA FETCHING FUNCTIONS (Same as original) ---

def get_fred_data(series_id, limit=10000):
    """
    Fetch historical data for a series from FRED API

    Args:
        series_id: FRED series identifier
        limit: Maximum number of observations to fetch

    Returns:
        list: Observations data or empty list on error
    """
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&limit={limit}&sort_order=asc"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            print(f"--- API ERROR for {series_id} (Status: {response.status_code}) ---")
            try:
                error_message = response.json().get('error_message', response.text)
                print(f"FRED Message: {error_message}")
            except json.JSONDecodeError:
                print(f"Raw Response: {response.text}")
            print("---------------------------------------------------------")
            return []

        data = response.json()

        if 'error_code' in data:
            print(f"--- FRED DATA ERROR for {series_id} ---")
            print(f"Error Message: {data.get('error_message')}")
            print("----------------------------------------")
            return []

        if 'observations' in data and data['observations']:
            return data['observations']
        else:
            print(f"--- WARNING: Series {series_id} returned 200 OK but NO observations data. ---")
            return []

    except Exception as e:
        print(f"Could not fetch data for {series_id}: {e}")

    return []

def fetch_all_fred_data() -> dict:
    """
    Fetch data for ALL indicators (called by Streamlit cache)

    Returns:
        dict: {series_id: [{Date, Value}, ...]}
    """
    all_series_data = {}
    print("\n--- Starting FRED Data Batch Fetch ---")

    for friendly_name, series_id in FRED_SERIES_IDS.items():
        print(f"Fetching data for: {friendly_name} ({series_id})")

        data = get_fred_data(series_id)

        # Transform structure and filter missing values ('.')
        new_data = [
            {"Date": item["date"], "Value": item["value"]}
            for item in data if item["value"] != '.'
        ]

        all_series_data[series_id] = new_data

    print("--- FRED Data Initial Fetch Complete ---\n")
    return all_series_data

# --- ENHANCED SIGNAL ANALYSIS ---

def analyze_signals(all_data_dict):
    """
    Analyze trading signals for all indicators

    Args:
        all_data_dict: Dictionary of {series_id: data} from cache

    Returns:
        dict: Analysis results with signals and statistics
    """
    results = {
        'signals': {},
        'statistics': {},
        'overall_signal': 'NEUTRAL',
        'buy_count': 0,
        'sell_count': 0,
        'neutral_count': 0
    }

    # Analyze each indicator
    for indicator_key, series_id in FRED_SERIES_IDS.items():
        data = all_data_dict.get(series_id, [])

        if not data:
            results['signals'][indicator_key] = 'NEUTRAL'
            results['statistics'][indicator_key] = {}
            continue

        # Convert to DataFrame
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        df.dropna(subset=['Value'], inplace=True)

        # Calculate signal
        signal = calculate_signal(indicator_key, df)
        results['signals'][indicator_key] = signal

        # Calculate statistics
        stats = calculate_statistics(df)
        results['statistics'][indicator_key] = stats

    # Aggregate overall signal
    overall, buy_count, sell_count, neutral_count = aggregate_signals(results['signals'])
    results['overall_signal'] = overall
    results['buy_count'] = buy_count
    results['sell_count'] = sell_count
    results['neutral_count'] = neutral_count

    return results

def format_signal_message(analysis_results):
    """
    Format analysis results into a readable message

    Args:
        analysis_results: Results from analyze_signals()

    Returns:
        str: Formatted message for display or Telegram
    """
    from config import INDICATOR_METADATA
    from utils import get_signal_emoji

    message = "📈 *Bitcoin Macro Signal Report* 📉\n\n"

    # Overall signal
    overall = analysis_results['overall_signal']
    buy_count = analysis_results['buy_count']
    sell_count = analysis_results['sell_count']
    neutral_count = analysis_results['neutral_count']
    total = buy_count + sell_count + neutral_count

    message += f"*Overall Signal:* {get_signal_emoji(overall)} *{overall}*\n"
    message += f"({buy_count}/{total} indicators bullish)\n\n"

    # Individual signals
    message += "*Indicator Breakdown:*\n"

    for indicator_key, signal in analysis_results['signals'].items():
        emoji = get_signal_emoji(signal)
        name = INDICATOR_METADATA.get(indicator_key, {}).get('name', indicator_key)
        stats = analysis_results['statistics'].get(indicator_key, {})
        change = stats.get('change_30d', 0)

        message += f"{emoji} *{name}*: {signal}"
        if change != 0:
            message += f" ({change:+.1f}% 30d)"
        message += "\n"

    # Summary
    message += f"\n*Summary:*\n"
    message += f"🟢 Buy Signals: *{buy_count}*\n"
    message += f"🔴 Sell Signals: *{sell_count}*\n"
    message += f"🟡 Neutral Signals: *{neutral_count}*\n"

    return message

def check_and_send_alerts(analysis_results, send_neutral=False):
    """
    Check if signal thresholds are met and send Telegram alerts

    Args:
        analysis_results: Results from analyze_signals()
        send_neutral: Whether to send neutral signals (default False)

    Returns:
        bool: True if alert was sent
    """
    overall = analysis_results['overall_signal']
    message = format_signal_message(analysis_results)

    # Add alert emoji for strong signals
    if overall == 'STRONG BUY':
        message += "\n🚨 *MAJOR BUY SIGNAL DETECTED* 🚨"
        send_telegram_message(message)
        return True
    elif overall == 'STRONG SELL':
        message += "\n🚨 *MAJOR SELL SIGNAL DETECTED* 🚨"
        send_telegram_message(message)
        return True
    elif overall in ['BUY', 'SELL']:
        message += f"\n⚠️ *{overall} Signal Active* ⚠️"
        send_telegram_message(message)
        return True
    elif send_neutral:
        message += "\n✅ Signal is neutral. No strong action required."
        send_telegram_message(message)
        return True
    else:
        print(message)
        print("\nNo strong signals detected. Monitoring continues...")
        return False

# --- MAIN EXECUTION ---

def main():
    """
    Main function for standalone execution
    Fetches data and analyzes signals
    """
    print("Fetching all FRED data...")
    all_data = fetch_all_fred_data()

    print("\nAnalyzing signals...")
    results = analyze_signals(all_data)

    print("\nGenerating report...")
    check_and_send_alerts(results, send_neutral=True)

if __name__ == "__main__":
    main()
