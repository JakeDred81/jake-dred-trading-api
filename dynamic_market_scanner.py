# dynamic_market_scanner.py (YFinance-Only Rewrite)

import yfinance as yf
import pandas as pd

# --- Candle Pattern Detector ---
def detect_candle_pattern(df):
    if len(df) < 3:
        return "Insufficient data"
    latest = df.iloc[-2]
    prev = df.iloc[-3]

    # Bullish Engulfing
    if prev['Close'] < prev['Open'] and latest['Close'] > latest['Open']:
        if latest['Open'] < prev['Close'] and latest['Close'] > prev['Open']:
            return "Bullish Engulfing"

    # Bearish Engulfing
    if prev['Close'] > prev['Open'] and latest['Close'] < latest['Open']:
        if latest['Open'] > prev['Close'] and latest['Close'] < prev['Open']:
            return "Bearish Engulfing"

    return "None"

# --- Core Scanner Function ---
def evaluate_with_context(ticker):
    try:
        df = yf.download(ticker, period="10d", interval="1d", auto_adjust=False)
        if df.empty or len(df) < 5:
            return {"ticker": ticker, "score": 0, "recommendation": "ERROR", "pattern": "None", "breakdown": {}, "error": "No data"}

        # Indicators
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().add(1).rolling(window=14).mean()))

        candle = detect_candle_pattern(df)
        volume = df['Volume'].iloc[-1]
        avgvol = df['Volume'].rolling(5).mean().iloc[-1]
        sma20 = df['SMA20'].iloc[-1]
        sma50 = df['SMA50'].iloc[-1]

        trend_type = "Uptrend" if sma20 > sma50 else "Downtrend"
        catalyst = "Volume spike" if volume > 1.3 * avgvol else "None"

        breakdown = {
            "Trend & Momentum": 2 if trend_type == "Uptrend" else 1,
            "Volume Catalyst": 2 if catalyst != "None" else 1,
            "Candle Pattern": 2 if candle in ["Bullish Engulfing", "Bearish Engulfing"] else 1,
            "Fundamentals": 1,
            "Risk/Reward Profile": 1
        }

        score = sum(breakdown.values())
        recommendation = "BUY" if score >= 8 else ("NEUTRAL" if score >= 5 else "AVOID")

        playbook = {
            "entry": "Breakout entry above resistance with volume confirmation",
            "stop": "Place below breakout base or prior pivot",
            "target": "Run to measured move or recent high",
            "options": {
                "conservative": "Vertical bull call spread",
                "aggressive": "Long call with delta 0.40+ and 2-3 week expiry"
            }
        }

        return {
            "ticker": ticker,
            "score": score,
            "recommendation": recommendation,
            "pattern": trend_type,
            "catalyst": catalyst,
            "candle_pattern": candle,
            "indicators": {
                "SMA20": round(sma20, 2),
                "SMA50": round(sma50, 2),
                "RSI": round(df['RSI'].iloc[-1], 2),
                "Volume": f"{volume:,} vs {int(avgvol):,}"
            },
            "breakdown": breakdown,
            "playbook": playbook
        }

    except Exception as e:
        return {"ticker": ticker, "score": 0, "recommendation": "ERROR", "pattern": "None", "breakdown": {}, "error": str(e)}
