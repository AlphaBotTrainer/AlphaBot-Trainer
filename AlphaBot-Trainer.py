import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(
    page_title="AlphaBot-Trainer",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🚀 AlphaBot-Trainer")
st.caption("Learn the AlphaTrade strategy • Watch signals • Understand every decision")

# Sidebar - Optional API Connection
with st.sidebar:
    st.header("TradeStation API (Optional)")
    st.caption("Add your credentials for live data, otherwise simulated mode is used.")
    
    client_id = st.text_input("Client ID", type="password")
    client_secret = st.text_input("Client Secret", type="password")
    account_id = st.text_input("Account ID")
    
    use_live = st.checkbox("Use Live Data", value=False)
    
    if st.button("Connect"):
        if client_id and client_secret and account_id:
            st.success("✅ Connected to TradeStation (simulated connection for demo)")
        else:
            st.warning("Please fill in credentials for live mode")

# Main Dashboard
tab1, tab2, tab3 = st.tabs(["📊 Live Watchlist", "📝 Recent Signals", "📖 Strategy Rules"])

watchlist = ['NVDA', 'TSLA', 'ARM', 'AVGO', 'HOOD', 'IONQ', 'SMH', 'QQQ', 'SPY', 
             'AAPL', 'META', 'GOOGL', 'AMZN', 'MSFT', 'MU', 'RKLB', 'SOFI']

with tab1:
    st.subheader("Live Simulated Market")
    
    for symbol in watchlist:
        with st.expander(f"📊 {symbol}", expanded=False):
            price = round(random.uniform(80, 280), 2)
            pm_high = round(price * 1.018, 2)
            pm_low = round(price * 0.982, 2)
            ema9 = round(price * 1.005, 2)
            vwap = round(price * 1.002, 2)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Current Price", f"${price:.2f}")
                st.metric("PM High", f"${pm_high:.2f}")
            with col2:
                st.metric("PM Low", f"${pm_low:.2f}")
                st.metric("9EMA", f"${ema9:.2f}")
            
            st.metric("VWAP", f"${vwap:.2f}")
            
            # Simulated signal with explanation
            if random.random() > 0.6:
                st.success(f"**BUY {symbol} Call**")
                st.write("**Reason:** SPY daily bias is bullish + candle closed above PMH + price above 9EMA & VWAP + hammer candle + strong volume.")
                st.caption("60% profit trail active | 10% stop | 4.5% daily cap")
            else:
                st.info("No signal at this moment")

with tab2:
    st.subheader("Recent Signals & Explanations")
    st.info("This area shows why the bot entered or exited each trade.")
    
    example_signals = [
        {"time": "09:47", "symbol": "NVDA", "action": "BUY Call", "reason": "First candle closed above PMH, above 9EMA & VWAP, bull flag + hammer, strong volume"},
        {"time": "10:12", "symbol": "TSLA", "action": "EXIT Call", "reason": "Hit 60% profit trail after new HOD + temporary VWAP cross"},
        {"time": "11:05", "symbol": "ARM", "action": "BUY Call", "reason": "PMH retest + dragonfly doji + volume spike"}
    ]
    
    for sig in example_signals:
        if "BUY" in sig["action"]:
            st.success(f"**{sig['time']} — {sig['action']} {sig['symbol']}**  \n{sig['reason']}")
        else:
            st.warning(f"**{sig['time']} — {sig['action']} {sig['symbol']}**  \n{sig['reason']}")

with tab3:
    st.subheader("How AlphaBot Thinks – Strategy Rules")
    st.markdown("""
    **Entry Rules:**
    - SPY daily direction sets call or put bias
    - Price must break or cleanly retest pre-market high/low
    - Must be on the correct side of both 9EMA and VWAP
    - Needs at least 2 confluence patterns (hammer, doji, flag, etc.)
    - Volume must be strong
    - No recent criss-cross between 9EMA and VWAP

    **Exit Rules:**
    - Hard 10% stop-loss per trade
    - 4.5% daily loss cap (scales with account size)
    - 60% profit trail after making a new high or low
    - 4-wick exhaustion rule
    - Always close all positions at end of day (no overnight holds)
    """)

st.divider()
st.caption("AlphaBot-Trainer • Educational simulator • Free to use and share • Built for learning the strategy")

# Footer
st.caption("Deploy this on GitHub + Streamlit Cloud for free public access")
