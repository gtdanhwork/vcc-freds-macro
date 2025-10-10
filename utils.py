"""
Utility functions for FRED Bitcoin Macro Dashboard
Includes calculations for trends, statistics, signals, and data processing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config import SIGNAL_THRESHOLDS, INDICATOR_METADATA, COLORS

def calculate_percentage_change(df, periods=1):
    """
    Calculate percentage change over specified periods

    Args:
        df: DataFrame with 'Value' column
        periods: Number of periods to look back (default 1)

    Returns:
        float: Percentage change
    """
    if len(df) < periods + 1:
        return 0.0

    current_value = df['Value'].iloc[-1]
    previous_value = df['Value'].iloc[-(periods + 1)]

    if previous_value == 0:
        return 0.0

    return ((current_value - previous_value) / previous_value) * 100

def calculate_moving_average(df, window=20):
    """
    Calculate simple moving average

    Args:
        df: DataFrame with 'Value' column
        window: Window size for MA (default 20)

    Returns:
        Series: Moving average values
    """
    if len(df) < window:
        return pd.Series([np.nan] * len(df))

    return df['Value'].rolling(window=window).mean()

def calculate_statistics(df):
    """
    Calculate comprehensive statistics for a dataset

    Args:
        df: DataFrame with 'Value' column

    Returns:
        dict: Statistics including min, max, mean, std, etc.
    """
    if df.empty or 'Value' not in df.columns:
        return {
            'count': 0,
            'latest': 0,
            'min': 0,
            'max': 0,
            'mean': 0,
            'median': 0,
            'std': 0,
            'change_1d': 0,
            'change_7d': 0,
            'change_30d': 0,
            'change_ytd': 0
        }

    values = df['Value']

    # Calculate changes
    change_1d = calculate_percentage_change(df, 1) if len(df) >= 2 else 0
    change_7d = calculate_percentage_change(df, 7) if len(df) >= 8 else 0
    change_30d = calculate_percentage_change(df, 30) if len(df) >= 31 else 0

    # Calculate YTD change
    current_year = datetime.now().year
    ytd_df = df[pd.to_datetime(df['Date']).dt.year == current_year]
    if len(ytd_df) >= 2:
        ytd_start = ytd_df['Value'].iloc[0]
        ytd_current = ytd_df['Value'].iloc[-1]
        change_ytd = ((ytd_current - ytd_start) / ytd_start * 100) if ytd_start != 0 else 0
    else:
        change_ytd = 0

    return {
        'count': len(values),
        'latest': float(values.iloc[-1]) if len(values) > 0 else 0,
        'min': float(values.min()),
        'max': float(values.max()),
        'mean': float(values.mean()),
        'median': float(values.median()),
        'std': float(values.std()),
        'change_1d': change_1d,
        'change_7d': change_7d,
        'change_30d': change_30d,
        'change_ytd': change_ytd
    }

def determine_trend(df, periods=20):
    """
    Determine if indicator is trending up, down, or sideways

    Args:
        df: DataFrame with 'Value' column
        periods: Lookback periods for trend analysis

    Returns:
        str: 'up', 'down', or 'neutral'
    """
    if len(df) < periods:
        return 'neutral'

    pct_change = calculate_percentage_change(df, periods)

    if pct_change > 2:
        return 'up'
    elif pct_change < -2:
        return 'down'
    else:
        return 'neutral'

def get_trend_emoji(trend):
    """
    Get emoji representation of trend

    Args:
        trend: 'up', 'down', or 'neutral'

    Returns:
        str: Emoji arrow
    """
    if trend == 'up':
        return '↑'
    elif trend == 'down':
        return '↓'
    else:
        return '→'

def get_trend_color(trend):
    """
    Get color for trend visualization

    Args:
        trend: 'up', 'down', or 'neutral'

    Returns:
        str: Color hex code
    """
    if trend == 'up':
        return COLORS['bullish']
    elif trend == 'down':
        return COLORS['bearish']
    else:
        return COLORS['neutral']

def calculate_signal(indicator_key, df):
    """
    Calculate buy/sell/neutral signal for an indicator

    Args:
        indicator_key: Key from seriesIds (e.g., 's&p500')
        df: DataFrame with historical data

    Returns:
        str: 'BUY', 'SELL', or 'NEUTRAL'
    """
    if indicator_key not in SIGNAL_THRESHOLDS:
        return 'NEUTRAL'

    thresholds = SIGNAL_THRESHOLDS[indicator_key]
    lookback = thresholds['lookback_periods']

    if len(df) < lookback + 1:
        return 'NEUTRAL'

    # Calculate percentage change over lookback period
    pct_change = calculate_percentage_change(df, lookback)

    # Compare with thresholds
    if pct_change >= thresholds['buy_threshold']:
        return 'BUY'
    elif pct_change <= thresholds['sell_threshold']:
        return 'SELL'
    else:
        return 'NEUTRAL'

def get_signal_emoji(signal):
    """
    Get emoji for signal type

    Args:
        signal: 'BUY', 'SELL', or 'NEUTRAL'

    Returns:
        str: Signal emoji
    """
    if signal == 'BUY':
        return '🟢'
    elif signal == 'SELL':
        return '🔴'
    else:
        return '🟡'

def get_signal_color(signal):
    """
    Get color for signal type

    Args:
        signal: 'BUY', 'SELL', or 'NEUTRAL'

    Returns:
        str: Color hex code
    """
    if signal == 'BUY':
        return COLORS['bullish']
    elif signal == 'SELL':
        return COLORS['bearish']
    else:
        return COLORS['neutral']

def aggregate_signals(signal_dict):
    """
    Aggregate individual signals into overall market signal

    Args:
        signal_dict: Dictionary of {indicator: signal}

    Returns:
        tuple: (overall_signal, buy_count, sell_count, neutral_count)
    """
    buy_count = sum(1 for s in signal_dict.values() if s == 'BUY')
    sell_count = sum(1 for s in signal_dict.values() if s == 'SELL')
    neutral_count = sum(1 for s in signal_dict.values() if s == 'NEUTRAL')

    total = len(signal_dict)

    # Determine overall signal based on buy signals count
    from config import OVERALL_SIGNAL_THRESHOLDS as thresholds

    if buy_count >= thresholds['strong_buy']:
        overall = 'STRONG BUY'
    elif buy_count >= thresholds['buy']:
        overall = 'BUY'
    elif buy_count >= thresholds['neutral_min'] and buy_count <= thresholds['neutral_max']:
        overall = 'NEUTRAL'
    elif buy_count >= thresholds['sell']:
        overall = 'SELL'
    else:
        overall = 'STRONG SELL'

    return overall, buy_count, sell_count, neutral_count

def format_value(value, indicator_key):
    """
    Format value according to indicator metadata

    Args:
        value: Numeric value
        indicator_key: Key from seriesIds

    Returns:
        str: Formatted value string
    """
    if indicator_key not in INDICATOR_METADATA:
        return f'{value:,.2f}'

    format_str = INDICATOR_METADATA[indicator_key]['format']

    # Handle trillion conversion for fed_balance_sheet
    if indicator_key == 'fed_balance_sheet':
        value = value / 1000  # Convert billions to trillions

    # Handle billion conversion for gdp
    if indicator_key == 'gdp':
        value = value / 1000  # Display in billions

    try:
        return format_str.format(value)
    except:
        return f'{value:,.2f}'

def create_sparkline_data(df, points=20):
    """
    Create simplified data for sparkline visualization

    Args:
        df: DataFrame with 'Value' column
        points: Number of points to include in sparkline

    Returns:
        list: Simplified values for sparkline
    """
    if df.empty:
        return []

    # Get last N points
    values = df['Value'].tail(points).tolist()
    return values

def calculate_volatility(df, window=30):
    """
    Calculate volatility (standard deviation of returns)

    Args:
        df: DataFrame with 'Value' column
        window: Window for volatility calculation

    Returns:
        float: Volatility percentage
    """
    if len(df) < window + 1:
        return 0.0

    # Calculate returns
    returns = df['Value'].pct_change()

    # Calculate rolling volatility
    volatility = returns.tail(window).std() * 100

    return volatility if not np.isnan(volatility) else 0.0

def calculate_correlation(df1, df2):
    """
    Calculate correlation between two indicators

    Args:
        df1: First DataFrame with 'Date' and 'Value' columns
        df2: Second DataFrame with 'Date' and 'Value' columns

    Returns:
        float: Correlation coefficient (-1 to 1)
    """
    if df1.empty or df2.empty:
        return 0.0

    # Merge on date to align data points
    merged = pd.merge(
        df1[['Date', 'Value']].rename(columns={'Value': 'v1'}),
        df2[['Date', 'Value']].rename(columns={'Value': 'v2'}),
        on='Date',
        how='inner'
    )

    if len(merged) < 2:
        return 0.0

    correlation = merged['v1'].corr(merged['v2'])

    return correlation if not np.isnan(correlation) else 0.0

def get_last_updated_time(df):
    """
    Get the last updated timestamp from dataframe

    Args:
        df: DataFrame with 'Date' column

    Returns:
        str: Formatted date string
    """
    if df.empty:
        return 'N/A'

    last_date = pd.to_datetime(df['Date'].iloc[-1])
    return last_date.strftime('%Y-%m-%d')

def export_to_csv(df, filename):
    """
    Export dataframe to CSV

    Args:
        df: DataFrame to export
        filename: Output filename

    Returns:
        str: Success message or error
    """
    try:
        df.to_csv(filename, index=False)
        return f'Successfully exported to {filename}'
    except Exception as e:
        return f'Error exporting: {str(e)}'

def export_to_json(df, filename):
    """
    Export dataframe to JSON

    Args:
        df: DataFrame to export
        filename: Output filename

    Returns:
        str: Success message or error
    """
    try:
        df.to_json(filename, orient='records', date_format='iso')
        return f'Successfully exported to {filename}'
    except Exception as e:
        return f'Error exporting: {str(e)}'
