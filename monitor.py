import os
import requests
import pandas as pd
import json
from datetime import date
from dotenv import load_dotenv
from seriesIds import FRED_SERIES_IDS

# Tải biến môi trường từ tệp .env
load_dotenv()

# --- CẤU HÌNH ---
FRED_API_KEY = os.getenv('FRED_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# FRED Series IDs for our indicators
# Find more here: https://fred.stlouisfed.org/
# FRED_SERIES_IDS = {
#     'cpi': 'CPIAUCSL',                # Consumer Price Index
# }

# --- CHỨC NĂNG HỖ TRỢ TELEGRAM ---

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

# --- LOGIC PHÂN TÍCH TÍN HIỆU (Giữ lại để tương thích) ---

def analyze_signals(value: str = FRED_SERIES_IDS['s&p500']) -> list:
    print("analyze_signals key", value)
    data_origin = get_fred_data(value, 10)
    print("data_origin", data_origin)
    if not data_origin:
        return []
    new_data = [{"Date": item["date"], "Value": item["value"]} for item in data_origin['observations']]
    return new_data
    # print("data", data)

    # values = [item["value"] for item in data]
    # print(values)

    
    # # 1. Inflation (CPI)
    # latest_cpi, prev_cpi = get_fred_data(FRED_SERIES_IDS['cpi'])
    # if latest_cpi and prev_cpi:
    #     signals['CPI'] = 'BUY' if latest_cpi > prev_cpi else 'SELL'

    # buy_count = list(signals.values()).count('BUY')
    # sell_count = list(signals.values()).count('SELL')
    
    # return signals, buy_count, sell_count

# --- CHỨC NĂNG LẤY DỮ LIỆU FRED ---

def get_fred_data(series_id, limit=10000): 
    """
    Lấy bộ dữ liệu lịch sử lớn nhất có thể cho một chuỗi dữ liệu từ FRED.
    Loại bỏ các tham số theo dõi phiên bản để tránh lỗi giới hạn 'vintage date'.
    """
    
    # URL được đơn giản hóa bằng cách loại bỏ '&realtime_start=...'
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&limit={limit}&sort_order=asc"
    
    try:
        response = requests.get(url)
        
        # 1. Kiểm tra Lỗi API/HTTP (4xx hoặc 5xx)
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
        
        # 2. Kiểm tra Lỗi Dữ liệu FRED (ví dụ: Không tìm thấy Chuỗi)
        if 'error_code' in data:
            print(f"--- FRED DATA ERROR for {series_id} ---")
            print(f"Error Message: {data.get('error_message')}")
            print("----------------------------------------")
            return []
            
        # 3. KIỂM TRA QUAN TRỌNG: Đảm bảo khóa observations tồn tại và không rỗng
        if 'observations' in data and data['observations']:
            return data['observations']
        else:
            print(f"--- CẢNH BÁO: Chuỗi {series_id} trả về 200 OK nhưng KHÔNG có dữ liệu observations. ---")
            return []
            
    except Exception as e:
        print(f"Không thể lấy dữ liệu cho {series_id}: {e}")
        
    return [] 

# ... rest of monitor.py remains the same
def fetch_all_fred_data() -> dict:
    """
    Hàm được gọi bởi cache Streamlit. Lấy dữ liệu cho TẤT CẢ các chỉ số.
    """
    all_series_data = {}
    print("\n--- Bắt đầu Lấy Dữ liệu FRED hàng loạt ban đầu ---")
    
    for friendly_name, series_id in FRED_SERIES_IDS.items(): 
        print(f"Fetching data for: {friendly_name} ({series_id})")

        # Gọi hàm đã cập nhật mà không có tham số ngày bắt đầu
        data = get_fred_data(series_id) 
        
        # Chuyển đổi cấu trúc dữ liệu và lọc các giá trị bị thiếu ('.')
        new_data = [
            {"Date": item["date"], "Value": item["value"]} 
            for item in data if item["value"] != '.'
        ]
        # Lưu trữ dữ liệu bằng ID FRED làm khóa tra cứu
        all_series_data[series_id] = new_data
        
    print("--- FRED Data Initial Fetch Complete ---\n")
    return all_series_data



# --- THỰC THI CHÍNH ---

def main():
    analyze_signals();    

    # # Format the message
    # message = "📈 *Macro Signal Report* 📉\n\n"
    # for factor, signal in signals.items():
    #     emoji = "🟢" if signal == 'BUY' else "🔴"
    #     message += f"{emoji} *{factor}:* {signal}\n"
    
    # message += f"\n*Summary:*\n"
    # message += f"🟢 Buy Signals: *{buy_count}*\n"
    # message += f"🔴 Sell Signals: *{sell_count}*\n\n"
    
    # # --- TRIGGER LOGIC (e.g., 4 out of 5 for this example) ---
    # if buy_count >= 4:
    #     message += "🚨 *MAJOR BUY SIGNAL DETECTED* 🚨"
    #     send_telegram_message(message)
    # elif sell_count >= 4:
    #     message += "🚨 *MAJOR SELL SIGNAL DETECTED* 🚨"
    #     send_telegram_message(message)
    # else:
    #     message += "Signal is neutral. No action required."
    #     print(message)
    #     # Optional: uncomment below to get a report even on neutral days
    #     send_telegram_message(message)

if __name__ == "__main__":
    main()