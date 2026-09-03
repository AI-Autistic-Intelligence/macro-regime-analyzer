import logging

import polars as pl

logger = logging.getLogger(__name__)

class PolarsFeaturePipeline:
    """High-performance feature engineering pipeline using Polars."""
    
    @staticmethod
    def process_features(df: pl.DataFrame, asset_columns: list[str]) -> pl.DataFrame:
        logger.info("Executing Polars Feature Pipeline...")
        
        # Stage 1: Returns
        ret_exprs = []
        for col in asset_columns:
            ret_col = f"{col}_Ret"
            ret_exprs.append(
                (pl.col(col) / pl.col(col).shift(1)).log().alias(ret_col)
            )
            
        df = df.with_columns(ret_exprs)
        
        # Stage 2: Volatility and Momentum
        adv_exprs = []
        for col in asset_columns:
            ret_col = f"{col}_Ret"
            adv_exprs.append(
                pl.col(ret_col).rolling_std(window_size=21).alias(f"{col}_Vol_21d")
            )
            adv_exprs.append(
                (pl.col(col) / pl.col(col).shift(63) - 1).alias(f"{col}_Mom_63d")
            )
            
        result = df.with_columns(adv_exprs).drop_nulls()
        
        logger.info(f"Feature engineering complete. Generated {len(ret_exprs) + len(adv_exprs)} features.")
        return result
