from src.features.feature_store import FeastFeatureStoreMock


def test_feast_store_mock():
    store = FeastFeatureStoreMock()
    features = store.get_online_features(["user_1"], ["SP500_Close"])
    
    assert "entity_id" in features
    assert features["entity_id"] == ["user_1"]
    assert "SP500_Close" in features
