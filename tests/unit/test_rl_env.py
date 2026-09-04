import numpy as np

from src.models.rl_env import MacroTradingEnv


def test_rl_environment():
    df_prices = np.array([100.0, 105.0, 110.0])
    df_regimes = np.array([1, 1, 0])
    df_sentiment = np.array([0.5, 0.8, -0.5])
    
    env = MacroTradingEnv(df_prices, df_regimes, df_sentiment, initial_balance=1000.0)
    
    obs, _info = env.reset()
    assert obs.shape == (5,)
    
    # Action 2 is BUY
    obs, _reward, _done, _truncated, _info = env.step(2)
    assert env.position == 1.0
    assert env.balance == 900.0
    
    # Action 0 is SELL
    obs, _reward, done, _truncated, _info = env.step(0)
    assert env.position == 0.0
    assert env.balance == 1005.0  # Bought at 100, sold at 105
    assert done is True
