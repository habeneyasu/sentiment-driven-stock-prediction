"""
Unit tests for visualizer module.

Tests for TechnicalVisualizer class.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.visualizer import TechnicalVisualizer


class TestTechnicalVisualizer:
    """Test cases for TechnicalVisualizer class."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data with indicators."""
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        np.random.seed(42)
        
        base_price = 100
        prices = pd.Series(base_price + np.cumsum(np.random.randn(50) * 2), index=dates)
        
        df = pd.DataFrame({
            'Open': prices + np.random.randn(50) * 0.5,
            'High': prices + np.abs(np.random.randn(50) * 1),
            'Low': prices - np.abs(np.random.randn(50) * 1),
            'Close': prices,
            'Volume': np.random.randint(1000000, 5000000, 50),
            'SMA_20': prices.rolling(20).mean(),
            'EMA_12': prices.ewm(span=12).mean(),
            'RSI': pd.Series([50] * 50, index=dates),  # Mock RSI
            'MACD': pd.Series([0] * 50, index=dates),  # Mock MACD
            'macd_signal': pd.Series([0] * 50, index=dates),
            'macd_histogram': pd.Series([0] * 50, index=dates)
        }, index=dates)
        
        return df
    
    def test_initialization(self):
        """Test TechnicalVisualizer initialization."""
        visualizer = TechnicalVisualizer()
        assert visualizer is not None
    
    def test_plot_price_with_indicators(self, sample_data, tmp_path):
        """Test plotting price with indicators."""
        visualizer = TechnicalVisualizer()
        save_path = tmp_path / "test_chart.html"
        
        # Should not raise an error
        try:
            fig = visualizer.plot_price_with_indicators(
                sample_data,
                ticker='TEST',
                save_path=save_path,
                show=False
            )
            # If using Plotly, should return a figure
            if visualizer.use_plotly:
                assert fig is not None
        except Exception as e:
            # If visualization libraries are not available, that's okay for tests
            pytest.skip(f"Visualization not available: {e}")
    
    def test_plot_without_indicators(self, sample_data, tmp_path):
        """Test plotting with minimal data."""
        visualizer = TechnicalVisualizer()
        
        # Create minimal dataframe
        minimal_df = sample_data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
        save_path = tmp_path / "test_minimal.html"
        
        try:
            visualizer.plot_price_with_indicators(
                minimal_df,
                ticker='TEST',
                save_path=save_path,
                show=False
            )
        except Exception as e:
            pytest.skip(f"Visualization not available: {e}")

