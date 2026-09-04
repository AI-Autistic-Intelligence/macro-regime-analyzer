from src.core.hft_engine import HFTEngine


def test_hft_engine():
    engine = HFTEngine(threshold=10.0)
    
    # Test Long signal
    assert engine.process_tick(price=40020.0, moving_avg=40000.0) == 1
    
    # Test Short signal
    assert engine.process_tick(price=39980.0, moving_avg=40000.0) == -1
    
    # Test Hold signal
    assert engine.process_tick(price=40005.0, moving_avg=40000.0) == 0
