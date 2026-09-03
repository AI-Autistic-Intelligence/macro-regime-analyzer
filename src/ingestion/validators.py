import logging

import pandera.polars as pa
import polars as pl

logger = logging.getLogger(__name__)

class IngestionSchema(pa.DataFrameModel):
    """
    Pandera Data Contract for incoming Kafka Market Ticks.
    Ensures that no corrupted data enters the machine learning pipeline.
    """
    Date: pa.Field(coerce=True) # Expected as string or date
    SP500_Close: pa.Field(ge=0.0, coerce=True, nullable=False)
    VIX_Close: pa.Field(ge=0.0, coerce=True, nullable=False)
    Interest_Rate: pa.Field(coerce=True, nullable=False)
    Inflation_Rate: pa.Field(coerce=True, nullable=False)
    GDP_Growth: pa.Field(coerce=True, nullable=False)
    
    class Config:
        strict = False # Allow extra columns (like index or raw metadata)
        coerce = True # Try to auto-cast types (e.g. string to float if possible)
        
def validate_tick(tick_dict: dict) -> pl.DataFrame:
    """
    Converts a raw dictionary tick to a Polars DataFrame and validates it against the Data Contract.
    Raises pa.errors.SchemaError if validation fails.
    """
    df = pl.DataFrame([tick_dict])
    validated_df = IngestionSchema.validate(df)
    return validated_df
