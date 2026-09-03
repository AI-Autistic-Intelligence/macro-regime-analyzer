import logging
import os

import yaml
from src.api.fred_client import FredClient
from src.api.yfinance_client import YFinanceClient
from src.features.engineering import FeatureEngineer
from src.models.regime_detector import RegimeDetector
from src.preprocessing.data_merger import DataMerger
from src.utils.validator import DataValidator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MainPipeline")

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    logger.info("Starting MacroRegime Analyzer (Senior Edition)")
    config = load_config()
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. Fetch Data
    start_date = config['data']['start_date']
    symbols = config['data']['market_symbols']
    macro_series = config['data']['macro_series']
    
    logger.info("Fetching market data...")
    market_df = YFinanceClient.fetch_data(symbols, start_date=start_date)
    
    logger.info("Fetching macro data...")
    macro_df = FredClient.fetch_data(macro_series, start_date=start_date)
    
    # 2. Preprocess & Merge
    merged_df = DataMerger.merge_and_align(market_df, macro_df)
    
    # 3. Feature Engineering
    features_df = FeatureEngineer.create_features(merged_df, asset_columns=symbols)
    
    # Define features used for model
    feature_cols = macro_series + [f"{sym}_Vol_21d" for sym in symbols] + [f"{sym}_Mom_63d" for sym in symbols]
    features_df.dropna(subset=feature_cols, inplace=True)
    
    # 4. Data Validation (Sanity Checks)
    DataValidator.validate_features(features_df, feature_cols)
    
    # 5. Out-of-sample Rolling Regime Detection
    model_cfg = config['model']
    detector = RegimeDetector(
        max_components=model_cfg['max_components'],
        rolling_window=model_cfg['rolling_window_days'],
        n_init=model_cfg['n_init'],
        random_state=model_cfg['random_state']
    )
    final_df = detector.fit_predict_rolling(features_df, feature_columns=feature_cols)
    
    # 6. Save Output (Database or Parquet would be better for huge datasets, CSV fine for this size)
    output_path = os.path.join(data_dir, 'processed_regimes.csv')
    final_df.to_csv(output_path)
    logger.info(f"Pipeline completed successfully. Data saved to {output_path}")

if __name__ == "__main__":
    main()
