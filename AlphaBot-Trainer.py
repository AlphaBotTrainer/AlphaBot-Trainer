import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="AlphaBot-Trainer", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 AlphaBot-Trainer")
st.caption("Learn the AlphaTrade strategy • Today's signals • Educational tool")

# Sidebar - Optional API
with st.sidebar:
    st.header("TradeStation API (Optional)")
    st.caption("Add credentials for live data (not required)")
    
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

tab1, tab2, tab3 = st.tabs(["📊 Live Simulated Market", "📝 Today's Signals", "📖 Strategy Rules"])

# Simulated daily P&L (for demo)
daily_pnl = round(random.uniform(800, 2800), 2)

with tab1:
    st.subheader("Live Simulated Market")
    
    for symbol in watchlist:
        with st.expander(f"**{symbol}**", expanded=False):
            price = round(random.uniform(80, 280), 2)
            pm_high = round(price * 1.018, 2)
            pm_low = round(price * 0.982, 2)
            ema9 = round(price * 1.005, 2)
            vwap = round(price * 1.002, 2)
            
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
            
            chart_data = pd.DataFrame({
                'Price': [price * (0.97 + i*0.006) for i in range(12)]
            })
            st.line_chart(chart_data, use_container_width=True)
            
            if has_buy_signal:
                st.success(f"**BUY Signal** — {score} confluence factors")
                st.caption("Breakout above PMH + above 9EMA & VWAP + momentum")
            else:
                st.info("No strong buy signal right now")

with tab2:
    st.subheader(f"📝 Today's Signals & P&L")
    st.metric("**Daily Profit & Loss**", f"${daily_pnl:,.2f}", delta="Positive" if daily_pnl > 0 else "Negative")
    
    st.write("**All signals generated today:**")
    
    # Simulated today's signals
    todays_signals = [
        {"time": "09:47", "symbol": "NVDA", "action": "BUY Call", "reason": "First candle closed above PMH + above 9EMA & VWAP + hammer + strong volume"},
        {"time": "10:12", "symbol": "TSLA", "action": "BUY Call", "reason": "PMH retest + dragonfly doji + volume spike"},
        {"time": "10:55", "symbol": "ARM", "action": "BUY Call", "reason": "Strong bull flag + breakout above PMH"},
        {"time": "11:40", "symbol": "NVDA", "action": "EXIT Call", "reason": "Hit 60% profit trail after new HOD"},
        {"time": "13:25", "symbol": "TSLA", "action": "EXIT Call", "reason": "4-wick exhaustion rule triggered"},
    ]
    
    for sig in todays_signals:
        if "BUY" in sig["action"]:
            st.success(f"**{sig['time']} — {sig['action']} {sig['symbol']}**  \n{sig['reason']}")
        else:
            st.warning(f"**{sig['time']} — {sig['action']} {sig['symbol']}**  \n{sig['reason']}")

with tab3:
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

st.divider()
st.caption("AlphaBot-Trainer • Educational simulator • API credentials optional")
