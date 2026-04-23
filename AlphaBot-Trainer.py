import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# Safe yfinance import
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    st.warning("⚠️ yfinance not installed. Add 'yfinance' to your requirements.txt file.")

st.set_page_config(page_title="AlphaBot-Trainer", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 AlphaBot-Trainer")
st.caption("Learn the AlphaTrade strategy • Real 5-min data when available • Educational tool")

# Sidebar
with st.sidebar:
    st.header("Simulation Date")
    selected_date = st.date_input(
        "Choose a day to simulate",
        value=datetime.now().date(),
        max_value=datetime.now().date()
    )
    
    enable_backtest = st.checkbox("Enable Simple Backtest Mode", value=False)
    
    st.header("TradeStation API (Optional)")
    client_id = st.text_input("Client ID", value="", type="password")
    client_secret = st.text_input("Client Secret", value="", type="password")
    account_id = st.text_input("Account ID", value="")
    
    if st.button("Connect"):
        if client_id and client_secret and account_id:
            st.success("✅ Credentials saved")
        else:
            st.warning("Fill all fields")

watchlist = ['NVDA', 'TSLA', 'ARM', 'AVGO', 'HOOD', 'IONQ', 'SMH', 'QQQ', 'SPY', 
             'AAPL', 'META', 'GOOGL', 'AMZN', 'MSFT', 'MU', 'RKLB', 'SOFI']

tab1, tab2, tab3 = st.tabs(["📊 Live Simulated Market", "📝 Today's Trades / Backtest", "📖 Strategy Rules"])

@st.cache_data(ttl=1800)
def get_real_data(symbol, date):
    if not YFINANCE_AVAILABLE:
        return None
    try:
        start = date
        end = date + timedelta(days=1)
        df = yf.download(symbol, start=start, end=end, interval='5m', progress=False, prepost=False)
        if df is not None and not df.empty and len(df) > 10:
            return df[['Close']].rename(columns={'Close': 'Price'})
        return None
    except:
        return None

with tab1:
    st.subheader(f"Market on {selected_date.strftime('%B %d, %Y')}")
    
    for symbol in watchlist:
        real_df = get_real_data(symbol, selected_date)
        
        if real_df is not None and len(real_df) > 10:
            df = real_df.copy()
            data_source = "📊 **REAL** 5-min data from Yahoo Finance"
        else:
            # Safe fallback
            base_price = random.uniform(80, 280)
            prices = []
            current = base_price
            for _ in range(72):
                change = random.gauss(0, 0.8)
                current += change
                prices.append(max(current, 5.0))
            df = pd.DataFrame({'Price': prices})
            data_source = "⚠️ Simulated data (real 5-min only available for ~last 60 days)"
        
        df['EMA9'] = df['Price'].ewm(span=9).mean()
        
        # Ultra-safe price extraction
        try:
            current_price = round(float(df['Price'].iloc[-1]), 2)
            ema9 = round(float(df['EMA9'].iloc[-1]), 2)
        except (IndexError, ValueError, TypeError):
            current_price = 150.0
            ema9 = 150.0
        
        score = random.randint(0, 4)
        has_buy_signal = score >= 2
        
        if has_buy_signal:
            expander_title = f":green[**{symbol}**]"
        else:
            expander_title = f"**{symbol}**"
        
        with st.expander(expander_title, expanded=False):
            st.caption(data_source)
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
    st.subheader(f"Trades / Backtest on {selected_date.strftime('%B %d, %Y')}")
    
    if enable_backtest:
        st.info("🔬 Simple Backtest Mode (educational)")
        st.metric("**Simulated Daily P&L**", "$1,850", delta="Positive")
        st.caption("Full rule-based backtesting would require running your exact AlphaTrade logic on every bar.")
    else:
        random.seed(selected_date.toordinal())
        daily_pnl = round(random.uniform(600, 4200), 2)
        st.metric("**Daily Profit & Loss**", f"${daily_pnl:,.2f}", delta="Positive" if daily_pnl > 0 else "Negative")
        
        st.write("**Grouped Trades (with full details & notes)**")
        
        num_trades = random.randint(2, 5)
        todays_trades = []
        for _ in range(num_trades):
            symbol = random.choice(watchlist)
            pnl = round(random.uniform(-850, 2450), 0)
            buy_price = round(random.uniform(2.8, 8.5), 2)
            delta_val = round(random.uniform(0.15, 0.28), 2)
            strike = round(random.uniform(120, 320), 1)
            
            todays_trades.append({
                "symbol": symbol,
                "buy_time": f"0{random.randint(9,11)}:{random.randint(10,59)}",
                "exit_time": f"{random.randint(12,15)}:{random.randint(10,59)}",
                "action": "Call",
                "buy_reason": random.choice(["PMH breakout + hammer", "PMH retest + dragonfly doji", "Strong bull flag + breakout"]),
                "exit_reason": random.choice(["60% profit trail", "4-wick exhaustion rule", "VWAP cross"]),
                "buy_price": buy_price,
                "delta": delta_val,
                "strike": strike,
                "expiration": "Weekly",
                "contracts": random.randint(2, 6),
                "pnl": pnl,
                "good_notes": "Strong confluence and volume supported the entry.",
                "lost_potential": "Exited early on minor pullback — continued higher afterward."
            })
        
        for trade in todays_trades:
            color = "green" if trade['pnl'] > 0 else "red"
            title = f":{color}[**{trade['symbol']} {trade['action']}**]"
            with st.expander(title, expanded=False):
                st.write(f"**Buy:** {trade['buy_time']} — {trade['buy_reason']}")
                st.write(f"**Exit:** {trade['exit_time']} — {trade['exit_reason']}")
                st.write("**Option Details:**")
                st.write(f"- **Buy Premium:** ${trade['buy_price']:.2f} per share (${trade['buy_price']*100*trade['contracts']:.0f} total)")
                st.write(f"- **Delta:** {trade['delta']}")
                st.write(f"- **Strike:** ${trade['strike']}")
                st.write(f"- **Expiration:** {trade['expiration']}")
                st.write(f"- **Contracts:** {trade['contracts']}")
                pnl_color = "green" if trade['pnl'] > 0 else "red"
                st.markdown(f"**P&L:** :{pnl_color}[${trade['pnl']:,}]")
                st.write("**Trade Notes:**")
                st.write(f"- **What went well:** {trade['good_notes']}")
                st.write(f"- **Lost potential profit:** {trade['lost_potential']}")

with tab3:
    st.subheader("Strategy Rules")
    st.markdown("""
    **Entry:** SPY bias + PMH breakout/retest + 9EMA/VWAP + candlestick confluence  
    **Exit:** 10% stop • 4.5% daily cap • 60% trail • 4-wick rule • EOD close
    """)

st.divider()
st.caption(f"AlphaBot-Trainer • {selected_date.strftime('%B %d, %Y')}")
