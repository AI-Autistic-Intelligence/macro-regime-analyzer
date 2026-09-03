import logging

logger = logging.getLogger(__name__)

class FeastFeatureStoreMock:
    """
    Mock implementation of a Feature Store interface (like Feast).
    In a real-world scenario, this module would connect to Feast's Registry 
    to retrieve pre-computed historical features from DuckDB (Offline Store)
    and low-latency online features from Redis (Online Store).
    """
    def __init__(self, repo_path: str = "./feature_repo"):
        self.repo_path = repo_path
        logger.info(f"Initialized Feature Store connection at {repo_path}")
        
    def get_online_features(self, entity_keys: list, feature_refs: list) -> dict:
        """
        Retrieves low-latency features for live inference.
        """
        logger.info(f"Fetching online features for {entity_keys}...")
        # Mocking the response that Feast would return
        return {
            "entity_id": entity_keys,
            "SP500_Close": [4500.0],
            "Volatility_21d": [0.12]
        }
