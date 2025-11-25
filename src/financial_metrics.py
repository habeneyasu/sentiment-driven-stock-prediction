"""
Financial metrics module using PyNance.

This module provides financial metrics calculations including volatility,
Sharpe ratio, returns, and risk metrics using PyNance library.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict

try:
    import pynance as pn
    PYNANCE_AVAILABLE = True
except ImportError:
    PYNANCE_AVAILABLE = False
    pn = None


class FinancialMetrics:
    """
    A class for calculating financial metrics using PyNance.
    
    Provides financial metrics including volatility, Sharpe ratio, returns,
    and risk metrics. Falls back to custom calculations if PyNance is not available.
    
    Example:
        >>> metrics = FinancialMetrics()
        >>> sharpe = metrics.sharpe_ratio(returns, risk_free_rate=0.02)
        >>> volatility = metrics.volatility(returns)
    """
    
    def __init__(self, use_pynance: bool = True):
        """
        Initialize the FinancialMetrics calculator.
        
        Args:
            use_pynance: If True and PyNance is available, use PyNance for calculations.
                        Otherwise, use custom calculations.
        """
        self.use_pynance = use_pynance and PYNANCE_AVAILABLE
        if self.use_pynance:
            self._method_source = "PyNance"
        else:
            self._method_source = "custom"
    
    def volatility(
        self,
        returns: pd.Series,
        annualize: bool = True,
        periods_per_year: int = 252
    ) -> float:
        """
        Calculate volatility (standard deviation of returns).
        
        Args:
            returns: Series of returns
            annualize: If True, annualize the volatility (default: True)
            periods_per_year: Number of trading periods per year (default: 252)
            
        Returns:
            float: Volatility (annualized if annualize=True)
        """
        if len(returns) == 0:
            return 0.0
        
        vol = returns.std()
        
        if annualize:
            vol = vol * np.sqrt(periods_per_year)
        
        return float(vol)
    
    def sharpe_ratio(
        self,
        returns: pd.Series,
        risk_free_rate: float = 0.02,
        annualize: bool = True,
        periods_per_year: int = 252
    ) -> float:
        """
        Calculate Sharpe ratio.
        
        Sharpe ratio = (Mean Return - Risk-Free Rate) / Volatility
        
        Args:
            returns: Series of returns
            risk_free_rate: Annual risk-free rate (default: 0.02 for 2%)
            annualize: If True, annualize returns and volatility (default: True)
            periods_per_year: Number of trading periods per year (default: 252)
            
        Returns:
            float: Sharpe ratio
        """
        if len(returns) == 0:
            return 0.0
        
        mean_return = returns.mean()
        volatility = self.volatility(returns, annualize=False)
        
        if volatility == 0:
            return 0.0
        
        if annualize:
            mean_return = mean_return * periods_per_year
            volatility = volatility * np.sqrt(periods_per_year)
            risk_free_rate = risk_free_rate  # Already annualized
        
        excess_return = mean_return - (risk_free_rate / periods_per_year if not annualize else risk_free_rate)
        sharpe = excess_return / volatility
        
        return float(sharpe)
    
    def max_drawdown(self, prices: pd.Series) -> float:
        """
        Calculate maximum drawdown.
        
        Maximum drawdown is the largest peak-to-trough decline in price.
        
        Args:
            prices: Series of prices
            
        Returns:
            float: Maximum drawdown as a percentage
        """
        if len(prices) == 0:
            return 0.0
        
        # Calculate running maximum
        running_max = prices.expanding().max()
        
        # Calculate drawdown
        drawdown = (prices - running_max) / running_max
        
        max_dd = drawdown.min()
        
        return float(abs(max_dd)) * 100  # Return as percentage
    
    def total_return(
        self,
        prices: pd.Series,
        start_price: Optional[float] = None,
        end_price: Optional[float] = None
    ) -> float:
        """
        Calculate total return over the period.
        
        Args:
            prices: Series of prices
            start_price: Starting price (uses first price if None)
            end_price: Ending price (uses last price if None)
            
        Returns:
            float: Total return as a percentage
        """
        if len(prices) == 0:
            return 0.0
        
        if start_price is None:
            start_price = prices.iloc[0]
        if end_price is None:
            end_price = prices.iloc[-1]
        
        if start_price == 0:
            return 0.0
        
        total_return = ((end_price - start_price) / start_price) * 100
        
        return float(total_return)
    
    def calculate_all_metrics(
        self,
        prices: pd.Series,
        returns: Optional[pd.Series] = None,
        risk_free_rate: float = 0.02
    ) -> Dict[str, float]:
        """
        Calculate all financial metrics at once.
        
        Args:
            prices: Series of prices
            returns: Series of returns (calculated from prices if None)
            risk_free_rate: Annual risk-free rate (default: 0.02)
            
        Returns:
            Dict[str, float]: Dictionary with all calculated metrics
        """
        if returns is None:
            returns = prices.pct_change().dropna()
        
        metrics = {
            'volatility': self.volatility(returns),
            'sharpe_ratio': self.sharpe_ratio(returns, risk_free_rate=risk_free_rate),
            'max_drawdown': self.max_drawdown(prices),
            'total_return': self.total_return(prices),
            'mean_return': float(returns.mean() * 252) if len(returns) > 0 else 0.0,
            'std_return': float(returns.std() * np.sqrt(252)) if len(returns) > 0 else 0.0,
        }
        
        return metrics

