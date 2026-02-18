"""Configuration management system."""
import os
import yaml
from pathlib import Path
from typing import Any, Dict
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

load_dotenv()


@dataclass
class BinanceConfig:
    """Binance API configuration."""
    api_key: str = ""
    api_secret: str = ""
    testnet: bool = True
    enabled: bool = True


@dataclass
class ModelConfig:
    """Machine learning model configuration."""
    model_type: str = "gradient_boosting"
    test_size: float = 0.2
    random_state: int = 42
    max_depth: int = 10
    learning_rate: float = 0.1
    n_estimators: int = 100
    use_lstm: bool = False
    lstm_units: int = 64
    lstm_lookback: int = 60


@dataclass
class TradingConfig:
    """Trading parameters."""
    paper_trading: bool = True
    position_size: float = 0.1
    max_daily_loss: float = 0.05
    stop_loss_percent: float = 2.0
    take_profit_percent: float = 5.0
    min_volatility: float = 0.5
    max_volatility: float = 5.0


@dataclass
class DataConfig:
    """Data collection configuration."""
    pairs: list = None
    timeframe: str = "1h"
    lookback_days: int = 90
    update_interval_minutes: int = 60
    cache_enabled: bool = True
    
    def __post_init__(self):
        if self.pairs is None:
            self.pairs = [
                "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT",
                "DOGEUSDT", "XRPUSDT", "SOLUSDT", "MATICUSDT"
            ]


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    log_dir: str = "data/logs"
    max_file_size: int = 10 * 1024 * 1024
    backup_count: int = 5


class Config:
    """Central configuration manager."""
    
    def __init__(self, config_file: str = "config/user_config.yaml"):
        self.config_file = Path(config_file)
        self.config_dir = self.config_file.parent
        self.config_dir.mkdir(exist_ok=True, parents=True)
        
        self.binance = BinanceConfig(
            api_key=os.getenv("BINANCE_API_KEY", ""),
            api_secret=os.getenv("BINANCE_API_SECRET", ""),
            testnet=os.getenv("BINANCE_TESTNET", "true").lower() == "true"
        )
        self.model = ModelConfig()
        self.trading = TradingConfig()
        self.data = DataConfig()
        self.logging = LoggingConfig()
        
        self.load()
    
    def load(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_file.exists():
            self.save()
            return
        
        try:
            with open(self.config_file, 'r') as f:
                config_data = yaml.safe_load(f) or {}
            
            if 'binance' in config_data:
                self.binance = BinanceConfig(**config_data['binance'])
            if 'model' in config_data:
                self.model = ModelConfig(**config_data['model'])
            if 'trading' in config_data:
                self.trading = TradingConfig(**config_data['trading'])
            if 'data' in config_data:
                self.data = DataConfig(**config_data['data'])
            if 'logging' in config_data:
                self.logging = LoggingConfig(**config_data['logging'])
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
    
    def save(self) -> None:
        """Save configuration to YAML file."""
        config_dict = {
            'binance': asdict(self.binance),
            'model': asdict(self.model),
            'trading': asdict(self.trading),
            'data': asdict(self.data),
            'logging': asdict(self.logging),
        }
        
        with open(self.config_file, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)
    
    def update(self, section: str, **kwargs) -> None:
        """Update specific config section."""
        if section == 'binance':
            for k, v in kwargs.items():
                setattr(self.binance, k, v)
        elif section == 'model':
            for k, v in kwargs.items():
                setattr(self.model, k, v)
        elif section == 'trading':
            for k, v in kwargs.items():
                setattr(self.trading, k, v)
        elif section == 'data':
            for k, v in kwargs.items():
                setattr(self.data, k, v)
        elif section == 'logging':
            for k, v in kwargs.items():
                setattr(self.logging, k, v)
        self.save()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'binance': asdict(self.binance),
            'model': asdict(self.model),
            'trading': asdict(self.trading),
            'data': asdict(self.data),
            'logging': asdict(self.logging),
        }


config = Config()
