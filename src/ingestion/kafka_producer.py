import asyncio
import json
import logging
from pathlib import Path

import polars as pl
from aiokafka import AIOKafkaProducer

from src.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers if hasattr(settings, 'kafka_bootstrap_servers') else 'localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        # Load dataset
        data_path = Path("data/raw/macro_data.csv")
        if not data_path.exists():
            logger.error("Data file not found.")
            return

        df = pl.read_csv(data_path)
        logger.info(f"Loaded {len(df)} records. Starting streaming...")

        # Stream row by row to simulate real-time ticks
        for row in df.iter_rows(named=True):
            await producer.send_and_wait("market-ticks", row)
            logger.info(f"Sent tick for {row.get('Date', 'Unknown')}")
            await asyncio.sleep(0.5) # Simulating tick delay
            
    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(start_producer())
