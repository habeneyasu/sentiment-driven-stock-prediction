"""
Pytest configuration and shared fixtures.

This file provides common fixtures used across multiple test files,
reducing code duplication and improving test maintainability.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


@pytest.fixture
def sample_dataframe():
    """
    Create a sample DataFrame for testing.
    
    Returns a DataFrame with typical analyst ratings data structure.
    """
    return pd.DataFrame({
        'headline': [
            'Stock prices rise on strong earnings',
            'Market falls on poor guidance',
            'Earnings beat expectations',
            'Company announces new product',
            'Analyst upgrades stock rating'
        ],
        'date': pd.to_datetime([
            '2020-01-01 09:00:00',
            '2020-01-02 10:00:00',
            '2020-01-03 11:00:00',
            '2020-01-04 12:00:00',
            '2020-01-05 13:00:00'
        ]),
        'publisher': [
            'Benzinga Insights',
            'author@example.com',
            'Market News',
            'writer@test.org',
            'Financial Times'
        ],
        'stock': ['AAPL', 'AAPL', 'MSFT', 'MSFT', 'GOOGL'],
        'url': [
            'https://example.com/1',
            'https://example.com/2',
            'https://example.com/3',
            'https://example.com/4',
            'https://example.com/5'
        ]
    })


@pytest.fixture
def sample_price_series():
    """
    Create a sample price series for technical analysis testing.
    
    Returns a Series with realistic stock price movements.
    """
    np.random.seed(42)  # For reproducible tests
    base_price = 100.0
    # Generate prices with slight upward trend and volatility
    prices = [base_price]
    for _ in range(49):
        change = np.random.randn() * 2  # Random walk with volatility
        prices.append(prices[-1] + change)
    return pd.Series(prices)


@pytest.fixture
def sample_returns_series():
    """
    Create a sample returns series for correlation testing.
    
    Returns a Series with realistic stock returns.
    """
    np.random.seed(42)
    # Generate returns with slight positive mean
    returns = np.random.normal(0.001, 0.02, 50)  # Mean 0.1%, std 2%
    return pd.Series(returns)


@pytest.fixture
def temp_csv_file(tmp_path):
    """
    Create a temporary CSV file for data loading tests.
    
    Args:
        tmp_path: Pytest temporary directory fixture
        
    Returns:
        Path: Path to temporary CSV file
    """
    test_file = tmp_path / "test_data.csv"
    df = pd.DataFrame({
        'headline': ['Test headline 1', 'Test headline 2', 'Test headline 3'],
        'date': ['2020-01-01', '2020-01-02', '2020-01-03'],
        'publisher': ['Publisher A', 'Publisher B', 'Publisher A'],
        'stock': ['AAPL', 'AAPL', 'MSFT'],
        'url': ['http://example.com/1', 'http://example.com/2', 'http://example.com/3']
    })
    df.to_csv(test_file, index=False)
    return test_file

