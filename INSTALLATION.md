# Installation Guide - AI Crypto Trading Platform

## System Requirements

- Python 3.10 or higher
- pip (Python package manager)
- Git
- 4GB RAM minimum
- 2GB disk space minimum

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/jai-fire/AI.git
cd AI
```

### 2. Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Create Data Directories

```bash
mkdir -p data/historical data/models data/logs data/backtest_results
mkdir -p config
```

### 6. Run the Application

**Dashboard:**
```bash
streamlit run dashboard/app.py
```

Access at: `http://localhost:8501`

**Backend API (Optional):**
```bash
cd backend
uvicorn api:app --reload
```

API docs: `http://localhost:8000/docs`

## Initial Configuration

1. Open dashboard at `http://localhost:8501`
2. Go to Settings page
3. Configure:
   - Binance API (optional, for live trading)
   - Trading parameters
   - Model preferences
   - Data sources

## Troubleshooting

### Module Not Found
```bash
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Change port for Streamlit
streamlit run dashboard/app.py --server.port 8502
```

### Binance Connection Issues
- Verify API keys
- Check internet connection
- Ensure testnet is enabled (default)

### Data Not Loading
- Check internet connection
- Verify Binance API status
- Check firewall settings

## Next Steps

1. Read README_FULL.md for detailed documentation
2. Explore the COMPLETE_PROJECT_GUIDE.md for code structure
3. Start with paper trading (default safe mode)
4. Test with historical data first
5. Monitor trading performance

## Support

For issues:
1. Check GitHub Issues
2. Review logs in `data/logs/`
3. Create new issue with details
