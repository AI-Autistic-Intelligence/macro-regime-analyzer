import logging
import mlflow

logger = logging.getLogger(__name__)

class ShadowModeEvaluator:
    """
    Epoch 17: Shadow Mode & CD
    Compares a newly trained model against the current production model.
    Promotes to production only if performance metrics (e.g., F1-score) are strictly better.
    """
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = mlflow.tracking.MlflowClient()
        
    def evaluate_and_promote(self, new_run_id: str, new_metric: float, prod_metric: float) -> bool:
        """
        :param new_run_id: The MLflow Run ID of the newly trained model
        :param new_metric: The performance score of the new model
        :param prod_metric: The performance score of the current production model
        :return: True if promoted, False otherwise
        """
        logger.info(f"Evaluating new model (Run: {new_run_id}) against Production")
        
        if new_metric > prod_metric:
            logger.info(f"New model outperforms Production ({new_metric} > {prod_metric}). Promoting!")
            # Register the model
            model_uri = f"runs:/{new_run_id}/model"
            mv = mlflow.register_model(model_uri, self.model_name)
            
            # Transition to Production
            self.client.transition_model_version_stage(
                name=self.model_name,
                version=mv.version,
                stage="Production",
                archive_existing_versions=True
            )
            return True
        else:
            logger.warning(f"New model is worse or equal ({new_metric} <= {prod_metric}). Discarding.")
            return False
