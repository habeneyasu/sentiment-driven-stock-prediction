"""
Example script demonstrating TA-Lib, PyNance, and visualization integration.

This script shows how to:
1. Load stock data
2. Calculate technical indicators using TA-Lib
3. Calculate financial metrics using PyNance
4. Visualize indicators on price charts
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.stock_data_loader import StockDataLoader
from src.technical_analyzer import TechnicalAnalyzer
from src.financial_metrics import FinancialMetrics
from src.visualizer import TechnicalVisualizer


def main():
    """Run example technical analysis workflow."""
    print("=" * 60)
    print("Technical Analysis Example: TA-Lib & PyNance Integration")
    print("=" * 60)
    
    # 1. Load stock data
    print("\n1. Loading stock data...")
    loader = StockDataLoader()
    data_file = Path(__file__).parent.parent / 'data' / 'AAPL.csv'
    
    if not data_file.exists():
        print(f"⚠ Data file not found: {data_file}")
        print("   Using yfinance to fetch data instead...")
        df = loader.load_from_yfinance('AAPL', period='1y')
    else:
        df = loader.load_from_csv(data_file)
    
    df = loader.prepare_ohlcv_data(df)
    print(f"   ✓ Loaded {len(df)} days of data")
    print(f"   Date range: {df.index[0].date()} to {df.index[-1].date()}")
    
    # 2. Calculate technical indicators using TA-Lib
    print("\n2. Calculating technical indicators with TA-Lib...")
    analyzer = TechnicalAnalyzer(use_talib=True)
    print(f"   Using: {analyzer._method_source}")
    
    # Calculate indicators
    df['SMA_20'] = analyzer.simple_moving_average(df['Close'], window=20)
    df['SMA_50'] = analyzer.simple_moving_average(df['Close'], window=50)
    df['EMA_12'] = analyzer.exponential_moving_average(df['Close'], span=12)
    df['EMA_26'] = analyzer.exponential_moving_average(df['Close'], span=26)
    df['RSI'] = analyzer.rsi(df['Close'], period=14)
    
    macd_df = analyzer.macd(df['Close'])
    df['MACD'] = macd_df['macd']
    df['macd_signal'] = macd_df['signal']
    df['macd_histogram'] = macd_df['histogram']
    
    print("   ✓ Calculated SMA, EMA, RSI, and MACD")
    
    # 3. Calculate financial metrics
    print("\n3. Calculating financial metrics...")
    metrics_calc = FinancialMetrics()
    returns = df['Close'].pct_change().dropna()
    all_metrics = metrics_calc.calculate_all_metrics(df['Close'], returns=returns)
    
    print(f"   ✓ Financial Metrics:")
    print(f"      - Total Return: {all_metrics['total_return']:.2f}%")
    print(f"      - Annualized Volatility: {all_metrics['volatility']:.2%}")
    print(f"      - Sharpe Ratio: {all_metrics['sharpe_ratio']:.2f}")
    print(f"      - Max Drawdown: {all_metrics['max_drawdown']:.2f}%")
    
    # 4. Create visualization
    print("\n4. Creating visualization...")
    visualizer = TechnicalVisualizer()
    
    figures_dir = Path(__file__).parent.parent / 'notebooks' / 'figures'
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = figures_dir / 'AAPL_technical_analysis_integrated.html'
    
    try:
        visualizer.plot_price_with_indicators(
            df,
            ticker='AAPL',
            save_path=output_file,
            show=False
        )
        print(f"   ✓ Saved visualization to: {output_file}")
    except Exception as e:
        print(f"   ⚠ Visualization error: {e}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()

