import logging

logger = logging.getLogger(__name__)

try:
    # Try importing the compiled Rust extension
    from macro_rust_core import evaluate_tick_hft
    RUST_ENABLED = True
except ImportError:
    logger.warning("Rust extension 'macro_rust_core' not found. Falling back to Python implementation. Compile with `maturin develop` for HFT speeds.")
    RUST_ENABLED = False
    
    def evaluate_tick_hft(price: float, moving_avg: float, threshold: float) -> int:
        if price > moving_avg + threshold:
            return 1
        elif price < moving_avg - threshold:
            return -1
        else:
            return 0

class HFTEngine:
    """
    Epoch 18: High-Frequency Trading Engine.
    Uses Rust bindings for ultra-low latency evaluations.
    """
    def __init__(self, threshold: float = 0.005):
        self.threshold = threshold
        
    def process_tick(self, price: float, moving_avg: float) -> int:
        return evaluate_tick_hft(price, moving_avg, self.threshold)
