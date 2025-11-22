"""
Unit tests for text_processor module.

Tests for TextPreprocessor, KeywordExtractor, and NLTKDataManager classes.
"""

import pytest
import pandas as pd
from src.text_processor import TextPreprocessor, KeywordExtractor, NLTKDataManager


class TestNLTKDataManager:
    """Test cases for NLTKDataManager class."""
    
    def test_required_resources_defined(self):
        """Test that all required resources are defined."""
        assert len(NLTKDataManager.REQUIRED_RESOURCES) > 0
        assert all(len(resource) == 2 for resource in NLTKDataManager.REQUIRED_RESOURCES)
    
    def test_ensure_resource_with_valid_name(self):
        """Test ensure_resource with valid resource name."""
        # This should not raise an error
        result = NLTKDataManager.ensure_resource('tokenizers/punkt', 'punkt')
        assert isinstance(result, bool)
    
    def test_ensure_all_resources(self):
        """Test that ensure_all_resources runs without error."""
        # Should complete without raising exceptions
        NLTKDataManager.ensure_all_resources()


class TestTextPreprocessor:
    """Test cases for TextPreprocessor class."""
    
    def test_initialization(self):
        """Test TextPreprocessor initialization."""
        preprocessor = TextPreprocessor()
        assert preprocessor.language == 'english'
        assert len(preprocessor.stop_words) > 0
    
    def test_preprocess_empty_string(self):
        """Test preprocessing empty string."""
        preprocessor = TextPreprocessor()
        result = preprocessor.preprocess("")
        assert result == ""
    
    def test_preprocess_nan(self):
        """Test preprocessing NaN value."""
        preprocessor = TextPreprocessor()
        result = preprocessor.preprocess(pd.NA)
        assert result == ""
    
    def test_preprocess_lowercase_conversion(self):
        """Test that text is converted to lowercase."""
        preprocessor = TextPreprocessor()
        result = preprocessor.preprocess("STOCK PRICES RISE")
        assert result.islower()
        assert "stock" in result
        assert "prices" in result
        assert "rise" in result
    
    def test_preprocess_removes_urls(self):
        """Test that URLs are removed from text."""
        preprocessor = TextPreprocessor()
        text = "Check this out https://example.com and www.test.com"
        result = preprocessor.preprocess(text)
        assert "https://example.com" not in result
        assert "www.test.com" not in result
    
    def test_preprocess_removes_special_characters(self):
        """Test that special characters are removed."""
        preprocessor = TextPreprocessor()
        text = "Stock prices rise 50%! #market"
        result = preprocessor.preprocess(text)
        # Should not contain special characters (only letters and spaces)
        assert not any(char.isdigit() for char in result.split())
        assert "#" not in result
        assert "%" not in result
    
    def test_preprocess_removes_stopwords(self):
        """Test that stopwords are removed."""
        preprocessor = TextPreprocessor()
        text = "the stock and the market"
        result = preprocessor.preprocess(text)
        # Common stopwords should be removed
        assert "the" not in result.split()
        assert "and" not in result.split()
    
    def test_preprocess_removes_short_tokens(self):
        """Test that very short tokens are removed."""
        preprocessor = TextPreprocessor()
        text = "a b c stock prices"
        result = preprocessor.preprocess(text)
        tokens = result.split()
        # All tokens should be longer than 2 characters
        assert all(len(token) > 2 for token in tokens)
    
    def test_preprocess_series(self):
        """Test preprocessing a pandas Series."""
        preprocessor = TextPreprocessor()
        series = pd.Series([
            "Stock prices rise",
            "Market falls today",
            "Earnings beat expectations"
        ])
        result = preprocessor.preprocess_series(series, show_progress=False)
        assert len(result) == len(series)
        assert all(isinstance(text, str) for text in result)


class TestKeywordExtractor:
    """Test cases for KeywordExtractor class."""
    
    def test_initialization_with_preprocessor(self):
        """Test initialization with provided preprocessor."""
        preprocessor = TextPreprocessor()
        extractor = KeywordExtractor(preprocessor)
        assert extractor.preprocessor is preprocessor
    
    def test_initialization_without_preprocessor(self):
        """Test initialization without preprocessor (creates new one)."""
        extractor = KeywordExtractor()
        assert extractor.preprocessor is not None
        assert isinstance(extractor.preprocessor, TextPreprocessor)
    
    def test_extract_keywords(self):
        """Test keyword extraction from text list."""
        extractor = KeywordExtractor()
        texts = [
            "stock prices rise",
            "stock market gains",
            "prices increase today"
        ]
        keywords = extractor.extract_keywords(texts, top_n=10)
        assert isinstance(keywords, dict)
        assert len(keywords) <= 10
        # Common words should appear
        assert "stock" in keywords or "prices" in keywords
    
    def test_extract_keywords_top_n(self):
        """Test that top_n parameter limits results."""
        extractor = KeywordExtractor()
        texts = ["word1 word2 word3 word4 word5"] * 10
        keywords = extractor.extract_keywords(texts, top_n=3)
        assert len(keywords) <= 3

