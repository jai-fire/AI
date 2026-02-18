# Quick Start - 5 Minutes to Running

## One-Command Setup

```bash
# Clone and setup
git clone https://github.com/jai-fire/AI.git && cd AI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## What You Get

✅ Real-time crypto market data
✅ AI-powered price predictions
✅ Backtesting engine
✅ Paper trading (safe, no real money)
✅ Risk management system
✅ Modern dark-themed dashboard

## First Steps

1. **Access Dashboard**: Open `http://localhost:8501`

2. **View Market Data** (Market Data page)
   - See live price charts
   - Technical indicators
   - 8 major crypto pairs included

3. **Train Model** (Model Training page)
   - Click "Start Training"
   - Wait 2-5 minutes
   - See performance metrics

4. **Run Backtest** (Backtesting page)
   - Choose trading pairs
   - Set time period
   - View results with equity curve

5. **Paper Trading** (Trading Panel page)
   - Completely risk-free
   - Real signals from your model
   - Track P&L

## Default Pairs Included

- Bitcoin (BTCUSDT)
- Ethereum (ETHUSDT)
- Binance Coin (BNBUSDT)
- Cardano (ADAUSDT)
- Dogecoin (DOGEUSDT)
- XRP (XRPUSDT)
- Solana (SOLUSDT)
- Polygon (MATICUSDT)

## Configuration (Optional)

**Add Binance API for Live Trading:**
1. Create API keys at https://www.binance.com/en/account/api-management
2. Edit `.env` file with your keys
3. Set `BINANCE_TESTNET=false` for paper trading

**Model Settings:**
Edit via Settings page in dashboard
- Change algorithms
- Adjust parameters
- Select features

## Useful Commands

```bash
# Check system status
streamlit run dashboard/app.py

# View logs
tail -f data/logs/*.log

# Restart fresh
rm data/backtest_results/* data/models/*
```

## Common Issues

**"Port 8501 already in use"**
```bash
streamlit run dashboard/app.py --server.port 8502
```

**"No data showing"**
- Check internet connection
- Wait 30 seconds for data to load
- Check logs: `data/logs/system.log`

**"Model training failed"**
- Ensure you have 90+ days of data
- Check Model Training logs
- Verify feature calculation

## Next: Deep Dive

- Read `README_FULL.md` for complete features
- See `COMPLETE_PROJECT_GUIDE.md` for code structure
- Check `INSTALLATION.md` for advanced setup
- Review `backend/` for API documentation

## Trading Strategy Tips

1. **Start with defaults** - Pre-configured for safety
2. **Use paper trading** - Test without real money
3. **Review backtest results** - Understand strategy
4. **Monitor live signals** - Check Trading Signals page
5. **Adjust parameters gradually** - Don't change everything at once

## Risk Warnings

⚠️ **Cryptocurrency trading is risky**
- Past performance ≠ future results
- Start with small amounts
- Never risk money you can't afford to lose
- Always use stop losses
- Monitor positions regularly

## Support

- 📖 Documentation: See README files
- 🐛 Issues: GitHub Issues
- 📧 Logs: `data/logs/` directory

Enjoy trading! 🚀
