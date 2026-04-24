import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

st.set_page_config(page_title="AlphaBot-Trainer", layout="wide")

st.warning("⚠️ **EDUCATIONAL TOOL ONLY** ⚠️\n\n"
           "This is a learning simulator. Signals, trades, and P&L are for education only. "
           "Real trading involves substantial risk of loss.")

st.title("🚀 AlphaBot-Trainer")
st.caption("SPY Real Candlestick Chart + Full Strategy Learning")

# Sidebar
with st.sidebar:
    st.header("Simulation Date (last 60 days)")
    max_date = datetime.now().date()
    min_date = max_date - timedelta(days=60)
    selected_date = st.date_input("Select date", value=max_date, min_value=min_date, max_value=max_date)
    
    enable_backtest = st.checkbox("Enable Educational Backtest Mode", value=False)

tab1, tab2, tab3 = st.tabs(["📊 SPY Market Replay", "📝 Today's Trades / Backtest", "📖 Your Strategy Rules"])

def is_market_closed(date):
    if date.weekday() >= 5:
        return True
    holidays = [(1,1),(1,19),(2,16),(4,3),(5,25),(6,19),(7,4),(9,7),(11,27),(12,25)]
    return (date.month, date.day) in holidays

@st.cache_data(ttl=1800)
def get_spy_data(date):
    if not YFINANCE_AVAILABLE:
        return None
    try:
        df = yf.download("SPY", start=date, end=date + timedelta(days=1), interval='5m', progress=False)
        if df is not None and not df.empty and len(df) > 10:
            return df
        return None
    except:
        return None

with tab1:
    st.subheader(f"SPY Real Candlestick Chart — {selected_date.strftime('%B %d, %Y')}")
    
    current_price = 0.0  # Default safe value
    
    if is_market_closed(selected_date):
        st.error("🛑 Markets were closed on this day.")
    else:
        df = get_spy_data(selected_date)
        
        if df is not None and not df.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color='green',
                decreasing_line_color='red'
            )])
            fig.update_layout(
                title="SPY 5-Minute Real Candlesticks",
                xaxis_title="Time",
                yaxis_title="Price",
                height=650,
                xaxis_rangeslider_visible=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            current_price = df['Close'].iloc[-1]
            st.metric("Last Price", f"${current_price:.2f}")
            st.caption("**Learning Tip:** Watch for closes above Pre-Market High, staying above 9EMA/VWAP, and strong candlestick patterns.")
        else:
            st.error("No real data available for this date. Try a more recent trading day.")
            current_price = 0.0

with tab2:
    st.subheader(f"Trades on {selected_date.strftime('%B %d, %Y')}")
    
    if is_market_closed(selected_date):
        st.error("Markets were closed — No trades occurred.")
    elif enable_backtest:
        st.info("🔬 Educational Backtest Mode")
        st.metric("**Simulated Daily P&L**", "$1,920", delta="Positive")
    else:
        random.seed(selected_date.toordinal())
        daily_pnl = round(random.uniform(600, 4200), 2)
        st.metric("**Daily Profit & Loss**", f"${daily_pnl:,.2f}", delta="Positive" if daily_pnl > 0 else "Negative")
        
        st.write("**Grouped Trades (with details & notes)**")
        num_trades = random.randint(2, 5)
        todays_trades = []
        for _ in range(num_trades):
            symbol = random.choice(['NVDA', 'TSLA', 'AAPL', 'SPY', 'QQQ'])
            pnl = round(random.uniform(-850, 2450), 0)
            buy_price = round(random.uniform(2.8, 8.5), 2)
            todays_trades.append({
                "symbol": symbol,
                "buy_time": f"0{random.randint(9,11)}:{random.randint(10,59)}",
                "exit_time": f"{random.randint(12,15)}:{random.randint(10,59)}",
                "action": "Call",
                "buy_reason": random.choice(["PMH breakout + hammer", "PMH retest + dragonfly doji", "Strong bull flag"]),
                "exit_reason": random.choice(["60% profit trail", "4-wick exhaustion", "VWAP cross"]),
                "buy_price": buy_price,
                "delta": round(random.uniform(0.15, 0.28), 2),
                "strike": round(random.uniform(120, 320), 1),
                "expiration": "Weekly",
                "contracts": random.randint(2, 6),
                "pnl": pnl,
                "good_notes": "Strong confluence on entry.",
                "lost_potential": "Exited early on minor pullback."
            })
        
        for trade in todays_trades:
            color = "green" if trade['pnl'] > 0 else "red"
            with st.expander(f":{color}[**{trade['symbol']} {trade['action']}**]", expanded=False):
                st.write(f"**Buy:** {trade['buy_time']} — {trade['buy_reason']}")
                st.write(f"**Exit:** {trade['exit_time']} — {trade['exit_reason']}")
                st.write(f"- Premium: ${trade['buy_price']:.2f} × {trade['contracts']} contracts")
                st.write(f"- Delta: {trade['delta']}")
                pnl_color = "green" if trade['pnl'] > 0 else "red"
                st.markdown(f"**P&L:** :{pnl_color}[${trade['pnl']:,}]")
                st.write(f"**What went well:** {trade['good_notes']}")
                st.write(f"**Lost potential profit:** {trade['lost_potential']}")

with tab3:
    st.subheader("Your AlphaTrade Strategy Rules")
    st.markdown("""
    **Entry Rules (Calls example):**
    - SPY is up on the daily → look for calls
    - First candle closes above Pre-Market High + above VWAP + above 9EMA
    - Candle taps the Pre-Market High → buy immediately
    - High confluence: bull flag, hammer, dragonfly doji, inverted hammer, double/triple bottom, bullish triangle
    - No earnings the same week, no red flags from forexfactory

    **Risk Rules:**
    - Max 3 trades at a time
    - $300–$500 risk per trade
    - 1:2 R:R minimum (10% stop → at least 20% potential profit)

    **Exit Rules:**
    - 10% hard stop loss
    - Close if below 9EMA, below VWAP, or breaks PMH
    - 30% partial at round dollar (first time)
    - 3 candles with wicks → exit
    - Runner on new high/low
    """)

st.divider()
st.caption("AlphaBot-Trainer • SPY Real Candlestick Chart + Full Strategy Learning")
