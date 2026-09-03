import pytest
from pandera.errors import SchemaError

from src.ingestion.validators import validate_tick


def test_valid_tick():
    valid_tick = {
        "Date": "2024-01-01",
        "SP500_Close": 4500.5,
        "VIX_Close": 15.2,
        "Interest_Rate": 5.25,
        "Inflation_Rate": 3.1,
        "GDP_Growth": 2.5
    }
    df = validate_tick(valid_tick)
    assert len(df) == 1
    assert "SP500_Close" in df.columns

def test_invalid_tick_negative_price():
    invalid_tick = {
        "Date": "2024-01-01",
        "SP500_Close": -100.0, # INVALID: must be >= 0
        "VIX_Close": 15.2,
        "Interest_Rate": 5.25,
        "Inflation_Rate": 3.1,
        "GDP_Growth": 2.5
    }
    with pytest.raises(SchemaError):
        validate_tick(invalid_tick)
        
def test_missing_column():
    invalid_tick = {
        "Date": "2024-01-01",
        "SP500_Close": 4500.0,
        # missing VIX
        "Interest_Rate": 5.25,
        "Inflation_Rate": 3.1,
        "GDP_Growth": 2.5
    }
    with pytest.raises(SchemaError):
        validate_tick(invalid_tick)
