from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.core.config import settings
from src.serving.api.v1.endpoints import router as v1_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
        description="Enterprise API for Macro Regime Inference"
    )
    
    # Health checks
    @app.get("/health/live", tags=["health"])
    async def liveness():
        return {"status": "ok"}
        
    @app.get("/health/ready", tags=["health"])
    async def readiness():
        # Ideally, check DB and Redis connections here
        return {"status": "ok"}
        
    # Include Routers
    app.include_router(v1_router, prefix="/api/v1")
    
    # Setup Prometheus Instrumentation
    Instrumentator().instrument(app).expose(app)
    
    return app

app = create_app()
