import logging

import redis.asyncio as redis

from src.domain.entities import RegimePrediction
from src.domain.interfaces import ICacheRepository

logger = logging.getLogger(__name__)

class RedisCache(ICacheRepository):
    """Redis low-latency cache for fast API serving."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.client = redis.from_url(redis_url, decode_responses=True)
        
    async def set_latest_regime(self, prediction: RegimePrediction) -> None:
        try:
            data = prediction.model_dump_json()
            await self.client.set("latest_regime", data)
        except Exception as e:
            logger.error(f"Redis Set Error: {e}")
            
    async def get_latest_regime(self) -> RegimePrediction | None:
        try:
            data = await self.client.get("latest_regime")
            if data:
                return RegimePrediction.model_validate_json(data)
            return None
        except Exception as e:
            logger.error(f"Redis Get Error: {e}")
            # Fallback gracefully
            return None
