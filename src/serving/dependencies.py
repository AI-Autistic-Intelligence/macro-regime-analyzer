from src.core.config import settings
from src.storage.duckdb_repository import DuckDBRepository
from src.storage.redis_cache import RedisCache


def get_db_repository() -> DuckDBRepository:
    """Dependency provider for DuckDB repository."""
    return DuckDBRepository(db_path=settings.duckdb_path)

def get_cache_repository() -> RedisCache:
    """Dependency provider for Redis Cache."""
    return RedisCache(redis_url=settings.redis_url)
