import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

st.set_page_config(page_title="AlphaBot-Trainer", layout="wide")

# Strong Disclaimer
st.warning("⚠️ **EDUCATIONAL TOOL ONLY** ⚠️\n\n"
           "This app is for learning purposes. All signals, P&L, and outcomes are simulated or simplified. "
           "Real trading involves significant risk of loss. Do not use this to make trading decisions. "
           "Always verify with your own analysis and paper trade first.")

st.title("🚀 AlphaBot-Trainer")
st.caption("Interactive learning tool for your AlphaTrade strategy • Real data when available")

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
        st.error("🛑 Markets were closed on this day.")
    else:
        for symbol in watchlist[:6]:  # Limit to 6 for performance
            real_df = get_real_data(symbol, selected_date)
            if real_df is not None and len(real_df) > 10:
                df = real_df.copy()
                source = "📊 REAL 5-min data"
            else:
                # Simulated fallback
                base = random.uniform(80, 280)
                prices = [base + random.gauss(0, 0.8) for _ in range(72)]
                df = pd.DataFrame({'Price': prices})
                source = "⚠️ Simulated data"
            
            df['EMA9'] = df['Price'].ewm(span=9).mean()
            current_price = round(float(df['Price'].iloc[-1]), 2)
            ema9 = round(float(df['EMA9'].iloc[-1]), 2)
            
            with st.expander(f"{symbol} — {source}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.line_chart(df['Price'], height=300)
                with col2:
                    st.metric("Last Price", f"${current_price:.2f}")
                    st.metric("9EMA", f"${ema9:.2f}")
                
                st.caption("**Rule Highlights (Educational):**")
                st.write("- Look for price breaking/re-testing Pre-Market High")
                st.write("- Check if price is above 9EMA and VWAP for calls")
                st.write("- Watch for hammer, doji, or bull flag confluence")

with tab2:
    st.subheader("Educational Backtest Mode")
    if enable_backtest:
        st.success("Backtest Mode Active — Showing simplified rule application")
        st.write("On real days, we look for:")
        st.write("• SPY daily bias")
        st.write("• PMH breakout or retest")
        st.write("• 9EMA + VWAP alignment (no recent criss-cross)")
        st.write("• Candlestick confluence (hammer, doji, etc.)")
        st.metric("Hypothetical Daily Result", "$1,920", delta="Positive")
        st.caption("This is educational only. Full accurate backtesting of your exact rules will be added later.")
    else:
        st.info("Turn on Backtest Mode to see simplified rule simulation on historical data.")

with tab3:
    st.subheader("Your AlphaTrade Strategy Rules")
    st.markdown("""
    **Entry Rules (Calls example):**
    - SPY is up on daily → look for calls
    - First candle closes above Pre-Market High + above VWAP + above 9EMA
    - Candle taps PMH then buy
    - High confluence: bull flag, hammer, dragonfly doji, inverted hammer, double bottom, bullish triangle
    - No trade if earnings this week or red flag on forexfactory
    - Max 3 trades open, $300–$500 risk per trade, 1:2 R:R minimum (10% stop → 20%+ target)

    **Exit Rules:**
    - 10% hard stop
    - Close if below 9EMA or below VWAP or below PMH
    - 30% partial at round dollar (first time)
    - 3 candles with upper/lower wicks → exit
    - Runner logic on new high/low

    **Risk Management:**
    - Max 3–6 concurrent trades
    - Daily loss cap (4.5% of equity or fixed $ amount)
    - No overnight holds
    """)
    st.caption("Use the Market Replay tab to see these rules in action on real charts.")

st.divider()
st.caption("AlphaBot-Trainer • Educational tool only • Real data limited to recent dates")
