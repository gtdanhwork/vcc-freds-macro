# Bitcoin Macro Factor Dashboard

Professional macroeconomic indicator dashboard for Bitcoin trading analysis.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app_enhanced.py
```

Open browser at `http://localhost:8501`

---

## 📊 Features

### Current Implementation (Active)
- ✅ **10 Macro Indicators**: S&P 500, Fed Rate, DXY, CPI, GDP, Unemployment, Consumer Confidence, Fed Balance Sheet, VIX, National Debt
- ✅ **4-Tab Interface**: Overview, Detailed Analysis, Trading Signals, Comparison
- ✅ **Signal Analysis**: Automated BUY/SELL/NEUTRAL recommendations
- ✅ **Data Freshness Monitoring**: Shows when data was last updated
- ✅ **Modular Architecture**: Clean, maintainable code
- ✅ **24-Hour Cache**: Optimal for macro analysis

### Future Options (Ready to Deploy)
- 📦 **Auto-Refresh**: 5-15 minute updates
- 📦 **Smart Polling**: Update after market hours
- 📦 **Real-Time Streaming**: WebSocket integration (requires paid API)

---

## 📁 Project Structure

```
vcc-freds-macro/
├── app_enhanced.py              # Main dashboard (modular)
├── app.py                       # Original simple version
│
├── components/                  # UI components
│   ├── metric_cards.py         # Metric cards
│   ├── charts.py               # Chart rendering
│   ├── sidebar.py              # Sidebar controls
│   ├── tabs.py                 # Tab content
│   └── data_monitor.py         # Data freshness monitoring
│
├── Core Logic
│   ├── monitor_enhanced.py     # FRED data & signals
│   ├── config.py               # Configuration
│   ├── utils.py                # Utilities
│   └── seriesIds.py            # Indicator definitions
│
├── future_implementations/      # Backup plans
│   └── realtime/               # Real-time update options
│
└── Documentation (.md files)
```

---

## 🎯 Data Update Strategy

### Current: 24-Hour Cache ✅

**How it works**:
- Data fetched from FRED once per day
- Cached for 24 hours
- Users see "Refreshed X ago" in sidebar
- Manual refresh available anytime

**Why this is optimal**:
- FRED data updates daily/monthly/quarterly (not real-time)
- Respects API limits (120 req/min)
- Fast user experience (< 1s load time)
- Appropriate for macro analysis

**See**: [DATA_FRESHNESS_README.md](DATA_FRESHNESS_README.md)

### Future: Real-Time Options 📦

If your company needs more frequent updates:

| Option | Update Frequency | Effort | Cost |
|--------|------------------|--------|------|
| Auto-refresh | Every 5-15 min | 30 min | Free |
| Smart polling | After market close | 2 hours | Free |
| WebSocket | Real-time | 1-2 weeks | $50-500/mo |

**See**: [REALTIME_OPTIONS_GUIDE.md](REALTIME_OPTIONS_GUIDE.md)

**Location**: `future_implementations/realtime/`

---

## 📚 Documentation

**📖 [Complete Documentation Index](docs/INDEX.md)** - Find everything organized by topic

### Quick Links

| Category | Key Documents |
|----------|---------------|
| **Getting Started** | [Setup Guide](docs/architecture/CLEAN_SETUP.md) · [User Guide](docs/user-guides/QUICK_START.md) |
| **Architecture** | [Code Structure](docs/architecture/MODULAR_STRUCTURE.md) · [Quick Reference](docs/architecture/MODULAR_QUICK_START.md) |
| **Data Updates** | [Freshness Guide](docs/data-updates/DATA_FRESHNESS_README.md) ⭐ · [Real-time Options](docs/data-updates/REALTIME_OPTIONS_GUIDE.md) |
| **Decisions** | [Why This Design](docs/decisions/DECISION_LOG.md) |

**Browse all docs**: [docs/](docs/) folder

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file:
```
FRED_API_KEY=your_fred_api_key_here
TELEGRAM_BOT_TOKEN=your_bot_token  # Optional
TELEGRAM_CHAT_ID=your_chat_id      # Optional
```

Get FRED API key: https://fred.stlouisfed.org/docs/api/api_key.html

### Customization

**Change cache duration**:
```python
# In app_enhanced.py, line 54
@st.cache_data(ttl=3600 * 24)  # Change 24 to desired hours
```

**Modify signal thresholds**:
```python
# In config.py, SIGNAL_THRESHOLDS section
's&p500': {
    'buy_threshold': 0.5,   # Adjust as needed
    'sell_threshold': -0.5,
    'lookback_periods': 20
}
```

**Add new indicators**:
1. Add to `seriesIds.py`
2. Add metadata to `config.py`
3. Restart dashboard

---

## 🎯 Use Cases

### Macro Analysis (Current) ✅
- Long-term Bitcoin trend analysis
- Economic indicator correlation
- Monthly/quarterly review
- **Perfect fit**: Data updates daily/monthly/quarterly

### Daily Trading (Backup Plan Ready) 📦
- After-market signal updates
- Daily decision support
- **Implementation**: Deploy `smart_polling.py`

### Real-Time Trading (Template Ready) 📦
- Intraday monitoring
- Live signal updates
- **Implementation**: WebSocket + paid API

---

## 🚀 Deployment

### Local Development
```bash
streamlit run app_enhanced.py
```

### Production (Streamlit Cloud)
1. Push to GitHub
2. Deploy on Streamlit Cloud
3. Add `.env` secrets in dashboard settings
4. Current cache strategy works perfectly!

### Production (Self-Hosted)
```bash
# Install dependencies
pip install -r requirements.txt

# Run with production settings
streamlit run app_enhanced.py --server.port 8501 --server.address 0.0.0.0
```

**Note**: 24h cache scales to unlimited users (cache is shared)

---

## 📊 Indicators

| Indicator | FRED ID | Update Frequency |
|-----------|---------|------------------|
| S&P 500 | SP500 | Daily |
| Fed Funds Rate | EFFR | Daily |
| Dollar Index (DXY) | DTWEXAFEGS | Daily |
| Fed Balance Sheet | WALCL | Weekly |
| CPI (Inflation) | CPIAUCSL | Monthly |
| Unemployment | UNRATE | Monthly |
| Consumer Confidence | UMCSENT | Monthly |
| National Debt/GDP | GFDEGDQ188S | Quarterly |
| GDP | GDPC1 | Quarterly |
| VIX (Volatility) | VIXCLS | Daily |

---

## 🔧 Troubleshooting

### "No module named components"
```bash
# Run from project root
cd vcc-freds-macro
streamlit run app_enhanced.py
```

### Data seems stale
Check sidebar "📊 Data Status" section:
- See when last refreshed
- Click "🔄 Refresh Data" to update manually
- Check "ℹ️ Data Update Frequencies" for details

### Need more frequent updates
See `future_implementations/realtime/` for ready-to-deploy options

---

## 📞 Support

- **Documentation**: See `.md` files in project root
- **Issues**: Check inline code comments
- **Future Features**: See `future_implementations/`

---

## 🎯 Quick Links

| What You Need | Where to Look |
|---------------|---------------|
| **Setup guide** | [docs/architecture/CLEAN_SETUP.md](docs/architecture/CLEAN_SETUP.md) |
| **User guide** | [docs/user-guides/QUICK_START.md](docs/user-guides/QUICK_START.md) |
| **Data freshness** | [docs/data-updates/DATA_FRESHNESS_README.md](docs/data-updates/DATA_FRESHNESS_README.md) |
| **Real-time options** | [docs/data-updates/REALTIME_OPTIONS_GUIDE.md](docs/data-updates/REALTIME_OPTIONS_GUIDE.md) |
| **Code structure** | [docs/architecture/MODULAR_STRUCTURE.md](docs/architecture/MODULAR_STRUCTURE.md) |
| **Why this design** | [docs/decisions/DECISION_LOG.md](docs/decisions/DECISION_LOG.md) |
| **All documentation** | [docs/INDEX.md](docs/INDEX.md) 📖 |

---

## ✅ Status

**Current Version**: Production Ready ✅
- 24-hour cache (optimal for macro analysis)
- Data freshness monitoring
- Manual refresh available
- Modular, maintainable code

**Backup Plans**: Ready to Deploy 📦
- Auto-refresh templates
- Smart polling templates
- WebSocket templates
- All documented and tested

**Next Steps**: None required - deploy as-is! 🚀

---

## 📝 License

MIT License - See LICENSE file

---

## 🙏 Acknowledgments

- **FRED API**: Federal Reserve Economic Data
- **Streamlit**: Dashboard framework
- **Plotly**: Interactive charts
- **Claude Code**: Development assistance

---

**Built with ❤️ for macro Bitcoin analysis**

*Current setup is optimal. Real-time options ready if needed.*
