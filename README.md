# Macro Regime Analyzer (Enterprise MLOps)

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg)
![Kafka](https://img.shields.io/badge/Redpanda-Streaming-black.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

An Enterprise-Grade Machine Learning Operations (MLOps) project designed to detect and predict macroeconomic regimes using both statistical models (Hidden Markov Models) and Deep Learning (Temporal Fusion Transformers / LSTM).

This project demonstrates Senior-level software engineering and ML engineering principles, strictly adhering to Clean Architecture, decoupling data ingestion, feature engineering, modeling, and API serving.

## 🚀 Key Features

*   **Clean Architecture**: Separation of concerns (`domain`, `ingestion`, `features`, `models`, `serving`).
*   **Event-Driven Streaming**: Real-time market tick ingestion using Redpanda (Kafka-compatible) and `aiokafka`.
*   **A/B Model Testing**: Dynamic routing between classical unsupervised learning (HMM) and Deep Learning (PyTorch LSTM).
*   **Ultra-Fast Data Engineering**: Pandas replaced with Rust-backed **Polars** for sub-millisecond feature generation.
*   **Low-Latency Caching**: Predictions are cached in **Redis** to ensure `< 2ms` latency for the API.
*   **"God Mode" Observability**: Full telemetry using **Prometheus** and **Grafana** (Hardware metrics, HTTP 4xx/5xx errors, Python GC, Latency Percentiles).

## 🏗️ Architecture Blueprint

```mermaid
graph TD
    A[Market Data Source] -->|Kafka Producer| B(Redpanda Broker)
    B -->|Kafka Consumer| C[Polars Feature Pipeline]
    C --> D{Model Router}
    D -->|?model_type=hmm| E[HMM (scikit-learn)]
    D -->|?model_type=lstm| F[LSTM (PyTorch)]
    E --> G[(Redis Cache)]
    F --> G
    H[Client Application] -->|FastAPI REST| G
    I[Prometheus] -->|Scrapes Metrics| H
    J[Grafana] -->|Visualizes| I
```

## 🛠️ Quickstart (Docker)

To launch the entire MLOps infrastructure locally:

```bash
docker compose up --build -d
```

### Services Deployed:
*   **FastAPI**: `http://localhost:8000` (Swagger UI: `http://localhost:8000/docs`)
*   **Grafana**: `http://localhost:3030` (User: `admin`, Pass: `admin`)
*   **Redpanda Console**: `http://localhost:8080` (Kafka UI)
*   **Prometheus**: `http://localhost:9090`

## 📊 Running the Stress Test

To simulate live production traffic and trigger Prometheus alerts (High 4xx rates, CPU spikes):

```bash
python scripts/stress_test.py
```
View the traffic live on the pre-provisioned Grafana "Enterprise API God Mode" dashboard.
