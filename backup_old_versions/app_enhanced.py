"""
Enhanced Bitcoin Macro Factor Dashboard
Multi-tab UI with overview, detailed analysis, signals, and comparison views
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
from seriesIds import FRED_SERIES_IDS
from monitor_enhanced import fetch_all_fred_data, analyze_signals
from config import (
    INDICATOR_CATEGORIES, INDICATOR_METADATA, COLORS,
    TIME_PERIODS, CHART_DEFAULTS, OVERALL_SIGNAL_THRESHOLDS
)
from utils import (
    calculate_statistics, determine_trend, get_trend_emoji,
    format_value, calculate_moving_average, get_signal_emoji,
    get_signal_color, calculate_correlation
)

# Page configuration
st.set_page_config(
    page_title="Bitcoin Macro Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
    }
    .bullish { color: #00C853; font-weight: bold; }
    .bearish { color: #FF1744; font-weight: bold; }
    .neutral { color: #FFB300; font-weight: bold; }
    .big-number { font-size: 32px; font-weight: bold; }
    .indicator-name { font-size: 14px; color: #B0B0B0; }
    .change-positive { color: #00C853; }
    .change-negative { color: #FF1744; }
    </style>
""", unsafe_allow_html=True)

# --- DATA CACHING ---
@st.cache_data(ttl=3600 * 24)  # Cache for 24 hours
def load_all_data():
    """Load and cache all FRED data"""
    return fetch_all_fred_data()

# Load data into session state
if "all_data" not in st.session_state:
    with st.spinner("📊 Loading historical FRED data... (First load may take a minute)"):
        st.session_state.all_data = load_all_data()
        st.session_state.last_refresh = pd.Timestamp.now()

# --- HELPER FUNCTIONS ---

def get_filtered_data(series_id, start_date, limit):
    """Filter cached data based on user input"""
    data = st.session_state.all_data.get(series_id, [])

    if not data:
        return pd.DataFrame({"Date": [], "Value": []})

    # Filter by date
    start_date_str = start_date.strftime("%Y-%m-%d")
    date_filtered_data = [
        item for item in data
        if item["Date"] >= start_date_str
    ]

    # Limit to most recent N values
    final_data = date_filtered_data[-limit:]

    # Convert to DataFrame
    df = pd.DataFrame(final_data, columns=["Date", "Value"])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df.dropna(subset=['Value'], inplace=True)

    return df

def create_metric_card(indicator_key, df):
    """Create a metric card with sparkline for overview"""
    if df.empty:
        # Show which indicator has no data
        metadata = INDICATOR_METADATA.get(indicator_key, {})
        st.warning(f"{metadata.get('icon', '❌')} {metadata.get('name', indicator_key)}\n\nNo data available")
        return None

    stats = calculate_statistics(df)
    metadata = INDICATOR_METADATA.get(indicator_key, {})

    latest_value = stats['latest']
    change_30d = stats['change_30d']
    trend = determine_trend(df, 20)
    trend_emoji = get_trend_emoji(trend)

    # Format value
    formatted_value = format_value(latest_value, indicator_key)

    # Color based on change
    change_color = "change-positive" if change_30d > 0 else "change-negative"

    # ============================================================
    # FIXED: Removed nested columns to prevent overflow
    # Cards are already in a 4-column grid from the Overview tab
    # Adding columns here was causing charts to overlay next cards
    # Now: Simple vertical stack (text above, chart below)
    # ============================================================

    # Indicator name, value, and change percentage
    st.markdown(f"<div class='indicator-name'>{metadata.get('icon', '')} {metadata.get('name', indicator_key)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{formatted_value}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='{change_color}'>{trend_emoji} {change_30d:+.2f}% (30d)</div>", unsafe_allow_html=True)

    # Sparkline chart below text
    sparkline_fig = go.Figure()
    sparkline_fig.add_trace(go.Scatter(
        x=df['Date'].tail(30),
        y=df['Value'].tail(30),
        mode='lines',
        line=dict(color=COLORS['primary'], width=1.5),
        fill='tozeroy',
        fillcolor=f"rgba(30, 136, 229, 0.1)"
    ))
    sparkline_fig.update_layout(
        showlegend=False,
        height=60,
        margin=dict(l=0, r=0, t=5, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(sparkline_fig, use_container_width=True, config={'displayModeBar': False}, key=f'spark_{indicator_key}')

def create_detailed_chart(df, indicator_key, chart_type='Line', show_ma=False):
    """Create detailed chart with options"""
    if df.empty:
        st.warning("No data available for this indicator")
        return

    metadata = INDICATOR_METADATA.get(indicator_key, {})

    # Create figure
    fig = go.Figure()

    # Main data trace
    if chart_type == 'Line':
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Value'],
            mode='lines',
            name=metadata.get('name', indicator_key),
            line=dict(color=COLORS['primary'], width=2)
        ))
    elif chart_type == 'Area':
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Value'],
            mode='lines',
            name=metadata.get('name', indicator_key),
            fill='tozeroy',
            line=dict(color=COLORS['primary'], width=2)
        ))
    elif chart_type == 'Bar':
        fig.add_trace(go.Bar(
            x=df['Date'],
            y=df['Value'],
            name=metadata.get('name', indicator_key),
            marker_color=COLORS['primary']
        ))

    # Add moving averages if requested
    if show_ma:
        for ma_period in [20, 50, 200]:
            if len(df) >= ma_period:
                ma_values = calculate_moving_average(df, ma_period)
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=ma_values,
                    mode='lines',
                    name=f'MA{ma_period}',
                    line=dict(width=1, dash='dash'),
                    opacity=0.7
                ))

    # Update layout
    fig.update_layout(
        title=f"{metadata.get('icon', '')} {metadata.get('name', indicator_key)}",
        xaxis_title="Date",
        yaxis_title=metadata.get('unit', 'Value'),
        template='plotly_dark',
        height=CHART_DEFAULTS['height'],
        hovermode='x unified',
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")

    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")

    # Time period selection
    st.subheader("📅 Time Period")
    period_preset = st.selectbox(
        "Quick Select",
        list(TIME_PERIODS.keys()),
        index=2  # Default to "Last 6 Months"
    )

    if period_preset != 'Custom':
        days = TIME_PERIODS[period_preset]
        default_start_date = date.today() - timedelta(days=days)
    else:
        default_start_date = date.today() - timedelta(days=365)

    start_date = st.date_input(
        "Start Date",
        value=default_start_date,
        max_value=date.today()
    )

    limit = st.number_input(
        "Max Data Points",
        min_value=10,
        max_value=10000,
        value=500,
        step=50
    )

    st.markdown("---")

    # Display options
    st.subheader("🎨 Display Options")
    show_table = st.checkbox("Show Data Table", value=False)
    show_statistics = st.checkbox("Show Statistics", value=True)

    st.markdown("---")

    # Last refresh time
    if "last_refresh" in st.session_state:
        st.caption(f"Last updated: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M')}")

# --- MAIN CONTENT ---

st.title("📈 Bitcoin Macro Factor Dashboard")
st.markdown("Monitor key macroeconomic indicators for Bitcoin trading signals")

# Tab navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🔍 Detailed Analysis",
    "🎯 Trading Signals",
    "📈 Comparison"
])

# --- TAB 1: OVERVIEW ---
with tab1:
    st.header("Macro Indicators Overview")
    st.markdown("Real-time view of all economic indicators")

    # Display indicators by category
    for category, indicators in INDICATOR_CATEGORIES.items():
        st.subheader(category)

        # Create columns for metric cards (4 per row)
        cols = st.columns(4)

        for idx, indicator_key in enumerate(indicators):
            series_id = FRED_SERIES_IDS[indicator_key]
            df = get_filtered_data(series_id, start_date, limit)

            with cols[idx % 4]:
                with st.container():
                    create_metric_card(indicator_key, df)

        st.markdown("---")

# --- TAB 2: DETAILED ANALYSIS ---
with tab2:
    st.header("Detailed Indicator Analysis")

    # Indicator selection
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        selected_key = st.selectbox(
            "Select Indicator",
            list(FRED_SERIES_IDS.keys()),
            format_func=lambda x: f"{INDICATOR_METADATA.get(x, {}).get('icon', '')} {INDICATOR_METADATA.get(x, {}).get('name', x)}"
        )

    with col2:
        chart_type = st.selectbox("Chart Type", ['Line', 'Area', 'Bar'])

    with col3:
        show_ma = st.checkbox("Show Moving Averages", value=False)

    # Get data for selected indicator
    selected_series_id = FRED_SERIES_IDS[selected_key]
    df = get_filtered_data(selected_series_id, start_date, limit)

    # Display chart
    create_detailed_chart(df, selected_key, chart_type, show_ma)

    # Statistics panel
    if show_statistics and not df.empty:
        st.subheader("📊 Statistics")

        stats = calculate_statistics(df)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Latest Value", format_value(stats['latest'], selected_key))
        with col2:
            st.metric("1-Day Change", f"{stats['change_1d']:+.2f}%")
        with col3:
            st.metric("7-Day Change", f"{stats['change_7d']:+.2f}%")
        with col4:
            st.metric("30-Day Change", f"{stats['change_30d']:+.2f}%")
        with col5:
            st.metric("YTD Change", f"{stats['change_ytd']:+.2f}%")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Minimum", format_value(stats['min'], selected_key))
        with col2:
            st.metric("Maximum", format_value(stats['max'], selected_key))
        with col3:
            st.metric("Average", format_value(stats['mean'], selected_key))
        with col4:
            st.metric("Std Dev", f"{stats['std']:.2f}")

    # Data table
    if show_table and not df.empty:
        st.subheader("📋 Data Table")
        st.dataframe(df.sort_values('Date', ascending=False), use_container_width=True)

# --- TAB 3: TRADING SIGNALS ---
with tab3:
    st.header("🎯 Trading Signal Analysis")
    st.markdown("Automated buy/sell signals based on macroeconomic trends")

    # Analyze all signals
    with st.spinner("Analyzing signals..."):
        analysis_results = analyze_signals(st.session_state.all_data)

    # Overall signal display
    overall_signal = analysis_results['overall_signal']
    buy_count = analysis_results['buy_count']
    sell_count = analysis_results['sell_count']
    neutral_count = analysis_results['neutral_count']
    total = buy_count + sell_count + neutral_count

    # Determine overall color
    if 'BUY' in overall_signal:
        signal_class = 'bullish'
    elif 'SELL' in overall_signal:
        signal_class = 'bearish'
    else:
        signal_class = 'neutral'

    # Overall signal card
    st.markdown(f"""
        <div style='background-color: #262730; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;'>
            <h2>Overall Market Signal</h2>
            <div class='{signal_class}' style='font-size: 48px; margin: 20px 0;'>
                {get_signal_emoji(overall_signal)} {overall_signal}
            </div>
            <p style='font-size: 18px; color: #B0B0B0;'>
                {buy_count} of {total} indicators bullish
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Signal summary
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🟢 Buy Signals", buy_count)
    with col2:
        st.metric("🔴 Sell Signals", sell_count)
    with col3:
        st.metric("🟡 Neutral Signals", neutral_count)

    st.markdown("---")

    # Individual indicator signals
    st.subheader("Indicator Breakdown")

    # Group by category
    for category, indicators in INDICATOR_CATEGORIES.items():
        with st.expander(f"{category}", expanded=True):
            for indicator_key in indicators:
                signal = analysis_results['signals'].get(indicator_key, 'NEUTRAL')
                stats = analysis_results['statistics'].get(indicator_key, {})
                metadata = INDICATOR_METADATA.get(indicator_key, {})

                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

                with col1:
                    st.markdown(f"{metadata.get('icon', '')} **{metadata.get('name', indicator_key)}**")

                with col2:
                    signal_color = 'bullish' if signal == 'BUY' else ('bearish' if signal == 'SELL' else 'neutral')
                    st.markdown(f"<span class='{signal_color}'>{get_signal_emoji(signal)} {signal}</span>", unsafe_allow_html=True)

                with col3:
                    change = stats.get('change_30d', 0)
                    change_class = 'change-positive' if change > 0 else 'change-negative'
                    st.markdown(f"<span class='{change_class}'>{change:+.2f}% (30d)</span>", unsafe_allow_html=True)

                with col4:
                    latest = stats.get('latest', 0)
                    st.markdown(f"{format_value(latest, indicator_key)}")

# --- TAB 4: COMPARISON ---
with tab4:
    st.header("📈 Indicator Comparison")
    st.markdown("Compare multiple indicators side by side")

    # Multi-select for indicators
    selected_indicators = st.multiselect(
        "Select Indicators to Compare (up to 4)",
        list(FRED_SERIES_IDS.keys()),
        default=['s&p500', 'dxy'],
        max_selections=4,
        format_func=lambda x: f"{INDICATOR_METADATA.get(x, {}).get('icon', '')} {INDICATOR_METADATA.get(x, {}).get('name', x)}"
    )

    if len(selected_indicators) >= 2:
        # Create comparison chart
        fig = go.Figure()

        for idx, indicator_key in enumerate(selected_indicators):
            series_id = FRED_SERIES_IDS[indicator_key]
            df = get_filtered_data(series_id, start_date, limit)
            metadata = INDICATOR_METADATA.get(indicator_key, {})

            if not df.empty:
                # Normalize to percentage change from first value
                first_value = df['Value'].iloc[0]
                normalized = ((df['Value'] - first_value) / first_value * 100)

                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=normalized,
                    mode='lines',
                    name=metadata.get('name', indicator_key),
                    line=dict(width=2)
                ))

        fig.update_layout(
            title="Normalized Comparison (% Change from Start)",
            xaxis_title="Date",
            yaxis_title="% Change",
            template='plotly_dark',
            height=500,
            hovermode='x unified',
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # Correlation matrix
        if len(selected_indicators) >= 2:
            st.subheader("Correlation Matrix")

            # Build correlation matrix
            correlation_data = {}
            for indicator_key in selected_indicators:
                series_id = FRED_SERIES_IDS[indicator_key]
                df = get_filtered_data(series_id, start_date, limit)
                if not df.empty:
                    correlation_data[indicator_key] = df

            # Calculate correlations
            corr_matrix = []
            for ind1 in selected_indicators:
                row = []
                for ind2 in selected_indicators:
                    if ind1 in correlation_data and ind2 in correlation_data:
                        corr = calculate_correlation(correlation_data[ind1], correlation_data[ind2])
                        row.append(corr)
                    else:
                        row.append(0)
                corr_matrix.append(row)

            # Display correlation heatmap
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr_matrix,
                x=[INDICATOR_METADATA.get(k, {}).get('name', k) for k in selected_indicators],
                y=[INDICATOR_METADATA.get(k, {}).get('name', k) for k in selected_indicators],
                colorscale='RdBu',
                zmid=0,
                text=[[f'{val:.2f}' for val in row] for row in corr_matrix],
                texttemplate='%{text}',
                textfont={"size": 12},
                colorbar=dict(title="Correlation")
            ))

            fig_corr.update_layout(
                title="Indicator Correlation",
                template='plotly_dark',
                height=400
            )

            st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Please select at least 2 indicators to compare")

# Footer
st.markdown("---")
st.caption("Data source: Federal Reserve Economic Data (FRED) | Dashboard by Claude Code")
