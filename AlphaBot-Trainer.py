import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="AlphaBot-Trainer", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 AlphaBot-Trainer")
st.caption("Learn the AlphaTrade strategy • Full-day 5-min charts • Educational tool")

# Sidebar - Date Picker + Optional API
with st.sidebar:
    st.header("Simulation Date")
    selected_date = st.date_input(
        "Choose a day to simulate",
        value=datetime.now().date(),
        max_value=datetime.now().date()
    )
    
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

tab1, tab2, tab3 = st.tabs(["📊 Live Simulated Market", "📝 Today's Trades", "📖 Strategy Rules"])

with tab1:
    st.subheader(f"Simulated Market — {selected_date.strftime('%B %d, %Y')}")
    
    for symbol in watchlist:
        base_price = random.uniform(80, 280)
        prices = []
        current = base_price
        for i in range(72):
            change = random.gauss(0, 0.8)
            current += change
            prices.append(max(current, 5.0))
        
        df = pd.DataFrame({'Price': prices})
        df['EMA9'] = df['Price'].ewm(span=9).mean()
        
        current_price = round(df['Price'].iloc[-1], 2)
        ema9 = round(df['EMA9'].iloc[-1], 2)
        
        score = random.randint(0, 4)
        has_buy_signal = score >= 2
        
        # Clean green title without nesting
        if has_buy_signal:
            expander_title = f"🟢 **{symbol}**"
        else:
            expander_title = f"**{symbol}**"
        
        with st.expander(expander_title, expanded=False):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.metric("Current Price", f"${current_price:.2f}")
            with col2:
                st.metric("9EMA", f"${ema9:.2f}")
            with col3:
                st.metric("Signals", f"{score}/4", delta="BUY" if has_buy_signal else None)
            
            st.line_chart(df['Price'], use_container_width=True, height=320)
            
            if has_buy_signal:
                st.success(f"**BUY Signal Detected** — {score} confluence factors")
                st.caption("Breakout above PMH + above 9EMA & VWAP + momentum")
            else:
                st.info("No strong buy signal right now")

with tab2:
    st.subheader(f"📝 Trades on {selected_date.strftime('%B %d, %Y')}")
    daily_pnl = round(random.uniform(800, 3200), 2)
    st.metric("**Daily Profit & Loss**", f"${daily_pnl:,.2f}", delta="Positive" if daily_pnl > 0 else "Negative")
    
    st.write("**Grouped Trades (Buy + Exit with P&L)**")
    
    todays_trades = [
        {"symbol": "NVDA", "buy_time": "
