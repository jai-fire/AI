import ccxt
import logging
from .config import Config

logger = logging.getLogger(__name__)

class ExecutionEngine:
    """Engine for executing trades (simulation or real)."""
    
    def __init__(self, config: Config, exchange: ccxt.Exchange):
        self.config = config
        self.exchange = exchange
        self.paper_balance = 10000.0 # Initial $10k for simulation
        self.positions = {} # symbol: amount
        
    def execute_trade(self, symbol: str, signal: int, amount: float):
        """Execute a trade based on signal."""
        if signal == 1: # Buy
            if self.config.trading.mode == 'live':
                return self._live_buy(symbol, amount)
            else:
                return self._simulate_buy(symbol, amount)
        elif signal == -1: # Sell
            if self.config.trading.mode == 'live':
                return self._live_sell(symbol, amount)
            else:
                return self._simulate_sell(symbol, amount)
        return None

    def _simulate_buy(self, symbol: str, amount: float):
        """Simulate a buy order."""
        price = self.exchange.fetch_ticker(symbol)['last']
        cost = amount * price
        if cost > self.paper_balance:
            logger.warning("Insufficient paper balance")
            return None
            
        self.paper_balance -= cost
        self.positions[symbol] = self.positions.get(symbol, 0) + amount
        logger.info(f"SIM BUY: {amount} {symbol} @ {price}. Balance: {self.paper_balance}")
        return {"id": "sim_buy", "symbol": symbol, "amount": amount, "price": price}

    def _simulate_sell(self, symbol: str, amount: float):
        """Simulate a sell order."""
        if symbol not in self.positions or self.positions[symbol] < amount:
            logger.warning("Insufficient position to sell")
            return None
            
        price = self.exchange.fetch_ticker(symbol)['last']
        gain = amount * price
        self.paper_balance += gain
        self.positions[symbol] -= amount
        logger.info(f"SIM SELL: {amount} {symbol} @ {price}. Balance: {self.paper_balance}")
        return {"id": "sim_sell", "symbol": symbol, "amount": amount, "price": price}

    def _live_buy(self, symbol: str, amount: float):
        """Place a live market buy order."""
        try:
            order = self.exchange.create_market_buy_order(symbol, amount)
            logger.info(f"LIVE BUY ORDER: {order['id']}")
            return order
        except Exception as e:
            logger.error(f"Live buy failed: {e}")
            return None

    def _live_sell(self, symbol: str, amount: float):
        """Place a live market sell order."""
        try:
            order = self.exchange.create_market_sell_order(symbol, amount)
            logger.info(f"LIVE SELL ORDER: {order['id']}")
            return order
        except Exception as e:
            logger.error(f"Live sell failed: {e}")
            return None
