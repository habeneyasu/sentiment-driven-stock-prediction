"""
Text processing and NLP utilities module.

This module provides classes and functions for text preprocessing,
tokenization, and NLP-related operations.
"""

import re
import pandas as pd
import nltk
import zipfile
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import List, Optional
from tqdm import tqdm


class NLTKDataManager:
    """
    Manages NLTK data downloads and verification.
    
    This class ensures required NLTK resources are available
    and handles corrupted data files.
    """
    
    REQUIRED_RESOURCES = [
        ('tokenizers/punkt', 'punkt'),
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('corpora/stopwords', 'stopwords'),
        ('corpora/wordnet', 'wordnet'),
    ]
    
    @staticmethod
    def ensure_resource(resource_name: str, download_name: Optional[str] = None) -> bool:
        """
        Ensure an NLTK resource is available, downloading if needed.
        
        Args:
            resource_name: NLTK resource path (e.g., 'tokenizers/punkt')
            download_name: Name for download (default: last part of resource_name)
            
        Returns:
            bool: True if resource is available, False otherwise
        """
        if download_name is None:
            download_name = resource_name.split('/')[-1]
        
        try:
            nltk.data.find(resource_name)
            return True
        except (LookupError, zipfile.BadZipFile, OSError):
            try:
                nltk.download(download_name, quiet=True)
                nltk.data.find(resource_name)  # Verify download
                return True
            except Exception:
                return False
    
    @classmethod
    def ensure_all_resources(cls) -> None:
        """
        Ensure all required NLTK resources are available.
        
        Downloads any missing or corrupted resources.
        """
        for resource_name, download_name in cls.REQUIRED_RESOURCES:
            cls.ensure_resource(resource_name, download_name)


class TextPreprocessor:
    """
    A class for preprocessing text data.
    
    Handles cleaning, tokenization, and stopword removal.
    """
    
    def __init__(self, language: str = 'english'):
        """
        Initialize the TextPreprocessor.
        
        Args:
            language: Language for stopwords (default: 'english')
        """
        self.language = language
        # Ensure NLTK data is available
        NLTKDataManager.ensure_all_resources()
        self.stop_words = set(stopwords.words(language))
    
    def preprocess(self, text: str) -> str:
        """
        Preprocess a single text string.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            str: Preprocessed text
        """
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and short tokens
        tokens = [token for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)
    
    def preprocess_series(self, series: pd.Series, show_progress: bool = True) -> pd.Series:
        """
        Preprocess a pandas Series of texts.
        
        Args:
            series: Series of texts to preprocess
            show_progress: Whether to show progress bar (default: True)
            
        Returns:
            pd.Series: Series of preprocessed texts
        """
        # Ensure punkt_tab is available
        NLTKDataManager.ensure_resource('tokenizers/punkt_tab', 'punkt_tab')
        
        try:
            if show_progress:
                tqdm.pandas(desc="Processing texts")
                return series.progress_apply(self.preprocess)
            else:
                return series.apply(self.preprocess)
        except (AttributeError, LookupError):
            # Fallback if tqdm.pandas not available or punkt_tab missing
            if 'punkt_tab' in str(Exception):
                NLTKDataManager.ensure_resource('tokenizers/punkt_tab', 'punkt_tab')
            return series.apply(self.preprocess)


class KeywordExtractor:
    """
    A class for extracting keywords and phrases from text.
    """
    
    def __init__(self, preprocessor: Optional[TextPreprocessor] = None):
        """
        Initialize the KeywordExtractor.
        
        Args:
            preprocessor: TextPreprocessor instance (creates new one if None)
        """
        self.preprocessor = preprocessor or TextPreprocessor()
    
    def extract_keywords(self, texts: List[str], top_n: int = 50) -> dict:
        """
        Extract top keywords from a list of texts.
        
        Args:
            texts: List of preprocessed texts
            top_n: Number of top keywords to return (default: 50)
            
        Returns:
            dict: Dictionary mapping keywords to frequencies
        """
        from collections import Counter
        
        all_tokens = []
        for text in texts:
            tokens = word_tokenize(str(text))
            all_tokens.extend(tokens)
        
        word_freq = Counter(all_tokens)
        return dict(word_freq.most_common(top_n))

