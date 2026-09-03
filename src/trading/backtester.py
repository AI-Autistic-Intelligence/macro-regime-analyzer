import logging
import pandas as pd
import numpy as np
import vectorbt as vbt

logger = logging.getLogger(__name__)

class RegimeBacktester:
    """
    Simulates trading strategies based on the Macro Regime predictions
    using vectorbt.
    """
    def __init__(self, price_data: pd.Series, regimes: pd.Series):
        """
        :param price_data: A pandas Series with datetime index representing asset prices (e.g., SP500 Close).
        :param regimes: A pandas Series with datetime index representing predicted regimes (0, 1, or 2).
        """
        self.prices = price_data
        self.regimes = regimes
        
        # Ensure indices match
        self.prices, self.regimes = self.prices.align(self.regimes, join='inner')

    def run_strategy(self) -> vbt.Portfolio:
        """
        Executes a simple strategy:
        Regime 1 (Risk-On): 100% Long
        Regime 0 (Risk-Off): Cash (Close all positions)
        Regime 2 (Neutral): Hold existing position
        
        Returns the vectorbt Portfolio object for performance analysis.
        """
        logger.info("Running backtest strategy based on Regimes...")
        
        # Generate entries and exits based on regime
        # Entry: when regime changes to 1
        entries = (self.regimes == 1) & (self.regimes.shift(1) != 1)
        
        # Exit: when regime changes to 0
        exits = (self.regimes == 0) & (self.regimes.shift(1) != 0)
        
        portfolio = vbt.Portfolio.from_signals(
            self.prices,
            entries,
            exits,
            init_cash=100_000.0,
            fees=0.001, # 0.1% fee per trade
            freq='D' # Daily frequency
        )
        
        return portfolio

    def get_metrics(self) -> dict:
        """
        Returns key performance indicators (KPIs) of the backtest.
        """
        portfolio = self.run_strategy()
        
        return {
            "Total_Return_%": portfolio.total_return() * 100,
            "Sharpe_Ratio": portfolio.sharpe_ratio(),
            "Max_Drawdown_%": portfolio.max_drawdown() * 100,
            "Win_Rate_%": portfolio.trades.win_rate() * 100
        }
