"""
Integration tests for the sentiment-driven stock prediction pipeline.

These tests verify that multiple modules work together correctly,
simulating real-world usage scenarios.
"""

import pytest
import pandas as pd
import numpy as np
from src.data_loader import DataLoader, DataPreprocessor
from src.text_processor import TextPreprocessor
from src.analyzer import DescriptiveAnalyzer, TimeSeriesAnalyzer
from src.sentiment_analyzer import SentimentAnalyzer, SentimentReturnLinker
from src.technical_analyzer import TechnicalAnalyzer


class TestDataPipeline:
    """Test complete data processing pipeline."""
    
    def test_end_to_end_preprocessing(self, tmp_path):
        """Test complete preprocessing pipeline."""
        # Create test data
        test_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({
            'headline': ['Stock prices rise', 'Market falls', 'Earnings beat'],
            'date': ['2020-01-01', '2020-01-02', '2020-01-03'],
            'publisher': ['Publisher A', 'Publisher B', 'Publisher A'],
            'stock': ['AAPL', 'AAPL', 'AAPL']
        })
        df.to_csv(test_file, index=False)
        
        # Load data
        loader = DataLoader(test_file)
        df_loaded = loader.load_data(show_progress=False)
        
        # Preprocess
        preprocessor = DataPreprocessor(df_loaded)
        df_processed = (preprocessor
                       .convert_dates()
                       .extract_temporal_features()
                       .calculate_text_features()
                       .get_dataframe())
        
        # Verify all features created
        assert 'year' in df_processed.columns
        assert 'headline_length' in df_processed.columns
        assert len(df_processed) == 3
    
    def test_sentiment_analysis_pipeline(self):
        """Test sentiment analysis on processed data."""
        df = pd.DataFrame({
            'headline': [
                'Stock prices surge on strong earnings',
                'Market crashes on poor results',
                'Earnings meet expectations'
            ],
            'date': pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-03']),
            'stock': ['AAPL', 'AAPL', 'AAPL']
        })
        
        # Preprocess text
        text_processor = TextPreprocessor()
        df['processed_headline'] = text_processor.preprocess_series(
            df['headline'], show_progress=False
        )
        
        # Analyze sentiment
        sentiment_analyzer = SentimentAnalyzer()
        sentiment_df = sentiment_analyzer.analyze_series(
            df['headline'], show_progress=False
        )
        
        # Verify sentiment analysis
        assert 'compound' in sentiment_df.columns
        assert 'sentiment_label' in sentiment_df.columns
        assert len(sentiment_df) == len(df)
        
        # First headline should be positive
        assert sentiment_df.iloc[0]['compound'] > 0


class TestSentimentReturnIntegration:
    """Test sentiment-return linking functionality."""
    
    def test_sentiment_return_correlation_workflow(self):
        """Test complete sentiment-return correlation workflow."""
        # Create sample data
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        sentiment_df = pd.DataFrame({
            'date': dates,
            'stock': ['AAPL'] * 10,
            'compound': np.random.uniform(-0.5, 0.5, 10)
        })
        
        # Create returns data (shifted by 1 day for lag)
        returns_df = pd.DataFrame({
            'date': dates + pd.Timedelta(days=1),
            'stock': ['AAPL'] * 10,
            'return': np.random.uniform(-0.02, 0.02, 10)
        })
        
        # Link sentiment with returns
        linker = SentimentReturnLinker()
        aligned = linker.align_sentiment_with_returns(
            sentiment_df, returns_df, lag_days=1
        )
        
        # Calculate correlation
        if len(aligned) > 1:
            correlation = linker.calculate_sentiment_return_correlation(
                aligned['compound'], aligned['return']
            )
            
            assert 'correlation' in correlation
            assert -1 <= correlation['correlation'] <= 1


class TestTechnicalAnalysisIntegration:
    """Test technical analysis integration."""
    
    def test_technical_indicators_with_price_data(self):
        """Test technical indicators on price series."""
        # Create sample price data
        np.random.seed(42)
        base_price = 100
        prices = pd.Series([
            base_price + np.random.randn() * 2 
            for _ in range(50)
        ])
        
        # Calculate all indicators
        analyzer = TechnicalAnalyzer()
        indicators = analyzer.calculate_all_indicators(prices)
        
        # Verify indicators are calculated
        assert 'sma_20' in indicators.columns
        assert 'rsi_14' in indicators.columns
        assert 'macd' in indicators.columns
        assert len(indicators) == len(prices)
        
        # Verify RSI is in valid range (0-100)
        rsi_valid = indicators['rsi_14'].dropna()
        if len(rsi_valid) > 0:
            assert (rsi_valid >= 0).all()
            assert (rsi_valid <= 100).all()


class TestCompleteWorkflow:
    """Test complete workflow from data to analysis."""
    
    def test_complete_analysis_workflow(self, tmp_path):
        """Test complete workflow: load -> preprocess -> analyze -> sentiment."""
        # Create test CSV
        test_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({
            'headline': [
                'AAPL stock rises on earnings beat',
                'AAPL shares fall on guidance cut',
                'AAPL maintains strong position'
            ],
            'date': ['2020-01-01 09:00:00', '2020-01-02 10:00:00', '2020-01-03 11:00:00'],
            'publisher': ['Publisher A', 'Publisher B', 'Publisher A'],
            'stock': ['AAPL', 'AAPL', 'AAPL']
        })
        df.to_csv(test_file, index=False)
        
        # Step 1: Load
        loader = DataLoader(test_file)
        df_loaded = loader.load_data(show_progress=False)
        
        # Step 2: Preprocess
        preprocessor = DataPreprocessor(df_loaded)
        df_processed = (preprocessor
                       .convert_dates()
                       .extract_temporal_features()
                       .calculate_text_features()
                       .get_dataframe())
        
        # Step 3: Descriptive analysis
        desc_analyzer = DescriptiveAnalyzer(df_processed)
        headline_stats = desc_analyzer.headline_stats()
        assert 'mean' in headline_stats
        
        # Step 4: Time series analysis
        ts_analyzer = TimeSeriesAnalyzer(df_processed)
        daily_counts = ts_analyzer.daily_counts()
        assert len(daily_counts) > 0
        
        # Step 5: Sentiment analysis
        sentiment_analyzer = SentimentAnalyzer()
        sentiment_df = sentiment_analyzer.analyze_series(
            df_processed['headline'], show_progress=False
        )
        assert len(sentiment_df) == len(df_processed)
        
        # Verify all steps completed successfully
        assert len(df_processed) == 3

