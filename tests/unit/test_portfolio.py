import numpy as np
from src.trading.portfolio import PortfolioOptimizer

def test_portfolio_optimization():
    # 2 assets: Asset A is low risk/low reward, Asset B is high risk/high reward
    expected_returns = np.array([0.05, 0.15])
    cov_matrix = np.array([
        [0.01, 0.00],
        [0.00, 0.10]
    ])
    
    optimizer = PortfolioOptimizer(expected_returns, cov_matrix)
    
    # Minimize risk without target return -> should heavily weight Asset A
    weights = optimizer.optimize_allocation()
    assert np.isclose(np.sum(weights), 1.0)
    assert weights[0] > weights[1]  # Asset A gets more weight due to lower variance
