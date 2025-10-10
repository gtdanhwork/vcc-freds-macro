"""
Chart rendering components
Contains functions for creating various chart types
"""

import streamlit as st
import plotly.graph_objects as go
from config import INDICATOR_METADATA, COLORS, CHART_DEFAULTS
from utils import calculate_moving_average


def create_sparkline_chart(df, indicator_key, height=60):
    """
    Create a mini sparkline chart

    Args:
        df: DataFrame with Date and Value columns
        indicator_key: Indicator identifier
        height: Chart height in pixels

    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'].tail(30),
        y=df['Value'].tail(30),
        mode='lines',
        line=dict(color=COLORS['primary'], width=1.5),
        fill='tozeroy',
        fillcolor=f"rgba(30, 136, 229, 0.1)"
    ))
    fig.update_layout(
        showlegend=False,
        height=height,
        margin=dict(l=0, r=0, t=5, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def create_detailed_chart(df, indicator_key, chart_type='Line', show_ma=False):
    """
    Create detailed chart with options for different visualization types

    Args:
        df: DataFrame with Date and Value columns
        indicator_key: Indicator identifier
        chart_type: 'Line', 'Area', or 'Bar'
        show_ma: Boolean to show moving averages

    Returns:
        None (renders directly to Streamlit)
    """
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

    st.plotly_chart(fig)


def create_comparison_chart(data_dict, selected_indicators):
    """
    Create normalized comparison chart for multiple indicators

    Args:
        data_dict: Dictionary of {indicator_key: DataFrame}
        selected_indicators: List of indicator keys to plot

    Returns:
        Plotly figure object
    """
    fig = go.Figure()

    for indicator_key in selected_indicators:
        df = data_dict.get(indicator_key)
        metadata = INDICATOR_METADATA.get(indicator_key, {})

        if df is not None and not df.empty:
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

    return fig


def create_correlation_heatmap(correlation_matrix, indicator_names):
    """
    Create correlation heatmap

    Args:
        correlation_matrix: 2D list of correlation values
        indicator_names: List of indicator names for labels

    Returns:
        Plotly figure object
    """
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=indicator_names,
        y=indicator_names,
        colorscale='RdBu',
        zmid=0,
        text=[[f'{val:.2f}' for val in row] for row in correlation_matrix],
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title="Correlation")
    ))

    fig.update_layout(
        title="Indicator Correlation",
        template='plotly_dark',
        height=400
    )

    return fig
