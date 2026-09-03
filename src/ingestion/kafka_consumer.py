import asyncio
import json
import logging

import numpy as np
from aiokafka import AIOKafkaConsumer

from src.core.config import settings
from src.models.lstm_detector import LSTMDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize ML model (heavy object)
lstm_model = LSTMDetector(input_dim=4)

async def start_consumer():
    consumer = AIOKafkaConsumer(
        "market-ticks",
        bootstrap_servers=settings.kafka_bootstrap_servers if hasattr(settings, 'kafka_bootstrap_servers') else 'localhost:9092',
        group_id="regime-inference-group",
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    await consumer.start()
    try:
        logger.info("Listening for market ticks...")
        async for msg in consumer:
            tick = msg.value
            logger.info(f"Consumed tick for Date: {tick.get('Date', 'N/A')}")
            
            # Data Contract Validation (Epoch 5)
            try:
                # We validate the raw dictionary against our Pandera schema
                # In a real app we'd import validate_tick from src.ingestion.validators
                # We mock it here for brevity if it's not imported
                from pandera.errors import SchemaError

                from src.ingestion.validators import validate_tick
                validated_df = validate_tick(tick)
            except SchemaError as e:
                logger.error(f"DATA CONTRACT VIOLATION! Routing to Dead Letter Queue. Error: {e!s}")
                # TODO: Route to Dead Letter Queue (DLQ) in Kafka or Redis
                continue # Skip this corrupt tick
            
            # Extract features (mocking a real vector)
            features = np.random.randn(4)
            
            # MULTITHREADING/CONCURRENCY: ML inference is CPU-bound and synchronous.
            # Running it directly would block the asyncio Event Loop and kill streaming throughput!
            # We offload it to a background thread pool using asyncio.to_thread.
            pred_dict = await asyncio.to_thread(lstm_model.predict_regime, features)
            
            logger.info(f"Inference Result (LSTM): Regime {pred_dict['regime']}")
            
            # TODO: Save to Redis repository here
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(start_consumer())
