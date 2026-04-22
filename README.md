# AlphaBot-Trainer
Beta Testing the training program for the Alpha Bot

# AlphaBot-Trainer

**Learn the AlphaTrade Strategy – Interactive Educational Simulator**

A free, beginner-friendly web app that teaches how the AlphaTrade Bot makes decisions.  
No TradeStation account or API key required to start learning.

### Features

- **Live Simulated Market** — Watch realistic price action across 26 popular symbols
- **Signal Explanations** — Plain English reasons why the bot enters or exits trades
- **Strategy Rules** — Clear breakdown of entry and exit logic
- **Optional Live Mode** — Connect your own TradeStation API credentials for real data
- **Mobile Friendly** — Works great on phones (add to home screen for app-like experience)

### How It Works

The app simulates the core logic of the AlphaTrade Bot:
- SPY daily bias (calls vs puts)
- Pre-market high/low breakout or retest
- 9EMA + VWAP alignment
- Candlestick confluence (hammer, doji, flag, etc.)
- Volume confirmation
- 60% profit trail, 10% stop, 4.5% daily cap, 4-wick rule

### Quick Start (Local)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/AlphaBot-Trainer.git
cd AlphaBot-Trainer

# 2. Install dependencies
pip install streamlit pandas

# 3. Run the app
streamlit run AlphaBot-Trainer.py

### How to Customize API Credentials (Live Mode)

# 1. Open the app in your browser.
# 2. Go to the sidebar on the left.
# 3. Fill in your TradeStation credentials:
- Client ID
- Client Secret
- Account ID

# 4. Check the "Use Live Data" box.
# 5. Click "Connect".

***The app will attempt to connect to TradeStation and show real market data and signals instead of simulated ones.
***
Note: Your credentials are only used during the current session and are not stored permanently.
