"""
Stock price data loading module.

This module provides functionality to load stock price data with OHLCV
(Open, High, Low, Close, Volume) columns from various sources.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Union, List
import yfinance as yf


class StockDataLoader:
    """
    A class for loading stock price data with OHLCV columns.
    
    Supports loading from:
    - CSV files with OHLCV columns
    - Yahoo Finance API (yfinance)
    - Custom data sources
    
    Attributes:
        df (Optional[pd.DataFrame]): Loaded stock price dataframe
    """
    
    def __init__(self):
        """Initialize the StockDataLoader."""
        self.df: Optional[pd.DataFrame] = None
    
    def load_from_csv(
        self,
        file_path: Union[str, Path],
        date_col: str = 'Date',
        required_columns: List[str] = ['Open', 'High', 'Low', 'Close', 'Volume']
    ) -> pd.DataFrame:
        """
        Load stock price data from CSV file.
        
        Args:
            file_path: Path to CSV file
            date_col: Name of date column (default: 'Date')
            required_columns: List of required OHLCV columns
            
        Returns:
            pd.DataFrame: DataFrame with OHLCV data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required columns are missing
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Stock data file not found: {file_path}")
        
        df = pd.read_csv(file_path)
        
        # Ensure date column is datetime
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col])
            df.set_index(date_col, inplace=True)
        
        # Verify required columns exist
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Ensure columns are numeric
        for col in required_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        self.df = df
        return df
    
    def load_from_yfinance(
        self,
        ticker: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "1y"
    ) -> pd.DataFrame:
        """
        Load stock price data from Yahoo Finance using yfinance.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            period: Period if dates not specified (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            pd.DataFrame: DataFrame with OHLCV data indexed by date
        """
        stock = yf.Ticker(ticker)
        
        if start_date and end_date:
            df = stock.history(start=start_date, end=end_date)
        else:
            df = stock.history(period=period)
        
        # Rename columns to standard format (yfinance uses Title Case)
        df.columns = [col.capitalize() if col else col for col in df.columns]
        
        # Ensure we have required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        if all(col in df.columns for col in required_cols):
            self.df = df[required_cols]
        else:
            self.df = df
        
        return self.df
    
    def prepare_ohlcv_data(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Prepare and validate OHLCV data for technical analysis.
        
        Ensures data is sorted by date and has no missing critical values.
        
        Args:
            df: DataFrame to prepare (uses self.df if None)
            
        Returns:
            pd.DataFrame: Prepared dataframe ready for analysis
        """
        if df is None:
            df = self.df.copy() if self.df is not None else None
        
        if df is None:
            raise ValueError("No data available. Load data first.")
        
        # Sort by date
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.sort_index()
        elif 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')
        
        # Remove rows with missing critical data
        required_cols = ['Open', 'High', 'Low', 'Close']
        df = df.dropna(subset=required_cols)
        
        # Ensure Volume is non-negative
        if 'Volume' in df.columns:
            df['Volume'] = df['Volume'].abs()
        
        return df
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get the loaded dataframe."""
        if self.df is None:
            raise ValueError("No data loaded. Call load_from_csv() or load_from_yfinance() first.")
        return self.df

