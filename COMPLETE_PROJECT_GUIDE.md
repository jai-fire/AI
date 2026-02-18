# COMPLETE AI CRYPTO TRADING PLATFORM - PROJECT SETUP GUIDE

This guide contains all the code files needed to build the complete trading platform.

## Quick Setup Instructions

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install: `pip install -r requirements.txt`
5. Run dashboard: `streamlit run dashboard/app.py`

## FILE STRUCTURE TO CREATE

### 1. backend/logger.py
```python
"""Structured logging system."""
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_data)

def setup_logger(name, config):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.logging.level))
    log_dir = Path(config.logging.log_dir)
    log_dir.mkdir(exist_ok=True, parents=True)
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / f"{name}.log",
        maxBytes=config.logging.max_file_size,
        backupCount=config.logging.backup_count
    )
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    return logger
```

### 2. backend/utils.py
```python
"""Utility functions for the trading platform."""
import numpy as np
import pandas as pd
from typing import Dict, List
from datetime import datetime, timedelta

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate technical indicators."""
    df = df.copy()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # EMA
    df['ema_12'] = df['close'].ewm(span=12).mean()
    df['ema_26'] = df['close'].ewm(span=26).mean()
    
    # SMA
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    
    # MACD
    macd = df['ema_12'] - df['ema_26']
    signal = macd.ewm(span=9).mean()
    df['macd'] = macd
    df['macd_signal'] = signal
    df['macd_hist'] = macd - signal
    
    # Bollinger Bands
    bb_mid = df['close'].rolling(window=20).mean()
    bb_std = df['close'].rolling(window=20).std()
    df['bb_upper'] = bb_mid + (bb_std * 2)
    df['bb_lower'] = bb_mid - (bb_std * 2)
    df['bb_mid'] = bb_mid
    
    # ATR
    df['tr1'] = df['high'] - df['low']
    df['tr2'] = abs(df['high'] - df['close'].shift())
    df['tr3'] = abs(df['low'] - df['close'].shift())
    df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
    df['atr'] = df['tr'].rolling(window=14).mean()
    
    # Momentum
    df['momentum'] = df['close'] - df['close'].shift(10)
    
    df = df.drop(['tr1', 'tr2', 'tr3', 'tr'], axis=1)
    return df

def prepare_ml_data(df: pd.DataFrame, target_window: int = 5) -> tuple:
    """Prepare data for ML models."""
    df = calculate_indicators(df)
    df = df.dropna()
    
    # Create target: 1 if price goes up, 0 if down
    df['target'] = (df['close'].shift(-target_window) > df['close']).astype(int)
    
    feature_cols = ['rsi', 'ema_12', 'ema_26', 'sma_20', 'sma_50',
                   'macd', 'macd_signal', 'bb_upper', 'bb_lower',
                   'atr', 'momentum', 'volume']
    
    X = df[feature_cols].fillna(0)
    y = df['target']
    
    return X, y, df

def calculate_performance_metrics(trades: List[Dict]) -> Dict:
    """Calculate trading performance metrics."""
    if not trades:
        return {}
    
    returns = [t['pnl'] for t in trades]
    winning_trades = [t for t in trades if t['pnl'] > 0]
    losing_trades = [t for t in trades if t['pnl'] < 0]
    
    total_return = sum(returns)
    avg_return = np.mean(returns)
    win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
    profit_factor = sum([t['pnl'] for t in winning_trades]) / abs(sum([t['pnl'] for t in losing_trades])) if losing_trades else 0
    
    return {
        'total_return': total_return,
        'avg_return': avg_return,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'total_trades': len(trades),
        'winning_trades': len(winning_trades),
        'losing_trades': len(losing_trades),
    }
```

### 3. backend/data/fetcher.py
```python
"""Data fetching from exchanges."""
import ccxt
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class BinanceFetcher:
    def __init__(self, testnet: bool = True):
        if testnet:
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
                'urls': {'api': {'public': 'https://testnet.binance.vision/api'}}
            })
        else:
            self.exchange = ccxt.binance({'enableRateLimit': True})
    
    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 500) -> pd.DataFrame:
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['symbol'] = symbol
            return df
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return pd.DataFrame()
    
    def fetch_multiple(self, symbols: List[str], timeframe: str = '1h', limit: int = 500) -> Dict[str, pd.DataFrame]:
        data = {}
        for symbol in symbols:
            data[symbol] = self.fetch_ohlcv(symbol, timeframe, limit)
        return data

class CoinGeckoFetcher:
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def fetch_current_price(self, coin_id: str) -> Optional[float]:
        try:
            url = f"{self.BASE_URL}/simple/price"
            params = {'ids': coin_id, 'vs_currencies': 'usd'}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return data.get(coin_id, {}).get('usd')
        except Exception as e:
            logger.error(f"Error fetching price for {coin_id}: {e}")
            return None
```

### 4. backend/data/__init__.py
```python
"""Data module."""
```

### 5. backend/models/__init__.py
```python
"""Models module."""
```

### 6. backend/trading/__init__.py
```python
"""Trading module."""
```

### 7. backend/backtesting/__init__.py
```python
"""Backtesting module."""
```

### 8. .env.example
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=true
```

## NEXT STEPS

After creating these files:

1. Create remaining modules (models/trainer.py, models/predictor.py, trading/engine.py, backtesting/simulator.py)
2. Create FastAPI app (backend/api.py)
3. Create Streamlit dashboard (dashboard/app.py and pages/)
4. Create data directories
5. Test the system

See README_FULL.md for complete documentation.
