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
    
    This class ensures required NLTK resources are available and handles
    corrupted data files. It automatically downloads missing resources and
    re-downloads corrupted ones (e.g., BadZipFile errors). This is essential
    for reliable text processing operations that depend on NLTK data.
    
    The class uses a static/class method approach since it manages global
    NLTK resources rather than instance-specific data.
    
    Attributes:
        REQUIRED_RESOURCES: List of tuples (resource_path, download_name)
                          for all NLTK resources needed by the project
    """
    
    # List of required NLTK resources: (resource_path, download_name)
    # resource_path: Path NLTK uses to find the resource
    # download_name: Name to pass to nltk.download()
    REQUIRED_RESOURCES = [
        ('tokenizers/punkt', 'punkt'),  # Legacy sentence tokenizer
        ('tokenizers/punkt_tab', 'punkt_tab'),  # Newer tokenizer (required for NLTK 3.8+)
        ('corpora/stopwords', 'stopwords'),  # Common stopwords for filtering
        ('corpora/wordnet', 'wordnet'),  # WordNet database for lemmatization
    ]
    
    @staticmethod
    def ensure_resource(resource_name: str, download_name: Optional[str] = None) -> bool:
        """
        Ensure an NLTK resource is available, downloading if needed.
        
        This method checks if an NLTK resource exists and is valid. If the
        resource is missing or corrupted (BadZipFile), it attempts to download
        it automatically. This handles common issues like:
        - Missing resources on first run
        - Corrupted downloads from network issues
        - Version mismatches requiring re-download
        
        Args:
            resource_name: NLTK resource path (e.g., 'tokenizers/punkt')
            download_name: Name for download (default: extracts from resource_name)
            
        Returns:
            bool: True if resource is available and valid, False if download failed
        
        Example:
            >>> NLTKDataManager.ensure_resource('tokenizers/punkt_tab', 'punkt_tab')
            True
        """
        # Extract download name from resource path if not provided
        # e.g., 'tokenizers/punkt' -> 'punkt'
        if download_name is None:
            download_name = resource_name.split('/')[-1]
        
        try:
            # Try to find the resource (raises LookupError if missing)
            nltk.data.find(resource_name)
            return True  # Resource exists and is valid
        except (LookupError, zipfile.BadZipFile, OSError):
            # Resource missing or corrupted - attempt download
            try:
                nltk.download(download_name, quiet=True)  # Download without verbose output
                nltk.data.find(resource_name)  # Verify download succeeded
                return True
            except Exception:
                # Download or verification failed
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
        Preprocess a single text string for NLP analysis.
        
        Performs a complete text cleaning pipeline:
        1. Handles missing/NaN values
        2. Converts to lowercase for case-insensitive analysis
        3. Removes URLs (common in news headlines)
        4. Removes special characters (keeps only letters and spaces)
        5. Tokenizes into words
        6. Removes stopwords and very short tokens
        
        This preprocessing is essential for consistent keyword extraction
        and topic modeling, as it normalizes text and removes noise.
        
        Args:
            text: Input text to preprocess (can be any string)
            
        Returns:
            str: Preprocessed text with cleaned, tokenized words joined by spaces
        
        Example:
            >>> preprocessor = TextPreprocessor()
            >>> result = preprocessor.preprocess("Stock prices RISE 50%! https://example.com")
            >>> # Returns: "stock prices rise"
        """
        # Handle missing values (NaN, None, etc.)
        if pd.isna(text):
            return ""
        
        # Convert to lowercase for case-insensitive analysis
        # This ensures "Stock" and "stock" are treated as the same word
        text = str(text).lower()
        
        # Remove URLs using regex
        # Pattern matches: http://..., https://..., www.example.com
        # \S+ matches any non-whitespace characters (greedy)
        text = re.sub(r'http\S+|www\.\S+', '', text)
        
        # Remove special characters but keep spaces
        # Pattern [^a-z\s] means: anything NOT lowercase letter or whitespace
        # Replaced with space to preserve word boundaries
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # Tokenize into individual words using NLTK's word tokenizer
        # This handles punctuation, contractions, etc. intelligently
        tokens = word_tokenize(text)
        
        # Filter tokens: remove stopwords and very short tokens
        # Stopwords (the, a, is, etc.) don't carry much meaning
        # Short tokens (<3 chars) are often noise or abbreviations
        tokens = [token for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        # Join tokens back into a single string
        return ' '.join(tokens)
    
    def preprocess_series(self, series: pd.Series, show_progress: bool = True) -> pd.Series:
        """
        Preprocess a pandas Series of texts efficiently.
        
        Applies the preprocess() method to each text in the Series. For large
        datasets (100k+ rows), this can take significant time, so progress
        tracking is provided. The method handles missing NLTK resources
        automatically and falls back gracefully if tqdm is unavailable.
        
        Args:
            series: Series of texts to preprocess (e.g., df['headline'])
            show_progress: Whether to show tqdm progress bar (default: True)
                         Useful for large datasets to track processing time
            
        Returns:
            pd.Series: Series of preprocessed texts with same index as input
        
        Example:
            >>> preprocessor = TextPreprocessor()
            >>> df['processed'] = preprocessor.preprocess_series(df['headline'])
            Processing texts: 100%|████████| 1400000/1400000 [05:23<00:00, 4321.5it/s]
        """
        # Ensure punkt_tab is available before processing
        # This is critical for newer NLTK versions (3.8+) that require punkt_tab
        NLTKDataManager.ensure_resource('tokenizers/punkt_tab', 'punkt_tab')
        
        try:
            if show_progress:
                # Enable tqdm progress bar for pandas apply operations
                # This provides visual feedback for long-running operations
                tqdm.pandas(desc="Processing texts")
                return series.progress_apply(self.preprocess)  # Shows progress bar
            else:
                # Standard apply without progress tracking (faster, cleaner output)
                return series.apply(self.preprocess)
        except (AttributeError, LookupError):
            # Fallback handling for edge cases:
            # - AttributeError: tqdm.pandas not available (older tqdm version)
            # - LookupError: punkt_tab still missing after download attempt
            if 'punkt_tab' in str(Exception):
                # Retry downloading punkt_tab if it's the issue
                NLTKDataManager.ensure_resource('tokenizers/punkt_tab', 'punkt_tab')
            # Use standard apply as fallback (no progress bar)
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
        Extract top keywords from a list of preprocessed texts.
        
        Tokenizes all texts, counts word frequencies, and returns the most
        common keywords. This is useful for identifying dominant themes,
        important terms, and key concepts across a corpus of documents.
        
        Args:
            texts: List of preprocessed text strings (should already be cleaned)
            top_n: Number of top keywords to return (default: 50)
                  Higher values provide more comprehensive keyword lists
        
        Returns:
            dict: Dictionary mapping keywords to their frequencies
                 Keys: keyword strings
                 Values: frequency counts (int)
                 Sorted by frequency (most common first)
        
        Example:
            >>> extractor = KeywordExtractor()
            >>> keywords = extractor.extract_keywords(processed_texts, top_n=20)
            >>> # Returns: {'earnings': 1250, 'stock': 980, 'price': 750, ...}
        """
        from collections import Counter
        
        # Collect all tokens from all texts
        all_tokens = []
        for text in texts:
            # Tokenize each text (texts should already be preprocessed)
            tokens = word_tokenize(str(text))
            all_tokens.extend(tokens)  # Add to master list
        
        # Count frequency of each token using Counter
        # Counter is efficient for frequency counting
        word_freq = Counter(all_tokens)
        
        # Return top N most common as dictionary
        # most_common(top_n) returns list of (word, count) tuples
        # dict() converts to dictionary format
        return dict(word_freq.most_common(top_n))

