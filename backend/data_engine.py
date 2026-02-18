import pandas as pd
import numpy as np
import ccxt
import time
from datetime import datetime
import logging
from .config import Config

logger = logging.getLogger(__name__)

class DataEngine:
    """Engine for fetching and preprocessing market data."""
    
    def __init__(self, config: Config):
        self.config = config
        self.exchange = self._init_exchange()
        
    def _init_exchange(self):
        """Initialize the CCXT exchange based on config."""
        exchange_class = getattr(ccxt, self.config.trading.exchange_id)
        params = {
            'apiKey': self.config.trading.api_key,
            'secret': self.config.trading.api_secret,
            'enableRateLimit': True,
        }
        if self.config.trading.testnet:
            params['options'] = {'defaultType': 'future'} 
            
        exchange = exchange_class(params)
        if self.config.trading.testnet and hasattr(exchange, 'set_sandbox_mode'):
            exchange.set_sandbox_mode(True)
        return exchange

    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 1000):
        """Fetch historical OHLCV data."""
        try:
            logger.info(f"Fetching {limit} candles for {symbol} on {timeframe}")
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None

    def add_technical_indicators(self, df: pd.DataFrame):
        """Add basic technical indicators to the dataframe."""
        if df is None or df.empty:
            return df
            
        # Simple Moving Averages
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()
        
        # Volatility (Bollinger Bands)
        df['std'] = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['sma_20'] + (df['std'] * 2)
        df['bb_lower'] = df['sma_20'] - (df['std'] * 2)
        
        return df.dropna()

    def get_realtime_price(self, symbol: str):
        """Fetch current ticker price."""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            logger.error(f"Error fetching realtime price: {e}")
            return None
