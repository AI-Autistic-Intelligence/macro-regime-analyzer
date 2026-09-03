import torch
from src.models.transformer_detector import MacroTransformer

def test_macro_transformer_output_shape():
    batch_size = 4
    seq_len = 10
    input_dim = 5
    num_classes = 3
    
    model = MacroTransformer(input_dim=input_dim, num_classes=num_classes)
    
    # Create dummy input tensor
    x = torch.randn(batch_size, seq_len, input_dim)
    
    # Forward pass
    logits = model(x)
    
    # Check shape
    assert logits.shape == (batch_size, num_classes)
