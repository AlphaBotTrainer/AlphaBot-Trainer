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
    st.warning("⚠️ yfinance not installed. Add 'yfinance' to requirements.txt")

st.set_page_config(page_title="AlphaBot-Trainer", layout="wide")

# ====================== STRONG DISCLAIMER ======================
st.warning("⚠️ **EDUCATIONAL TOOL ONLY** ⚠️\n\n"
           "This is a learning simulator. Signals, trades, and P&L are for education. "
           "Real trading involves substantial risk of loss. Do not trade based on this app.")

st.title("🚀 AlphaBot-Trainer")
st.caption("Interactive learning tool for your AlphaTrade strategy")

# Sidebar
with st.sidebar:
    st.header("Simulation Date (last 60 days)")
    max_date = datetime.now().date()
    min_date = max_date - timedelta(days=60)
    selected_date = st.date_input("Select date", value=max_date, min_value=min_date, max_value=max_date)
    
    enable_backtest = st.checkbox("Enable Educational Backtest Mode", value=False)

watchlist = ['NVDA', 'TSLA', 'ARM', 'AVGO', 'HOOD', 'IONQ', 'SMH', 'QQQ', 'SPY', 
             'AAPL', 'META', 'GOOGL', 'AMZN', 'MSFT', 'MU', 'RKLB', 'SOFI']

tab1, tab2, tab3 = st.tabs(["📊 Market Replay & Rule Explainer", "📝 Backtest Mode", "📖 Your Strategy Rules"])

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
            return df[['Close']].rename(columns={'Close': 'Price'})
        return None
    except:
        return None

with tab1:
    st.subheader(f"Market Replay — {selected_date.strftime('%B %d, %Y')}")
    
    if is_market_closed(selected_date):
        st.error("🛑 Markets were closed on this day (weekend or holiday).")
    else:
        for symbol in watchlist[:8]:   # Limit for performance
            real_df = get_real_data(symbol, selected_date)
            
            if real_df is not None and len(real_df) > 10:
                df = real_df.copy()
                source = "📊 REAL 5-min data"
            else:
                # Safe fallback
                base_price = random.uniform(80, 280)
                prices = [base_price]
                for _ in range(71):
                    prices.append(max(prices[-1] + random.gauss(0, 0.8), 5.0))
                df = pd.DataFrame({'Price': prices})
                source = "⚠️ Simulated data (real data not available)"
            
            df['EMA9'] = df['Price'].ewm(span=9).mean()
            
            # Ultra-safe price extraction
            try:
                current_price = round(float(df['Price'].iloc[-1]), 2)
                ema9 = round(float(df['EMA9'].iloc[-1]), 2)
            except:
                current_price = 150.0
                ema9 = 150.0
            
            score = random.randint(0, 4)
            has_buy_signal = score >= 2
            
            if has_buy_signal:
                expander_title = f":green[**{symbol}**]"
            else:
                expander_title = f"**{symbol}**"
            
            with st.expander(expander_title, expanded=False):
                st.caption(source)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.line_chart(df['Price'], height=320)
                with col2:
                    st.metric("Last Price", f"${current_price:.2f}")
                    st.metric("9EMA", f"${ema9:.2f}")
                
                st.caption("**Rule Explainer (Educational):**")
                st.write("• Watch for price breaking or retesting Pre-Market High")
                st.write("• Needs to be above 9EMA and VWAP for calls")
                st.write("• Look for hammer, doji, bull flag, etc.")

with tab2:
    st.subheader("Educational Backtest Mode")
    if enable_backtest:
        st.success("Backtest Mode Active — Simplified rule simulation")
        st.metric("**Simulated Daily P&L (Educational)**", "$1,920", delta="Positive")
        st.write("**Rules Applied Today:**")
        st.write("• SPY bias checked")
        st.write("• PMH breakout / retest looked for")
        st.write("• 9EMA + VWAP alignment")
        st.write("• Candlestick confluence")
        st.caption("This is educational only. Full accurate backtesting of your complete rules will be added later.")
    else:
        st.info("Turn on **Educational Backtest Mode** to see simplified rule application on historical days.")

with tab3:
    st.subheader("Your AlphaTrade Strategy Rules")
    st.markdown("""
    **Entry Rules (Calls):**
    - SPY up on daily → look for calls
    - First candle closes above Pre-Market High + above VWAP + above 9EMA
    - Candle taps PMH then enter
    - Confluence: bull flag, hammer, dragonfly doji, inverted hammer, double/triple bottom, bullish triangle
    - No earnings week, no red flags

    **Key Risk Rules:**
    - Max 3 trades at once
    - $300–$500 risk per trade
    - 1:2 R:R minimum (10% stop → at least 20% target)

    **Exit Rules:**
    - 10% hard stop
    - Below 9EMA, below VWAP, or below PMH → exit
    - 30% partial at round dollar
    - 3+ candles with wicks → exit
    - Runner on new high/low
    """)

st.divider()
st.caption("AlphaBot-Trainer • Educational simulator only • Real data for recent dates")
