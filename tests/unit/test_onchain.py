from src.ingestion.onchain import OnChainAnalyzer


def test_onchain_analyzer():
    analyzer = OnChainAnalyzer()
    
    gas_price = analyzer.get_current_gas_price()
    
    assert isinstance(gas_price, float)
    assert gas_price > 0.0
