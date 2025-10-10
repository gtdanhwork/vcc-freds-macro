"""
WebSocket Streaming Example - BACKUP PLAN
Real-time data streaming using WebSockets (REQUIRES PAID API)

STATUS: Template only (requires API subscription)
EFFORT: 1-2 weeks full implementation
COST: $50-500/month for API
USE CASE: Professional trading platforms, real-time needs
"""

import streamlit as st
import json
import threading
from datetime import datetime

"""
IMPORTANT: This is a TEMPLATE, not a working implementation!

To use WebSocket streaming:
1. Choose a real-time data provider:
   - Alpha Vantage ($50-500/month)
   - Polygon.io ($29-999/month)
   - Finnhub ($0-400/month)
   - IEX Cloud ($0-2000/month)

2. Sign up and get API key

3. Install websocket library:
   pip install websocket-client

4. Adapt this template to your chosen provider

5. Test thoroughly before production
"""


# Example 1: Alpha Vantage WebSocket (Template)
def setup_alphavantage_stream(api_key):
    """
    Stream real-time stock data from Alpha Vantage

    Args:
        api_key: Your Alpha Vantage API key

    Note: This is a TEMPLATE. Alpha Vantage WebSocket requires paid plan.
    """
    import websocket

    # WebSocket URL (example - check Alpha Vantage docs for actual URL)
    ws_url = f"wss://ws.alphavantage.co/stream?apikey={api_key}"

    def on_message(ws, message):
        """Handle incoming data"""
        try:
            data = json.loads(message)

            # Update session state with new data
            if 'realtime_data' not in st.session_state:
                st.session_state.realtime_data = {}

            # Store latest price
            symbol = data.get('symbol')
            price = data.get('price')

            if symbol and price:
                st.session_state.realtime_data[symbol] = {
                    'price': price,
                    'timestamp': datetime.now(),
                    'data': data
                }

                # Trigger Streamlit rerun to update UI
                st.rerun()

        except Exception as e:
            st.error(f"Error processing message: {e}")

    def on_error(ws, error):
        """Handle errors"""
        st.error(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        """Handle connection close"""
        st.warning("WebSocket connection closed")

    def on_open(ws):
        """Handle connection open"""
        st.success("WebSocket connected")

        # Subscribe to symbols (example)
        subscribe_message = {
            "action": "subscribe",
            "symbols": ["SPY", "QQQ", "DIA"]  # S&P 500, Nasdaq, Dow ETFs
        }
        ws.send(json.dumps(subscribe_message))

    # Create WebSocket connection
    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    # Run in background thread
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    return ws


# Example 2: Polygon.io WebSocket (Template)
def setup_polygon_stream(api_key):
    """
    Stream real-time stock data from Polygon.io

    Args:
        api_key: Your Polygon.io API key

    Note: Requires Polygon.io subscription ($29-999/month)
    """
    import websocket

    ws_url = f"wss://socket.polygon.io/stocks"

    def on_message(ws, message):
        try:
            data = json.loads(message)

            # Polygon sends different message types
            for msg in data:
                if msg.get('ev') == 'T':  # Trade event
                    symbol = msg.get('sym')
                    price = msg.get('p')

                    if 'realtime_data' not in st.session_state:
                        st.session_state.realtime_data = {}

                    st.session_state.realtime_data[symbol] = {
                        'price': price,
                        'timestamp': datetime.now(),
                        'volume': msg.get('s', 0)
                    }

                    st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

    def on_open(ws):
        # Authenticate
        auth_message = {"action": "auth", "params": api_key}
        ws.send(json.dumps(auth_message))

        # Subscribe to symbols
        subscribe_message = {
            "action": "subscribe",
            "params": "T.SPY,T.QQQ,T.DIA"  # Trade events for ETFs
        }
        ws.send(json.dumps(subscribe_message))

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_open=on_open
    )

    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    return ws


# Example 3: Display real-time data in Streamlit
def display_realtime_data():
    """
    Display real-time data in dashboard

    Usage:
        # In app_enhanced.py:
        from components.websocket_example import setup_polygon_stream, display_realtime_data

        # Initialize WebSocket connection
        if 'ws' not in st.session_state:
            st.session_state.ws = setup_polygon_stream(api_key="YOUR_KEY")

        # Display real-time data
        display_realtime_data()
    """

    st.subheader("📡 Real-Time Market Data")

    if 'realtime_data' not in st.session_state or not st.session_state.realtime_data:
        st.info("Waiting for real-time data...")
        return

    # Display each symbol's data
    cols = st.columns(len(st.session_state.realtime_data))

    for idx, (symbol, data) in enumerate(st.session_state.realtime_data.items()):
        with cols[idx]:
            st.metric(
                label=symbol,
                value=f"${data['price']:.2f}",
                delta=None  # Could calculate delta from previous
            )

            # Show last update time
            time_ago = (datetime.now() - data['timestamp']).total_seconds()
            st.caption(f"Updated {time_ago:.0f}s ago")


# Example 4: Finnhub WebSocket (Template)
def setup_finnhub_stream(api_key):
    """
    Stream real-time data from Finnhub

    Note: Finnhub has a free tier! Good for testing.
    """
    import websocket

    ws_url = f"wss://ws.finnhub.io?token={api_key}"

    def on_message(ws, message):
        data = json.loads(message)

        # Finnhub sends trades in 'data' field
        if data.get('type') == 'trade':
            for trade in data.get('data', []):
                symbol = trade.get('s')
                price = trade.get('p')

                if 'realtime_data' not in st.session_state:
                    st.session_state.realtime_data = {}

                st.session_state.realtime_data[symbol] = {
                    'price': price,
                    'timestamp': datetime.now()
                }

                st.rerun()

    def on_open(ws):
        # Subscribe to symbols
        ws.send(json.dumps({'type': 'subscribe', 'symbol': 'SPY'}))
        ws.send(json.dumps({'type': 'subscribe', 'symbol': 'QQQ'}))

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_open=on_open
    )

    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    return ws


# Example usage / test
if __name__ == "__main__":
    st.title("WebSocket Streaming Test")

    st.warning("""
    ⚠️ This is a TEMPLATE only!

    To use:
    1. Sign up for a real-time data provider
    2. Get API key
    3. Install: pip install websocket-client
    4. Replace YOUR_API_KEY below
    5. Test connection
    """)

    # Example initialization (replace with your API key)
    if st.button("Test WebSocket (requires API key)"):
        api_key = "YOUR_API_KEY_HERE"  # Replace this!

        if api_key == "YOUR_API_KEY_HERE":
            st.error("Please replace YOUR_API_KEY_HERE with actual API key")
        else:
            # Initialize WebSocket
            if 'ws' not in st.session_state:
                st.session_state.ws = setup_finnhub_stream(api_key)

            # Display data
            display_realtime_data()


"""
COST COMPARISON:

Finnhub:
- Free tier: 60 API calls/min
- Paid: $0-400/month
- Good for testing

Polygon.io:
- Starter: $29/month
- Advanced: $199-999/month
- Professional quality

Alpha Vantage:
- Standard: $50/month
- Premium: $250-500/month
- Good documentation

IEX Cloud:
- Free tier: Limited
- Paid: $0-2000/month
- Excellent data quality

RECOMMENDATION:
Start with Finnhub free tier for testing,
then upgrade to Polygon.io if going to production.
"""
