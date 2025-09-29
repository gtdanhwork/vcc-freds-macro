import os
import requests
import pandas as pd
import json
from datetime import date
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
FRED_API_KEY = os.getenv('FRED_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# FRED Series IDs for our indicators
# Find more here: https://fred.stlouisfed.org/
FRED_SERIES_IDS = {
    'cpi': 'CPIAUCSL',                # Consumer Price Index
}

# --- HELPER FUNCTIONS ---

def send_telegram_message(message):
    """Sends a message to your Telegram bot."""
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

def get_fred_data(series_id, limit=30, observations_start='2025-08-01', freq='m'):
    """Fetches the last few data points for a given series from FRED."""
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&limit={limit}"
    try:
        response = requests.get(url)
        data = response.json()
        if 'observations' in data and len(data['observations']) >= 29:
            # Get the two most recent values
            return data
    except Exception as e:
        print(f"Could not fetch data for {series_id}: {e}")
    return None, None

# --- SIGNAL ANALYSIS LOGIC ---

def analyze_signals():
    """Analyzes all macro factors and returns buy/sell counts."""
    signals = {}
    
    # 1. Inflation (CPI)
    latest_cpi, prev_cpi = get_fred_data(FRED_SERIES_IDS['cpi'])
    if latest_cpi and prev_cpi:
        signals['CPI'] = 'BUY' if latest_cpi > prev_cpi else 'SELL'

    # --- Add functions for the other 5 indicators here ---
    # For simplicity, we'll work with the 5 we've implemented.

    buy_count = list(signals.values()).count('BUY')
    sell_count = list(signals.values()).count('SELL')
    
    return signals, buy_count, sell_count



# --- MAIN EXECUTION ---]

def main():
    print("Running macro factor analysis...")
    # signals, buy_count, sell_count = analyze_signals()
    data = get_fred_data(FRED_SERIES_IDS['cpi'], 2)

    print(data)
    
    # Format the message
    message = "📈 *Macro Signal Report* 📉\n\n"
    for factor, signal in signals.items():
        emoji = "🟢" if signal == 'BUY' else "🔴"
        message += f"{emoji} *{factor}:* {signal}\n"
    
    message += f"\n*Summary:*\n"
    message += f"🟢 Buy Signals: *{buy_count}*\n"
    message += f"🔴 Sell Signals: *{sell_count}*\n\n"
    
    # --- TRIGGER LOGIC (e.g., 4 out of 5 for this example) ---
    if buy_count >= 8:
        message += "🚨 *MAJOR BUY SIGNAL DETECTED* 🚨"
        send_telegram_message(message)
    elif sell_count >= 8:
        message += "🚨 *MAJOR SELL SIGNAL DETECTED* 🚨"
        send_telegram_message(message)
    else:
        message += "Signal is neutral. No action required."
        print(message)
        # Optional: uncomment below to get a report even on neutral days
        send_telegram_message(message)

if __name__ == "__main__":
    main()
