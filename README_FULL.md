# AI-Driven Crypto Trading Platform

## Overview

A production-ready, modular AI-driven cryptocurrency trading platform with a complete web dashboard, backend API, and continuous machine learning pipeline. This system enables traders to view live market data, train prediction models, generate trading signals, run backtesting simulations, execute paper trading, and optionally execute real trades via exchange APIs.

## Key Features

### 📊 Data Pipeline
- Real-time OHLCV data fetching from Binance
- Secondary data source integration (CoinGecko)
- Historical data storage and validation
- Automatic periodic data updates
- Data cleaning and normalization

### 🧠 Machine Learning
- Multiple ML models: Gradient Boosting, XGBoost, Ensemble, LSTM
- Automated feature engineering (RSI, EMA, SMA, MACD, Bollinger Bands, ATR)
- Model versioning and registry
- Continuous learning with scheduled retraining
- Performance tracking and evaluation

### 💰 Trading Capabilities
- Paper trading (default, risk-free)
- Live trading mode (optional with Binance credentials)
- Position sizing and risk management
- Order execution simulation
- Stop loss and take profit automation

### 📈 Backtesting Engine
- Realistic trade simulation
- Equity curve visualization
- Performance metrics: Sharpe ratio, win rate, drawdown, total return
- Strategy testing with historical data

### 🛡️ Risk Management
- Maximum position size limits
- Daily loss limits
- Volatility filters
- Risk per trade controls

### 🖥️ Dashboard
- Modern dark theme interface
- Real-time market data visualization
- Model training interface
- Backtesting results visualization
- Trading signals and positions
- System logs and monitoring
- Full configuration management via GUI

## Technology Stack

- **Backend**: Python, FastAPI
- **Data Processing**: Pandas, NumPy, SciPy
- **Machine Learning**: Scikit-learn, XGBoost, PyTorch LSTM
- **APIs**: Binance public API, CoinGecko API
- **Trading Integration**: CCXT
- **Visualization**: Plotly
- **Task Scheduling**: APScheduler
- **Database**: SQLite/PostgreSQL
- **Frontend**: Streamlit

## Project Structure

```
crypto-trading-platform/
├── backend/
│   ├── config.py              # Configuration management
│   ├── logger.py              # Logging system
│   ├── api.py                 # FastAPI endpoints
│   ├── utils.py               # Utility functions
│   ├── data/
│   │   ├── fetcher.py         # Data fetching
│   │   ├── processor.py       # Data processing
│   │   └── storage.py         # Data storage
│   ├── models/
│   │   ├── trainer.py         # Model training
│   │   ├── predictor.py       # Predictions
│   │   └── registry.py        # Model versioning
│   ├── trading/
│   │   ├── engine.py          # Trading engine
│   │   ├── risk_manager.py    # Risk management
│   │   └── order_executor.py  # Order execution
│   └── backtesting/
│       └── simulator.py       # Backtesting
├── dashboard/
│   ├── app.py                 # Main Streamlit app
│   ├── pages/
│   │   ├── 01_Overview.py
│   │   ├── 02_Market_Data.py
│   │   ├── 03_Model_Training.py
│   │   ├── 04_Trading_Signals.py
│   │   ├── 05_Backtesting.py
│   │   ├── 06_Trading_Panel.py
│   │   ├── 07_Settings.py
│   │   └── 08_Logs.py
│   └── components/
│       ├── charts.py
│       ├── forms.py
│       └── utils.py
├── config/
│   └── default.yaml           # Default config
├── data/
│   ├── historical/            # Historical OHLCV data
│   ├── models/                # Trained models
│   ├── logs/                  # System logs
│   └── backtest_results/      # Backtest results
├── requirements.txt
├── .env.example
└── README.md
```

## Installation

### Prerequisites
- Python 3.10+
- pip or conda
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jai-fire/AI.git
   cd AI
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Binance API keys (optional for paper trading)
   ```

## Usage

### Running the Dashboard

```bash
streamlit run dashboard/app.py
```

Access the dashboard at `http://localhost:8501`

### Running the Backend API

```bash
cd backend
uvicorn api:app --reload
```

API documentation: `http://localhost:8000/docs`

## Configuration

Edit configuration via GUI in the Settings page or manually edit `config/user_config.yaml`:

```yaml
binance:
  api_key: ""
  api_secret: ""
  testnet: true
  enabled: true

model:
  model_type: "gradient_boosting"
  test_size: 0.2
  n_estimators: 100
  use_lstm: false

trading:
  paper_trading: true
  position_size: 0.1
  max_daily_loss: 0.05
  stop_loss_percent: 2.0
  take_profit_percent: 5.0

data:
  pairs:
    - BTCUSDT
    - ETHUSDT
  timeframe: "1h"
  lookback_days: 90
```

## Dashboard Pages

### Overview
- System status
- Portfolio summary
- Key metrics
- Recent trades

### Market Data
- Live price charts
- Technical indicators
- Market analysis

### Model Training
- Training controls
- Model selection
- Training logs
- Performance metrics

### Trading Signals
- Live predictions
- Signal strength
- Confidence levels
- Trading recommendations

### Backtesting
- Strategy testing
- Performance analysis
- Risk metrics
- Equity curves

### Trading Panel
- Active positions
- Order history
- Manual order entry
- Position management

### Settings
- System configuration
- API credentials
- Model parameters
- Risk settings

### Logs
- System events
- Trading logs
- Model training logs
- Error tracking

## API Endpoints

- `GET /api/market/prices` - Current prices
- `GET /api/market/ohlcv/{symbol}` - OHLCV data
- `POST /api/models/train` - Train model
- `GET /api/models/predict/{symbol}` - Get prediction
- `POST /api/trading/backtest` - Run backtest
- `GET /api/trading/positions` - Get positions
- `POST /api/trading/execute` - Execute trade
- `GET /api/config` - Get configuration
- `PUT /api/config` - Update configuration

## Risk Management

The platform implements multiple safeguards:

1. **Position Sizing**: Limits position size to configured percentage
2. **Daily Loss Limit**: Stops trading if daily loss exceeds threshold
3. **Volatility Filter**: Avoids trading during extreme volatility
4. **Stop Loss/Take Profit**: Automatic exit levels
5. **Risk Per Trade**: Configurable risk amount per trade

## Security Considerations

- Single-user mode (no authentication needed)
- Store API keys in `.env` file (never commit to Git)
- Use testnet for initial testing
- Paper trading mode is default (risk-free)
- All trades can be manually verified before execution

## Performance Metrics

The system tracks:
- Win rate
- Profit factor
- Sharpe ratio
- Maximum drawdown
- Average trade duration
- Return on investment

## Troubleshooting

### No data showing in charts
- Check internet connection
- Verify Binance API accessibility
- Check logs for errors

### Model training fails
- Ensure sufficient historical data
- Check for missing values
- Verify model parameters

### Trades not executing
- Verify paper trading is enabled
- Check position size settings
- Review risk management rules

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black backend/
flake8 backend/
```

## Future Enhancements

- Advanced neural networks (Transformers)
- Multi-exchange support
- Advanced portfolio optimization
- Real-time alerts
- Mobile app
- REST API authentication
- Database migration to PostgreSQL

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create a Pull Request

## Support

For issues and feature requests, please create an GitHub issue.

## Disclaimer

This project is for educational purposes. Cryptocurrency trading involves substantial risk of loss. Past performance does not guarantee future results. Always conduct thorough research and consider consulting with financial advisors before trading.
