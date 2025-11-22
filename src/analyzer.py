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
    A class for computing descriptive statistics on the dataset.
    
    This analyzer provides methods to compute summary statistics for various
    aspects of the analyst ratings dataset, including headline characteristics
    and publisher activity patterns. All methods return dictionaries with
    standardized keys for easy consumption by reporting or visualization code.
    
    Example:
        >>> analyzer = DescriptiveAnalyzer(df)
        >>> stats = analyzer.headline_stats()
        >>> print(f"Mean headline length: {stats['mean']:.1f} characters")
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DescriptiveAnalyzer with a DataFrame.
        
        The DataFrame should contain preprocessed data with columns like
        'headline_length', 'headline_word_count', and 'publisher' for
        the analyzer methods to work correctly.
        
        Args:
            df: DataFrame to analyze (should be preprocessed with DataPreprocessor)
        
        Note:
            The DataFrame is stored by reference, not copied. Modifications to
            the original DataFrame will affect analyzer results.
        """
        self.df = df  # Store reference to DataFrame (no copy for memory efficiency)
    
    def headline_stats(self) -> Dict[str, float]:
        """
        Compute comprehensive headline length statistics.
        
        Calculates key descriptive statistics for headline lengths including
        central tendency (mean, median), variability (std), and range (min, max).
        These statistics help understand the distribution of headline lengths
        in the dataset, which can reveal patterns in how news is written.
        
        Returns:
            dict: Dictionary with keys:
                - 'mean': Average headline length in characters
                - 'median': Median headline length (robust to outliers)
                - 'std': Standard deviation (measure of variability)
                - 'min': Shortest headline length
                - 'max': Longest headline length
        
        Raises:
            ValueError: If headline_length column doesn't exist
                       (run DataPreprocessor.calculate_text_features() first)
        
        Example:
            >>> analyzer = DescriptiveAnalyzer(df)
            >>> stats = analyzer.headline_stats()
            >>> # Output: {'mean': 67.3, 'median': 65.0, 'std': 18.2, 'min': 10, 'max': 250}
        """
        if 'headline_length' not in self.df.columns:
            raise ValueError("headline_length column not found. Run preprocessing first.")
        
        # Calculate descriptive statistics
        # All values converted to float for JSON serialization and consistency
        return {
            'mean': float(self.df['headline_length'].mean()),  # Average length
            'median': float(self.df['headline_length'].median()),  # Middle value (less affected by outliers)
            'std': float(self.df['headline_length'].std()),  # Standard deviation (spread of data)
            'min': float(self.df['headline_length'].min()),  # Shortest headline
            'max': float(self.df['headline_length'].max()),  # Longest headline
        }
    
    def publisher_stats(self) -> Dict[str, any]:
        """
        Compute publisher activity and distribution statistics.
        
        Analyzes the distribution of articles across publishers to understand
        the publishing landscape. This helps identify:
        - Total number of unique publishers
        - Average and median articles per publisher
        - Most active publisher
        - Distribution characteristics (e.g., if few publishers dominate)
        
        Returns:
            dict: Dictionary with keys:
                - 'total_publishers': Number of unique publishers
                - 'mean_articles': Average articles per publisher
                - 'median_articles': Median articles per publisher (robust metric)
                - 'max_articles': Maximum articles by any single publisher
                - 'top_publisher': Name of most active publisher
                - 'top_publisher_count': Article count for top publisher
        
        Raises:
            ValueError: If publisher column doesn't exist
        
        Example:
            >>> analyzer = DescriptiveAnalyzer(df)
            >>> stats = analyzer.publisher_stats()
            >>> # Output: {'total_publishers': 1250, 'mean_articles': 1120.5, ...}
        """
        if 'publisher' not in self.df.columns:
            raise ValueError("publisher column not found.")
        
        # Count articles per publisher (value_counts returns Series sorted by count descending)
        publisher_counts = self.df['publisher'].value_counts()
        
        return {
            'total_publishers': int(publisher_counts.count()),  # Number of unique publishers
            'mean_articles': float(publisher_counts.mean()),  # Average articles per publisher
            'median_articles': float(publisher_counts.median()),  # Median (less affected by outliers)
            'max_articles': int(publisher_counts.max()),  # Highest article count
            'top_publisher': publisher_counts.index[0],  # Publisher name with most articles
            'top_publisher_count': int(publisher_counts.iloc[0]),  # Count for top publisher
        }


class TimeSeriesAnalyzer:
    """
    A class for time series analysis of publication frequency.
    
    This analyzer provides methods to examine temporal patterns in article
    publication, including daily counts, hourly distributions, and monthly
    trends. It automatically handles date column conversion and ensures
    proper datetime formatting for time series operations.
    
    Example:
        >>> analyzer = TimeSeriesAnalyzer(df)
        >>> daily = analyzer.daily_counts()
        >>> hourly = analyzer.hourly_distribution()
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the TimeSeriesAnalyzer with a DataFrame.
        
        The DataFrame is copied to avoid modifying the original. The analyzer
        automatically ensures the date_only column exists and is properly
        formatted for time series analysis.
        
        Args:
            df: DataFrame with date information (should have 'date' or 'date_only' column)
        
        Note:
            If 'date_only' doesn't exist, it will be created from 'date' column.
            The DataFrame is copied to preserve immutability.
        """
        self.df = df.copy()  # Copy to avoid modifying original DataFrame
        self._ensure_date_column()  # Ensure date column is ready for analysis
    
    def _ensure_date_column(self) -> None:
        """
        Ensure date_only column exists and is in datetime format.
        
        This helper method handles the common case where temporal features
        haven't been extracted yet. It creates date_only from the date column
        if needed, and ensures it's in datetime format for time series operations.
        
        The method is idempotent - safe to call multiple times.
        """
        # Create date_only from date column if it doesn't exist
        if 'date_only' not in self.df.columns:
            if 'date' in self.df.columns:
                # Ensure date is datetime before extracting date component
                if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
                    self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
                # Extract date without time component (for daily grouping)
                self.df['date_only'] = self.df['date'].dt.date
        
        # Convert date_only to datetime if it's still an object type
        # This happens when date_only was created from .dt.date (returns date objects)
        if self.df['date_only'].dtype == 'object':
            self.df['date_only'] = pd.to_datetime(self.df['date_only'])
    
    def daily_counts(self) -> pd.Series:
        """
        Get daily article publication counts for time series analysis.
        
        Groups articles by date and counts publications per day. This is useful
        for identifying publication patterns, spikes during market events, and
        overall trends over time. The result is sorted chronologically.
        
        Returns:
            pd.Series: Daily article counts with datetime index
                     Index: dates (datetime)
                     Values: article counts (int)
        
        Example:
            >>> analyzer = TimeSeriesAnalyzer(df)
            >>> daily = analyzer.daily_counts()
            >>> # Returns Series like:
            >>> # 2020-01-01    1250
            >>> # 2020-01-02    1180
            >>> # ...
        """
        # Group by date and count articles per day
        daily = self.df.groupby('date_only').size()
        
        # Ensure index is datetime for proper time series operations
        daily.index = pd.to_datetime(daily.index)
        
        # Sort chronologically for time series analysis
        return daily.sort_index()
    
    def hourly_distribution(self) -> pd.Series:
        """
        Get hourly distribution of article publications throughout the day.
        
        Analyzes what times of day articles are typically published. This reveals
        patterns like peak publication hours (often during market hours) and can
        be useful for understanding publication schedules and market activity timing.
        
        Returns:
            pd.Series: Article counts by hour (0-23)
                     Index: hour of day (0-23)
                     Values: article counts (int)
        
        Example:
            >>> analyzer = TimeSeriesAnalyzer(df)
            >>> hourly = analyzer.hourly_distribution()
            >>> # Returns Series like:
            >>> # 0     125   (midnight)
            >>> # 9     2340  (9 AM - peak hour)
            >>> # 17    1890  (5 PM)
            >>> # ...
        """
        # Extract hour if not already present
        if 'hour' not in self.df.columns:
            if 'date' in self.df.columns:
                # Ensure date is datetime before extracting hour
                if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
                    self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
                # Extract hour component (0-23)
                self.df['hour'] = self.df['date'].dt.hour
        
        # Count articles by hour and sort by hour (0-23)
        return self.df['hour'].value_counts().sort_index()
    
    def monthly_trends(self) -> pd.Series:
        """
        Get monthly article publication counts for trend analysis.
        
        Groups articles by year-month to identify long-term trends, seasonal
        patterns, and growth/decline in publication volume over time. Uses
        pandas Period for proper month-level grouping.
        
        Returns:
            pd.Series: Article counts by year-month
                     Index: Period objects (e.g., '2020-01', '2020-02')
                     Values: article counts (int)
        
        Raises:
            ValueError: If date column doesn't exist
        
        Example:
            >>> analyzer = TimeSeriesAnalyzer(df)
            >>> monthly = analyzer.monthly_trends()
            >>> # Returns Series like:
            >>> # 2020-01    34500
            >>> # 2020-02    31200
            >>> # ...
        """
        if 'date' not in self.df.columns:
            raise ValueError("Date column required for monthly analysis.")
        
        # Ensure date is datetime before period conversion
        if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        
        # Convert to year-month period for grouping (e.g., '2020-01')
        self.df['year_month'] = self.df['date'].dt.to_period('M')
        
        # Group by year-month and count articles
        return self.df.groupby('year_month').size()


class PublisherAnalyzer:
    """
    A class for analyzing publisher patterns and characteristics.
    
    This analyzer helps understand the publisher landscape by identifying
    email-based publishers, extracting domains, and analyzing publisher
    behavior patterns. Useful for understanding data quality and publisher
    distribution.
    
    Example:
        >>> analyzer = PublisherAnalyzer(df)
        >>> is_email = analyzer.identify_email_publishers()
        >>> domains = analyzer.extract_email_domains()
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the PublisherAnalyzer with a DataFrame.
        
        Args:
            df: DataFrame with publisher information (must have 'publisher' column)
        
        Note:
            The DataFrame is stored by reference for memory efficiency.
        """
        self.df = df  # Store reference (no copy needed for read-only operations)
    
    def identify_email_publishers(self) -> pd.Series:
        """
        Identify which publishers are email addresses vs. named publishers.
        
        In the dataset, some publishers are stored as email addresses (e.g.,
        'author@benzinga.com') while others are names (e.g., 'Benzinga Insights').
        This method uses regex pattern matching to distinguish between them.
        
        Returns:
            pd.Series: Boolean Series where True indicates email address publisher
                     Index: matches DataFrame index
                     Values: True for email addresses, False for names
        
        Example:
            >>> analyzer = PublisherAnalyzer(df)
            >>> is_email = analyzer.identify_email_publishers()
            >>> email_count = is_email.sum()  # Count email-based publishers
        """
        import re
        # Regex pattern for valid email addresses
        # Matches: local@domain.tld format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # str.match() returns True for matching strings, False otherwise
        # na=False treats NaN values as False (not email addresses)
        return self.df['publisher'].str.match(email_pattern, na=False)
    
    def extract_email_domains(self) -> pd.Series:
        """
        Extract email domains from publisher column for domain analysis.
        
        For publishers that are email addresses, extracts the domain portion
        (e.g., 'benzinga.com' from 'author@benzinga.com'). This enables analysis
        of which organizations contribute most articles when using email-based
        publisher identification.
        
        Returns:
            pd.Series: Email domains extracted from publisher column
                     Index: matches DataFrame index
                     Values: domain strings (e.g., 'benzinga.com') or NaN for non-email publishers
        
        Example:
            >>> analyzer = PublisherAnalyzer(df)
            >>> domains = analyzer.extract_email_domains()
            >>> domain_counts = domains.value_counts()  # Count articles per domain
        """
        import re
        # First identify which publishers are emails
        email_mask = self.identify_email_publishers()
        
        # Filter to only email publishers
        email_publishers = self.df[email_mask]['publisher']
        
        # Extract domain using regex: capture everything after @
        # Pattern: @([\w.]+) captures domain and TLD
        # [0] gets first (and only) capture group
        domains = email_publishers.str.extract(r'@([\w.]+)')[0]
        
        return domains  # Returns Series with domains or NaN for non-email rows

