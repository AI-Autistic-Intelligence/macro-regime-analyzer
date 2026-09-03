# Macro Regime Analyzer (MRA) 📈🤖

An **Enterprise-Grade MLOps Pipeline** built to analyze macroeconomic regimes and stream real-time financial market data. It uses Deep Learning (LSTM) for regime detection and Explainable AI (SHAP) to interpret predictions, all orchestrated within a distributed microservices architecture.

## 🏗️ Architecture & Tech Stack

This project is built for high throughput, low latency, and robust machine learning lifecycle management.

- **Ingestion**: `Redpanda` (Kafka-compatible) for event-driven streaming, `Binance Websockets` for real-time market data.
- **Data Processing**: `Polars` for ultra-fast vectorized data transformations.
- **Validation**: `Pandera` for Data Contracts (Schema-on-read).
- **Feature Store**: `Feast` mock repository for online/offline feature serving.
- **Storage**: `DuckDB` (Lakehouse) for analytical queries and `Redis` for high-speed API caching.
- **Machine Learning**: `PyTorch` (LSTM) for temporal sequence modeling.
- **Explainable AI (XAI)**: `SHAP` DeepExplainer for feature importance scoring.
- **MLOps**: `MLflow` for experiment tracking and model registry.
- **Background Tasks**: `Celery` + `RabbitMQ` for asynchronous model retraining.
- **Serving**: `FastAPI` + `Uvicorn` for RESTful endpoints with JWT Authentication.
- **Infrastructure**: `Docker Compose` for containerized deployment, ready for `Kubernetes`.
- **CI/CD**: `GitHub Actions` for automated testing and linting (`Ruff` + `Pytest`).

## 🚀 Quickstart

Ensure you have Docker and Docker Compose installed on your machine.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AI-Autistic-Intelligence/macro-regime-analyzer.git
   cd macro-regime-analyzer
   ```

2. **Start the Infrastructure:**
   ```bash
   # This spins up FastAPI, Redis, Redpanda, MLflow, Celery, Grafana, and Prometheus
   docker-compose up -d --build
   ```

3. **Run the Real-time Ingestion:**
   ```bash
   # Connects to Binance and starts publishing to Redpanda
   python src/ingestion/websocket_client.py
   ```

## 📚 Project Structure

```
.
├── src/
│   ├── core/         # Configs, Security (JWT), Exceptions
│   ├── domain/       # Pydantic Entities
│   ├── features/     # Polars pipelines and Feast Feature Store definitions
│   ├── ingestion/    # Binance websockets, Kafka Consumer, Pandera validators
│   ├── models/       # PyTorch LSTM, MLflow Tracker, SHAP Explainer
│   ├── serving/      # FastAPI Server, Routers, Dependencies
│   ├── storage/      # DuckDB Lakehouse, Redis Cache wrappers
│   └── tasks/        # Celery background workers (Model Retraining)
├── tests/            # Unit, Integration, and E2E (Hypothesis) tests
├── scripts/          # Stress testing scripts
├── k8s/              # Kubernetes manifests
├── .github/          # CI/CD workflows
└── docker-compose.yml
```

## 🔒 API Endpoints

The API is served at `http://localhost:8000`. 
Interactive Swagger Documentation is available at `http://localhost:8000/docs`.

### Authentication
- `POST /api/v1/auth/token` - Get JWT Access Token

### Predictions
- `GET /api/v1/predict/latest` - Get the latest macro regime prediction (Cached)
- `POST /api/v1/predict/explain` - Get SHAP values for a specific feature array

### Management
- `POST /api/v1/models/retrain` - Trigger async Celery model retraining

## ✅ Testing & Linting

We enforce strict quality control. The project uses `Ruff` for lightning-fast linting and `Pytest` for anti-regression testing.

```bash
# Run Linter
ruff check .

# Run Tests
docker-compose exec macro_analyzer python -m pytest tests/
```
