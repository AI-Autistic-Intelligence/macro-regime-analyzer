import logging

from fastapi import APIRouter, Depends, HTTPException

from src.domain.entities import RegimePrediction
from src.domain.interfaces import ICacheRepository
from src.serving.dependencies import get_cache_repository

logger = logging.getLogger(__name__)
router = APIRouter()


import numpy as np
from prometheus_client import Counter, Gauge

from src.models.drift_detector import ConceptDriftDetector
from src.models.lstm_detector import LSTMDetector

lstm_model = LSTMDetector(input_dim=4)
# Initialize Drift Detector with a dummy baseline (normally loaded from disk)
dummy_baseline = np.random.randn(100, 4)
drift_detector = ConceptDriftDetector(baseline_data=dummy_baseline, window_size=50)

# Prometheus Metrics
DRIFT_P_VALUE = Gauge("macro_drift_pvalue", "Kolmogorov-Smirnov P-Value for Data Drift")
AB_DISAGREEMENT = Counter("macro_ab_test_disagreement_total", "Total times HMM and LSTM disagreed")
DRIFT_ALERTS = Counter("macro_drift_alerts_total", "Total times Concept Drift was detected")

@router.get("/regime/current", response_model=RegimePrediction)
async def get_current_regime(
    model_type: str | None = "hmm",
    cache: ICacheRepository = Depends(get_cache_repository)  # noqa: B008
):
    """
    Low latency endpoint to fetch the most recent regime prediction.
    Reads strictly from Redis to guarantee sub-millisecond response times.
    Supports routing to different models (hmm or lstm).
    """
    
    # Simulate data ingestion for drift tracking
    mock_new_feature = np.random.randn() 
    
    # Simulate drift randomly for demonstration (1% chance to drop p-value)
    if np.random.rand() < 0.01:
        mock_new_feature += 5.0 # anomaly
        
    drift_result = drift_detector.update(mock_new_feature)
    
    # Update Prometheus Metrics
    DRIFT_P_VALUE.set(drift_result["p_value"])
    if drift_result["is_drifting"]:
        DRIFT_ALERTS.inc()
        
    if model_type == "lstm":
        dummy_features = np.random.randn(1, 1, 4)
        pred_dict = lstm_model.predict_regime(dummy_features)
        
        # Simulate A/B Testing Disagreement (10% chance)
        if np.random.rand() < 0.10:
            AB_DISAGREEMENT.inc()
            
        return RegimePrediction(
            timestamp="2024-01-01T00:00:00Z",
            regime=pred_dict["regime"],
            probabilities=pred_dict["probabilities"],
            model_info=pred_dict["model_type"]
        )

    prediction = await cache.get_latest_regime()
    if not prediction:
        logger.warning("Cache miss for latest regime.")
        raise HTTPException(status_code=404, detail="Regime prediction not found in cache. Is the pipeline running?")
    return prediction

from pydantic import BaseModel

from src.models.explainer import RegimeExplainer

# Initialize SHAP explainer with a dummy background (100 samples, 1 timestep, 4 features)
# In production, this would be a random sample of the training data
dummy_background = np.random.randn(100, 1, 4)
explainer = RegimeExplainer(lstm_model.model, dummy_background)

class ExplanationResponse(BaseModel):
    predicted_regime: int
    feature_importance: dict

@router.get("/regime/explain", response_model=ExplanationResponse)
async def explain_current_regime():
    """
    Returns SHAP feature importance for the latest prediction to provide XAI (Explainable AI).
    """
    # Mock pulling the latest features from the Feature Store (Epoch 7 preview)
    latest_features = np.random.randn(1, 1, 4)
    
    # Calculate SHAP values
    explanation = explainer.explain_prediction(latest_features)
    
    return ExplanationResponse(
        predicted_regime=explanation["predicted_regime"],
        feature_importance=explanation["feature_importance"]
    )

from src.ingestion.sentiment import SentimentAnalyzer
from src.ingestion.onchain import OnChainAnalyzer

sentiment_analyzer = SentimentAnalyzer()
onchain_analyzer = OnChainAnalyzer()

class SentimentResponse(BaseModel):
    text: str
    label: str
    score: float

@router.post("/sentiment/analyze", response_model=SentimentResponse)
async def analyze_sentiment(text: str):
    """
    Epoch 20 & 24: Analyzes sentiment of a financial news headline.
    """
    result = sentiment_analyzer.analyze_text(text)
    return SentimentResponse(
        text=text,
        label=result["label"],
        score=result["score"]
    )

class OnChainResponse(BaseModel):
    gas_price_gwei: float

@router.get("/onchain/gas", response_model=OnChainResponse)
async def get_gas_price():
    """
    Epoch 22 & 24: Fetches current Ethereum gas price as a macro indicator.
    """
    gas_price = onchain_analyzer.get_current_gas_price()
    return OnChainResponse(gas_price_gwei=gas_price)
