import yfinance as yf
import pandas as pd

def evaluate_with_context(ticker):
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if df.empty or len(df) < 50:
            return {
                "ticker": ticker,
                "score": 0,
                "recommendation": "ERROR",
                "pattern": "None",
                "breakdown": {},
                "error": "Insufficient data"
            }

        df["SMA20"] = df["Close"].rolling(window=20).mean()
        df["SMA50"] = df["Close"].rolling(window=50).mean()
        df["RSI"] = compute_rsi(df["Close"])
        df["MACD"], df["MACD_signal"] = compute_macd(df["Close"])
        volume_spike = df["Volume"].iloc[-1] > df["Volume"].rolling(window=20).mean().iloc[-1] * 1.5

        trend = "Uptrend" if df["SMA20"].iloc[-1] > df["SMA50"].iloc[-1] else "Downtrend"
        macd_cross = "Bullish crossover" if df["MACD"].iloc[-1] > df["MACD_signal"].iloc[-1] else "Bearish crossover"
        candle = detect_candle_pattern(df)

        breakdown = {
            "Technical Pattern": 2 if trend == "Uptrend" and macd_cross == "Bullish crossover" else 1,
            "Trend & Momentum": 2 if df["RSI"].iloc[-1] > 50 else 1,
            "News/Catalyst": 2 if volume_spike else 1,
            "Fundamentals": 1,  # Placeholder
            "Risk/Reward Profile": 1  # Placeholder
        }

        score = sum(breakdown.values())

        playbook = {
            "entry": "Enter on bullish confirmation near support or breakout level",
            "stop": "Place below recent swing low or support",
            "target": "Run to recent high or resistance",
            "options": {
                "conservative": "Debit call spread (0.30-0.40 delta)",
                "aggressive": "Long call (0.45+ delta, 2-4 week expiry)"
            }
        }

        return {
            "ticker": ticker,
            "score": score,
            "recommendation": "BUY" if score >= 7 else "NEUTRAL",
            "pattern": trend,
            "catalyst": "Volume spike" if volume_spike else "None",
            "candle_pattern": candle,
            "indicators": {
                "RSI": round(df["RSI"].iloc[-1], 2),
                "MACD": macd_cross,
                "SMA20": round(df["SMA20"].iloc[-1], 2),
                "SMA50": round(df["SMA50"].iloc[-1], 2),
                "Volume": int(df["Volume"].iloc[-1])
            },
            "breakdown": breakdown,
            "playbook": playbook
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "score": 0,
            "recommendation": "ERROR",
            "pattern": "None",
            "breakdown": {},
            "error": str(e)
        }

# --- SUPPORT FUNCTIONS ---
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_macd(series, fast=12, slow=26, signal=9):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def detect_candle_pattern(df):
    if len(df) < 3:
        return "Insufficient data"
    latest = df.iloc[-2]
    prev = df.iloc[-3]

    if prev["Close"] < prev["Open"] and latest["Close"] > latest["Open"]:
        if latest["Open"] < prev["Close"] and latest["Close"] > prev["Open"]:
            return "Bullish Engulfing"

    if prev["Close"] > prev["Open"] and latest["Close"] < latest["Open"]:
        if latest["Open"] > prev["Close"] and latest["Close"] < prev["Open"]:
            return "Bearish Engulfing"

    return "None"
