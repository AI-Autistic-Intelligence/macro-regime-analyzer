import logging

import numpy as np
from scipy.stats import ks_2samp

logger = logging.getLogger(__name__)

class ConceptDriftDetector:
    """
    Tracks Data Drift in production using the Kolmogorov-Smirnov (KS) test.
    Compares a rolling window of recent production data against a baseline reference distribution.
    """
    def __init__(self, baseline_data: np.ndarray, window_size: int = 100, p_value_threshold: float = 0.05):
        self.baseline_data = baseline_data
        self.window_size = window_size
        self.p_value_threshold = p_value_threshold
        
        self.recent_data = []
        self.current_p_value = 1.0
        
    def update(self, new_feature: float) -> dict:
        """
        Ingests a new feature data point, updates the rolling window, 
        and calculates the KS statistic if the window is full.
        """
        self.recent_data.append(new_feature)
        
        if len(self.recent_data) > self.window_size:
            self.recent_data.pop(0)
            
        if len(self.recent_data) == self.window_size:
            # Perform KS test between baseline and recent window
            # We take the first feature column if baseline is 2D, or just a 1D vector
            base = self.baseline_data[:, 0] if len(self.baseline_data.shape) > 1 else self.baseline_data
            
            statistic, p_value = ks_2samp(base, self.recent_data)
            self.current_p_value = float(p_value)
            
            is_drifting = p_value < self.p_value_threshold
            
            if is_drifting:
                logger.warning(f"CONCEPT DRIFT DETECTED! P-Value dropped to {p_value:.4f}")
                
            return {
                "p_value": self.current_p_value,
                "is_drifting": is_drifting
            }
            
        return {
            "p_value": self.current_p_value,
            "is_drifting": False
        }
