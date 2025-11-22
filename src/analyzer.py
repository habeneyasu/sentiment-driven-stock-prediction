"""
Data analysis and statistics module.

This module provides classes for performing various analyses
on the analyst ratings dataset.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from collections import Counter


class DescriptiveAnalyzer:
    """
    A class for computing descriptive statistics.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DescriptiveAnalyzer.
        
        Args:
            df: DataFrame to analyze
        """
        self.df = df
    
    def headline_stats(self) -> Dict[str, float]:
        """
        Compute headline length statistics.
        
        Returns:
            dict: Dictionary with headline statistics
        """
        if 'headline_length' not in self.df.columns:
            raise ValueError("headline_length column not found. Run preprocessing first.")
        
        return {
            'mean': float(self.df['headline_length'].mean()),
            'median': float(self.df['headline_length'].median()),
            'std': float(self.df['headline_length'].std()),
            'min': float(self.df['headline_length'].min()),
            'max': float(self.df['headline_length'].max()),
        }
    
    def publisher_stats(self) -> Dict[str, any]:
        """
        Compute publisher activity statistics.
        
        Returns:
            dict: Dictionary with publisher statistics
        """
        if 'publisher' not in self.df.columns:
            raise ValueError("publisher column not found.")
        
        publisher_counts = self.df['publisher'].value_counts()
        
        return {
            'total_publishers': int(publisher_counts.count()),
            'mean_articles': float(publisher_counts.mean()),
            'median_articles': float(publisher_counts.median()),
            'max_articles': int(publisher_counts.max()),
            'top_publisher': publisher_counts.index[0],
            'top_publisher_count': int(publisher_counts.iloc[0]),
        }


class TimeSeriesAnalyzer:
    """
    A class for time series analysis of publication frequency.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the TimeSeriesAnalyzer.
        
        Args:
            df: DataFrame with date information
        """
        self.df = df.copy()
        self._ensure_date_column()
    
    def _ensure_date_column(self) -> None:
        """Ensure date_only column exists and is datetime."""
        if 'date_only' not in self.df.columns:
            if 'date' in self.df.columns:
                if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
                    self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
                self.df['date_only'] = self.df['date'].dt.date
        
        # Convert to datetime for analysis
        if self.df['date_only'].dtype == 'object':
            self.df['date_only'] = pd.to_datetime(self.df['date_only'])
    
    def daily_counts(self) -> pd.Series:
        """
        Get daily article counts.
        
        Returns:
            pd.Series: Daily article counts indexed by date
        """
        daily = self.df.groupby('date_only').size()
        daily.index = pd.to_datetime(daily.index)
        return daily.sort_index()
    
    def hourly_distribution(self) -> pd.Series:
        """
        Get hourly article distribution.
        
        Returns:
            pd.Series: Article counts by hour (0-23)
        """
        if 'hour' not in self.df.columns:
            if 'date' in self.df.columns:
                if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
                    self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
                self.df['hour'] = self.df['date'].dt.hour
        
        return self.df['hour'].value_counts().sort_index()
    
    def monthly_trends(self) -> pd.Series:
        """
        Get monthly article counts.
        
        Returns:
            pd.Series: Article counts by year-month
        """
        if 'date' not in self.df.columns:
            raise ValueError("Date column required for monthly analysis.")
        
        if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        
        self.df['year_month'] = self.df['date'].dt.to_period('M')
        return self.df.groupby('year_month').size()


class PublisherAnalyzer:
    """
    A class for analyzing publisher patterns.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the PublisherAnalyzer.
        
        Args:
            df: DataFrame with publisher information
        """
        self.df = df
    
    def identify_email_publishers(self) -> pd.Series:
        """
        Identify which publishers are email addresses.
        
        Returns:
            pd.Series: Boolean series indicating email publishers
        """
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return self.df['publisher'].str.match(email_pattern, na=False)
    
    def extract_email_domains(self) -> pd.Series:
        """
        Extract email domains from publisher column.
        
        Returns:
            pd.Series: Email domains (NaN for non-email publishers)
        """
        import re
        email_publishers = self.df[self.identify_email_publishers()]['publisher']
        domains = email_publishers.str.extract(r'@([\w.]+)')[0]
        return domains

