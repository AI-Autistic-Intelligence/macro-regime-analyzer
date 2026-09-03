from datetime import datetime

from pydantic import BaseModel, Field


class RegimePrediction(BaseModel):
    """Domain entity representing a regime prediction."""
    timestamp: datetime
    regime_id: int = Field(ge=0)
    probabilities: list[float]
    model_version: str
    is_anomaly: bool = False

class MarketDataTick(BaseModel):
    """Domain entity representing a raw market tick."""
    symbol: str
    timestamp: datetime
    price: float
    volume: float | None = None
