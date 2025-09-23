import os
import requests
import pandas as pd
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
    'fed_rate': 'FEDFUNDS',           # Federal Funds Rate
    'fed_balance_sheet': 'WALCL',     # Fed's Balance Sheet (Monetary Policy)
    'dxy': 'DTWEXBGS',                # US Dollar Index
    'gdp': 'GDPC1',                   # Gross Domestic Product ( 'GDPC1' for real GDP )
    'geopolitial_risk': 'USEPUINDXD', # Economic Policy Uncertainty Index for U.S.
    's&p500': 'SP500',                # S&P 500 Index
    'unemployment': 'UNRATE',         # Unemployment Rate
    'national_debt': 'GFDEGDQ188S',   # Federal Debt: Total Public Debt as Percent of Gross Domestic Product
    'consumer_confidence': 'UMCSENT', # University of Michigan: Consumer Sentiment Index / CONCCONF: Conference Board Consumer Confidence Index (Not seasonally adjusted) / CSCICP03USM665S: Consumer Opinion Survey: Confidence Indicator for the U.S.
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

def get_fred_data(series_id, limit=2):
    """Fetches the last few data points for a given series from FRED."""
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&limit={limit}&sort_order=desc"
    try:
        response = requests.get(url)
        data = response.json()
        if 'observations' in data and len(data['observations']) >= 2:
            # Get the two most recent values
            latest_value = float(data['observations'][0]['value'])
            previous_value = float(data['observations'][1]['value'])
            return latest_value, previous_value
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

    # 2. Interest Rates (Fed Funds)
    latest_rate, prev_rate = get_fred_data(FRED_SERIES_IDS['fed_rate'])
    if latest_rate and prev_rate:
        signals['Interest Rates'] = 'SELL' if latest_rate > prev_rate else 'BUY'
        
    # 3. Monetary Policy (Fed Balance Sheet)
    latest_bs, prev_bs = get_fred_data(FRED_SERIES_IDS['fed_balance_sheet'])
    if latest_bs and prev_bs:
        # Expanding balance sheet (QE) is a BUY signal
        signals['Monetary Policy'] = 'BUY' if latest_bs > prev_bs else 'SELL'

    # 4. Dollar Index (DXY)
    latest_dxy, prev_dxy = get_fred_data(FRED_SERIES_IDS['dxy'])
    if latest_dxy and prev_dxy:
        signals['DXY'] = 'SELL' if latest_dxy > prev_dxy else 'BUY'

    # 5. GDP Growth (GDPC1)
    latest_gdp, prev_gdp = get_fred_data(FRED_SERIES_IDS['gdp'])
    if latest_gdp and prev_gdp:
        signals['GDP'] = 'BUY' if latest_gdp > prev_gdp else 'SELL'

    # 6. Geopolitical Risk (USEPUINDXD)
    latest_geo, prev_geo = get_fred_data(FRED_SERIES_IDS['geopolitial_risk'])
    if latest_geo and prev_geo:
        signals['Geopolitical Risk'] = 'BUY' if latest_geo > prev_geo else 'SELL'

    # 7. s&p500 (SP500)
    latest_sp500, prev_sp500 = get_fred_data(FRED_SERIES_IDS['s&p500'])
    if latest_sp500 and prev_sp500:
        signals['SP500'] = 'BUY' if latest_sp500 > prev_sp500 else 'SELL'

    # 8. Unemployment
    latest_unemp, prev_unemp = get_fred_data(FRED_SERIES_IDS['unemployment'])
    if latest_unemp and prev_unemp:
        # Higher unemployment -> anticipates looser policy -> BUY
        signals['Unemployment'] = 'BUY' if latest_unemp > prev_unemp else 'SELL'

    # 9. National Debt
    latest_debt, prev_debt = get_fred_data(FRED_SERIES_IDS['national_debt'])
    if latest_debt and prev_debt:
        # Rising debt -> potential fiscal issues -> SELL
        signals['National Debt'] = 'BUY' if latest_debt > prev_debt else 'SELL'

    # 10. Consumer Confidence
    latest_conf, prev_conf = get_fred_data(FRED_SERIES_IDS['consumer_confidence'])
    if latest_conf and prev_conf:
        signals['Consumer Confidence'] = 'BUY' if latest_conf > prev_conf else 'SELL'

    # --- Add functions for the other 5 indicators here ---
    # For simplicity, we'll work with the 5 we've implemented.

    buy_count = list(signals.values()).count('BUY')
    sell_count = list(signals.values()).count('SELL')
    
    return signals, buy_count, sell_count

# --- MAIN EXECUTION ---

def main():
    print("Running macro factor analysis...")
    signals, buy_count, sell_count = analyze_signals()
    
    # Format the message
    message = "📈 *Macro Signal Report* 📉\n\n"
    for factor, signal in signals.items():
        emoji = "🟢" if signal == 'BUY' else "🔴"
        message += f"{emoji} *{factor}:* {signal}\n"
    
    message += f"\n*Summary:*\n"
    message += f"🟢 Buy Signals: *{buy_count}*\n"
    message += f"🔴 Sell Signals: *{sell_count}*\n\n"
    
    # --- TRIGGER LOGIC (e.g., 4 out of 5 for this example) ---
    if buy_count >= 4:
        message += "🚨 *MAJOR BUY SIGNAL DETECTED* 🚨"
        send_telegram_message(message)
    elif sell_count >= 4:
        message += "🚨 *MAJOR SELL SIGNAL DETECTED* 🚨"
        send_telegram_message(message)
    else:
        message += "Signal is neutral. No action required."
        print(message)
        # Optional: uncomment below to get a report even on neutral days
        send_telegram_message(message)

if __name__ == "__main__":
    main()
