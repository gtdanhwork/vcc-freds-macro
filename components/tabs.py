"""
Tab rendering components for different dashboard views
"""

import streamlit as st
from seriesIds import FRED_SERIES_IDS
from config import INDICATOR_CATEGORIES, INDICATOR_METADATA
from monitor_enhanced import analyze_signals
from utils import get_signal_emoji, calculate_correlation
from .metric_cards import create_metric_card, create_stats_summary
from .charts import create_detailed_chart, create_comparison_chart, create_correlation_heatmap


def render_overview_tab(get_filtered_data_func, start_date, limit):
    """
    Render the Overview tab with all indicators in grid layout

    Args:
        get_filtered_data_func: Function to get filtered data for an indicator
        start_date: Filter start date
        limit: Max data points
    """
    st.header("Macro Indicators Overview")
    st.markdown("Real-time view of all economic indicators")

    # Display indicators by category
    for category, indicators in INDICATOR_CATEGORIES.items():
        st.subheader(category)

        # Create columns for metric cards (4 per row)
        cols = st.columns(4)

        for idx, indicator_key in enumerate(indicators):
            series_id = FRED_SERIES_IDS[indicator_key]
            df = get_filtered_data_func(series_id, start_date, limit)

            with cols[idx % 4]:
                with st.container():
                    create_metric_card(indicator_key, df)

        st.markdown("---")


def render_analysis_tab(get_filtered_data_func, start_date, limit, show_table, show_statistics):
    """
    Render the Detailed Analysis tab

    Args:
        get_filtered_data_func: Function to get filtered data
        start_date: Filter start date
        limit: Max data points
        show_table: Boolean to show data table
        show_statistics: Boolean to show statistics panel
    """
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
    df = get_filtered_data_func(selected_series_id, start_date, limit)

    # Display chart
    create_detailed_chart(df, selected_key, chart_type, show_ma)

    # Statistics panel
    if show_statistics and not df.empty:
        st.subheader("📊 Statistics")

        stats = create_stats_summary(selected_key, df)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Latest Value", stats['latest'])
        with col2:
            st.metric("1-Day Change", stats['change_1d'])
        with col3:
            st.metric("7-Day Change", stats['change_7d'])
        with col4:
            st.metric("30-Day Change", stats['change_30d'])
        with col5:
            st.metric("YTD Change", stats['change_ytd'])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Minimum", stats['min'])
        with col2:
            st.metric("Maximum", stats['max'])
        with col3:
            st.metric("Average", stats['mean'])
        with col4:
            st.metric("Std Dev", stats['std'])

    # Data table
    if show_table and not df.empty:
        st.subheader("📋 Data Table")
        st.dataframe(df.sort_values('Date', ascending=False), width="stretch")


def render_signals_tab(all_data):
    """
    Render the Trading Signals tab

    Args:
        all_data: Dictionary of all cached FRED data
    """
    st.header("🎯 Trading Signal Analysis")
    st.markdown("Automated buy/sell signals based on macroeconomic trends")

    # Analyze all signals
    with st.spinner("Analyzing signals..."):
        analysis_results = analyze_signals(all_data)

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
                    from utils import format_value
                    latest = stats.get('latest', 0)
                    st.markdown(f"{format_value(latest, indicator_key)}")


def render_comparison_tab(get_filtered_data_func, start_date, limit):
    """
    Render the Comparison tab

    Args:
        get_filtered_data_func: Function to get filtered data
        start_date: Filter start date
        limit: Max data points
    """
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
        # Build data dictionary
        data_dict = {}
        for indicator_key in selected_indicators:
            series_id = FRED_SERIES_IDS[indicator_key]
            df = get_filtered_data_func(series_id, start_date, limit)
            if not df.empty:
                data_dict[indicator_key] = df

        # Create comparison chart
        fig = create_comparison_chart(data_dict, selected_indicators)
        st.plotly_chart(fig, width="stretch")

        # Correlation matrix
        if len(selected_indicators) >= 2:
            st.subheader("Correlation Matrix")

            # Calculate correlations
            corr_matrix = []
            for ind1 in selected_indicators:
                row = []
                for ind2 in selected_indicators:
                    if ind1 in data_dict and ind2 in data_dict:
                        corr = calculate_correlation(data_dict[ind1], data_dict[ind2])
                        row.append(corr)
                    else:
                        row.append(0)
                corr_matrix.append(row)

            # Get indicator names
            indicator_names = [INDICATOR_METADATA.get(k, {}).get('name', k) for k in selected_indicators]

            # Display correlation heatmap
            fig_corr = create_correlation_heatmap(corr_matrix, indicator_names)
            st.plotly_chart(fig_corr, width="stretch")
    else:
        st.info("Please select at least 2 indicators to compare")
