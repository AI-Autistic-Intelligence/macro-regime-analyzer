import pytest
from unittest.mock import MagicMock, patch
from src.models.shadow_mode import ShadowModeEvaluator

@patch("src.models.shadow_mode.mlflow")
def test_shadow_mode_promotion(mock_mlflow):
    # Setup mock
    evaluator = ShadowModeEvaluator("LSTM_Regime_Model")
    
    # Test case 1: New model is better -> promote
    promoted = evaluator.evaluate_and_promote("run123", 0.95, 0.90)
    assert promoted is True
    assert mock_mlflow.register_model.called
    
    # Test case 2: New model is worse -> do not promote
    mock_mlflow.reset_mock()
    promoted = evaluator.evaluate_and_promote("run456", 0.80, 0.90)
    assert promoted is False
    assert not mock_mlflow.register_model.called
