"""
Metric card components for Overview dashboard
"""

import streamlit as st
import plotly.graph_objects as go
from config import INDICATOR_METADATA, COLORS
from utils import calculate_statistics, determine_trend, get_trend_emoji, format_value


def create_metric_card(indicator_key, df):
    """
    Create a metric card with sparkline for overview display

    Args:
        indicator_key: Key from seriesIds (e.g., 's&p500')
        df: DataFrame with Date and Value columns

    Returns:
        None (renders directly to Streamlit)
    """
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
    st.plotly_chart(sparkline_fig, config={'displayModeBar': False}, key=f'spark_{indicator_key}')


def create_stats_summary(indicator_key, df):
    """
    Create statistics summary cards

    Args:
        indicator_key: Key from seriesIds
        df: DataFrame with data

    Returns:
        dict: Statistics for display
    """
    if df.empty:
        return None

    stats = calculate_statistics(df)
    return {
        'latest': format_value(stats['latest'], indicator_key),
        'change_1d': f"{stats['change_1d']:+.2f}%",
        'change_7d': f"{stats['change_7d']:+.2f}%",
        'change_30d': f"{stats['change_30d']:+.2f}%",
        'change_ytd': f"{stats['change_ytd']:+.2f}%",
        'min': format_value(stats['min'], indicator_key),
        'max': format_value(stats['max'], indicator_key),
        'mean': format_value(stats['mean'], indicator_key),
        'std': f"{stats['std']:.2f}"
    }
