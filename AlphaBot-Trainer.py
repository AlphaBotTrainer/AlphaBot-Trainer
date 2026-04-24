import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

st.set_page_config(page_title="AlphaBot-Trainer", layout="wide")

st.warning("⚠️ **EDUCATIONAL TOOL ONLY** ⚠️\n\n"
           "This is a learning simulator. Do not use for real trading decisions.")

st.title("🚀 AlphaBot-Trainer")
st.caption("SPY Real Candlestick Chart + Strategy Learning")

with st.sidebar:
    st.header("Simulation Date (last 60 days)")
    max_date = datetime.now().date()
    selected_date = st.date_input("Select date", value=max_date, 
                                  min_value=max_date - timedelta(days=60), 
                                  max_value=max_date)

tab1, tab2, tab3 = st.tabs(["📊 SPY Market Replay", "📝 Today's Trades", "📖 Strategy Rules"])

def is_market_closed(d):
    return d.weekday() >= 5

@st.cache_data(ttl=3600)
def get_spy_data(date):
    if not HAS_YFINANCE:
        return None
    try:
        df = yf.download("SPY", start=date, end=date + timedelta(days=1), interval='5m', progress=False)
        if df is not None and not df.empty and len(df) > 5:
            return df
        return None
    except:
        return None

with tab1:
    st.subheader(f"SPY — {selected_date.strftime('%B %d, %Y')}")

    if is_market_closed(selected_date):
        st.error("🛑 Markets were closed on this day.")
    else:
        df = get_spy_data(selected_date)
        
        if df is not None and not df.empty:
            try:
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    increasing_line_color='green',
                    decreasing_line_color='red'
                )])
                fig.update_layout(height=650, title="SPY 5-Minute Real Candlesticks")
                st.plotly_chart(fig, use_container_width=True)
                
                # Super safe price extraction
                last_price = float(df['Close'].iloc[-1])
                st.metric("Last Price", f"${last_price:.2f}")
            except Exception as e:
                st.error(f"Could not display chart: {str(e)}")
                st.info("Trying simulated chart instead...")
                # Simulated fallback
                base = 580.0
                times = pd.date_range(start=selected_date, periods=72, freq='5min')
                prices = [base + i*0.2 + random.gauss(0, 1.5) for i in range(72)]
                fig_sim = go.Figure(data=[go.Candlestick(
                    x=times,
                    open=[p-0.5 for p in prices],
                    high=[p+1 for p in prices],
                    low=[p-1 for p in prices],
                    close=prices,
                    increasing_line_color='green',
                    decreasing_line_color='red'
                )])
                fig_sim.update_layout(height=500, title="Simulated SPY Candles")
                st.plotly_chart(fig_sim, use_container_width=True)
        else:
            st.warning("No real data available for this date.")
            st.info("Showing simulated chart for demonstration.")

with tab2:
    st.subheader(f"Trades on {selected_date.strftime('%B %d, %Y')}")
    if is_market_closed(selected_date):
        st.error("No trades — Market closed")
    else:
        st.info("Educational simulated trades")
        st.metric("Simulated Daily P&L", "$1,650", delta="Positive")

with tab3:
    st.subheader("Your AlphaTrade Strategy Rules")
    st.markdown("""
    **Entry Rules (Calls example):**
    - SPY is up on the daily → look for calls
    - First candle closes above Pre-Market High + above VWAP + above 9EMA
    - Candle taps the Pre-Market High → buy immediately
    - High confluence (bull flag, hammer, dragonfly doji, etc.)

    **Exit Rules:**
    - 10% hard stop
    - Below 9EMA or VWAP
    - 30% partial at round dollar
    - 3-wick rule
    - Runner on new highs
    """)

st.caption("AlphaBot-Trainer • Educational only")
