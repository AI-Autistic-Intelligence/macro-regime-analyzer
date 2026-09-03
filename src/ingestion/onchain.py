import logging

logger = logging.getLogger(__name__)

try:
    from web3 import Web3
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False

class OnChainAnalyzer:
    """
    Epoch 22: Blockchain Integrations
    Fetches on-chain metrics (e.g., Ethereum gas prices, block data) to act as additional macro features.
    """
    def __init__(self, rpc_url: str = "https://cloudflare-eth.com"):
        if not WEB3_AVAILABLE:
            logger.warning("web3 not installed. Running in mock mode.")
            self.w3 = None
        else:
            self.w3 = Web3(Web3.HTTPProvider(rpc_url))
            if not self.w3.is_connected():
                logger.error("Failed to connect to Ethereum RPC node.")
                self.w3 = None
            else:
                logger.info("Successfully connected to Ethereum RPC node.")
                
    def get_current_gas_price(self) -> float:
        """
        Returns the current gas price in Gwei.
        High gas prices might indicate network congestion / risk-on behavior in DeFi.
        """
        if self.w3 is None:
            # Mock mode
            return 25.0
            
        try:
            gas_price_wei = self.w3.eth.gas_price
            gas_price_gwei = float(gas_price_wei) / 10**9
            return gas_price_gwei
        except Exception as e:
            logger.error(f"Failed to fetch gas price: {e}")
            return 0.0
