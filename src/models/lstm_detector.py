import numpy as np
import torch
from torch import nn


class LSTMRegimeModel(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64, num_layers: int = 2, num_regimes: int = 3):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, num_regimes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        # x shape: (batch, sequence_length, features)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        
        out, (_hn, _cn) = self.lstm(x, (h0.detach(), c0.detach()))
        
        # We just want the output of the last time step
        out = self.fc(out[:, -1, :])
        return self.softmax(out)

class LSTMDetector:
    def __init__(self, input_dim: int = 4):
        self.model = LSTMRegimeModel(input_dim=input_dim)
        self.model.eval() # Set to evaluation mode for inference

    def predict_regime(self, features: np.ndarray) -> dict:
        """
        Features should be a 1D array or 2D array representing a single sequence.
        For demonstration, we wrap it into the required shape (1, seq_len, features)
        """
        if len(features.shape) == 1:
            # Fake sequence length of 1 if only single step passed
            features = features.reshape(1, 1, -1)
        elif len(features.shape) == 2:
            features = np.expand_dims(features, axis=0)
            
        with torch.no_grad():
            x_tensor = torch.tensor(features, dtype=torch.float32)
            probs = self.model(x_tensor).numpy()[0]
            
        return {
            "regime": int(np.argmax(probs)),
            "probabilities": probs.tolist(),
            "model_type": "LSTM"
        }
