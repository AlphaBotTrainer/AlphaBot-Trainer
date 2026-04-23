import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="AlphaBot-Trainer", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 AlphaBot-Trainer")
st.caption("Learn the AlphaTrade strategy • Grouped trades with detailed notes • Educational tool")

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

tab1, tab2, tab3 = st.tabs(["📊 Live Simulated Market", "📝 Today's Trades", "📖 Strategy Rules"])

with tab1:
    st.subheader("Live Simulated Market - Full Day 5-min Charts")
    
    for symbol in watchlist:
        with st.expander(f"**{symbol}**", expanded=False):
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
            
            title = f":green[**{symbol}**]" if has_buy_signal else f"**{symbol}**"
            
            with st.expander(title, expanded=False):
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
    st.subheader("📝 Today's Trades & P&L")
    daily_pnl = round(random.uniform(800, 3200), 2)
    st.metric("**Daily Profit & Loss**", f"${daily_pnl:,.2f}", delta="Positive" if daily_pnl > 0 else "Negative")
    
    st.write("**Grouped Trades (Buy + Exit with detailed notes)**")
    
    todays_trades = [
        {
            "symbol": "NVDA",
            "buy_time": "09:47",
            "exit_time": "11:25",
            "action": "Call",
            "buy_reason": "PMH breakout + hammer + strong volume",
            "exit_reason": "Hit 60% profit trail",
            "buy_price": 4.85,
            "delta": 0.22,
            "strike": 142.50,
            "expiration": "Weekly",
            "contracts": 4,
            "pnl": 1240,
            "good_notes": "Excellent entry on confluence and volume. Trail captured a large portion of the move.",
            "lost_potential": "Left ~$680 on the table. Could have trailed at 50% instead of 60% or ignored minor pullback."
        },
        {
            "symbol": "TSLA",
            "buy_time": "10:12",
            "exit_time": "13:40",
            "action": "Call",
            "buy_reason": "PMH retest + dragonfly doji",
            "exit_reason": "4-wick exhaustion rule",
            "buy_price": 6.20,
            "delta": 0.18,
            "strike": 318.00,
            "expiration": "Weekly",
            "contracts": 3,
            "pnl": -380,
            "good_notes": "Good entry timing on retest with doji confirmation.",
            "lost_potential": "Exited too early on minor wick exhaustion. The stock reversed and continued higher later."
        },
        {
            "symbol": "ARM",
            "buy_time": "10:55",
            "exit_time": "14:15",
            "action": "Call",
            "buy_reason": "Strong bull flag + breakout",
            "exit_reason": "VWAP cross",
            "buy_price": 3.45,
            "delta": 0.25,
            "strike": 148.50,
            "expiration": "Weekly",
            "contracts": 5,
            "pnl": 920,
            "good_notes": "Strong confluence entry on bull flag breakout.",
            "lost_potential": "Missed additional $450 as the stock continued running after temporary VWAP cross."
        }
    ]
    
    for trade in todays_trades:
        color = "green" if trade['pnl'] > 0 else "red"
        title = f":{color}[**{trade['symbol']} {trade['action']}**]"
        
        with st.expander(title, expanded=False):
            st.write(f"**Buy:** {trade['buy_time']} — {trade['buy_reason']}")
            st.write(f"**Exit:** {trade['exit_time']} — {trade['exit_reason']}")
            
            st.write("**Option Details:**")
            st.write(f"- **Buy Premium:** ${trade['buy_price']:.2f} per share (${trade['buy_price']*100*trade['contracts']:.0f} total)")
            st.write(f"- **Delta at entry:** {trade['delta']}")
            st.write(f"- **Strike:** ${trade['strike']}")
            st.write(f"- **Expiration:** {trade['expiration']}")
            st.write(f"- **Contracts:** {trade['contracts']}")
            
            pnl_color = "green" if trade['pnl'] > 0 else "red"
            st.markdown(f"**P&L for this trade:** :{pnl_color}[${trade['pnl']:,}]")
            
            st.write("**Trade Notes:**")
            st.write(f"- **What went well:** {trade['good_notes']}")
            st.write(f"- **Lost potential profit:** {trade['lost_potential']}")

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
st.caption("AlphaBot-Trainer • Educational simulator with detailed trade notes")
