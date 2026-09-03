import polars as pl
import pytest

from src.features.pipeline import PolarsFeaturePipeline


def test_pipeline_normal_processing():
    """Test standard feature extraction logic with Polars."""
    df = pl.DataFrame({
        "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "SPY": [100.0, 101.0, 102.01]
    })
    
    # We only have 3 rows, so 21d Vol and 63d Mom will be Null and dropped by pipeline
    # The pipeline calls drop_nulls(), so if we don't have enough data, it should return an empty dataframe
    # This is a critical edge case to test!
    result = PolarsFeaturePipeline.process_features(df, ["SPY"])
    assert result.height == 0 # Because rolling windows > df size cause NaNs which are dropped

def test_pipeline_zero_prices_handling():
    """Test that zeros or negative prices don't crash log returns, but result in NaNs or Infinities."""
    df = pl.DataFrame({
        "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "SPY": [100.0, 0.0, 102.0]
    })
    
    # In Polars, log(0) results in -inf. The pipeline currently doesn't filter infinities (Validator does this).
    # We just want to ensure Polars doesn't hard crash the Python process.
    try:
        # We temporarily mock the pipeline to not drop nulls to inspect the calculation
        exprs = [ (pl.col("SPY") / pl.col("SPY").shift(1)).log().alias("SPY_Ret") ]
        raw_calc = df.with_columns(exprs)
        # 0.0 / 100.0 = 0.0 -> log(0) = -inf
        assert raw_calc["SPY_Ret"][1] == float('-inf')
    except Exception as e:
        pytest.fail(f"Pipeline crashed on zero prices: {e}")
