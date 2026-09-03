import numpy as np

from src.models.explainer import RegimeExplainer
from src.models.lstm_detector import LSTMRegimeModel


def test_explainer_initialization():
    model = LSTMRegimeModel(input_dim=4)
    bg_data = np.random.randn(10, 1, 4)
    explainer = RegimeExplainer(model, bg_data)
    
    assert explainer is not None
    assert explainer.explainer is not None

def test_explain_prediction():
    model = LSTMRegimeModel(input_dim=4)
    bg_data = np.random.randn(10, 1, 4)
    explainer = RegimeExplainer(model, bg_data)
    
    test_feature = np.random.randn(1, 1, 4)
    explanation = explainer.explain_prediction(test_feature)
    
    assert "predicted_regime" in explanation
    assert "feature_importance" in explanation
    assert "Returns" in explanation["feature_importance"]
    assert "Volatility_21d" in explanation["feature_importance"]
    assert "Momentum_63d" in explanation["feature_importance"]
    assert "Volume_Trend" in explanation["feature_importance"]

def test_explainer_with_1d_array():
    model = LSTMRegimeModel(input_dim=4)
    bg_data = np.random.randn(10, 1, 4)
    explainer = RegimeExplainer(model, bg_data)
    
    test_feature = np.random.randn(4)  # 1D array should be auto-reshaped
    explanation = explainer.explain_prediction(test_feature)
    
    assert "predicted_regime" in explanation
