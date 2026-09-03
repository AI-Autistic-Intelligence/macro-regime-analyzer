import torch
import torch.nn as nn

class MacroTransformer(nn.Module):
    """
    Epoch 15: Transformer-based model for Macro Regime detection.
    Replaces or supplements the LSTM to capture longer-term attention weights.
    """
    def __init__(self, input_dim: int, num_classes: int, d_model: int = 64, nhead: int = 4, num_layers: int = 2):
        super().__init__()
        self.d_model = d_model
        
        # Linear layer to map input features to d_model dimensions
        self.embedding = nn.Linear(input_dim, d_model)
        
        # Positional Encoding could be added here, but for macro regimes 
        # sometimes raw sequences are sufficient if short, or we rely on the transformer
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, 
            nhead=nhead, 
            batch_first=True,
            dropout=0.1
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Output layer
        self.fc_out = nn.Linear(d_model, num_classes)
        
    def forward(self, x):
        # x shape: (batch, seq_len, input_dim)
        
        # Map to d_model: (batch, seq_len, d_model)
        emb = self.embedding(x)
        
        # Transformer pass
        out = self.transformer(emb)
        
        # Take the output of the last time step for classification
        last_out = out[:, -1, :]
        
        # Logits for classes
        logits = self.fc_out(last_out)
        return logits
