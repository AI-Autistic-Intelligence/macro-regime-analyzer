import logging

import numpy as np
import shap
import torch

logger = logging.getLogger(__name__)

class RegimeExplainer:
    """
    Explainable AI (XAI) module using SHAP values.
    Provides feature importance for Deep Learning models.
    """
    def __init__(self, model, background_data: np.ndarray):
        """
        Initializes the SHAP DeepExplainer.
        model: the PyTorch model
        background_data: A representative sample of training data to form the baseline
        """
        self.model = model
        self.model.eval()
        # We need a tensor for the background
        bg_tensor = torch.tensor(background_data, dtype=torch.float32)
        
        # DeepExplainer is optimized for neural networks
        self.explainer = shap.DeepExplainer(self.model, bg_tensor)
        logger.info("SHAP DeepExplainer initialized.")
        
    def explain_prediction(self, features: np.ndarray) -> dict:
        """
        Calculates SHAP values for a given instance to explain 'why' the model 
        predicted a specific regime.
        """
        if len(features.shape) == 1:
            features = features.reshape(1, 1, -1)
        elif len(features.shape) == 2:
            features = np.expand_dims(features, axis=0)
            
        x_tensor = torch.tensor(features, dtype=torch.float32)
        
        # Calculate SHAP values
        # shap_values is a list of arrays (one for each class/regime)
        shap_values = self.explainer.shap_values(x_tensor)
        
        # Format the output for the API (extracting the values for the most likely class)
        with torch.no_grad():
            probs = self.model(x_tensor).numpy()[0]
        predicted_class = int(np.argmax(probs))
        
        # shap_values[predicted_class] has shape (1, seq_len, num_features) in older SHAP
        # In newer SHAP, it's an array of shape (batch, seq_len, num_features, num_classes)
        if isinstance(shap_values, list):
            importance = shap_values[predicted_class][0, -1, :].tolist()
        else:
            importance = shap_values[0, -1, :, predicted_class].tolist()
        return {
            "predicted_regime": predicted_class,
            "feature_importance": {
                "Returns": importance[0],
                "Volatility_21d": importance[1],
                "Momentum_63d": importance[2],
                "Volume_Trend": importance[3] if len(importance) > 3 else 0.0
            }
        }
