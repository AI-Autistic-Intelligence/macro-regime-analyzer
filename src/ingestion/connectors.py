import json
import logging
from collections.abc import Awaitable, Callable
from datetime import datetime

import websockets
from tenacity import retry, stop_after_attempt, wait_exponential

from src.domain.entities import MarketDataTick

logger = logging.getLogger(__name__)

class BinanceWebSocketConnector:
    """
    Real-Time WebSocket connector for streaming market data.
    Implements robust retry logic with exponential backoff (Resiliency Pillar).
    """
    
    def __init__(self, stream_url: str = "wss://stream.binance.com:9443/ws/btcusdt@trade"):
        self.stream_url = stream_url
        
    @retry(wait=wait_exponential(multiplier=1, min=2, max=60), stop=stop_after_attempt(5))
    async def connect_and_listen(self, on_tick_callback: Callable[[MarketDataTick], Awaitable[None]]):
        """
        Connects to the websocket and listens for incoming streams.
        Passes parsed domain entities to the provided async callback.
        """
        logger.info(f"Attempting to connect to WebSocket: {self.stream_url}")
        
        async with websockets.connect(self.stream_url) as websocket:
            logger.info("Successfully connected to WebSocket.")
            
            try:
                async for message in websocket:
                    data = json.loads(message)
                    
                    # Parse Binance specific trade format into our Domain Entity
                    if 'p' in data and 'q' in data:
                        tick = MarketDataTick(
                            symbol="BTCUSDT",
                            timestamp=datetime.fromtimestamp(data['E'] / 1000.0),
                            price=float(data['p']),
                            volume=float(data['q'])
                        )
                        
                        # Process tick asynchronously
                        await on_tick_callback(tick)
                        
            except websockets.exceptions.ConnectionClosed as e:
                logger.error(f"WebSocket connection closed unexpectedly: {e}")
                raise # Raise to trigger tenacity retry
