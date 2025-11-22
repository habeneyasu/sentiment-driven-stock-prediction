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
    
    Attributes:
        data_path (Path): Path to the CSV data file
        chunk_size (int): Size of chunks for reading large files
        df (Optional[pd.DataFrame]): Loaded dataframe
    """
    
    def __init__(self, data_path: Union[str, Path], chunk_size: int = 100000):
        """
        Initialize the DataLoader.
        
        Args:
            data_path: Path to the CSV data file
            chunk_size: Number of rows to read per chunk (default: 100000)
        """
        self.data_path = Path(data_path)
        self.chunk_size = chunk_size
        self.df: Optional[pd.DataFrame] = None
        
    def load_data(self, show_progress: bool = True) -> pd.DataFrame:
        """
        Load data from CSV file using chunked reading for large files.
        
        Args:
            show_progress: Whether to show progress bar (default: True)
            
        Returns:
            pd.DataFrame: Loaded dataframe
            
        Raises:
            FileNotFoundError: If data file doesn't exist
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        chunks = []
        
        # Estimate total chunks for progress bar
        try:
            file_size = self.data_path.stat().st_size
            estimated_rows = int(file_size / 500)  # Rough estimate
            total_chunks = max(1, estimated_rows // self.chunk_size)
        except:
            total_chunks = None
        
        # Read in chunks
        chunk_reader = pd.read_csv(self.data_path, chunksize=self.chunk_size)
        iterator = tqdm(chunk_reader, desc="Loading chunks", total=total_chunks) if show_progress else chunk_reader
        
        for chunk in iterator:
            chunks.append(chunk)
        
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
    
    This class handles date conversion, temporal feature extraction,
    and text preprocessing.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DataPreprocessor.
        
        Args:
            df: DataFrame to preprocess
        """
        self.df = df.copy()
    
    def convert_dates(self) -> 'DataPreprocessor':
        """
        Convert date column to datetime format.
        
        Returns:
            self: For method chaining
        """
        if 'date' in self.df.columns:
            if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
                self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        return self
    
    def extract_temporal_features(self) -> 'DataPreprocessor':
        """
        Extract temporal features from date column.
        
        Creates: year, month, day, day_of_week, hour, date_only
        
        Returns:
            self: For method chaining
        """
        if 'date' not in self.df.columns:
            raise ValueError("Date column not found. Run convert_dates() first.")
        
        # Ensure date is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
            self.convert_dates()
        
        # Extract temporal features
        self.df['year'] = self.df['date'].dt.year
        self.df['month'] = self.df['date'].dt.month
        self.df['day'] = self.df['date'].dt.day
        self.df['day_of_week'] = self.df['date'].dt.day_name()
        self.df['hour'] = self.df['date'].dt.hour
        self.df['date_only'] = self.df['date'].dt.date
        
        return self
    
    def calculate_text_features(self) -> 'DataPreprocessor':
        """
        Calculate text-based features from headlines.
        
        Creates: headline_length, headline_word_count
        
        Returns:
            self: For method chaining
        """
        if 'headline' not in self.df.columns:
            raise ValueError("Headline column not found.")
        
        self.df['headline_length'] = self.df['headline'].str.len()
        self.df['headline_word_count'] = self.df['headline'].str.split().str.len()
        
        return self
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Get the preprocessed dataframe.
        
        Returns:
            pd.DataFrame: The preprocessed dataframe
        """
        return self.df

