import gymnasium as gym
from gymnasium import spaces
import numpy as np

class MacroTradingEnv(gym.Env):
    """
    Epoch 21: RL Agent Optimization
    A custom Gymnasium environment for an RL agent to learn optimal trading rules 
    given macro regimes and sentiment scores.
    """
    def __init__(self, df_prices, df_regimes, df_sentiment, initial_balance=10000.0):
        super(MacroTradingEnv, self).__init__()
        
        self.df_prices = df_prices
        self.df_regimes = df_regimes
        self.df_sentiment = df_sentiment
        
        self.initial_balance = initial_balance
        self.max_steps = len(df_prices) - 1
        
        # Action Space: 0 (Sell), 1 (Hold), 2 (Buy)
        self.action_space = spaces.Discrete(3)
        
        # Observation Space: [Price, Regime, Sentiment, Balance, Position]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.balance = self.initial_balance
        self.position = 0.0
        
        return self._get_observation(), {}
        
    def _get_observation(self):
        price = self.df_prices[self.current_step]
        regime = self.df_regimes[self.current_step]
        sentiment = self.df_sentiment[self.current_step]
        return np.array([price, regime, sentiment, self.balance, self.position], dtype=np.float32)
        
    def step(self, action):
        current_price = self.df_prices[self.current_step]
        
        # Execute Action
        if action == 2: # Buy
            if self.balance >= current_price:
                self.position += 1
                self.balance -= current_price
        elif action == 0: # Sell
            if self.position > 0:
                self.position -= 1
                self.balance += current_price
                
        self.current_step += 1
        done = self.current_step >= self.max_steps
        
        # Reward is the portfolio value change
        new_price = self.df_prices[self.current_step] if not done else current_price
        portfolio_value = self.balance + (self.position * new_price)
        reward = portfolio_value - self.initial_balance # Simplified reward
        
        return self._get_observation(), reward, done, False, {}
