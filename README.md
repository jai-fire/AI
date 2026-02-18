# AI-Driven Crypto Trading Platform 🚀

A production-ready, modular AI trading system with a modern dashboard, cross-platform support (Windows & Linux), and machine learning pipeline.

## 🌟 Key Features

*   **Real-time Data**: Multi-source fetching from Binance & CoinGecko.
*   **AI Engine**: XGBoost, Gradient Boosting, and Ensemble models.
*   **Advanced Indicators**: RSI, MACD, Bollinger Bands, ATR, etc.
*   **Simulation**: Paper trading & realistic backtesting engine.
*   **Modern UI**: Streamlit dark-theme dashboard with interactive Plotly charts.
*   **Cross-Platform**: Fully tested on Windows 10/11 and Ubuntu/Linux.

## 📁 Project Structure

```text
├── backend/            # Core logic & API
│   ├── data/           # Ingestion & Processing
│   ├── models/         # ML Pipeline
│   └── trading/        # Execution & Risk
├── dashboard/          # Streamlit UI
├── config/             # YAML configurations
└── data/               # Local storage (CSV, Models, Logs)
```

## 🚀 Quick Start (5 Minutes)

### 1. Clone & Setup
```bash
git clone https://github.com/jai-fire/AI.git && cd AI
python -m venv venv
# Linux: source venv/bin/activate | Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure
Copy `.env.example` to `.env` and add your Binance API keys (optional for paper trading).

### 3. Launch Platform
```bash
# Start the Dashboard
streamlit run dashboard/app.py
```

## 🛠 Platform Guide

1.  **Market Data**: View live price action and technical overlays.
2.  **Training**: Train models on historical data with one click.
3.  **Backtesting**: Validate your strategy before going live.
4.  **Trading**: Manage paper/live positions with automated risk controls.

## ⚖️ Disclaimer
Trading involves risk. This software is for educational purposes. Always use paper trading before live execution.
