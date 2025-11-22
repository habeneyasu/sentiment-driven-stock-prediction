"""
Unit tests for technical_analyzer module.

Tests for TechnicalAnalyzer class.
"""

import pytest
import pandas as pd
import numpy as np
from src.technical_analyzer import TechnicalAnalyzer


class TestTechnicalAnalyzer:
    """Test cases for TechnicalAnalyzer class."""
    
    def test_initialization(self):
        """Test TechnicalAnalyzer initialization."""
        analyzer = TechnicalAnalyzer()
        assert analyzer is not None
    
    def test_simple_moving_average(self):
        """Test Simple Moving Average calculation."""
        analyzer = TechnicalAnalyzer()
        prices = pd.Series([100, 102, 104, 106, 108, 110])
        sma = analyzer.simple_moving_average(prices, window=3)
        
        assert len(sma) == len(prices)
        assert pd.isna(sma.iloc[0])  # First window-1 values are NaN
        assert pd.isna(sma.iloc[1])
        # SMA of first 3 values: (100+102+104)/3 = 102
        assert abs(sma.iloc[2] - 102.0) < 0.01
    
    def test_exponential_moving_average(self):
        """Test Exponential Moving Average calculation."""
        analyzer = TechnicalAnalyzer()
        prices = pd.Series([100, 102, 104, 106, 108])
        ema = analyzer.exponential_moving_average(prices, span=3)
        
        assert len(ema) == len(prices)
        # EMA should be more responsive to recent prices than SMA
        assert ema.iloc[-1] > 100
    
    def test_exponential_moving_average_custom_alpha(self):
        """Test EMA with custom alpha parameter."""
        analyzer = TechnicalAnalyzer()
        prices = pd.Series([100, 102, 104, 106])
        ema = analyzer.exponential_moving_average(prices, span=3, alpha=0.5)
        
        assert len(ema) == len(prices)
    
    def test_rsi(self):
        """Test Relative Strength Index calculation."""
        analyzer = TechnicalAnalyzer()
        # Create price series with upward trend
        prices = pd.Series([100, 102, 104, 106, 108, 110])
        rsi = analyzer.rsi(prices, period=3)
        
        assert len(rsi) == len(prices)
        # RSI should be > 50 for upward trending prices
        assert rsi.iloc[-1] > 50 if not pd.isna(rsi.iloc[-1]) else True
    
    def test_rsi_downward_trend(self):
        """Test RSI with downward trending prices."""
        analyzer = TechnicalAnalyzer()
        prices = pd.Series([110, 108, 106, 104, 102, 100])
        rsi = analyzer.rsi(prices, period=3)
        
        assert len(rsi) == len(prices)
        # RSI should be < 50 for downward trending prices
        assert rsi.iloc[-1] < 50 if not pd.isna(rsi.iloc[-1]) else True
    
    def test_macd(self):
        """Test MACD calculation."""
        analyzer = TechnicalAnalyzer()
        prices = pd.Series(range(100, 150))  # Upward trend
        macd_df = analyzer.macd(prices)
        
        assert isinstance(macd_df, pd.DataFrame)
        assert 'macd' in macd_df.columns
        assert 'signal' in macd_df.columns
        assert 'histogram' in macd_df.columns
        assert len(macd_df) == len(prices)
    
    def test_macd_custom_periods(self):
        """Test MACD with custom periods."""
        analyzer = TechnicalAnalyzer()
        prices = pd.Series(range(100, 120))
        macd_df = analyzer.macd(prices, fast_period=5, slow_period=10, signal_period=3)
        
        assert 'macd' in macd_df.columns
        assert 'signal' in macd_df.columns
    
    def test_bollinger_bands(self):
        """Test Bollinger Bands calculation."""
        analyzer = TechnicalAnalyzer()
        prices = pd.Series([100, 102, 104, 106, 108, 110, 112])
        bands = analyzer.bollinger_bands(prices, window=5)
        
        assert isinstance(bands, pd.DataFrame)
        assert 'middle' in bands.columns
        assert 'upper' in bands.columns
        assert 'lower' in bands.columns
        # Upper band should be above middle, lower below
        assert (bands['upper'] > bands['middle']).all()
        assert (bands['lower'] < bands['middle']).all()
    
    def test_bollinger_bands_custom_std(self):
        """Test Bollinger Bands with custom standard deviation."""
        analyzer = TechnicalAnalyzer()
        prices = pd.Series(range(100, 110))
        bands = analyzer.bollinger_bands(prices, window=5, num_std=1.5)
        
        assert 'upper' in bands.columns
        assert 'lower' in bands.columns
    
    def test_calculate_all_indicators(self):
        """Test calculation of all indicators at once."""
        analyzer = TechnicalAnalyzer()
        prices = pd.Series(range(100, 150))
        volume = pd.Series(range(1000000, 1000050))
        
        indicators = analyzer.calculate_all_indicators(prices, volume=volume)
        
        assert isinstance(indicators, pd.DataFrame)
        assert 'sma_20' in indicators.columns
        assert 'sma_50' in indicators.columns
        assert 'rsi_14' in indicators.columns
        assert 'macd' in indicators.columns
        assert 'bb_upper' in indicators.columns
        assert 'volume_ratio' in indicators.columns
    
    def test_calculate_all_indicators_no_volume(self):
        """Test calculate_all_indicators without volume."""
        analyzer = TechnicalAnalyzer()
        prices = pd.Series(range(100, 150))
        
        indicators = analyzer.calculate_all_indicators(prices)
        
        assert 'sma_20' in indicators.columns
        assert 'volume_ratio' not in indicators.columns  # Should not be present without volume

