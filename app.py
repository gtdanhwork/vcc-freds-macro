import streamlit as st
import pandas as pd
import plotly.express as px
from monitor import analyze_signals
from seriesIds import FRED_SERIES_IDS

st.title("Bitcoin Macro Factor Dashboard")

st.write("This dashboard monitors key macroeconomic indicators to generate a trading signal for Bitcoin.")

# Dropdown hiển thị tên (values) với giá trị mặc định là CPI
selected_display = st.selectbox(
    "Pick indicator",
    list(FRED_SERIES_IDS.values()),
    index=0
)

# Lấy key tương ứng
selected_key = [k for k,v in FRED_SERIES_IDS.items() if v == selected_display][0]

# Hàm fetch dữ liệu từ FRED
def fetch_data():
    return analyze_signals(selected_display)

# Khởi tạo session_state
if "selected_key" not in st.session_state:
    st.session_state.selected_key = selected_key
if "data" not in st.session_state:
    st.session_state.data = fetch_data()

# Nếu dropdown thay đổi, cập nhật dữ liệu mới
if st.session_state.selected_key != selected_key:
    st.session_state.selected_key = selected_key
    st.session_state.data = fetch_data()

# --- Hiển thị bảng ---
st.subheader("Indicator Data:")
st.write(pd.DataFrame(st.session_state.data))

# --- Hiển thị biểu đồ ---
fig = px.line(
    st.session_state.data,
    x="Date",
    y="Value",
    title=f"{selected_display} over Time"
)
st.plotly_chart(fig, use_container_width=True, key="macro_chart")

# --- Nút refresh ---
col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("Refresh Data"):
        st.session_state.data = fetch_data()
