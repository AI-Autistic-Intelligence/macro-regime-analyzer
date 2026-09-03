import logging
import os

import mlflow

logger = logging.getLogger(__name__)

class ExperimentTracker:
    """
    MLOps Experiment Tracking using MLflow.
    """
    def __init__(self, experiment_name: str = "Macro_Regime_Detection"):
        self.mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
        mlflow.set_tracking_uri(self.mlflow_uri)
        
        # Set or create the experiment
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            self.experiment_id = mlflow.create_experiment(experiment_name)
        else:
            self.experiment_id = experiment.experiment_id
            
        mlflow.set_experiment(experiment_name)
        logger.info(f"MLflow Tracker initialized at {self.mlflow_uri} for experiment {experiment_name}")

    def log_model_metrics(self, model_type: str, metrics: dict, params: dict = None):
        """
        Logs hyperparameters and evaluation metrics for a specific model run.
        """
        with mlflow.start_run(run_name=f"{model_type}_training"):
            if params:
                mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            logger.info(f"Logged {model_type} metrics to MLflow.")
