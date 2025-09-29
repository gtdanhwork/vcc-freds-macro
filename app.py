import streamlit as st
import pandas as pd
import json
from datetime import date
from monitor import analyze_signals, get_fred_data # Import the function from your other file
import plotly.express as px
from seriesIds import FRED_SERIES_IDS

st.title("Bitcoin Macro Factor Dashboard")

st.write("This dashboard monitors key macroeconomic indicators to generate a trading signal for Bitcoin.")

# Dropdown hiển thị tên (values) với giá trị mặc định là CPI
selected_display = st.selectbox(
    "Pick indicator",
    list(FRED_SERIES_IDS.values()),
    index=0  # 0 là vị trí đầu tiên trong list
)

# Lấy key tương ứng
selected_key = [k for k,v in FRED_SERIES_IDS.items() if v == selected_display][0]
print("selected", selected_key, selected_display)

# Hàm giả lập fetch dữ liệu
def fetch_data():
    data = analyze_signals(selected_display)
    print("data from analyze_signals", data)
    return pd.DataFrame(data)

# --- Khởi tạo session_state ---
if "df" not in st.session_state:
    st.session_state.df = fetch_data()  # load dữ liệu lần đầu

# --- Hiển thị bảng ---
""
"Indicator Data:"
st.write(st.session_state.df)

# --- Hiển thị biểu đồ ---
fig = px.line(
    st.session_state.df, 
    x="Date", 
    y="Value", 
    title=f"{selected_display} over Time"
)
st.plotly_chart(fig, key="macro_chart")

# --- Nút refresh ---
col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("Refresh Data"):
        st.session_state.df = fetch_data()  # cập nhật dữ liệu mới