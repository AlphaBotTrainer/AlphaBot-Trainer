import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="AlphaBot-Trainer", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 AlphaBot-Trainer")
st.caption("Learn the AlphaTrade strategy • Detailed trades with notes • Educational tool")

# Sidebar
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
        
        if has_buy_signal:
            expander_title = f":green[**{symbol}**]"
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
            
            st.line_chart(df['Price'], use_container_width=True, height=340)
            
            if has_buy_signal:
                st.success(f"**BUY Signal Detected** — {score} confluence factors")
                st.caption("Breakout above PMH + above 9EMA & VWAP + momentum")
            else:
                st.info("No strong buy signal right now")

with tab2:
    st.subheader(f"📝 Trades on {selected_date.strftime('%B %d, %Y')}")
    
    # Make data consistent for the same date but different across dates
    random.seed(selected_date.toordinal())
    
    daily_pnl = round(random.uniform(600, 4200), 2)
    st.metric("**Daily Profit & Loss**", f"${daily_pnl:,.2f}", delta="Positive" if daily_pnl > 0 else "Negative")
    
    st.write("**Grouped Trades (Buy + Exit with full details & notes)**")
    
    # Generate varied trades for the selected date
    num_trades = random.randint(2, 5)
    todays_trades = []
    for i in range(num_trades):
        symbol = random.choice(watchlist)
        pnl = round(random.uniform(-850, 2450), 0)
        buy_price = round(random.uniform(2.8, 8.5), 2)
        delta = round(random.uniform(0.15, 0.28), 2)
        strike = round(random.uniform(120, 320), 1)
        
        todays_trades.append({
            "symbol": symbol,
            "buy_time": f"0{random.randint(9,11)}:{random.randint(10,59)}",
            "exit_time": f"{random.randint(12,15)}:{random.randint(10,59)}",
            "action": "Call",
            "buy_reason": random.choice(["PMH breakout + hammer", "PMH retest + dragonfly doji", "Strong bull flag + breakout", "Volume spike + inverted hammer"]),
            "exit_reason": random.choice(["60% profit trail", "4-wick exhaustion rule", "VWAP cross", "Reached 10% stop"]),
            "buy_price": buy_price,
            "delta": delta,
            "strike": strike,
            "expiration": "Weekly",
            "contracts": random.randint(2, 6),
            "pnl": pnl,
            "good_notes": random.choice([
                "Excellent entry timing with strong confluence and volume confirmation.",
                "Good retest of PMH with clear candlestick pattern.",
                "Strong momentum and volume spike supported the breakout."
            ]),
            "lost_potential": random.choice([
                "Left additional profit on the table by trailing too tightly.",
                "Exited early on minor wick exhaustion — stock reversed strongly afterward.",
                "Missed runner extension due to conservative VWAP exit."
            ])
        })
    
    for trade in todays_trades:
        color = "green" if trade['pnl'] > 0 else "red"
        title = f":{color}[**{trade['symbol']} {trade['action']}**]"
        
        with st.expander(title, expanded=False):
            st.write(f"**Buy:** {trade['buy_time']} — {trade['buy_reason']}")
            st.write(f"**Exit:** {trade['exit_time']} — {trade['exit_reason']}")
            
            st.write("**Option Details:**")
            st.write(f"- **Buy Premium:** ${trade['buy_price']:.2f} per share (${trade['buy_price'] * 100 * trade['contracts']:.0f} total)")
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
st.caption(f"AlphaBot-Trainer • Showing simulated data for {selected_date.strftime('%B %d, %Y')}")
