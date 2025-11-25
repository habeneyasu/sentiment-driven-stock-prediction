"""
Visualization module for technical indicators and price charts.

This module provides visualization routines for overlaying technical indicators
(SMA, EMA, RSI, MACD) on price series using Plotly for interactive charts.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple
from pathlib import Path

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    go = None
    make_subplots = None

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None
    mdates = None


class TechnicalVisualizer:
    """
    A class for visualizing technical indicators on price charts.
    
    Provides methods to create comprehensive charts overlaying SMA, EMA, RSI,
    and MACD on price series. Supports both interactive (Plotly) and static
    (Matplotlib) visualizations.
    
    Example:
        >>> visualizer = TechnicalVisualizer()
        >>> visualizer.plot_price_with_indicators(
        ...     df, ticker='AAPL', indicators=['sma_20', 'ema_12', 'rsi', 'macd']
        ... )
    """
    
    def __init__(self, use_plotly: bool = True):
        """
        Initialize the TechnicalVisualizer.
        
        Args:
            use_plotly: If True and Plotly is available, use Plotly for interactive charts.
                       Otherwise, use Matplotlib for static charts.
        """
        self.use_plotly = use_plotly and PLOTLY_AVAILABLE
        if not self.use_plotly and not MATPLOTLIB_AVAILABLE:
            raise ImportError("Either Plotly or Matplotlib must be installed for visualization")
    
    def plot_price_with_indicators(
        self,
        df: pd.DataFrame,
        ticker: str,
        indicators: Optional[Dict[str, pd.Series]] = None,
        save_path: Optional[Path] = None,
        show: bool = True
    ) -> Optional[go.Figure]:
        """
        Create a comprehensive chart with price and technical indicators.
        
        Creates a multi-panel chart showing:
        - Price chart with SMA/EMA overlays
        - RSI indicator
        - MACD indicator
        - Volume (if available)
        
        Args:
            df: DataFrame with OHLCV data and indicator columns
            ticker: Stock ticker symbol for title
            indicators: Optional dict of indicator names to Series
                       If None, looks for standard columns in df
            save_path: Optional path to save the figure (HTML for Plotly, PNG for Matplotlib)
            show: If True, display the chart (default: True)
            
        Returns:
            go.Figure if using Plotly, None if using Matplotlib
        """
        if self.use_plotly:
            return self._plot_plotly(df, ticker, indicators, save_path, show)
        else:
            return self._plot_matplotlib(df, ticker, indicators, save_path, show)
    
    def _plot_plotly(
        self,
        df: pd.DataFrame,
        ticker: str,
        indicators: Optional[Dict[str, pd.Series]],
        save_path: Optional[Path],
        show: bool
    ) -> go.Figure:
        """Create Plotly interactive chart."""
        # Determine number of rows based on available indicators
        rows = 1  # Price chart
        has_rsi = False
        has_macd = False
        has_volume = 'Volume' in df.columns
        
        # Check for indicators
        if indicators is None:
            indicators = {}
            if 'RSI' in df.columns or 'rsi' in df.columns:
                has_rsi = True
                rows += 1
            if 'MACD' in df.columns or 'macd' in df.columns:
                has_macd = True
                rows += 1
            if 'macd_signal' in df.columns:
                has_macd = True
        else:
            if 'rsi' in indicators or 'RSI' in indicators:
                has_rsi = True
                rows += 1
            if 'macd' in indicators or 'MACD' in indicators:
                has_macd = True
                rows += 1
        
        if has_volume:
            rows += 1
        
        # Create subplots
        subplot_titles = [f'{ticker} - Price Chart with Moving Averages']
        if has_rsi:
            subplot_titles.append('RSI (Relative Strength Index)')
        if has_macd:
            subplot_titles.append('MACD (Moving Average Convergence Divergence)')
        if has_volume:
            subplot_titles.append('Volume')
        
        row_heights = [0.4] + ([0.2] * (rows - 1))
        if has_volume:
            row_heights[-1] = 0.2
        
        fig = make_subplots(
            rows=rows, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=subplot_titles,
            row_heights=row_heights
        )
        
        row_idx = 1
        
        # Price chart with moving averages
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Close'],
                name='Close Price',
                line=dict(color='blue', width=2)
            ),
            row=row_idx, col=1
        )
        
        # Add SMA if available
        for sma_col in ['SMA_20', 'sma_20', 'SMA_50', 'sma_50']:
            if sma_col in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[sma_col],
                        name=sma_col.replace('_', ' ').upper(),
                        line=dict(color='orange', width=1, dash='dash')
                    ),
                    row=row_idx, col=1
                )
        
        # Add EMA if available
        for ema_col in ['EMA_12', 'ema_12', 'EMA_26', 'ema_26']:
            if ema_col in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[ema_col],
                        name=ema_col.replace('_', ' ').upper(),
                        line=dict(color='green', width=1, dash='dot')
                    ),
                    row=row_idx, col=1
                )
        
        # RSI
        if has_rsi:
            row_idx += 1
            rsi_col = 'RSI' if 'RSI' in df.columns else 'rsi'
            if rsi_col in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[rsi_col],
                        name='RSI',
                        line=dict(color='purple', width=2)
                    ),
                    row=row_idx, col=1
                )
                # Add overbought/oversold lines
                fig.add_hline(y=70, line_dash="dash", line_color="red", 
                            annotation_text="Overbought (70)", row=row_idx, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green",
                            annotation_text="Oversold (30)", row=row_idx, col=1)
                fig.update_yaxes(range=[0, 100], row=row_idx, col=1)
        
        # MACD
        if has_macd:
            row_idx += 1
            macd_col = 'MACD' if 'MACD' in df.columns else 'macd'
            signal_col = 'MACD_signal' if 'MACD_signal' in df.columns else 'macd_signal'
            hist_col = 'MACD_histogram' if 'MACD_histogram' in df.columns else 'macd_histogram'
            
            if macd_col in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[macd_col],
                        name='MACD',
                        line=dict(color='blue', width=2)
                    ),
                    row=row_idx, col=1
                )
            
            if signal_col in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[signal_col],
                        name='Signal',
                        line=dict(color='red', width=2)
                    ),
                    row=row_idx, col=1
                )
            
            if hist_col in df.columns:
                colors = ['green' if x >= 0 else 'red' for x in df[hist_col]]
                fig.add_trace(
                    go.Bar(
                        x=df.index,
                        y=df[hist_col],
                        name='Histogram',
                        marker_color=colors,
                        opacity=0.6
                    ),
                    row=row_idx, col=1
                )
        
        # Volume
        if has_volume:
            row_idx += 1
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['Volume'],
                    name='Volume',
                    marker_color='lightblue',
                    opacity=0.6
                ),
                row=row_idx, col=1
            )
        
        # Update layout
        fig.update_xaxes(title_text="Date", row=rows, col=1)
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        if has_rsi:
            fig.update_yaxes(title_text="RSI", row=2, col=1)
        if has_macd:
            fig.update_yaxes(title_text="MACD", row=2 + (1 if has_rsi else 0), col=1)
        if has_volume:
            fig.update_yaxes(title_text="Volume", row=rows, col=1)
        
        fig.update_layout(
            height=800,
            title_text=f'{ticker} - Technical Analysis',
            showlegend=True,
            hovermode='x unified'
        )
        
        if save_path:
            if save_path.suffix == '.html' or save_path.suffix == '':
                save_path = save_path.with_suffix('.html')
            fig.write_html(str(save_path))
        
        if show:
            fig.show()
        
        return fig
    
    def _plot_matplotlib(
        self,
        df: pd.DataFrame,
        ticker: str,
        indicators: Optional[Dict[str, pd.Series]],
        save_path: Optional[Path],
        show: bool
    ) -> None:
        """Create Matplotlib static chart."""
        # Determine number of subplots
        rows = 1
        has_rsi = 'RSI' in df.columns or 'rsi' in df.columns
        has_macd = 'MACD' in df.columns or 'macd' in df.columns
        has_volume = 'Volume' in df.columns
        
        if has_rsi:
            rows += 1
        if has_macd:
            rows += 1
        if has_volume:
            rows += 1
        
        fig, axes = plt.subplots(rows, 1, figsize=(14, 4 * rows), sharex=True)
        if rows == 1:
            axes = [axes]
        
        row_idx = 0
        
        # Price chart
        ax = axes[row_idx]
        ax.plot(df.index, df['Close'], label='Close Price', color='blue', linewidth=2)
        
        # Add SMA
        for sma_col in ['SMA_20', 'sma_20', 'SMA_50', 'sma_50']:
            if sma_col in df.columns:
                ax.plot(df.index, df[sma_col], label=sma_col.replace('_', ' ').upper(),
                       linestyle='--', linewidth=1)
        
        # Add EMA
        for ema_col in ['EMA_12', 'ema_12', 'EMA_26', 'ema_26']:
            if ema_col in df.columns:
                ax.plot(df.index, df[ema_col], label=ema_col.replace('_', ' ').upper(),
                       linestyle=':', linewidth=1)
        
        ax.set_ylabel('Price ($)')
        ax.set_title(f'{ticker} - Price Chart with Moving Averages')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # RSI
        if has_rsi:
            row_idx += 1
            ax = axes[row_idx]
            rsi_col = 'RSI' if 'RSI' in df.columns else 'rsi'
            ax.plot(df.index, df[rsi_col], label='RSI', color='purple', linewidth=2)
            ax.axhline(y=70, color='red', linestyle='--', label='Overbought (70)')
            ax.axhline(y=30, color='green', linestyle='--', label='Oversold (30)')
            ax.set_ylabel('RSI')
            ax.set_title('RSI (Relative Strength Index)')
            ax.set_ylim(0, 100)
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        # MACD
        if has_macd:
            row_idx += 1
            ax = axes[row_idx]
            macd_col = 'MACD' if 'MACD' in df.columns else 'macd'
            signal_col = 'MACD_signal' if 'MACD_signal' in df.columns else 'macd_signal'
            hist_col = 'MACD_histogram' if 'MACD_histogram' in df.columns else 'macd_histogram'
            
            if macd_col in df.columns:
                ax.plot(df.index, df[macd_col], label='MACD', color='blue', linewidth=2)
            if signal_col in df.columns:
                ax.plot(df.index, df[signal_col], label='Signal', color='red', linewidth=2)
            if hist_col in df.columns:
                colors = ['green' if x >= 0 else 'red' for x in df[hist_col]]
                ax.bar(df.index, df[hist_col], label='Histogram', alpha=0.6, color=colors)
            
            ax.set_ylabel('MACD')
            ax.set_title('MACD (Moving Average Convergence Divergence)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        # Volume
        if has_volume:
            row_idx += 1
            ax = axes[row_idx]
            ax.bar(df.index, df['Volume'], label='Volume', alpha=0.6, color='lightblue')
            ax.set_ylabel('Volume')
            ax.set_title('Volume')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        axes[-1].set_xlabel('Date')
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        axes[-1].xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(axes[-1].xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        if save_path:
            if save_path.suffix == '':
                save_path = save_path.with_suffix('.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close(fig)

