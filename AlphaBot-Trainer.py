import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(page_title="AlphaBot SPY Trainer", layout="wide")

# Strong Disclaimer
st.warning("⚠️ **EDUCATIONAL TOOL ONLY** ⚠️\n\n"
           "This is a learning simulator focused on SPY. All signals and examples are for education. "
           "Real trading carries substantial risk of loss. Do not trade based on this app.")

st.title("🚀 AlphaBot SPY Trainer")
st.caption("Real candlestick charts + Rule Explainer for SPY • Last 60 days")

# Sidebar
with st.sidebar:
    st.header("Chart Date")
    max_date = datetime.now().date()
    min_date = max_date - timedelta(days=60)
    selected_date = st.date_input("Select date", value=max_date, min_value=min_date, max_value=max_date)
    
    refresh = st.button("Refresh Latest Data")

# Get real SPY data
def get_spy_data(date):
    try:
        start = date
        end = date + timedelta(days=1)
        df = yf.download("SPY", start=start, end=end, interval="5m", progress=False)
        if not df.empty:
            return df
        return None
    except:
        return None

df = get_spy_data(selected_date)

st.subheader(f"SPY — {selected_date.strftime('%B %d, %Y')}")

if df is None or df.empty:
    st.error("No real data available for this date (markets closed or data not accessible). Try a recent trading day.")
else:
    # Create real Candlestick Chart
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
        title="SPY 5-Minute Candlestick Chart",
        xaxis_title="Time",
        yaxis_title="Price",
        height=600,
        xaxis_rangeslider_visible=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent price stats
    current_price = df['Close'].iloc[-1]
    day_high = df['High'].max()
    day_low = df['Low'].min()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current / Last Price", f"${current_price:.2f}")
    with col2:
        st.metric("Day High", f"${day_high:.2f}")
    with col3:
        st.metric("Day Low", f"${day_low:.2f}")

    st.caption("**How to use this for learning your AlphaTrade rules:**")
    st.write("• Look for candles closing above the Pre-Market High (first 30-60 min range)")
    st.write("• Check if price stays above 9EMA and VWAP")
    st.write("• Watch for hammer / doji / bull flag patterns at support")
    st.write("• Note any strong volume on breakouts")

# Educational Backtest / Rule Notes
st.subheader("Quick Rule Reminder for SPY")
st.markdown("""
**For Calls (SPY up on daily):**
- Wait for first strong candle closing **above Pre-Market High**
- Must be **above VWAP and 9EMA**
- High confluence (hammer, bull flag, etc.)
- Enter on retest of PMH

**Exits:**
- 10% stop loss
- Below 9EMA or VWAP → exit
- 30% partial at round dollar
- Trail runners on new highs
""")

st.divider()
st.caption("AlphaBot SPY Trainer • Real candlestick data via yfinance • Educational only")
