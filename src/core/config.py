from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "MacroRegime Analyzer"
    version: str = "2.0.0"
    
    # DB
    duckdb_path: str = "data/lakehouse.duckdb"
    redis_url: str = "redis://localhost:6379"
    
    # Model
    n_components: int = 3
    rolling_window: int = 1000

settings = Settings()
