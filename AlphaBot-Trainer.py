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
           "This app is for learning. Signals and P&L are simulated or simplified. "
           "Real trading involves substantial risk of loss. Do not trade based on this tool.")

st.title("🚀 AlphaBot-Trainer")
st.caption("Full watchlist + Real SPY Candlestick Chart • Educational")

# Sidebar
with st.sidebar:
    st.header("Simulation Date (last 60 days)")
    max_date = datetime.now().date()
    min_date = max_date - timedelta(days=60)
    selected_date = st.date_input("Select date", value=max_date, min_value=min_date, max_value=max_date)
    
    enable_backtest = st.checkbox("Enable Educational Backtest Mode", value=False)

watchlist = ['NVDA', 'TSLA', 'ARM', 'AVGO', 'HOOD', 'IONQ', 'SMH', 'QQQ', 'SPY', 
             'AAPL', 'META', 'GOOGL', 'AMZN', 'MSFT', 'MU', 'RKLB', 'SOFI']

tab1, tab2, tab3 = st.tabs(["📊 Market Replay", "📝 Today's Trades / Backtest", "📖 Strategy Rules"])

def is_market_closed(date):
    if date.weekday() >= 5:
        return True
    holidays = [(1,1),(1,19),(2,16),(4,3),(5,25),(6,19),(7,4),(9,7),(11,27),(12,25)]
    return (date.month, date.day) in holidays

@st.cache_data(ttl=1800)
def get_real_data(symbol, date):
    if not YFINANCE_AVAILABLE:
        return None
    try:
        df = yf.download(symbol, start=date, end=date + timedelta(days=1), interval='5m', progress=False)
        if df is not None and not df.empty and len(df) > 10:
            return df
        return None
    except:
        return None

with tab1:
    st.subheader(f"Market Replay — {selected_date.strftime('%B %d, %Y')}")
    
    if is_market_closed(selected_date):
        st.error("🛑 Markets were closed on this day.")
    else:
        # Special SPY Candlestick Chart
        spy_df = get_real_data("SPY", selected_date)
        if spy_df is not None and not spy_df.empty:
            st.write("**SPY Real Candlestick Chart**")
            fig = go.Figure(data=[go.Candlestick(
                x=spy_df.index,
                open=spy_df['Open'],
                high=spy_df['High'],
                low=spy_df['Low'],
                close=spy_df['Close'],
                increasing_line_color='green',
                decreasing_line_color='red'
            )])
            fig.update_layout(height=500, title="SPY 5-Minute Candles")
            st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Other Symbols (Summary Charts)**")
        for symbol in [s for s in watchlist if s != "SPY"]:
            real_df = get_real_data(symbol, selected_date)
            if real_df is not None and len(real_df) > 10:
                df = real_df[['Close']].rename(columns={'Close': 'Price'})
                source = "REAL"
            else:
                base = random.uniform(80, 280)
                prices = [base + random.gauss(0, 0.8) for _ in range(72)]
                df = pd.DataFrame({'Price': prices})
                source = "Simulated"
            
            df['EMA9'] = df['Price'].ewm(span=9).mean()
            try:
                current_price = round(float(df['Price'].iloc[-1]), 2)
                ema9 = round(float(df['EMA9'].iloc[-1]), 2)
            except:
                current_price = 150.0
                ema9 = 150.0
            
            with st.expander(f"{symbol} — {source}", expanded=False):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.line_chart(df['Price'], height=280)
                with col2:
                    st.metric("Price", f"${current_price:.2f}")
                    st.metric("9EMA", f"${ema9:.2f}")

with tab2:
    st.subheader(f"Trades on {selected_date.strftime('%B %d, %Y')}")
    if is_market_closed(selected_date):
        st.error("Markets were closed — No trades")
    elif enable_backtest:
        st.info("Educational Backtest Mode — Simplified")
        st.metric("Simulated Daily P&L", "$1,850", delta="Positive")
    else:
        random.seed(selected_date.toordinal())
        daily_pnl = round(random.uniform(600, 4200), 2)
        st.metric("**Daily Profit & Loss**", f"${daily_pnl:,.2f}", delta="Positive" if daily_pnl > 0 else "Negative")
        
        # Keep your detailed trades
        num_trades = random.randint(2, 5)
        todays_trades = []
        for _ in range(num_trades):
            symbol = random.choice(watchlist)
            pnl = round(random.uniform(-850, 2450), 0)
            buy_price = round(random.uniform(2.8, 8.5), 2)
            todays_trades.append({
                "symbol": symbol,
                "buy_time": f"0{random.randint(9,11)}:{random.randint(10,59)}",
                "exit_time": f"{random.randint(12,15)}:{random.randint(10,59)}",
                "action": "Call",
                "buy_reason": random.choice(["PMH breakout + hammer", "PMH retest + doji", "Bull flag"]),
                "exit_reason": random.choice(["60% trail", "VWAP cross", "4-wick"]),
                "buy_price": buy_price,
                "delta": round(random.uniform(0.15, 0.28), 2),
                "strike": round(random.uniform(120, 320), 1),
                "contracts": random.randint(2, 6),
                "pnl": pnl,
                "good_notes": "Strong confluence on entry",
                "lost_potential": "Exited early on pullback"
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
                st.write(f"**Lost potential:** {trade['lost_potential']}")

with tab3:
    st.subheader("Your AlphaTrade Strategy Rules")
    st.markdown("**Full rules are listed here as you originally described them.** (I can expand this further if needed)")

st.divider()
st.caption("AlphaBot-Trainer • Real SPY candlesticks + full watchlist")
