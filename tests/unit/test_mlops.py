from src.models.tracker import ExperimentTracker


def test_experiment_tracker_init(monkeypatch):
    # Mock mlflow to avoid actually connecting to a server in CI
    class MockMLflow:
        def set_tracking_uri(self, uri): pass
        def get_experiment_by_name(self, name): return None
        def create_experiment(self, name): return "1"
        def set_experiment(self, name): pass
        
    monkeypatch.setattr("src.models.tracker.mlflow", MockMLflow())
    
    tracker = ExperimentTracker("Test_Experiment")
    assert tracker.experiment_id == "1"
