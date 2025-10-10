"""
Components package for Bitcoin Macro Dashboard
Contains reusable UI components
"""

from .metric_cards import create_metric_card
from .charts import create_detailed_chart, create_sparkline_chart
from .sidebar import render_sidebar
from .tabs import render_overview_tab, render_analysis_tab, render_signals_tab, render_comparison_tab
from .data_monitor import (
    render_cache_status,
    render_update_frequency_info,
    render_realtime_disclaimer,
    render_data_freshness_badge
)

__all__ = [
    'create_metric_card',
    'create_detailed_chart',
    'create_sparkline_chart',
    'render_sidebar',
    'render_overview_tab',
    'render_analysis_tab',
    'render_signals_tab',
    'render_comparison_tab',
    'render_cache_status',
    'render_update_frequency_info',
    'render_realtime_disclaimer',
    'render_data_freshness_badge'
]
