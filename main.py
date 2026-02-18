import time
import logging
from backend.config import Config
from backend.data_engine import DataEngine
from backend.strategy import Strategy
from backend.executor import ExecutionEngine
from backend.trainer import ModelTrainer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_trading_bot():
    """Main loop for the trading bot."""
    logger.info("Starting AI Trading Bot...")
    
    config = Config()
    data_engine = DataEngine(config)
    strategy = Strategy(config)
    executor = ExecutionEngine(config, data_engine.exchange)
    
    symbol = "BTC/USDT"
    
    while True:
        try:
            # 1. Fetch Data
            df = data_engine.fetch_ohlcv(symbol, timeframe='1h', limit=100)
            df = data_engine.add_technical_indicators(df)
            
            # 2. Generate Signals
            signals = strategy.generate_signals(df)
            latest_signal = signals['signal'].iloc[-1]
            
            # 3. Execute Trades
            if latest_signal != 0:
                price = df['close'].iloc[-1]
                amount = strategy.calculate_position_size(executor.paper_balance, price)
                executor.execute_trade(symbol, latest_signal, amount)
                
            logger.info(f"Loop finished. Current paper balance: {executor.paper_balance}")
            
            # Wait for next candle (or a set interval)
            time.sleep(60) # Run every minute for testing
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user.")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_trading_bot()
