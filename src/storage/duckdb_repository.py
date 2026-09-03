
import duckdb

from src.domain.entities import MarketDataTick
from src.domain.interfaces import IDataRepository


class DuckDBRepository(IDataRepository):
    """DuckDB Analytical Store Implementation."""
    
    def __init__(self, db_path: str = "data/lakehouse.duckdb"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        with duckdb.connect(self.db_path) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS market_data (
                    symbol VARCHAR,
                    timestamp TIMESTAMP,
                    price DOUBLE,
                    volume DOUBLE
                )
            """)
            
    async def save_ticks(self, ticks: list[MarketDataTick]) -> None:
        # In a real async environment, we'd use async wrappers or run_in_executor
        with duckdb.connect(self.db_path) as con:
            # Convert to list of tuples for fast insert
            data = [(t.symbol, t.timestamp, t.price, t.volume) for t in ticks]
            con.executemany("INSERT INTO market_data VALUES (?, ?, ?, ?)", data)
            
    async def get_historical_data(self, start_date: str, end_date: str) -> list:
        with duckdb.connect(self.db_path) as con:
            df = con.execute(f"SELECT * FROM market_data WHERE timestamp >= '{start_date}' AND timestamp <= '{end_date}'").df()
        return df.to_dict('records')
