import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="AlphaBot-Trainer", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 AlphaBot-Trainer")
st.caption("Learn the AlphaTrade strategy • Signal explanations • Educational tool")

# Sidebar for optional API (kept for future)
with st.sidebar:
    st.header("TradeStation API (Optional)")
    st.caption("Add credentials for live data (not required)")
    st.info("Currently running in realistic simulated mode")

watchlist = ['NVDA', 'TSLA', 'ARM', 'AVGO', 'HOOD', 'IONQ', 'SMH', 'QQQ', 'SPY', 
             'AAPL', 'META', 'GOOGL', 'AMZN', 'MSFT', 'MU', 'RKLB', 'SOFI']

st.subheader("📊 Live Simulated Market")

for symbol in watchlist:
    with st.expander(f"**{symbol}**", expanded=False):
        # Realistic simulated data
        price = round(random.uniform(80, 280), 2)
        pm_high = round(price * 1.018, 2)
        pm_low = round(price * 0.982, 2)
        ema9 = round(price * 1.005, 2)
        vwap = round(price * 1.002, 2)
        
        # Confluence score
        score = random.randint(0, 4)
        has_buy_signal = score >= 2
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.metric("Price", f"${price:.2f}")
            st.metric("PM High", f"${pm_high:.2f}")
        with col2:
            st.metric("PM Low", f"${pm_low:.2f}")
            st.metric("9EMA", f"${ema9:.2f}")
        with col3:
            st.metric("Signals", f"{score}/4", delta="BUY" if has_buy_signal else None)
        
        st.metric("VWAP", f"${vwap:.2f}")
        
        # Simulated 5-min chart
        chart_data = pd.DataFrame({
            'Price': [price * (0.97 + i*0.006) for i in range(12)]
        })
        st.line_chart(chart_data, use_container_width=True)
        
        if has_buy_signal:
            st.success(f"**BUY Signal** — {score} confluence factors")
            st.caption("Breakout above PMH + above 9EMA & VWAP + momentum")
        else:
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

st.caption("AlphaBot-Trainer • Educational simulator • No API required")
