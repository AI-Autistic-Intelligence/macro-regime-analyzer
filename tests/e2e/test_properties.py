import numpy as np
import pandas as pd
from hypothesis import given, settings
from hypothesis import strategies as st

from src.models.hmm_detector import HMMDetector


@settings(max_examples=50, deadline=None)
@given(
    feature1=st.lists(st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False), min_size=100, max_size=100),
    feature2=st.lists(st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False), min_size=100, max_size=100)
)
def test_hmm_stability_on_random_distributions(feature1, feature2):
    """
    Property-Based Test: Ensure the HMM doesn't crash on various weird (but structurally valid) numeric distributions.
    This tests the breaking point of the scikit-learn / hmmlearn wrappers.
    """
    dates = pd.date_range("2020-01-01", periods=100)
    df = pd.DataFrame(index=dates)
    df['feat1'] = feature1
    df['feat2'] = feature2
    
    # Edge case: if all features are exactly the same (variance = 0), StandardScaler will scale them to 0, 
    # but hmmlearn might throw a singular matrix error. Let's see if our model handles or surfaces it gracefully.
    # For general random floats, it should fit without crashing the Python process.
    detector = HMMDetector(n_components=2, random_state=42)
    
    try:
        out_df = detector.fit_predict(df, ['feat1', 'feat2'])
        
        # Invariants: 
        # 1. Output dataframe should have the same length as input
        assert len(out_df) == 100
        
        # 2. Regime columns must exist
        assert 'Regime' in out_df.columns
        assert 'Regime_0_Prob' in out_df.columns
        assert 'Regime_1_Prob' in out_df.columns
        
        # 3. Probabilities must sum to 1 (with slight floating point tolerance)
        prob_sum = out_df['Regime_0_Prob'] + out_df['Regime_1_Prob']
        assert np.allclose(prob_sum, 1.0, atol=1e-5)
        
    except ValueError as e:
        # We allow ValueErrors if hmmlearn detects singular matrices (e.g. variance 0)
        # This shows we know *where* it breaks, rather than an unexpected exception.
        assert "fitting" in str(e).lower() or "singular" in str(e).lower()
