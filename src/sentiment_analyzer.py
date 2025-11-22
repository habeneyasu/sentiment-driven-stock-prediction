"""
Sentiment analysis module.

This module provides sentiment analysis functionality for financial headlines,
including VADER sentiment analysis and sentiment-return correlation analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """
    A class for analyzing sentiment in financial headlines.
    
    Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment
    analysis, which is specifically tuned for social media and financial text.
    VADER provides compound scores ranging from -1 (most negative) to +1 (most positive).
    
    Attributes:
        analyzer: VADER SentimentIntensityAnalyzer instance
        compound_threshold: Threshold for classifying sentiment (default: 0.05)
    
    Example:
        >>> sentiment_analyzer = SentimentAnalyzer()
        >>> scores = sentiment_analyzer.analyze_headline("Stock prices surge on strong earnings")
        >>> print(f"Sentiment: {scores['compound']:.3f}")
    """
    
    def __init__(self, compound_threshold: float = 0.05):
        """
        Initialize the SentimentAnalyzer.
        
        Args:
            compound_threshold: Threshold for sentiment classification (default: 0.05)
                               Scores above threshold = positive
                               Scores below -threshold = negative
                               Otherwise = neutral
        """
        self.analyzer = SentimentIntensityAnalyzer()
        self.compound_threshold = compound_threshold
    
    def analyze_headline(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single headline.
        
        Returns a dictionary with sentiment scores:
        - compound: Overall sentiment score (-1 to +1)
        - pos: Positive sentiment score (0 to 1)
        - neu: Neutral sentiment score (0 to 1)
        - neg: Negative sentiment score (0 to 1)
        
        Args:
            text: Headline text to analyze
            
        Returns:
            dict: Dictionary with sentiment scores
        
        Example:
            >>> analyzer = SentimentAnalyzer()
            >>> scores = analyzer.analyze_headline("Stock prices rise")
            >>> # Returns: {'compound': 0.4404, 'pos': 0.5, 'neu': 0.5, 'neg': 0.0}
        """
        if pd.isna(text) or not text:
            # Return neutral sentiment for empty/missing text
            return {'compound': 0.0, 'pos': 0.0, 'neu': 1.0, 'neg': 0.0}
        
        # Get sentiment scores from VADER
        scores = self.analyzer.polarity_scores(str(text))
        return scores
    
    def analyze_series(self, series: pd.Series, show_progress: bool = True) -> pd.DataFrame:
        """
        Analyze sentiment for a pandas Series of headlines.
        
        Processes all headlines and returns a DataFrame with sentiment scores
        for each headline. This enables batch processing and analysis.
        
        Args:
            series: Series of headline texts to analyze
            show_progress: Whether to show progress bar (default: True)
            
        Returns:
            pd.DataFrame: DataFrame with columns:
                - compound: Overall sentiment score
                - pos: Positive score
                - neu: Neutral score
                - neg: Negative score
                - sentiment_label: 'positive', 'negative', or 'neutral'
        
        Example:
            >>> analyzer = SentimentAnalyzer()
            >>> df['sentiment'] = analyzer.analyze_series(df['headline'])
        """
        from tqdm import tqdm
        
        # Analyze each headline
        if show_progress:
            tqdm.pandas(desc="Analyzing sentiment")
            sentiment_scores = series.progress_apply(self.analyze_headline)
        else:
            sentiment_scores = series.apply(self.analyze_headline)
        
        # Convert list of dicts to DataFrame
        sentiment_df = pd.DataFrame(list(sentiment_scores))
        
        # Add sentiment label based on compound score
        sentiment_df['sentiment_label'] = sentiment_df['compound'].apply(
            lambda x: 'positive' if x > self.compound_threshold 
                     else 'negative' if x < -self.compound_threshold 
                     else 'neutral'
        )
        
        return sentiment_df
    
    def get_sentiment_summary(self, sentiment_df: pd.DataFrame) -> Dict[str, any]:
        """
        Get summary statistics for sentiment analysis results.
        
        Calculates distribution of sentiment labels and average scores,
        providing an overview of overall sentiment in the dataset.
        
        Args:
            sentiment_df: DataFrame with sentiment scores (from analyze_series)
            
        Returns:
            dict: Dictionary with summary statistics
        """
        return {
            'total_headlines': len(sentiment_df),
            'positive_count': int((sentiment_df['sentiment_label'] == 'positive').sum()),
            'negative_count': int((sentiment_df['sentiment_label'] == 'negative').sum()),
            'neutral_count': int((sentiment_df['sentiment_label'] == 'neutral').sum()),
            'positive_pct': float((sentiment_df['sentiment_label'] == 'positive').mean() * 100),
            'negative_pct': float((sentiment_df['sentiment_label'] == 'negative').mean() * 100),
            'neutral_pct': float((sentiment_df['sentiment_label'] == 'neutral').mean() * 100),
            'avg_compound': float(sentiment_df['compound'].mean()),
            'median_compound': float(sentiment_df['compound'].median()),
        }


class SentimentReturnLinker:
    """
    A class for linking sentiment scores with stock returns.
    
    This class enables correlation analysis between headline sentiment
    and subsequent stock price movements, which is the core of sentiment-driven
    stock prediction.
    
    Example:
        >>> linker = SentimentReturnLinker()
        >>> correlation = linker.calculate_sentiment_return_correlation(
        ...     sentiment_scores, stock_returns, lag_days=1
        ... )
    """
    
    def __init__(self):
        """Initialize the SentimentReturnLinker."""
        pass
    
    def calculate_returns(self, prices: pd.Series, method: str = 'simple') -> pd.Series:
        """
        Calculate stock returns from price series.
        
        Supports both simple returns (P_t / P_{t-1} - 1) and log returns
        (ln(P_t / P_{t-1})). Log returns are preferred for statistical analysis
        as they are symmetric and additive.
        
        Args:
            prices: Series of stock prices (should be sorted by date)
            method: 'simple' or 'log' (default: 'simple')
            
        Returns:
            pd.Series: Returns series (first value will be NaN)
        
        Example:
            >>> prices = pd.Series([100, 105, 110, 108])
            >>> returns = linker.calculate_returns(prices, method='simple')
            >>> # Returns: [NaN, 0.05, 0.0476, -0.0182]
        """
        if method == 'simple':
            # Simple returns: (P_t / P_{t-1}) - 1
            returns = prices.pct_change()
        elif method == 'log':
            # Log returns: ln(P_t / P_{t-1})
            returns = np.log(prices / prices.shift(1))
        else:
            raise ValueError(f"Unknown method: {method}. Use 'simple' or 'log'")
        
        return returns
    
    def align_sentiment_with_returns(
        self,
        sentiment_df: pd.DataFrame,
        returns_df: pd.DataFrame,
        date_col: str = 'date',
        stock_col: str = 'stock',
        lag_days: int = 1
    ) -> pd.DataFrame:
        """
        Align sentiment scores with stock returns for correlation analysis.
        
        This method matches headlines with subsequent stock returns, accounting
        for a time lag (e.g., sentiment today affects returns tomorrow). This
        enables analysis of whether positive/negative sentiment predicts returns.
        
        Args:
            sentiment_df: DataFrame with sentiment scores and dates
            returns_df: DataFrame with stock returns and dates
            date_col: Name of date column in both DataFrames
            stock_col: Name of stock ticker column
            lag_days: Number of days to lag returns (default: 1)
                    lag_days=1 means sentiment today -> returns tomorrow
        
        Returns:
            pd.DataFrame: Merged DataFrame with sentiment and returns aligned
        
        Example:
            >>> aligned = linker.align_sentiment_with_returns(
            ...     sentiment_df, returns_df, lag_days=1
            ... )
            >>> correlation = aligned['compound'].corr(aligned['return'])
        """
        # Ensure dates are datetime
        sentiment_df = sentiment_df.copy()
        returns_df = returns_df.copy()
        
        sentiment_df[date_col] = pd.to_datetime(sentiment_df[date_col])
        returns_df[date_col] = pd.to_datetime(returns_df[date_col])
        
        # Shift returns forward by lag_days to align with sentiment
        # If lag_days=1: sentiment on day 0 aligns with return on day 1
        returns_df['aligned_date'] = returns_df[date_col] - pd.Timedelta(days=lag_days)
        
        # Merge on date and stock ticker
        merged = pd.merge(
            sentiment_df,
            returns_df[[stock_col, 'aligned_date', 'return']],
            left_on=[date_col, stock_col],
            right_on=['aligned_date', stock_col],
            how='inner'
        )
        
        return merged
    
    def calculate_sentiment_return_correlation(
        self,
        sentiment_scores: pd.Series,
        returns: pd.Series
    ) -> Dict[str, float]:
        """
        Calculate correlation between sentiment and returns.
        
        Computes Pearson correlation coefficient and related statistics
        to measure the strength of relationship between sentiment and returns.
        
        Args:
            sentiment_scores: Series of sentiment compound scores
            returns: Series of stock returns (aligned with sentiment)
            
        Returns:
            dict: Dictionary with correlation statistics:
                - correlation: Pearson correlation coefficient
                - p_value: Statistical significance (if scipy available)
                - positive_correlation: Correlation for positive returns only
                - negative_correlation: Correlation for negative returns only
        """
        # Remove NaN values for correlation calculation
        valid_mask = sentiment_scores.notna() & returns.notna()
        sentiment_clean = sentiment_scores[valid_mask]
        returns_clean = returns[valid_mask]
        
        if len(sentiment_clean) < 2:
            return {
                'correlation': 0.0,
                'p_value': 1.0,
                'positive_correlation': 0.0,
                'negative_correlation': 0.0
            }
        
        # Calculate overall correlation
        correlation = sentiment_clean.corr(returns_clean)
        
        # Calculate correlation for positive vs negative returns
        positive_mask = returns_clean > 0
        negative_mask = returns_clean < 0
        
        positive_corr = (sentiment_clean[positive_mask].corr(returns_clean[positive_mask]) 
                        if positive_mask.sum() > 1 else 0.0)
        negative_corr = (sentiment_clean[negative_mask].corr(returns_clean[negative_mask]) 
                        if negative_mask.sum() > 1 else 0.0)
        
        # Calculate p-value if scipy is available
        try:
            from scipy.stats import pearsonr
            _, p_value = pearsonr(sentiment_clean, returns_clean)
        except ImportError:
            p_value = np.nan
        
        return {
            'correlation': float(correlation) if not pd.isna(correlation) else 0.0,
            'p_value': float(p_value) if not pd.isna(p_value) else np.nan,
            'positive_correlation': float(positive_corr) if not pd.isna(positive_corr) else 0.0,
            'negative_correlation': float(negative_corr) if not pd.isna(negative_corr) else 0.0,
        }

