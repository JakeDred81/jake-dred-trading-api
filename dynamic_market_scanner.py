# dynamic_market_scanner.py — Clean Rewrite w/ YFinance Only

import yfinance as yf
import pandas as pd

# --- Candle Pattern Detection ---
def detect_candle_pattern(df):
    if len(df) < 3:
        return "Insufficient data"

    latest = df.iloc[-2]  # yesterday's candle
    prev = df.iloc[-3]

    prev_open = float(prev['Open'])
    prev_close = float(prev['Close'])
    latest_open = float(latest['Open'])
    latest_close = float(latest['Close'])

    if (prev_close < prev_open and latest_close > latest_open and
        latest_open < prev_close and latest_close > prev_open):
        return "Bullish Engulfing"

    if (prev_close > prev_open and latest_close < latest_open and
        latest_open > prev_close and latest_close < prev_open):
        return "Bearish Engulfing"

    return "None"

# --- Core Evaluation Scanner ---
def evaluate_with_context(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", auto_adjust=True)
        print(f"\n📊 Raw data for {ticker}:\n{df.tail()}\n")

        if df.empty or df.isnull().values.any():
            raise ValueError(f"No valid data for {ticker}")

        candle = detect_candle_pattern(df)

        sma20 = df['Close'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else df['Close'].mean()
        sma50 = df['Close'].rolling(window=50).mean().iloc[-1] if len(df) >= 50 else df['Close'].mean()
        volume = df['Volume'].iloc[-1]
        avgvol = df['Volume'].mean()

        macd = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
        macd_signal = macd.ewm(span=9).mean()
        macd_trend = "Bullish crossover" if macd.iloc[-1] > macd_signal.iloc[-1] else "Bearish crossover"
        trend = "Uptrend" if sma20 > sma50 else "Downtrend"
        catalyst = "Volume spike" if volume > 1.3 * avgvol else "None"

        rec = "BUY" if trend == "Uptrend" and macd_trend == "Bullish crossover" else "NEUTRAL"

        breakdown = {
            "Technical Pattern": 2 if rec == "BUY" else 1,
            "Trend & Momentum": 2 if trend == "Uptrend" else 1,
            "News/Catalyst": 2 if catalyst != "None" else 1,
            "Fundamentals": 1,
            "Risk/Reward Profile": 1
        }

        score = sum(breakdown.values())

        playbook = {
            "entry": "Bounce or breakout above resistance",
            "stop": "Below support or MA base",
            "target": "Run to previous high or measured move",
            "options": {
                "conservative": "Vertical spread — Buy 0.40 delta call, sell 0.25 delta call",
                "aggressive": "Long call (0.45+ delta, 2-4 weeks out)"
            }
        }

        return {
            "ticker": ticker,
            "score": score,
            "recommendation": rec,
            "pattern": rec.title(),
            "catalyst": catalyst,
            "candle_pattern": candle,
            "indicators": {
                "MACD": macd_trend,
                "Trend": trend,
                "SMA20 vs SMA50": f"{sma20:.2f} vs {sma50:.2f}",
                "Volume": f"{volume:,} vs avg {avgvol:,.0f}"
            },
            "breakdown": breakdown,
            "playbook": playbook
        }

    except Exception as e:
        print(f"❌ Exception for {ticker}: {e}")
        return {
            "ticker": ticker,
            "score": 0,
            "recommendation": "ERROR",
            "pattern": "None",
            "breakdown": {},
            "error": str(e)
        }