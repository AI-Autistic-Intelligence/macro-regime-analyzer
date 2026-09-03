from abc import ABC, abstractmethod

from src.domain.entities import MarketDataTick, RegimePrediction


class IRegimeDetector(ABC):
    """Interface for Regime Detection Models."""
    @abstractmethod
    def predict(self, features: dict) -> RegimePrediction:
        pass
        
    @abstractmethod
    def calibrate(self, historical_data: list) -> None:
        pass

class IDataRepository(ABC):
    """Interface for Historical Data Storage."""
    @abstractmethod
    async def save_ticks(self, ticks: list[MarketDataTick]) -> None:
        pass
        
    @abstractmethod
    async def get_historical_data(self, start_date: str, end_date: str) -> list:
        pass

class ICacheRepository(ABC):
    """Interface for Fast Cache (e.g., Redis)."""
    @abstractmethod
    async def set_latest_regime(self, prediction: RegimePrediction) -> None:
        pass
        
    @abstractmethod
    async def get_latest_regime(self) -> RegimePrediction | None:
        pass
