# Architecture Overview

This system uses a microservice architecture built on Docker, Kafka, and Redis.

```mermaid
graph TD;
  A[Binance WebSocket] --> B[Kafka (Redpanda)];
  B --> C[Polars Processor];
  C --> D[PyTorch LSTM Model];
  D --> E[Redis Cache];
  E --> F[FastAPI Backend];
```