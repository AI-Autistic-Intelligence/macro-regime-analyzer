import asyncio
import json
import logging

import websockets
from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

async def binance_ticker_loop():
    """
    Epoch 10: Real-time Websocket Ingestion.
    Connects to Binance live feed to ingest BTCUSDT ticks and stream them to Redpanda/Kafka.
    """
    uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    
    try:
        producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
        await producer.start()
    except Exception as e:  # noqa: BLE001
        logger.error(f"Failed to start Kafka Producer for Websocket: {e}")
        return

    logger.info("Connecting to Binance Live Websocket...")
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                
                # Format to our schema
                tick = {
                    "Date": str(data["E"]),
                    "SP500_Close": float(data["p"]), # Mocking BTC as SP500 for testing
                    "VIX_Close": 15.0,
                    "Interest_Rate": 5.0,
                    "Inflation_Rate": 2.0,
                    "GDP_Growth": 1.5
                }
                
                await producer.send_and_wait("market_ticks", json.dumps(tick).encode('utf-8'))
                logger.info(f"Streamed live tick: {tick['SP500_Close']}")
                
    except Exception as e:  # noqa: BLE001
        logger.error(f"Websocket error: {e}")
    finally:
        await producer.stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(binance_ticker_loop())
