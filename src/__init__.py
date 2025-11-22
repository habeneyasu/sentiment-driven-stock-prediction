"""
Sentiment-Driven Stock Prediction - Source Package

This package provides modular components for data loading, preprocessing,
text analysis, statistical analysis, sentiment analysis, and technical
analysis of analyst ratings and stock data.
"""

from .data_loader import DataLoader, DataPreprocessor
from .text_processor import TextPreprocessor, KeywordExtractor, NLTKDataManager
from .analyzer import DescriptiveAnalyzer, TimeSeriesAnalyzer, PublisherAnalyzer
from .sentiment_analyzer import SentimentAnalyzer, SentimentReturnLinker
from .technical_analyzer import TechnicalAnalyzer

__all__ = [
    # Data loading
    'DataLoader',
    'DataPreprocessor',
    # Text processing
    'TextPreprocessor',
    'KeywordExtractor',
    'NLTKDataManager',
    # Analysis
    'DescriptiveAnalyzer',
    'TimeSeriesAnalyzer',
    'PublisherAnalyzer',
    # Sentiment analysis
    'SentimentAnalyzer',
    'SentimentReturnLinker',
    # Technical analysis
    'TechnicalAnalyzer',
]

__version__ = '0.2.0'

