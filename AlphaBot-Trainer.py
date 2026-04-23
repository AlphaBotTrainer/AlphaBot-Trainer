import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="AlphaBot-Trainer", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 AlphaBot-Trainer")
st.caption("Learn the AlphaTrade strategy • Real 5-min charts • Signal explanations")

# Sidebar
with st.sidebar:
    st.header("Optional Live Mode")
    st.caption("Add TradeStation credentials for real data (future feature)")
    st.info("Currently running in realistic simulated mode")

watchlist = ['NVDA', 'TSLA', 'ARM', 'AVGO', 'HOOD', 'IONQ', 'SMH', 'QQQ', 'SPY', 
             'AAPL', 'META', 'GOOGL', 'AMZN', 'MSFT', 'MU', 'RKLB', 'SOFI']

st.subheader("📊 Live Simulated Market (Realistic Data)")

for symbol in watchlist:
    try:
        # Fetch real 5-min data safely
        end = datetime.now()
        start = end - timedelta(days=5)  # More buffer days
        
        df = yf.download(
            symbol, 
            interval="5m", 
            start=start, 
            end=end, 
            progress=False,
            prepost=True
        )
        
        if df.empty or len(df) < 10:
            st.caption(f"⚠️ No recent data for {symbol}")
            continue
            
        df = df.tail(60)  # Last ~5 hours of 5-min bars
        
        current_price = round(df['Close'].iloc[-1], 2)
        pm_high = round(df['High'].max(), 2)
        pm_low = round(df['Low'].min(), 2)
        
        # Calculate indicators
        df['EMA9'] = df['Close'].ewm(span=9).mean()
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        df['VWAP'] = (typical_price * df['Volume']).cumsum() / df['Volume'].cumsum()
        
        ema9 = round(df['EMA9'].iloc[-1], 2)
        vwap = round(df['VWAP'].iloc[-1], 2)
        
        # Simple confluence score
        score = 0
        if current_price > pm_high and current_price > ema9 and current_price > vwap:
            score += 2  # Strong breakout
        if current_price > df['Close'].iloc[-10]:
            score += 1
        if (df['High'].iloc[-1] - df['Close'].iloc[-1]) < (df['Close'].iloc[-1] - df['Low'].iloc[-1]) * 0.4:
            score += 1  # Hammer-like
        
        has_buy_signal = score >= 2
        
        # Display
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
                st.success(f"**BUY Signal** — {score} confluence factors")
                st.caption("Breakout above PMH + above 9EMA & VWAP + momentum")
            else:
                st.info("No strong buy signal right now")
                
    except Exception as e:
        st.caption(f"Could not load {symbol} (data temporarily unavailable)")

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

st.caption("AlphaBot-Trainer • Educational tool • Data from last trading session")
