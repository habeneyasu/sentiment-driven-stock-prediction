"""
Technical analysis module.

This module provides technical analysis indicators for stock price data,
including moving averages, RSI, MACD, and other common indicators.
Uses pandas and numpy for calculations (TA-Lib alternative).
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple


class TechnicalAnalyzer:
    """
    A class for calculating technical analysis indicators.
    
    Provides common technical indicators used in stock analysis without
    requiring TA-Lib. All calculations use pandas and numpy for efficiency
    and compatibility.
    
    Example:
        >>> analyzer = TechnicalAnalyzer()
        >>> sma = analyzer.simple_moving_average(prices, window=20)
        >>> rsi = analyzer.rsi(prices, period=14)
    """
    
    def __init__(self):
        """Initialize the TechnicalAnalyzer."""
        pass
    
    def simple_moving_average(
        self, 
        prices: pd.Series, 
        window: int = 20
    ) -> pd.Series:
        """
        Calculate Simple Moving Average (SMA).
        
        SMA is the average price over a specified window period. It smooths
        out price fluctuations and helps identify trends. Common windows:
        - 20 days: Short-term trend
        - 50 days: Medium-term trend
        - 200 days: Long-term trend
        
        Args:
            prices: Series of closing prices
            window: Number of periods for moving average (default: 20)
            
        Returns:
            pd.Series: Moving average values (first window-1 values are NaN)
        
        Example:
            >>> analyzer = TechnicalAnalyzer()
            >>> sma_20 = analyzer.simple_moving_average(prices, window=20)
        """
        return prices.rolling(window=window).mean()
    
    def exponential_moving_average(
        self,
        prices: pd.Series,
        span: int = 20,
        alpha: Optional[float] = None
    ) -> pd.Series:
        """
        Calculate Exponential Moving Average (EMA).
        
        EMA gives more weight to recent prices, making it more responsive
        to recent price changes than SMA. Useful for trend-following strategies.
        
        Args:
            prices: Series of closing prices
            span: Span parameter for EMA (default: 20)
            alpha: Smoothing factor (0 < alpha <= 1). If None, uses 2/(span+1)
            
        Returns:
            pd.Series: EMA values
        
        Example:
            >>> analyzer = TechnicalAnalyzer()
            >>> ema_12 = analyzer.exponential_moving_average(prices, span=12)
        """
        if alpha is None:
            alpha = 2.0 / (span + 1.0)
        return prices.ewm(alpha=alpha, adjust=False).mean()
    
    def rsi(
        self,
        prices: pd.Series,
        period: int = 14
    ) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).
        
        RSI measures momentum and identifies overbought (>70) or oversold (<30)
        conditions. Values range from 0 to 100.
        
        Args:
            prices: Series of closing prices
            period: Number of periods for RSI calculation (default: 14)
            
        Returns:
            pd.Series: RSI values (0-100, first period values are NaN)
        
        Example:
            >>> analyzer = TechnicalAnalyzer()
            >>> rsi_14 = analyzer.rsi(prices, period=14)
            >>> # RSI > 70: overbought, RSI < 30: oversold
        """
        # Calculate price changes
        delta = prices.diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses using exponential moving average
        avg_gains = gains.ewm(span=period, adjust=False).mean()
        avg_losses = losses.ewm(span=period, adjust=False).mean()
        
        # Calculate RS (Relative Strength) and RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def macd(
        self,
        prices: pd.Series,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ) -> pd.DataFrame:
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        MACD is a trend-following momentum indicator. It consists of:
        - MACD line: Difference between fast and slow EMA
        - Signal line: EMA of MACD line
        - Histogram: Difference between MACD and signal line
        
        Args:
            prices: Series of closing prices
            fast_period: Period for fast EMA (default: 12)
            slow_period: Period for slow EMA (default: 26)
            signal_period: Period for signal line EMA (default: 9)
            
        Returns:
            pd.DataFrame: DataFrame with columns:
                - macd: MACD line
                - signal: Signal line
                - histogram: MACD - Signal
        
        Example:
            >>> analyzer = TechnicalAnalyzer()
            >>> macd_df = analyzer.macd(prices)
            >>> # Buy signal when MACD crosses above signal line
        """
        # Calculate fast and slow EMAs
        ema_fast = self.exponential_moving_average(prices, span=fast_period)
        ema_slow = self.exponential_moving_average(prices, span=slow_period)
        
        # MACD line is difference between fast and slow EMA
        macd_line = ema_fast - ema_slow
        
        # Signal line is EMA of MACD line
        signal_line = self.exponential_moving_average(macd_line, span=signal_period)
        
        # Histogram is difference between MACD and signal
        histogram = macd_line - signal_line
        
        return pd.DataFrame({
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        })
    
    def bollinger_bands(
        self,
        prices: pd.Series,
        window: int = 20,
        num_std: float = 2.0
    ) -> pd.DataFrame:
        """
        Calculate Bollinger Bands.
        
        Bollinger Bands consist of:
        - Middle band: SMA
        - Upper band: SMA + (num_std * standard deviation)
        - Lower band: SMA - (num_std * standard deviation)
        
        Prices near upper band suggest overbought, near lower band suggest oversold.
        
        Args:
            prices: Series of closing prices
            window: Period for moving average (default: 20)
            num_std: Number of standard deviations for bands (default: 2.0)
            
        Returns:
            pd.DataFrame: DataFrame with columns:
                - middle: SMA (middle band)
                - upper: Upper band
                - lower: Lower band
        
        Example:
            >>> analyzer = TechnicalAnalyzer()
            >>> bands = analyzer.bollinger_bands(prices)
            >>> # Price touching upper band: potential sell signal
        """
        # Calculate middle band (SMA)
        middle = self.simple_moving_average(prices, window=window)
        
        # Calculate standard deviation
        std = prices.rolling(window=window).std()
        
        # Calculate upper and lower bands
        upper = middle + (num_std * std)
        lower = middle - (num_std * std)
        
        return pd.DataFrame({
            'middle': middle,
            'upper': upper,
            'lower': lower
        })
    
    def calculate_all_indicators(
        self,
        prices: pd.Series,
        volume: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Calculate multiple technical indicators at once.
        
        Convenience method to calculate common indicators in one call.
        Useful for feature engineering in machine learning models.
        
        Args:
            prices: Series of closing prices
            volume: Optional series of trading volumes
            
        Returns:
            pd.DataFrame: DataFrame with all calculated indicators as columns
        """
        indicators = pd.DataFrame(index=prices.index)
        
        # Moving averages
        indicators['sma_20'] = self.simple_moving_average(prices, window=20)
        indicators['sma_50'] = self.simple_moving_average(prices, window=50)
        indicators['ema_12'] = self.exponential_moving_average(prices, span=12)
        indicators['ema_26'] = self.exponential_moving_average(prices, span=26)
        
        # Momentum indicators
        indicators['rsi_14'] = self.rsi(prices, period=14)
        
        # MACD components
        macd_df = self.macd(prices)
        indicators['macd'] = macd_df['macd']
        indicators['macd_signal'] = macd_df['signal']
        indicators['macd_histogram'] = macd_df['histogram']
        
        # Bollinger Bands
        bb_df = self.bollinger_bands(prices)
        indicators['bb_upper'] = bb_df['upper']
        indicators['bb_middle'] = bb_df['middle']
        indicators['bb_lower'] = bb_df['lower']
        
        # Price-based features
        indicators['price_change'] = prices.pct_change()
        indicators['price_change_abs'] = prices.pct_change().abs()
        
        # Volume features (if provided)
        if volume is not None:
            indicators['volume_sma'] = self.simple_moving_average(volume, window=20)
            indicators['volume_ratio'] = volume / indicators['volume_sma']
        
        return indicators

