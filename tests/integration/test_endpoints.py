from datetime import UTC, datetime

from fastapi.testclient import TestClient

from src.domain.entities import RegimePrediction
from src.domain.interfaces import ICacheRepository
from src.serving.dependencies import get_cache_repository
from src.serving.server import app

client = TestClient(app)

class MockCacheEmpty(ICacheRepository):
    async def set_latest_regime(self, prediction):
        pass
    async def get_latest_regime(self):
        return None

class MockCacheHit(ICacheRepository):
    async def set_latest_regime(self, prediction):
        pass
    async def get_latest_regime(self):
        return RegimePrediction(
            timestamp=datetime.now(UTC),
            regime_id=1,
            probabilities=[0.1, 0.8, 0.1],
            model_version="v2.0.0"
        )

def test_api_health_live():
    """Test the liveness probe."""
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_current_regime_cache_miss():
    """Test how the API handles a cache miss (e.g. Redis is empty on startup)."""
    # Override dependency with an empty cache mock
    app.dependency_overrides[get_cache_repository] = MockCacheEmpty
    
    response = client.get("/api/v1/regime/current")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
    
    # Clean up overrides
    app.dependency_overrides.clear()

def test_get_current_regime_cache_hit():
    """Test successful retrieval from cache."""
    app.dependency_overrides[get_cache_repository] = MockCacheHit
    
    response = client.get("/api/v1/regime/current")
    assert response.status_code == 200
    data = response.json()
    assert data["regime_id"] == 1
    assert data["model_version"] == "v2.0.0"
    
    app.dependency_overrides.clear()
