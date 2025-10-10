"""
Configuration file for FRED Bitcoin Macro Dashboard
Contains categories, color schemes, thresholds, and display settings
"""

# Indicator Categories for organized display
INDICATOR_CATEGORIES = {
    'Market Indices': ['s&p500', 'dxy'],
    'Monetary Policy': ['fed_rate', 'fed_balance_sheet'],
    'Economic Health': ['gdp', 'cpi', 'unemployment', 'consumer_confidence'],
    'Risk & Debt': ['geopolitial_risk', 'national_debt']
}

# Indicator display metadata
INDICATOR_METADATA = {
    's&p500': {
        'name': 'S&P 500',
        'unit': 'points',
        'format': '{:,.0f}',
        'icon': '📈',
        'description': 'S&P 500 stock market index',
        'higher_is_better': True
    },
    'fed_rate': {
        'name': 'Fed Funds Rate',
        'unit': '%',
        'format': '{:.2f}%',
        'icon': '🏦',
        'description': 'Federal Reserve interest rate',
        'higher_is_better': None  # Context-dependent
    },
    'dxy': {
        'name': 'Dollar Index',
        'unit': 'index',
        'format': '{:.2f}',
        'icon': '💵',
        'description': 'US Dollar strength vs basket of currencies',
        'higher_is_better': False  # Stronger dollar = bearish for BTC
    },
    'fed_balance_sheet': {
        'name': 'Fed Balance Sheet',
        'unit': 'trillion',
        'format': '{:.2f}T',
        'icon': '🏛️',
        'description': 'Federal Reserve total assets',
        'higher_is_better': True  # More liquidity = bullish
    },
    'cpi': {
        'name': 'CPI (Inflation)',
        'unit': '%',
        'format': '{:.1f}%',
        'icon': '📊',
        'description': 'Consumer Price Index - inflation measure',
        'higher_is_better': False
    },
    'unemployment': {
        'name': 'Unemployment',
        'unit': '%',
        'format': '{:.1f}%',
        'icon': '👥',
        'description': 'Unemployment rate',
        'higher_is_better': False
    },
    'consumer_confidence': {
        'name': 'Consumer Confidence',
        'unit': 'index',
        'format': '{:.1f}',
        'icon': '🛒',
        'description': 'University of Michigan Consumer Sentiment',
        'higher_is_better': True
    },
    'national_debt': {
        'name': 'National Debt/GDP',
        'unit': '% of GDP',
        'format': '{:.1f}%',
        'icon': '💳',
        'description': 'Federal debt as % of GDP',
        'higher_is_better': False
    },
    'gdp': {
        'name': 'GDP Growth',
        'unit': 'billion',
        'format': '{:,.0f}B',
        'icon': '🌐',
        'description': 'Gross Domestic Product (Real)',
        'higher_is_better': True
    },
    'geopolitial_risk': {
        'name': 'VIX (Volatility)',
        'unit': 'index',
        'format': '{:.2f}',
        'icon': '⚠️',
        'description': 'CBOE Volatility Index - market fear gauge',
        'higher_is_better': False
    }
}

# Color scheme
COLORS = {
    'bullish': '#00C853',      # Green
    'bearish': '#FF1744',      # Red
    'neutral': '#FFB300',      # Amber/Yellow
    'primary': '#1E88E5',      # Blue
    'background': '#0E1117',   # Dark background
    'card_bg': '#262730',      # Card background
    'text_primary': '#FAFAFA', # White text
    'text_secondary': '#B0B0B0' # Gray text
}

# Signal thresholds for trading signals
# These can be customized based on your strategy
SIGNAL_THRESHOLDS = {
    's&p500': {
        'buy_threshold': 0.5,   # % increase threshold
        'sell_threshold': -0.5,
        'lookback_periods': 20
    },
    'fed_rate': {
        'buy_threshold': -0.1,  # Rate cuts = bullish
        'sell_threshold': 0.1,  # Rate hikes = bearish
        'lookback_periods': 3
    },
    'dxy': {
        'buy_threshold': -1.0,  # Dollar weakness = bullish for BTC
        'sell_threshold': 1.0,
        'lookback_periods': 20
    },
    'fed_balance_sheet': {
        'buy_threshold': 1.0,   # Expansion = bullish
        'sell_threshold': -1.0,
        'lookback_periods': 4
    },
    'cpi': {
        'buy_threshold': -0.2,  # Falling inflation = bullish
        'sell_threshold': 0.2,
        'lookback_periods': 3
    },
    'unemployment': {
        'buy_threshold': -0.3,  # Falling unemployment = bullish
        'sell_threshold': 0.3,
        'lookback_periods': 3
    },
    'consumer_confidence': {
        'buy_threshold': 2.0,
        'sell_threshold': -2.0,
        'lookback_periods': 3
    },
    'national_debt': {
        'buy_threshold': -1.0,  # Decreasing debt = bullish
        'sell_threshold': 1.0,
        'lookback_periods': 4
    },
    'gdp': {
        'buy_threshold': 0.5,
        'sell_threshold': -0.5,
        'lookback_periods': 4
    },
    'geopolitial_risk': {
        'buy_threshold': -5.0,  # Falling VIX = bullish
        'sell_threshold': 5.0,
        'lookback_periods': 20
    }
}

# Overall signal aggregation thresholds
OVERALL_SIGNAL_THRESHOLDS = {
    'strong_buy': 7,    # Need 7+ buy signals
    'buy': 6,           # Need 6 buy signals
    'neutral_min': 4,   # 4-5 buy signals = neutral
    'neutral_max': 5,
    'sell': 3,          # 3 or fewer buy signals = sell
    'strong_sell': 2    # 2 or fewer = strong sell
}

# Chart default settings
CHART_DEFAULTS = {
    'height': 400,
    'template': 'plotly_dark',
    'line_width': 2,
    'show_grid': True,
    'moving_averages': [20, 50, 200]
}

# Time period presets
TIME_PERIODS = {
    'Last 30 Days': 30,
    'Last 90 Days': 90,
    'Last 6 Months': 180,
    'Last Year': 365,
    'Last 2 Years': 730,
    'Last 5 Years': 1825,
    'All Time': 10000
}

# Export settings
EXPORT_FORMATS = ['CSV', 'JSON', 'Excel']
