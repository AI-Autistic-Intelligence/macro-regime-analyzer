import numpy as np
from scipy.optimize import minimize


class PortfolioOptimizer:
    """
    Epoch 19: Portfolio Optimization & Risk Management
    Uses Markowitz Mean-Variance optimization to allocate capital across multiple assets based on Regime.
    """
    def __init__(self, expected_returns: np.ndarray, cov_matrix: np.ndarray):
        self.expected_returns = expected_returns
        self.cov_matrix = cov_matrix
        self.num_assets = len(expected_returns)
        
    def _portfolio_variance(self, weights: np.ndarray) -> float:
        return weights.T @ self.cov_matrix @ weights
        
    def optimize_allocation(self, target_return: float | None = None) -> np.ndarray:
        """
        Finds the optimal asset weights to minimize variance (risk).
        """
        init_weights = np.ones(self.num_assets) / self.num_assets
        
        # Constraints: weights sum to 1
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}]
        
        if target_return is not None:
            constraints.append({'type': 'eq', 'fun': lambda x: np.dot(x, self.expected_returns) - target_return})
            
        # Bounds: weights between 0 and 1 (No short selling in this basic version)
        bounds = tuple((0.0, 1.0) for _ in range(self.num_assets))
        
        result = minimize(
            self._portfolio_variance, 
            init_weights, 
            method='SLSQP', 
            bounds=bounds, 
            constraints=constraints
        )
        
        return result.x
