import streamlit as st
import pandas as pd
import yfinance as yf
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="AlphaBot-Trainer", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 AlphaBot-Trainer")
st.caption("Learn the AlphaTrade strategy • Real 5-min charts • Signal explanations")

# Sidebar - Optional API Connection
with st.sidebar:
    st.header("TradeStation API (Optional)")
    st.caption("Add your credentials for live data, otherwise simulated mode is used.")
    
    client_id = st.text_input("Client ID", value="", type="password")
    client_secret = st.text_input("Client Secret", value="", type="password")
    account_id = st.text_input("Account ID", value="")
    
    use_live = st.checkbox("Use Live Data", value=False)
    
    if st.button("Connect"):
        if client_id and client_secret and account_id:
            st.success("✅ Credentials saved for this session")
        else:
            st.warning("Please fill in all fields for live mode")

watchlist = ['NVDA', 'TSLA', 'ARM', 'AVGO', 'HOOD', 'IONQ', 'SMH', 'QQQ', 'SPY', 
             'AAPL', 'META', 'GOOGL', 'AMZN', 'MSFT', 'MU', 'RKLB', 'SOFI']

st.subheader("📊 Live Simulated Market")

for symbol in watchlist:
    try:
        # Safe yfinance fetch with fallback
        df = yf.download(
            symbol,
            interval="5m",
            period="5d",
            progress=False,
            prepost=False
        )
        
        if df.empty or len(df) < 15:
            raise Exception("Insufficient data")
        
        df = df.tail(60)  # Last ~5 hours of 5-min bars
        
        current_price = round(df['Close'].iloc[-1], 2)
        pm_high = round(df['High'].max(), 2)
        pm_low = round(df['Low'].min(), 2)
        
        df['EMA9'] = df['Close'].ewm(span=9).mean()
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        df['VWAP'] = (typical_price * df['Volume']).cumsum() / df['Volume'].cumsum()
        
        ema9 = round(df['EMA9'].iloc[-1], 2)
        vwap = round(df['VWAP'].iloc[-1], 2)
        
        # Confluence score
        score = 0
        if current_price > pm_high and current_price > ema9 and current_price > vwap:
            score += 2
        if current_price > df['Close'].iloc[-10]:
            score += 1
        if (df['High'].iloc[-1] - df['Close'].iloc[-1]) < (df['Close'].iloc[-1] - df['Low'].iloc[-1]) * 0.35:
            score += 1
        
        has_buy_signal = score >= 2
        
        # Display
        title = f"**{symbol}**" if has_buy_signal else symbol
        with st.expander(title, expanded=False):
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
                
    except:
        # Fallback simulated view when yfinance fails
        with st.expander(symbol, expanded=False):
            price = round(random.uniform(80, 280), 2)
            pm_high = round(price * 1.018, 2)
            pm_low = round(price * 0.982, 2)
            ema9 = round(price * 1.005, 2)
            vwap = round(price * 1.002, 2)
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.metric("Price", f"${price:.2f}")
                st.metric("PM High", f"${pm_high:.2f}")
            with col2:
                st.metric("PM Low", f"${pm_low:.2f}")
                st.metric("9EMA", f"${ema9:.2f}")
            with col3:
                st.metric("Signals", "0/4")
            
            st.metric("VWAP", f"${vwap:.2f}")
            st.caption("5-min chart temporarily unavailable — simulated view")
            st.info("No strong buy signal right now")

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

st.caption("AlphaBot-Trainer • Educational tool • Real data when available, simulated fallback otherwise")
