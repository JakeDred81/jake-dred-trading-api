# dynamic_market_scanner.py (TradingView-Free Version)

import yfinance as yf
import pandas as pd
import numpy as np

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

# --- RSI Calculation ---
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# --- MACD Calculation ---
def calculate_macd(series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

# --- Core Scanner Function ---
def evaluate_with_context(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d")
        if df.empty:
            return {"score": 0, "recommendation": "ERROR", "pattern": "None", "breakdown": {}}

        df.dropna(inplace=True)

        close = df['Close']
        volume = df['Volume']
        avgvol = volume.rolling(window=20).mean()
        sma20 = close.rolling(window=20).mean()
        sma50 = close.rolling(window=50).mean()
        rsi = calculate_rsi(close).iloc[-1]
        macd, macd_signal = calculate_macd(close)

        macd_trend = "Bullish crossover" if macd.iloc[-1] > macd_signal.iloc[-1] else "Bearish crossover"
        trend_type = "Uptrend" if sma20.iloc[-1] > sma50.iloc[-1] else "Downtrend"
        catalyst = "Volume spike" if volume.iloc[-1] > 1.3 * avgvol.iloc[-1] else "None"
        candle = detect_candle_pattern(df)

        recommendation = "BUY" if trend_type == "Uptrend" and macd_trend == "Bullish crossover" and rsi < 70 else "NEUTRAL"

        breakdown = {
            "Technical Pattern": 2 if recommendation == "BUY" else 1,
            "Trend & Momentum": 2 if trend_type == "Uptrend" else 1,
            "News/Catalyst": 2 if catalyst != "None" else 1,
            "Fundamentals": 1,
            "Risk/Reward Profile": 1
        }

        score = sum(breakdown.values())

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
            "pattern": recommendation,
            "catalyst": catalyst,
            "candle_pattern": candle,
            "indicators": {
                "RSI": round(rsi, 2),
                "MACD": macd_trend,
                "SMA20_vs_SMA50": trend_type,
                "Volume": f"{volume.iloc[-1]:,} vs {avgvol.iloc[-1]:,}"
            },
            "breakdown": breakdown,
            "playbook": playbook
        }

    except Exception as e:
        return {"error": str(e)}
