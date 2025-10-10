# Data Update Guide - Understanding Data Freshness

## ❓ Your Question: Is Data Updated Live or Daily?

**Short Answer**: Data updates **once per day** (24-hour cache), not live/real-time.

**Long Answer**: It's more nuanced - different indicators update at different frequencies on FRED, but your dashboard caches everything for 24 hours.

---

## 📊 How Data Updates Work

### Your Dashboard Cache

```python
@st.cache_data(ttl=3600 * 24)  # Cache for 24 hours
def load_all_data():
    return fetch_all_fred_data()
```

**What this means**:
1. **First load**: Dashboard fetches all data from FRED API
2. **Data is cached**: Stored in memory for 24 hours
3. **Subsequent loads**: Uses cached data (no API call)
4. **After 24 hours**: Cache expires, next user triggers fresh fetch
5. **Manual refresh**: "🔄 Refresh Data" button clears cache immediately

---

## 🔄 FRED Source Update Frequencies

### Daily Updates (Most Recent)
- **S&P 500** - Updates daily after market close
- **Federal Funds Rate** - Updates daily
- **Dollar Index (DXY)** - Updates daily
- **VIX (Volatility)** - Updates daily

### Weekly Updates
- **Fed Balance Sheet** - Updates every Thursday

### Monthly Updates (1-2 Day Lag)
- **CPI (Inflation)** - Released ~13th of month
- **Unemployment Rate** - Released first Friday of month
- **Consumer Confidence** - Released last Tuesday of month

### Quarterly Updates (Significant Lag)
- **GDP** - Released ~1 month after quarter ends
- **National Debt/GDP** - Released quarterly

---

## 📅 Data Freshness Timeline

### Example Scenario:

**Monday 9 AM** - User A opens dashboard
- ✅ Fetches fresh data from FRED API
- ✅ S&P 500 data is from Friday (latest)
- ✅ CPI data is from last month
- ⏰ Data cached for 24 hours

**Monday 3 PM** - User B opens dashboard
- ✅ Uses cached data from 9 AM (6 hours old)
- ❌ No API call made
- ✅ Same data as User A

**Tuesday 10 AM** - User C opens dashboard
- ✅ Cache expired (> 24 hours)
- ✅ Fetches fresh data from FRED
- ✅ S&P 500 now has Monday's data
- ⏰ New 24-hour cache starts

---

## 🎯 New Features Added

I've added **Data Freshness Monitoring** to your dashboard:

### 1. Cache Status Display (Sidebar)
Shows:
- ✅ When data was last refreshed
- ⏰ When cache will expire
- 🔄 Next auto-refresh time

Example:
```
📊 Data Status
✅ Refreshed 2h 15m ago
Cache expires in 21h
Next auto-refresh: 2025-10-07 09:00
```

### 2. Update Frequency Info (Sidebar Expander)
Click "ℹ️ Data Update Frequencies" to see:
- How often each indicator updates on FRED
- Latest data date for each indicator
- Explanation of caching behavior

### 3. Data Freshness Badges (Optional)
You can add to metric cards to show:
- 🟢 Fresh data (within expected update frequency)
- 🟡 Slightly old (within 2x update frequency)
- 🔴 Stale data (older than 2x update frequency)

---

## ⚙️ Customization Options

### Option 1: Change Cache Duration

**Current**: 24 hours
**Location**: `app_enhanced.py`, line 54

```python
# More frequent updates (but more API calls)
@st.cache_data(ttl=3600 * 6)  # 6 hours

# Less frequent updates (fewer API calls)
@st.cache_data(ttl=3600 * 48)  # 48 hours

# No cache (always fresh, but slow and hits API limits)
@st.cache_data(ttl=0)  # Not recommended!
```

**Trade-offs**:
- ⬇️ Lower TTL = Fresher data, more API calls, slower loads
- ⬆️ Higher TTL = Faster loads, less API calls, older data

---

### Option 2: Different Cache for Different Indicators

For advanced users, cache daily indicators separately from monthly:

```python
@st.cache_data(ttl=3600 * 6)  # 6 hours for daily indicators
def load_daily_data():
    # Fetch S&P500, VIX, DXY, Fed Rate
    pass

@st.cache_data(ttl=3600 * 48)  # 48 hours for monthly indicators
def load_monthly_data():
    # Fetch CPI, Unemployment, etc.
    pass
```

---

### Option 3: Scheduled Auto-Refresh

For deployment, set up a cron job or scheduled task:

**Linux/Mac (crontab)**:
```bash
# Clear Streamlit cache daily at 9 AM
0 9 * * * curl http://localhost:8501  # Trigger page load
```

**Windows (Task Scheduler)**:
- Create task to open dashboard URL daily
- Forces cache refresh at predictable time

---

## 🚀 For Deployment

### Recommended Settings:

**1. Production Cache Strategy**:
```python
# Cache for 12 hours (refresh twice daily)
@st.cache_data(ttl=3600 * 12)
```

**Why**:
- Daily indicators get refreshed before market open
- Not too aggressive on API calls
- Users get reasonable freshness

**2. Add Data Freshness Disclaimer**:
Already added! Shows in sidebar:
```
ℹ️ Data Freshness Notice
- Dashboard caches data for 24 hours
- FRED updates vary by indicator
- This is not real-time data
```

**3. Monitor API Usage**:
- FRED API limit: **120 requests/minute**
- Your dashboard: **10 indicators = 10 requests per cache load**
- With 24h cache: Safe for hundreds of users

---

## 📊 What Users Will See Now

### Sidebar Shows:

1. **Data Status Section**:
   ```
   📊 Data Status
   ✅ Refreshed 45 min ago
   Cache expires in 23h
   Next auto-refresh: 2025-10-07 09:15
   ```

2. **Update Frequency Expander**:
   ```
   ℹ️ Data Update Frequencies

   How often does data update?

   Your dashboard caches data for 24 hours.
   FRED sources update at different frequencies:

   Daily Updates: S&P 500, Fed Rate, DXY, VIX
   Weekly Updates: Fed Balance Sheet
   Monthly Updates: CPI, Unemployment, Consumer Confidence
   Quarterly Updates: GDP, National Debt

   [Latest Data Dates Table]
   ```

3. **Manual Refresh Button**:
   ```
   [🔄 Refresh Data]  ← Click to update immediately
   ```

---

## 🔍 How to Check Data Freshness

### Method 1: Sidebar Status
Look at "📊 Data Status" in sidebar:
- Shows when data was last fetched
- Shows cache expiry countdown

### Method 2: Latest Data Dates Table
Click "ℹ️ Data Update Frequencies" expander:
- Shows actual latest date for each indicator
- Compare to expected update frequency

### Method 3: Check FRED Directly
Visit: https://fred.stlouisfed.org/series/[SERIES_ID]
- Example: https://fred.stlouisfed.org/series/SP500
- Compare latest date there vs. your dashboard

---

## ⚠️ Important Limitations

### Not Real-Time Because:

1. **Dashboard Cache** (24 hours)
   - Even if FRED updates, your cache doesn't

2. **FRED API Lag** (varies)
   - FRED itself isn't real-time
   - Daily indicators update after market close
   - Monthly indicators lag by days/weeks

3. **Quarterly Indicators** (significant lag)
   - GDP released ~1 month after quarter
   - Your dashboard might show data from months ago

### This Is Normal!
- Macro analysis doesn't need real-time data
- Trends matter more than minute-by-minute changes
- 24-hour freshness is sufficient for macro trading

---

## 🎯 Recommendations

### For Development:
```python
# Short cache for testing
@st.cache_data(ttl=3600)  # 1 hour
```

### For Production:
```python
# Balanced approach
@st.cache_data(ttl=3600 * 12)  # 12 hours
```

### For High-Traffic:
```python
# Longer cache to reduce API load
@st.cache_data(ttl=3600 * 24)  # 24 hours (current)
```

---

## 📝 Quick Reference

| Indicator | FRED Updates | Your Cache | Effective Freshness |
|-----------|--------------|------------|---------------------|
| S&P 500 | Daily | 24h | 24-48 hours old |
| Fed Rate | Daily | 24h | 24-48 hours old |
| VIX | Daily | 24h | 24-48 hours old |
| Fed Balance | Weekly | 24h | Up to 7+ days old |
| CPI | Monthly | 24h | Up to 30+ days old |
| GDP | Quarterly | 24h | Up to 90+ days old |

**Effective Freshness** = Time since FRED received data + Your cache age

---

## 🛠️ Testing Data Freshness

### Test Cache Behavior:

1. **Open dashboard** - Note "Refreshed X ago" time
2. **Wait 5 minutes**
3. **Refresh browser** - Time should increase to "X+5 min ago"
4. **Click "🔄 Refresh Data"** - Time resets to "Refreshed 0 min ago"

### Test Data Updates:

1. **Note latest data date** in "Latest Data Dates" table
2. **Wait 24+ hours**
3. **Open dashboard** - Should fetch new data
4. **Check if dates changed** - Daily indicators should update

---

## ✅ Summary

**Your Setup**:
- ✅ Data cached for 24 hours
- ✅ Manual refresh available
- ✅ Now shows cache status and freshness
- ✅ Users know data is not real-time

**FRED Reality**:
- Daily indicators: 1-day lag
- Weekly indicators: Up to 7-day lag
- Monthly indicators: Up to 30-day lag
- Quarterly indicators: Up to 90-day lag

**Combined Freshness**:
- Best case: ~24 hours old (daily indicators)
- Worst case: Months old (quarterly indicators)
- **This is normal for macro analysis!**

**User Knows Because**:
- Sidebar shows "Refreshed X ago"
- Expander explains update frequencies
- Latest dates table shows actual data dates

Your dashboard now **transparently communicates data freshness** to users! 🎉
