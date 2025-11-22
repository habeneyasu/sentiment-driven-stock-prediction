"""
Unit tests for data_loader module.

Tests for DataLoader and DataPreprocessor classes.
"""

import pytest
import pandas as pd
from pathlib import Path
from src.data_loader import DataLoader, DataPreprocessor


class TestDataLoader:
    """Test cases for DataLoader class."""
    
    def test_initialization(self, tmp_path):
        """Test DataLoader initialization."""
        # Create a temporary CSV file
        test_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        df.to_csv(test_file, index=False)
        
        loader = DataLoader(test_file, chunk_size=2)
        assert loader.data_path == Path(test_file)
        assert loader.chunk_size == 2
        assert loader.df is None
    
    def test_load_data(self, tmp_path):
        """Test data loading functionality."""
        test_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        df.to_csv(test_file, index=False)
        
        loader = DataLoader(test_file)
        loaded_df = loader.load_data(show_progress=False)
        
        assert loaded_df is not None
        assert len(loaded_df) == 3
        assert 'col1' in loaded_df.columns
        assert 'col2' in loaded_df.columns


class TestDataPreprocessor:
    """Test cases for DataPreprocessor class."""
    
    def test_convert_dates(self):
        """Test date conversion."""
        df = pd.DataFrame({
            'date': ['2020-01-01', '2020-01-02', '2020-01-03']
        })
        
        preprocessor = DataPreprocessor(df)
        preprocessor.convert_dates()
        
        result_df = preprocessor.get_dataframe()
        assert pd.api.types.is_datetime64_any_dtype(result_df['date'])
    
    def test_extract_temporal_features(self):
        """Test temporal feature extraction."""
        df = pd.DataFrame({
            'date': pd.to_datetime(['2020-01-01', '2020-02-15', '2020-03-20'])
        })
        
        preprocessor = DataPreprocessor(df)
        preprocessor.extract_temporal_features()
        
        result_df = preprocessor.get_dataframe()
        assert 'year' in result_df.columns
        assert 'month' in result_df.columns
        assert 'day_of_week' in result_df.columns
        assert 'hour' in result_df.columns
    
    def test_calculate_text_features(self):
        """Test text feature calculation."""
        df = pd.DataFrame({
            'headline': ['Short', 'This is a longer headline', 'Medium length text']
        })
        
        preprocessor = DataPreprocessor(df)
        preprocessor.calculate_text_features()
        
        result_df = preprocessor.get_dataframe()
        assert 'headline_length' in result_df.columns
        assert 'headline_word_count' in result_df.columns
        assert result_df['headline_length'].iloc[0] == 5

