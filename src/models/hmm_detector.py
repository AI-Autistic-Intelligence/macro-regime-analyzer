import logging
import warnings

import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)

class HMMDetector:
    """Enterprise-grade Hidden Markov Model for Regime Detection."""
    
    def __init__(self, n_components: int = 3, random_state: int = 42):
        self.n_components = n_components
        self.random_state = random_state
        self.scaler = StandardScaler()
        
    def fit_predict(self, df: pd.DataFrame, feature_columns: list) -> pd.DataFrame:
        logger.info(f"Training Hidden Markov Model with {self.n_components} components...")
        
        X = df[feature_columns].values
        
        # Guard against zero-variance features causing singular matrix in hmmlearn
        if np.all(np.var(X, axis=0) == 0):
            raise ValueError("Fitting failed: Singular matrix (zero variance features).")
            
        X_scaled = self.scaler.fit_transform(X)
        
        # Initialize HMM
        model = hmm.GaussianHMM(
            n_components=self.n_components, 
            covariance_type="full", 
            n_iter=1000,
            random_state=self.random_state
        )
        
        # Fit Model
        model.fit(X_scaled)
        
        # Predict Regimes
        regimes = model.predict(X_scaled)
        probs = model.predict_proba(X_scaled)
        
        out_df = df.copy()
        out_df['Regime'] = regimes
        
        for i in range(self.n_components):
            out_df[f'Regime_{i}_Prob'] = probs[:, i]
            
        logger.info("HMM training complete.")
        return out_df
