"""
Unit tests for analyzer module.

Tests for DescriptiveAnalyzer, TimeSeriesAnalyzer, and PublisherAnalyzer classes.
"""

import pytest
import pandas as pd
import numpy as np
from src.analyzer import DescriptiveAnalyzer, TimeSeriesAnalyzer, PublisherAnalyzer


class TestDescriptiveAnalyzer:
    """Test cases for DescriptiveAnalyzer class."""
    
    def test_initialization(self):
        """Test DescriptiveAnalyzer initialization."""
        df = pd.DataFrame({'col1': [1, 2, 3]})
        analyzer = DescriptiveAnalyzer(df)
        assert analyzer.df is df
    
    def test_headline_stats(self):
        """Test headline statistics calculation."""
        df = pd.DataFrame({
            'headline_length': [50, 60, 70, 80, 90]
        })
        analyzer = DescriptiveAnalyzer(df)
        stats = analyzer.headline_stats()
        
        assert 'mean' in stats
        assert 'median' in stats
        assert 'std' in stats
        assert 'min' in stats
        assert 'max' in stats
        assert stats['mean'] == 70.0
        assert stats['min'] == 50.0
        assert stats['max'] == 90.0
    
    def test_headline_stats_missing_column(self):
        """Test that missing column raises ValueError."""
        df = pd.DataFrame({'other_col': [1, 2, 3]})
        analyzer = DescriptiveAnalyzer(df)
        with pytest.raises(ValueError, match="headline_length"):
            analyzer.headline_stats()
    
    def test_publisher_stats(self):
        """Test publisher statistics calculation."""
        df = pd.DataFrame({
            'publisher': ['A', 'A', 'A', 'B', 'B', 'C']
        })
        analyzer = DescriptiveAnalyzer(df)
        stats = analyzer.publisher_stats()
        
        assert 'total_publishers' in stats
        assert 'mean_articles' in stats
        assert 'median_articles' in stats
        assert 'max_articles' in stats
        assert 'top_publisher' in stats
        assert stats['total_publishers'] == 3
        assert stats['top_publisher'] == 'A'
        assert stats['top_publisher_count'] == 3
    
    def test_publisher_stats_missing_column(self):
        """Test that missing publisher column raises ValueError."""
        df = pd.DataFrame({'other_col': [1, 2, 3]})
        analyzer = DescriptiveAnalyzer(df)
        with pytest.raises(ValueError, match="publisher"):
            analyzer.publisher_stats()


class TestTimeSeriesAnalyzer:
    """Test cases for TimeSeriesAnalyzer class."""
    
    def test_initialization(self):
        """Test TimeSeriesAnalyzer initialization."""
        df = pd.DataFrame({
            'date': pd.to_datetime(['2020-01-01', '2020-01-02'])
        })
        analyzer = TimeSeriesAnalyzer(df)
        assert 'date_only' in analyzer.df.columns
    
    def test_daily_counts(self):
        """Test daily counts calculation."""
        df = pd.DataFrame({
            'date': pd.to_datetime([
                '2020-01-01', '2020-01-01', '2020-01-02', '2020-01-02', '2020-01-02'
            ])
        })
        analyzer = TimeSeriesAnalyzer(df)
        daily = analyzer.daily_counts()
        
        assert isinstance(daily, pd.Series)
        assert len(daily) == 2
        assert daily.iloc[0] == 2  # 2 articles on 2020-01-01
        assert daily.iloc[1] == 3  # 3 articles on 2020-01-02
    
    def test_hourly_distribution(self):
        """Test hourly distribution calculation."""
        df = pd.DataFrame({
            'date': pd.to_datetime([
                '2020-01-01 09:00:00',
                '2020-01-01 09:00:00',
                '2020-01-01 10:00:00'
            ])
        })
        analyzer = TimeSeriesAnalyzer(df)
        hourly = analyzer.hourly_distribution()
        
        assert isinstance(hourly, pd.Series)
        assert 9 in hourly.index
        assert 10 in hourly.index
        assert hourly[9] == 2
        assert hourly[10] == 1
    
    def test_monthly_trends(self):
        """Test monthly trends calculation."""
        df = pd.DataFrame({
            'date': pd.to_datetime([
                '2020-01-15', '2020-01-20', '2020-02-10', '2020-02-15'
            ])
        })
        analyzer = TimeSeriesAnalyzer(df)
        monthly = analyzer.monthly_trends()
        
        assert isinstance(monthly, pd.Series)
        assert len(monthly) == 2
        assert monthly.iloc[0] == 2  # 2 articles in January
        assert monthly.iloc[1] == 2  # 2 articles in February
    
    def test_monthly_trends_missing_date(self):
        """Test that missing date column raises ValueError."""
        df = pd.DataFrame({'other_col': [1, 2, 3]})
        analyzer = TimeSeriesAnalyzer(df)
        with pytest.raises(ValueError, match="Date column required"):
            analyzer.monthly_trends()


class TestPublisherAnalyzer:
    """Test cases for PublisherAnalyzer class."""
    
    def test_initialization(self):
        """Test PublisherAnalyzer initialization."""
        df = pd.DataFrame({'publisher': ['A', 'B']})
        analyzer = PublisherAnalyzer(df)
        assert analyzer.df is df
    
    def test_identify_email_publishers(self):
        """Test email publisher identification."""
        df = pd.DataFrame({
            'publisher': [
                'author@example.com',
                'Benzinga Insights',
                'writer@test.org',
                'Market News'
            ]
        })
        analyzer = PublisherAnalyzer(df)
        is_email = analyzer.identify_email_publishers()
        
        assert isinstance(is_email, pd.Series)
        assert is_email.iloc[0] == True  # author@example.com
        assert is_email.iloc[1] == False  # Benzinga Insights
        assert is_email.iloc[2] == True  # writer@test.org
        assert is_email.iloc[3] == False  # Market News
    
    def test_extract_email_domains(self):
        """Test email domain extraction."""
        df = pd.DataFrame({
            'publisher': [
                'author@example.com',
                'Benzinga Insights',
                'writer@example.com',
                'editor@test.org'
            ]
        })
        analyzer = PublisherAnalyzer(df)
        domains = analyzer.extract_email_domains()
        
        assert isinstance(domains, pd.Series)
        # Should extract domains for email publishers
        email_mask = analyzer.identify_email_publishers()
        assert domains[email_mask].notna().all()
        assert 'example.com' in domains.values
        assert 'test.org' in domains.values

