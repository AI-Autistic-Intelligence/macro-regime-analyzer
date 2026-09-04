import pandas as pd

from src.trading.backtester import RegimeBacktester


def test_backtester_metrics():
    # Create mock daily dates
    dates = pd.date_range("2024-01-01", periods=10, freq="D")
    
    # Create mock prices (going up then down)
    prices = pd.Series([100, 105, 110, 115, 120, 115, 110, 105, 100, 95], index=dates)
    
    # Create mock regimes
    # Regime 1 (Risk-On) for first 5 days, Regime 0 (Risk-Off) for next 5 days
    regimes = pd.Series([1, 1, 1, 1, 1, 0, 0, 0, 0, 0], index=dates)
    
    backtester = RegimeBacktester(prices, regimes)
    metrics = backtester.get_metrics()
    
    assert "Total_Return_%" in metrics
    assert "Sharpe_Ratio" in metrics
    assert "Max_Drawdown_%" in metrics
    assert "Win_Rate_%" in metrics
    
    # Because we exited at 115 on day 6 and didn't ride the downtrend to 95, 
    # our return should be positive despite the asset being down overall at the end.
    assert metrics["Total_Return_%"] > 0
