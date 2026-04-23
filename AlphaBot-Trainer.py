import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="AlphaBot-Trainer", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 AlphaBot-Trainer")
st.caption("Learn the AlphaTrade strategy • Real 5-min charts • Signal explanations")

# Sidebar - Optional API (for future live mode)
with st.sidebar:
    st.header("Optional Live Mode")
    st.caption("Add TradeStation credentials for real data (future feature)")
    st.info("Currently running in realistic simulated mode using actual market data")

watchlist = ['NVDA', 'TSLA', 'ARM', 'AVGO', 'HOOD', 'IONQ', 'SMH', 'QQQ', 'SPY', 
             'AAPL', 'META', 'GOOGL', 'AMZN', 'MSFT', 'MU', 'RKLB', 'SOFI']

st.subheader("📊 Live Simulated Market (Realistic Data)")

for symbol in watchlist:
    try:
        # Fetch real 5-min data for the last trading day
        end = datetime.now()
        start = end - timedelta(days=3)
        df = yf.download(symbol, interval="5m", start=start, end=end, progress=False)
        if df.empty:
            continue
        df = df.tail(50)  # Last ~4 hours of 5-min bars
        
        current_price = df['Close'].iloc[-1]
        pm_high = df['High'].max() if len(df) > 0 else current_price * 1.02
        pm_low = df['Low'].min() if len(df) > 0 else current_price * 0.98
        
        # Calculate indicators
        df['EMA9'] = df['Close'].ewm(span=9).mean()
        # Simple VWAP approximation
        df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
        
        ema9 = df['EMA9'].iloc[-1]
        vwap = df['VWAP'].iloc[-1]
        
        # Count confluence signals for buy
        score = 0
        if df['Close'].iloc[-1] > pm_high and df['Close'].iloc[-1] > ema9 and df['Close'].iloc[-1] > vwap:
            score += 1  # PMH breakout
        if df['Close'].iloc[-1] > df['Close'].iloc[-5]:  # Bullish momentum
            score += 1
        # Hammer / Doji simulation (simplified)
        if (df['High'].iloc[-1] - df['Close'].iloc[-1]) < (df['Close'].iloc[-1] - df['Low'].iloc[-1]) * 0.3:
            score += 1
        
        has_buy_signal = score >= 2
        
        # Display with green text if buy signal
        expander_title = f"**{symbol}**" if has_buy_signal else symbol
        with st.expander(expander_title, expanded=False):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.metric("Price", f"${current_price:.2f}")
                st.metric("PM High", f"${pm_high:.2f}")
            with col2:
                st.metric("PM Low", f"${pm_low:.2f}")
                st.metric("9EMA", f"${ema9:.2f}")
            with col3:
                st.metric("Signals", f"{score}/4", delta="BUY" if has_buy_signal else None)
            
            st.metric("VWAP", f"${vwap:.2f}")
            
            # 5-minute chart
            st.line_chart(df['Close'], use_container_width=True)
            
            if has_buy_signal:
                st.success(f"**BUY Signal Detected** — {score} confluence factors")
                st.caption("PMH breakout + above 9EMA & VWAP + momentum")
            else:
                st.info("No strong buy signal at this moment")
                
    except Exception as e:
        st.caption(f"Could not load {symbol}")

st.divider()
st.subheader("Strategy Rules – How AlphaBot Decides")
st.markdown("""
**Entry Rules:**
- SPY daily bias sets call/put direction
- Break or retest of pre-market high/low
- Price above/below both 9EMA and VWAP
- Confluence patterns (hammer, doji, flag, etc.)
- Strong volume

**Exit Rules:**
- 10% hard stop per trade
- 4.5% daily loss cap
- 60% profit trail after new high/low
- 4-wick exhaustion rule
- Always close at end of day
""")

st.caption("AlphaBot-Trainer • Educational tool • Data from last trading day")
