# Quick Start Guide - Enhanced Bitcoin Macro Dashboard

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Environment Variables
Make sure your `.env` file contains:
```
FRED_API_KEY=your_fred_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token  # Optional
TELEGRAM_CHAT_ID=your_telegram_chat_id      # Optional
```

### Step 3: Run the Dashboard
```bash
streamlit run app_enhanced.py
```

Your browser will open automatically at `http://localhost:8501`

---

## 📱 Dashboard Tour

### Tab 1: Overview 📊
**What you'll see**: All 10 macro indicators in a grid layout

**Use it to**: Get a quick snapshot of the entire macro environment
- Each card shows: current value, 30-day change, mini chart
- Color-coded arrows show trends (↑ up, ↓ down, → neutral)
- Organized by category for easy scanning

**Action**: Scan for unusual movements or trends

---

### Tab 2: Detailed Analysis 🔍
**What you'll see**: Deep dive into a single indicator

**Use it to**: Analyze specific indicators in detail
- Select any indicator from dropdown
- Choose chart type (Line, Area, or Bar)
- Toggle moving averages (MA20, MA50, MA200)
- View comprehensive statistics
- See data table (optional)

**Action**: Investigate interesting trends from Overview tab

---

### Tab 3: Trading Signals 🎯
**What you'll see**: Automated buy/sell recommendations

**Use it to**: Get trading signal recommendations
- **Overall Signal**: Aggregated BUY/SELL/NEUTRAL for Bitcoin
- **Signal count**: How many indicators are bullish/bearish
- **Individual signals**: Each indicator's recommendation
- **30-day changes**: Context for each signal

**Signal meanings**:
- 🟢 **BUY**: Indicator trending bullish
- 🔴 **SELL**: Indicator trending bearish
- 🟡 **NEUTRAL**: No strong trend

**Action**: Use as input for trading decisions (not financial advice!)

---

### Tab 4: Comparison 📈
**What you'll see**: Multiple indicators overlaid and compared

**Use it to**: Find relationships between indicators
- Select 2-4 indicators to compare
- **Normalized chart**: Shows % change from start date
- **Correlation matrix**: How indicators move together
  - +1.0 = perfect positive correlation
  - -1.0 = perfect negative correlation
  - 0.0 = no correlation

**Action**: Discover which indicators predict each other

---

## ⚙️ Sidebar Controls

### 🔄 Refresh Data
- Clears 24-hour cache
- Fetches fresh data from FRED API
- Use once per day or when you need latest data

### 📅 Time Period
- **Quick Select**: Choose preset ranges (30d, 90d, 1yr, etc.)
- **Start Date**: Custom date range
- **Max Data Points**: Limit number of points displayed

### 🎨 Display Options
- **Show Data Table**: Toggle raw data table
- **Show Statistics**: Toggle stats panel

---

## 💡 Pro Tips

### For Daily Monitoring:
1. Start on **Overview** tab to scan all indicators
2. Look for large % changes (red or green)
3. Jump to **Detailed Analysis** for any unusual indicators
4. Check **Trading Signals** for overall recommendation

### For Research:
1. Use **Comparison** tab to test hypotheses
2. Compare S&P 500 vs Bitcoin-related indicators
3. Check correlation matrix for relationships
4. Adjust time periods to see different market cycles

### For Signal-Based Trading:
1. Check **Trading Signals** tab daily
2. Look for **STRONG BUY** or **STRONG SELL** (7+ signals)
3. Review individual indicator signals for context
4. Cross-reference with your own analysis

---

## 🔔 Setting Up Telegram Alerts

### Why Use Alerts?
Get notified automatically when strong signals appear (7+ buy or sell signals)

### Setup:
1. Create a Telegram bot via [@BotFather](https://t.me/botfather)
2. Get your chat ID via [@userinfobot](https://t.me/userinfobot)
3. Add to `.env` file:
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=123456789
   ```
4. Test by running: `python monitor_enhanced.py`

### Alert Triggers:
- **STRONG BUY**: 7+ bullish indicators
- **STRONG SELL**: 2 or fewer bullish indicators
- **BUY/SELL**: 6 or 3 bullish indicators

You can customize thresholds in `config.py` → `OVERALL_SIGNAL_THRESHOLDS`

---

## 🎛️ Customizing Signals

### To make signals more/less sensitive:

**Edit**: `config.py` → `SIGNAL_THRESHOLDS`

**Example** (make S&P 500 less sensitive):
```python
's&p500': {
    'buy_threshold': 2.0,   # Changed from 0.5 (needs +2% to trigger BUY)
    'sell_threshold': -2.0, # Changed from -0.5
    'lookback_periods': 20
}
```

**Example** (use longer trend for Fed Rate):
```python
'fed_rate': {
    'buy_threshold': -0.1,
    'sell_threshold': 0.1,
    'lookback_periods': 10  # Changed from 3 (looks at 10 periods instead)
}
```

After changes, restart the dashboard to apply.

---

## 📊 Understanding Indicators

### Market Indices
- **S&P 500**: Stock market performance (↑ = risk-on)
- **DXY**: Dollar strength (↑ = bearish for BTC)

### Monetary Policy
- **Fed Rate**: Interest rates (↑ = tighter money, bearish)
- **Fed Balance Sheet**: Money printing (↑ = bullish for BTC)

### Economic Health
- **GDP**: Economic growth (↑ = healthy economy)
- **CPI**: Inflation (↑ = bullish for BTC as inflation hedge)
- **Unemployment**: Job market (↓ = healthy economy)
- **Consumer Confidence**: Spending sentiment (↑ = bullish)

### Risk & Debt
- **VIX**: Market fear (↑ = high fear, bearish)
- **National Debt**: Government debt as % of GDP (↑ = bearish long-term)

---

## 🔍 Interpreting Signals

### Example Scenario:

**Overall Signal: 🟢 STRONG BUY (8/10 bullish)**

**Individual Signals**:
- 🟢 S&P 500: BUY (+3.5% 30d) - Stock market rising
- 🟢 Fed Rate: BUY (-0.2% 30d) - Rate cuts beginning
- 🔴 DXY: SELL (+2.1% 30d) - Dollar strengthening (bearish)
- 🟢 Fed Balance Sheet: BUY (+1.8% 30d) - QE expanding
- 🟢 CPI: BUY (-0.3% 30d) - Inflation cooling
- 🟢 Unemployment: BUY (-0.1% 30d) - Jobs improving
- 🟢 Consumer Confidence: BUY (+2.5% 30d) - Consumers optimistic
- 🟡 National Debt: NEUTRAL (0.1% 30d) - Stable
- 🟢 GDP: BUY (+0.8% 30d) - Economy growing
- 🟢 VIX: BUY (-8.2% 30d) - Fear declining

**Interpretation**:
- Strong macro environment for risk assets
- Liquidity increasing (Fed Balance Sheet up)
- Risk appetite improving (VIX down, S&P up)
- Only concern: Strong dollar (but 8/10 bullish)
- **Action**: Consider BUY signal for Bitcoin

---

## ⚠️ Important Notes

### This is NOT Financial Advice
- Signals are based on historical correlations
- Past performance doesn't guarantee future results
- Always do your own research
- Consider your risk tolerance
- Consult a financial advisor

### Data Limitations
- FRED data updates with lag (monthly/quarterly for some indicators)
- Cache refreshes once per 24 hours
- Some indicators may be sparse (quarterly GDP)

### Best Practices
- Use signals as ONE input in your decision-making
- Combine with technical analysis
- Monitor multiple timeframes
- Consider Bitcoin-specific factors (halving, regulations, etc.)

---

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Try running original to test
streamlit run app.py
```

### No data showing
- Check FRED_API_KEY in `.env` file
- Run `python monitor_enhanced.py` to test API connection
- Check console for error messages

### All signals are NEUTRAL
- Normal if indicators aren't trending strongly
- Try adjusting thresholds in `config.py`
- Check different time periods

### Charts not interactive
- Ensure plotly is installed: `pip install plotly --upgrade`
- Try refreshing browser
- Check browser console for JavaScript errors

---

## 📖 More Resources

- **Full Documentation**: See `IMPLEMENTATION_GUIDE.md`
- **Code Details**: See inline comments in each `.py` file
- **Configuration**: Edit `config.py` for customization
- **FRED API**: https://fred.stlouisfed.org/docs/api/
- **Streamlit Docs**: https://docs.streamlit.io

---

## 🎉 You're Ready!

Open your dashboard and start monitoring the macro environment for Bitcoin trading signals!

```bash
streamlit run app_enhanced.py
```

**Enjoy your new dashboard!** 🚀📈
