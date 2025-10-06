import streamlit as st
import pandas as pd
import json
from datetime import date, timedelta
from monitor import analyze_signals, get_fred_data, fetch_all_fred_data # Import the function from your other file
import plotly.express as px
from seriesIds import FRED_SERIES_IDS

st.title("Bitcoin Macro Factor Dashboard")
st.write("This dashboard monitors key macroeconomic indicators to generate a trading signal for Bitcoin.")
st.set_page_config(layout="wide")

# --- HÀM TẠO CACHE DỮ LIỆU MỚI ---
# Cache trong 24 giờ. Lần tải đầu tiên sẽ gọi API cho TẤT CẢ các chỉ số.
@st.cache_data(ttl=3600 * 24)
def load_all_data(indicators):
    """
    Tải và tạo cache ban đầu cho TẤT CẢ dữ liệu FRED từ API.
    Danh sách các chỉ số được truyền vào làm khóa cache.
    """
    return fetch_all_fred_data()

# --- Tải và lưu dữu liệu trong Session State (Streamlit)  ---
# Điều kiện: Chưa lưu vào Session State 
if "all_data" not in st.session_state:
    with st.spinner("Loading ALL historical FRED data... This happens only once per day."):
        # Gọi hàm đã tạo cache
        st.session_state.all_data = load_all_data(list(FRED_SERIES_IDS.keys()))

# --- USER INPUT CONTROLS (in the sidebar) ---

st.sidebar.header("Data Filters & Selection")

# 1. Lựa chọn Chỉ số (Hiển thị tên thân thiện, lấy giá trị ID FRED)
selected_key_name = st.sidebar.selectbox( 
    "Pick Indicator",
    list(FRED_SERIES_IDS.keys()), # Hiển thị khóa thân thiện (ví dụ: 's&p500')
    index=0 
)

# Lấy ID FRED (giá trị) tương ứng
selected_fred_id = FRED_SERIES_IDS[selected_key_name]
selected_display_name = selected_key_name

# 2. Đầu vào giới hạn số lượng giá trị (Limit)
limit = st.sidebar.number_input(
    "Limit to the latest N values",
    min_value=1,
    max_value=1000,
    value=30, # Default to 30
    step=1
)

# 3. Đầu vào phạm vi Ngày (Ngày Bắt đầu)
today = date.today()
default_start_date = today - timedelta(days=365) # Default to 1 year ago
start_date = st.sidebar.date_input(
    "Filter by Start Date",
    value=default_start_date,
    max_value=today,
    format="YYYY/MM/DD"
)


show_table = st.sidebar.checkbox("Show Table", value=True)
show_chart = st.sidebar.checkbox("Show Chart", value=True)

if st.sidebar.button("Refresh ALL Data (Clears Cache)"):
    # Xóa cache một cách rõ ràng để buộc gọi API mới
    st.cache_data.clear() 
    st.rerun()

# --- DATA FILTERING LOGIC (Runs instantly from cached data) ---

# Hàm LỌC dữ liệu từ cache 
def get_filtered_data(series_id, start_date, limit):
    """Filters the cached data based on user input (runs instantly) and ensures correct data types."""
    
    # 1. Truy xuất toàn bộ dữ liệu cho chỉ số đã chọn từ cache session
    data = st.session_state.all_data.get(series_id, [])
    
    # Nếu không tìm thấy dữ liệu trong cache (ví dụ: lỗi lấy dữ liệu API), 
    # trả về một DataFrame rỗng ngay lập tức.
    if not data:
        return pd.DataFrame({"Date": [], "Value": []})

    # 2. Lọc theo Ngày 
    start_date_str = start_date.strftime("%Y-%m-%d")
    date_filtered_data = [
        item for item in data 
        if item["Date"] >= start_date_str
    ]
    
    # 3. Lọc theo Giới hạn (lấy N giá trị gần nhất)
    # Điều này tự động xử lý các dữ liệu thưa thớt (Hàng tháng/Quý) một cách duyên dáng
    final_data = date_filtered_data[-limit:]

    # Chuyển đổi sang DataFrame, đặt rõ ràng các cột để đảm bảo 'Date' và 'Value' tồn tại.
    df = pd.DataFrame(final_data, columns=["Date", "Value"])
   
    # 4.Chuyển đổi Loại dữ liệu và Làm sạch !!!
    
    # Chuyển đổi cột 'Date' từ chuỗi sang đối tượng datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Chuyển đổi cột 'Value' sang loại số (float)
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    
    # Loại bỏ các hàng mà 'Value' là NaN (tức là làm sạch mọi giá trị '.' còn sót lại)
    df.dropna(subset=['Value'], inplace=True)
    
    # Nếu tất cả các điểm dữ liệu không hợp lệ và bị loại bỏ, trả về một DataFrame rỗng
    if df.empty:
        return pd.DataFrame({"Date": [], "Value": []})

    return df
    
# --- Tạo DataFrame ĐỂ HIỂN THỊ từ CACHE ---
st.session_state.df = get_filtered_data(selected_fred_id, start_date, limit)

# --- Hiển thị Dữ liệu và Biểu đồ ---

st.header(f"Data for: {selected_display_name} ({selected_fred_id})")
col1, col2 = st.columns(2)
with col1:
    fig = px.line(
        st.session_state.df, 
        x="Date", 
        y="Value", 
    )
    if show_chart:
        st.plotly_chart(fig, key="macro_chart", width='stretch')
with col2:  
    if show_table:
        st.dataframe(st.session_state.df, width='stretch')