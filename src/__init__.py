"""
Sentiment-Driven Stock Prediction - Source Package

This package provides modular components for data loading, preprocessing,
text analysis, and statistical analysis of analyst ratings data.
"""

from .data_loader import DataLoader, DataPreprocessor
from .text_processor import TextPreprocessor, KeywordExtractor, NLTKDataManager
from .analyzer import DescriptiveAnalyzer, TimeSeriesAnalyzer, PublisherAnalyzer

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
]

__version__ = '0.1.0'

