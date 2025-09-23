import streamlit as st
from monitor import analyze_signals # Import the function from your other file

st.title("Bitcoin Macro Factor Dashboard")

st.write("This dashboard monitors key macroeconomic indicators to generate a trading signal for Bitcoin.")

if st.button("Refresh Data"):
    signals, buy_count, sell_count = analyze_signals()
    
    st.header("Signal Summary")
    st.metric(label="🟢 Buy Signals", value=f"{buy_count}")
    st.metric(label="🔴 Sell Signals", value=f"{sell_count}")

    st.header("Individual Indicator Status")
    for factor, signal in signals.items():
        st.write(f"- **{factor}:** {'🟢 BUY' if signal == 'BUY' else '🔴 SELL'}")
