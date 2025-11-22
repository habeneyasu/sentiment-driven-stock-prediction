"""
Unit tests for sentiment_analyzer module.

Tests for SentimentAnalyzer and SentimentReturnLinker classes.
"""

import pytest
import pandas as pd
import numpy as np
from src.sentiment_analyzer import SentimentAnalyzer, SentimentReturnLinker


class TestSentimentAnalyzer:
    """Test cases for SentimentAnalyzer class."""
    
    def test_initialization(self):
        """Test SentimentAnalyzer initialization."""
        analyzer = SentimentAnalyzer()
        assert analyzer.compound_threshold == 0.05
        assert analyzer.analyzer is not None
    
    def test_initialization_custom_threshold(self):
        """Test initialization with custom threshold."""
        analyzer = SentimentAnalyzer(compound_threshold=0.1)
        assert analyzer.compound_threshold == 0.1
    
    def test_analyze_headline_positive(self):
        """Test analysis of positive headline."""
        analyzer = SentimentAnalyzer()
        scores = analyzer.analyze_headline("Stock prices surge on strong earnings")
        assert 'compound' in scores
        assert 'pos' in scores
        assert 'neu' in scores
        assert 'neg' in scores
        assert scores['compound'] > 0  # Should be positive
    
    def test_analyze_headline_negative(self):
        """Test analysis of negative headline."""
        analyzer = SentimentAnalyzer()
        scores = analyzer.analyze_headline("Stock prices crash on poor earnings")
        assert scores['compound'] < 0  # Should be negative
    
    def test_analyze_headline_empty(self):
        """Test analysis of empty headline."""
        analyzer = SentimentAnalyzer()
        scores = analyzer.analyze_headline("")
        assert scores['compound'] == 0.0
        assert scores['neu'] == 1.0
    
    def test_analyze_headline_nan(self):
        """Test analysis of NaN headline."""
        analyzer = SentimentAnalyzer()
        scores = analyzer.analyze_headline(pd.NA)
        assert scores['compound'] == 0.0
    
    def test_analyze_series(self):
        """Test batch sentiment analysis."""
        analyzer = SentimentAnalyzer()
        series = pd.Series([
            "Stock prices rise",
            "Market falls",
            "Earnings beat expectations"
        ])
        result = analyzer.analyze_series(series, show_progress=False)
        
        assert isinstance(result, pd.DataFrame)
        assert 'compound' in result.columns
        assert 'sentiment_label' in result.columns
        assert len(result) == len(series)
    
    def test_get_sentiment_summary(self):
        """Test sentiment summary statistics."""
        analyzer = SentimentAnalyzer()
        sentiment_df = pd.DataFrame({
            'compound': [0.5, 0.3, -0.2, -0.4, 0.0],
            'sentiment_label': ['positive', 'positive', 'negative', 'negative', 'neutral']
        })
        summary = analyzer.get_sentiment_summary(sentiment_df)
        
        assert 'total_headlines' in summary
        assert 'positive_count' in summary
        assert 'negative_count' in summary
        assert 'neutral_count' in summary
        assert summary['total_headlines'] == 5
        assert summary['positive_count'] == 2
        assert summary['negative_count'] == 2
        assert summary['neutral_count'] == 1


class TestSentimentReturnLinker:
    """Test cases for SentimentReturnLinker class."""
    
    def test_initialization(self):
        """Test SentimentReturnLinker initialization."""
        linker = SentimentReturnLinker()
        assert linker is not None
    
    def test_calculate_returns_simple(self):
        """Test simple return calculation."""
        linker = SentimentReturnLinker()
        prices = pd.Series([100, 105, 110, 108])
        returns = linker.calculate_returns(prices, method='simple')
        
        assert len(returns) == len(prices)
        assert pd.isna(returns.iloc[0])  # First value should be NaN
        assert abs(returns.iloc[1] - 0.05) < 0.001  # 5% return
        assert abs(returns.iloc[2] - 0.0476) < 0.01  # ~4.76% return
    
    def test_calculate_returns_log(self):
        """Test log return calculation."""
        linker = SentimentReturnLinker()
        prices = pd.Series([100, 105, 110])
        returns = linker.calculate_returns(prices, method='log')
        
        assert len(returns) == len(prices)
        assert pd.isna(returns.iloc[0])
        # Log return should be approximately ln(105/100) ≈ 0.04879
        assert abs(returns.iloc[1] - np.log(105/100)) < 0.001
    
    def test_calculate_returns_invalid_method(self):
        """Test that invalid method raises ValueError."""
        linker = SentimentReturnLinker()
        prices = pd.Series([100, 105, 110])
        with pytest.raises(ValueError, match="Unknown method"):
            linker.calculate_returns(prices, method='invalid')
    
    def test_align_sentiment_with_returns(self):
        """Test alignment of sentiment with returns."""
        linker = SentimentReturnLinker()
        
        sentiment_df = pd.DataFrame({
            'date': pd.to_datetime(['2020-01-01', '2020-01-02']),
            'stock': ['AAPL', 'AAPL'],
            'compound': [0.5, -0.3]
        })
        
        returns_df = pd.DataFrame({
            'date': pd.to_datetime(['2020-01-02', '2020-01-03']),
            'stock': ['AAPL', 'AAPL'],
            'return': [0.02, -0.01]
        })
        
        aligned = linker.align_sentiment_with_returns(
            sentiment_df, returns_df, lag_days=1
        )
        
        assert len(aligned) > 0
        assert 'compound' in aligned.columns
        assert 'return' in aligned.columns
    
    def test_calculate_sentiment_return_correlation(self):
        """Test sentiment-return correlation calculation."""
        linker = SentimentReturnLinker()
        
        sentiment_scores = pd.Series([0.5, 0.3, -0.2, -0.4, 0.1])
        returns = pd.Series([0.02, 0.01, -0.01, -0.02, 0.005])
        
        correlation_stats = linker.calculate_sentiment_return_correlation(
            sentiment_scores, returns
        )
        
        assert 'correlation' in correlation_stats
        assert 'p_value' in correlation_stats
        assert 'positive_correlation' in correlation_stats
        assert 'negative_correlation' in correlation_stats
        assert -1 <= correlation_stats['correlation'] <= 1
    
    def test_calculate_correlation_with_nans(self):
        """Test correlation calculation handles NaN values."""
        linker = SentimentReturnLinker()
        
        sentiment_scores = pd.Series([0.5, np.nan, -0.2, 0.3, np.nan])
        returns = pd.Series([0.02, 0.01, np.nan, 0.01, 0.005])
        
        correlation_stats = linker.calculate_sentiment_return_correlation(
            sentiment_scores, returns
        )
        
        # Should handle NaNs gracefully
        assert 'correlation' in correlation_stats

