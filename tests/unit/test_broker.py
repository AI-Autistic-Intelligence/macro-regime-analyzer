import pytest
from src.trading.broker import BrokerClient

def test_broker_execution():
    broker = BrokerClient(testnet=True)
    
    # Initial state should be no position
    assert broker.current_position is None
    
    # Execute a Buy signal (Regime 1)
    executed = broker.execute_regime_signal("BTC/USDT", regime=1)
    assert executed is True
    assert broker.current_position == "LONG"
    
    # Execute another Buy signal (Regime 1), should not trade again
    executed = broker.execute_regime_signal("BTC/USDT", regime=1)
    assert executed is False
    assert broker.current_position == "LONG"
    
    # Execute a Sell signal (Regime 0)
    executed = broker.execute_regime_signal("BTC/USDT", regime=0)
    assert executed is True
    assert broker.current_position == "SHORT"
