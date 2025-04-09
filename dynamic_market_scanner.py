# dynamic_market_scanner.py (YFinance-only version)

import yfinance as yf
import pandas as pd

# --- Candle Pattern Detector ---
def detect_candle_pattern(df):
    if len(df) < 3:
        return "Insufficient data"
    latest = df.iloc[-2]
    prev = df.iloc[-3]

    if prev['Close'] < prev['Open'] and latest['Close'] > latest['Open']:
        if latest['Open'] < prev['Close'] and latest['Close'] > prev['Open']:
            return "Bullish Engulfing"

    if prev['Close'] > prev['Open'] and latest['Close'] < latest['Open']:
        if latest['Open'] > prev['Close'] and latest['Close'] < prev['Open']:
            return "Bearish Engulfing"

    return "None"

# --- Core Scanner ---
def evaluate_with_context(ticker):
    try:
        df = yf.download(ticker, period="30d", interval="1d", auto_adjust=True)

        if df is None or df.empty:
            raise ValueError("No data returned by yfinance")

        # Technical calculations...
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
        df['Signal'] = df['MACD'].ewm(span=9).mean()
        df['VolumeSpike'] = df['Volume'] > df['Volume'].rolling(window=20).mean() * 1.3

        latest = df.iloc[-1]
        candle = detect_candle_pattern(df)

        rec = "BUY" if latest['SMA20'] > latest['SMA50'] and latest['MACD'] > latest['Signal'] else "NEUTRAL"
        trend_type = "Uptrend" if latest['SMA20'] > latest['SMA50'] else "Downtrend"
        catalyst = "Volume spike" if latest['VolumeSpike'] else "None"

        breakdown = {
            "Technical Pattern": 2 if rec == "BUY" else 1,
            "Trend & Momentum": 2 if trend_type == "Uptrend" else 1,
            "News/Catalyst": 2 if catalyst != "None" else 1,
            "Fundamentals": 1,
            "Risk/Reward Profile": 1
        }

        score = sum(breakdown.values())

        return {
            "ticker": ticker,
            "score": score,
            "recommendation": rec,
            "pattern": trend_type,
            "catalyst": catalyst,
            "candle_pattern": candle,
            "indicators": {
                "SMA20": round(latest['SMA20'], 2),
                "SMA50": round(latest['SMA50'], 2),
                "MACD": round(latest['MACD'], 2),
                "Signal": round(latest['Signal'], 2),
                "Volume": int(latest['Volume'])
            },
            "breakdown": breakdown,
            "playbook": {
                "entry": "Breakout above recent high with volume",
                "stop": "Below SMA20 or prior swing low",
                "target": "Run to prior high or Fibonacci extension",
                "options": {
                    "conservative": "Bull call spread, 30DTE",
                    "aggressive": "Long call, 0.40 Delta, 7-14DTE"
                }
            }
        }

    except Exception as e:
        print(f"❌ Exception for {ticker}: {e}")
        return {
            "ticker": ticker,
            "score": 0,
            "recommendation": "ERROR",
            "pattern": "None",
            "breakdown": {},
            "catalyst": str(e)
        }
