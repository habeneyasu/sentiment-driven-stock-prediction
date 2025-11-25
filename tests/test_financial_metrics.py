"""
Unit tests for financial_metrics module.

Tests for FinancialMetrics class.
"""

import pytest
import pandas as pd
import numpy as np
from src.financial_metrics import FinancialMetrics


class TestFinancialMetrics:
    """Test cases for FinancialMetrics class."""
    
    def test_initialization(self):
        """Test FinancialMetrics initialization."""
        metrics = FinancialMetrics()
        assert metrics is not None
    
    def test_volatility(self):
        """Test volatility calculation."""
        metrics = FinancialMetrics()
        returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
        vol = metrics.volatility(returns, annualize=False)
        
        assert vol > 0
        assert isinstance(vol, float)
    
    def test_volatility_annualized(self):
        """Test annualized volatility calculation."""
        metrics = FinancialMetrics()
        returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
        vol_annual = metrics.volatility(returns, annualize=True)
        vol_daily = metrics.volatility(returns, annualize=False)
        
        assert vol_annual > vol_daily
    
    def test_sharpe_ratio(self):
        """Test Sharpe ratio calculation."""
        metrics = FinancialMetrics()
        returns = pd.Series([0.01, 0.02, 0.01, 0.02, 0.01])
        sharpe = metrics.sharpe_ratio(returns, risk_free_rate=0.02)
        
        assert isinstance(sharpe, float)
    
    def test_max_drawdown(self):
        """Test maximum drawdown calculation."""
        metrics = FinancialMetrics()
        prices = pd.Series([100, 110, 105, 120, 115, 130])
        max_dd = metrics.max_drawdown(prices)
        
        assert max_dd >= 0
        assert isinstance(max_dd, float)
    
    def test_total_return(self):
        """Test total return calculation."""
        metrics = FinancialMetrics()
        prices = pd.Series([100, 102, 104, 106, 108, 110])
        total_ret = metrics.total_return(prices)
        
        assert total_ret == 10.0  # (110 - 100) / 100 * 100
    
    def test_calculate_all_metrics(self):
        """Test calculation of all metrics at once."""
        metrics = FinancialMetrics()
        prices = pd.Series([100, 102, 104, 106, 108, 110])
        returns = prices.pct_change().dropna()
        
        all_metrics = metrics.calculate_all_metrics(prices, returns=returns)
        
        assert isinstance(all_metrics, dict)
        assert 'volatility' in all_metrics
        assert 'sharpe_ratio' in all_metrics
        assert 'max_drawdown' in all_metrics
        assert 'total_return' in all_metrics
        assert 'mean_return' in all_metrics
        assert 'std_return' in all_metrics

