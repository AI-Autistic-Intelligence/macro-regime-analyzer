from src.tasks.celery_app import retrain_lstm_model


def test_retrain_lstm_model():
    # Since we are mocking the task, it should just run synchronously and return success
    result = retrain_lstm_model()
    
    assert "status" in result
    assert result["status"] == "success"
    assert "new_accuracy" in result
    assert result["new_accuracy"] > 0.8
