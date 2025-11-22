"""
Data loading and preprocessing module.

This module provides classes and functions for loading and preprocessing
the analyst ratings dataset.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Union
from tqdm import tqdm


class DataLoader:
    """
    A class for loading and basic preprocessing of the analyst ratings dataset.
    
    This class provides efficient chunked reading for large CSV files (>1GB),
    which prevents memory issues when loading datasets with millions of rows.
    It uses pandas' chunked reading capability combined with tqdm for progress
    tracking.
    
    Attributes:
        data_path (Path): Path to the CSV data file
        chunk_size (int): Size of chunks for reading large files (rows per chunk)
        df (Optional[pd.DataFrame]): Loaded dataframe (None until load_data() is called)
    
    Example:
        >>> loader = DataLoader('data/raw_analyst_ratings.csv', chunk_size=100000)
        >>> df = loader.load_data()
        >>> print(f"Loaded {len(df)} rows")
    """
    
    def __init__(self, data_path: Union[str, Path], chunk_size: int = 100000):
        """
        Initialize the DataLoader with file path and chunk size.
        
        The chunk_size parameter determines how many rows are read into memory
        at once. For very large files (>500MB), smaller chunks (50k-100k) are
        recommended to manage memory usage.
        
        Args:
            data_path: Path to the CSV data file (can be string or Path object)
            chunk_size: Number of rows to read per chunk (default: 100000)
                       Smaller values use less memory but may be slower
        
        Note:
            The file is not loaded until load_data() is called. This allows
            for configuration before loading.
        """
        self.data_path = Path(data_path)
        self.chunk_size = chunk_size
        self.df: Optional[pd.DataFrame] = None  # Lazy loading - dataframe created on demand
        
    def load_data(self, show_progress: bool = True) -> pd.DataFrame:
        """
        Load data from CSV file using chunked reading for large files.
        
        This method reads the CSV file in chunks to avoid loading the entire
        dataset into memory at once. Each chunk is processed and then concatenated
        into a single DataFrame. This approach is essential for files >1GB.
        
        The method estimates total chunks based on file size to provide accurate
        progress tracking. If estimation fails, progress bar will still work
        but without a total count.
        
        Args:
            show_progress: Whether to show tqdm progress bar (default: True)
                         Set to False for cleaner output in scripts/logs
            
        Returns:
            pd.DataFrame: Complete loaded dataframe with all rows concatenated
            
        Raises:
            FileNotFoundError: If data file doesn't exist at the specified path
        
        Example:
            >>> loader = DataLoader('data/large_file.csv')
            >>> df = loader.load_data(show_progress=True)
            Loading chunks: 100%|████████| 14/14 [00:05<00:00,  2.5it/s]
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        chunks = []  # Store each chunk before concatenation
        
        # Estimate total chunks for accurate progress bar
        # Uses file size as proxy for row count (rough estimate: ~500 bytes/row)
        try:
            file_size = self.data_path.stat().st_size
            estimated_rows = int(file_size / 500)  # Rough estimate based on average row size
            total_chunks = max(1, estimated_rows // self.chunk_size)
        except (OSError, AttributeError):
            # If file size can't be determined, progress bar won't show total
            total_chunks = None
        
        # Create chunked reader - pandas reads file in chunks without loading all at once
        chunk_reader = pd.read_csv(self.data_path, chunksize=self.chunk_size)
        
        # Wrap with progress bar if requested, otherwise use iterator directly
        iterator = tqdm(chunk_reader, desc="Loading chunks", total=total_chunks) if show_progress else chunk_reader
        
        # Read each chunk and store in list
        # This approach uses less memory than loading entire file at once
        for chunk in iterator:
            chunks.append(chunk)
        
        # Concatenate all chunks into single DataFrame
        # ignore_index=True creates new sequential index (0, 1, 2, ...)
        self.df = pd.concat(chunks, ignore_index=True)
        return self.df
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Get the loaded dataframe.
        
        Returns:
            pd.DataFrame: The loaded dataframe
            
        Raises:
            ValueError: If data hasn't been loaded yet
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        return self.df


class DataPreprocessor:
    """
    A class for preprocessing the analyst ratings dataset.
    
    This class provides a fluent interface for data preprocessing operations,
    allowing method chaining (e.g., preprocessor.convert_dates().extract_temporal_features()).
    It handles date conversion, temporal feature extraction, and text feature
    calculation without modifying the original DataFrame.
    
    All methods return 'self' to enable method chaining, making the preprocessing
    pipeline more readable and concise.
    
    Example:
        >>> preprocessor = DataPreprocessor(df)
        >>> processed_df = (preprocessor
        ...     .convert_dates()
        ...     .extract_temporal_features()
        ...     .calculate_text_features()
        ...     .get_dataframe())
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DataPreprocessor with a copy of the input DataFrame.
        
        A copy is made to ensure the original DataFrame is not modified,
        following the principle of immutability. This allows safe experimentation
        without affecting the source data.
        
        Args:
            df: DataFrame to preprocess (will be copied, not modified in place)
        
        Note:
            The original DataFrame passed in remains unchanged. All modifications
            are made to the internal copy.
        """
        self.df = df.copy()  # Create copy to avoid modifying original DataFrame
    
    def convert_dates(self) -> 'DataPreprocessor':
        """
        Convert date column to pandas datetime format.
        
        This method checks if the 'date' column exists and converts it to
        datetime dtype if it's not already. The conversion uses 'coerce' error
        handling, which converts invalid dates to NaT (Not a Time) rather than
        raising an error. This is important for datasets with missing or malformed
        date values.
        
        Returns:
            self: For method chaining (allows: preprocessor.convert_dates().extract_temporal_features())
        
        Note:
            - Only converts if column exists (no error if missing)
            - Uses 'coerce' to handle invalid dates gracefully
            - Skips conversion if already datetime type (idempotent operation)
        
        Example:
            >>> preprocessor = DataPreprocessor(df)
            >>> preprocessor.convert_dates()  # Converts '2020-01-01' strings to datetime
        """
        if 'date' in self.df.columns:
            # Check if already datetime to avoid unnecessary conversion
            if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
                # errors='coerce' converts invalid dates to NaT instead of raising error
                self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        return self
    
    def extract_temporal_features(self) -> 'DataPreprocessor':
        """
        Extract temporal features from date column for time series analysis.
        
        Creates the following new columns:
        - year: 4-digit year (e.g., 2020)
        - month: Month number 1-12
        - day: Day of month 1-31
        - day_of_week: Day name (Monday, Tuesday, etc.)
        - hour: Hour of day 0-23 (useful for publication time analysis)
        - date_only: Date without time component (for daily aggregations)
        
        These features enable various time-based analyses:
        - Publication patterns by day of week
        - Hourly distribution of articles
        - Monthly/yearly trends
        - Daily aggregation for time series
        
        Returns:
            self: For method chaining
        
        Raises:
            ValueError: If date column doesn't exist (run convert_dates() first)
        
        Example:
            >>> preprocessor = DataPreprocessor(df)
            >>> preprocessor.convert_dates().extract_temporal_features()
            >>> # Now df has: year, month, day, day_of_week, hour, date_only columns
        """
        if 'date' not in self.df.columns:
            raise ValueError("Date column not found. Run convert_dates() first.")
        
        # Ensure date is datetime before using .dt accessor
        # This handles cases where convert_dates() wasn't called first
        if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
            self.convert_dates()
        
        # Extract temporal features using pandas datetime accessor (.dt)
        # These operations are vectorized and efficient for large datasets
        self.df['year'] = self.df['date'].dt.year  # Extract year component
        self.df['month'] = self.df['date'].dt.month  # Extract month (1-12)
        self.df['day'] = self.df['date'].dt.day  # Extract day of month
        self.df['day_of_week'] = self.df['date'].dt.day_name()  # Monday, Tuesday, etc.
        self.df['hour'] = self.df['date'].dt.hour  # Extract hour (0-23) for time analysis
        self.df['date_only'] = self.df['date'].dt.date  # Date without time (for daily grouping)
        
        return self
    
    def calculate_text_features(self) -> 'DataPreprocessor':
        """
        Calculate text-based features from headline column.
        
        Creates two new columns:
        - headline_length: Character count (including spaces)
        - headline_word_count: Number of words (space-separated)
        
        These features are useful for:
        - Descriptive statistics (average headline length)
        - Filtering (e.g., headlines >100 characters)
        - Analysis of headline style by publisher
        - Identifying outliers (very short or very long headlines)
        
        Returns:
            self: For method chaining
        
        Raises:
            ValueError: If headline column doesn't exist
        
        Example:
            >>> preprocessor = DataPreprocessor(df)
            >>> preprocessor.calculate_text_features()
            >>> # Headline "Stock prices rise" -> length=17, word_count=3
        """
        if 'headline' not in self.df.columns:
            raise ValueError("Headline column not found.")
        
        # Calculate character length (including spaces and punctuation)
        # Uses pandas string accessor (.str) for vectorized operations
        self.df['headline_length'] = self.df['headline'].str.len()
        
        # Calculate word count by splitting on whitespace and counting tokens
        # .str.split() creates list of words, .str.len() counts items in list
        self.df['headline_word_count'] = self.df['headline'].str.split().str.len()
        
        return self
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Get the preprocessed dataframe.
        
        Returns:
            pd.DataFrame: The preprocessed dataframe
        """
        return self.df

