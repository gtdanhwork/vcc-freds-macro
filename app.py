import streamlit as st
import pandas as pd
import json
from datetime import date
from monitor import analyze_signals, get_fred_data # Import the function from your other file
import seriesIds

FRED_SERIES_ID = seriesIds.FRED_SERIES_IDS

STATIC_DATE_START = '2053-07-01'
STATIC_DATE_END = date.today()


st.title("Bitcoin Macro Factor Dashboard")

st.write("This dashboard monitors key macroeconomic indicators to generate a trading signal for Bitcoin.")

# if st.button("Refresh Data"):
#     data = get_fred_data(FRED_SERIES_ID['s&p500'])

#     observations = data['observations']

#     df = pd.DataFrame(observations)
#     df['date'] = pd.to_datetime(df['date'])
#     # df.set_index('date', inplace=True)

#     sorted_df = df.sort_values(by='value', ascending=True)


#     st.line_chart(sorted_df, x='date', y='value', use_container_width=True)
#     st.write(df)

    # signals, buy_count, sell_count = analyze_signals()

if st.button("Refresh Data"):
    signals, buy_count, sell_count = analyze_signals()
    
    st.header("Signal Summary")
    st.metric(label="🟢 Buy Signals", value=f"{buy_count}")
    st.metric(label="🔴 Sell Signals", value=f"{sell_count}")

    st.header("Individual Indicator Status")
    for factor, signal in signals.items():
        st.write(f"- **{factor}:** {'🟢 BUY' if signal == 'BUY' else '🔴 SELL'}")