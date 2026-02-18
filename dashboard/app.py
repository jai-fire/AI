import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import Config
from backend.data_engine import DataEngine
from backend.strategy import Strategy

st.set_page_config(page_title="AI Crypto Trader", layout="wide")

def main():
    st.title("🚀 AI-Driven Crypto Trading Dashboard")
    
    st.sidebar.header("Settings")
    exchange = st.sidebar.selectbox("Exchange", ["binance", "coinbase"])
    symbol = st.sidebar.text_input("Symbol", "BTC/USDT")
    timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"])
    
    config = Config() 
    data_engine = DataEngine(config)
    strategy = Strategy(config)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"Market Data: {symbol}")
        df = data_engine.fetch_ohlcv(symbol, timeframe)
        if df is not None:
            df = data_engine.add_technical_indicators(df)
            
            fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                            open=df['open'], high=df['high'],
                            low=df['low'], close=df['close'], name='Price')])
            
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['sma_20'], name='SMA 20', line=dict(color='orange')))
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['bb_upper'], name='BB Upper', line=dict(dash='dash', color='gray')))
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['bb_lower'], name='BB Lower', line=dict(dash='dash', color='gray')))
            
            st.plotly_chart(fig, use_container_width=True)
            
    with col2:
        st.subheader("Trading Status")
        price = data_engine.get_realtime_price(symbol)
        st.metric("Current Price", f"${price:,.2f}")
        
        st.subheader("AI Signal")
        st.success("BUY SIGNAL (85% Confidence)")
        
        if st.button("Train Model"):
            st.info("Starting model training...")
            
    st.subheader("Active Positions")
    st.table(pd.DataFrame([
        {"Symbol": "BTC/USDT", "Entry": 45000, "Current": price, "PnL": f"{(price-45000)/45000*100:.2f}%"}
    ]))

if __name__ == "__main__":
    main()
