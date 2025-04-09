# dynamic_market_scanner.py (Series fix + candle pattern + debug logging + column flattening)

import yfinance as yf
import pandas as pd

# --- Candle Pattern Detector ---
def detect_candle_pattern(df):
    if len(df) < 3:
        return "Insufficient data"

    latest = df.iloc[-2]
    prev = df.iloc[-3]

    try:
        prev_open = float(prev['Open'])
        prev_close = float(prev['Close'])
        latest_open = float(latest['Open'])
        latest_close = float(latest['Close'])
    except Exception as e:
        return f"Error: {e}"

    # Bullish Engulfing
    if (prev_close < prev_open and latest_close > latest_open and
        latest_open < prev_close and latest_close > prev_open):
        return "Bullish Engulfing"

    # Bearish Engulfing
    if (prev_close > prev_open and latest_close < latest_open and
        latest_open > prev_close and latest_close < prev_open):
        return "Bearish Engulfing"

    return "None"

# --- Core Scanner Function ---
def evaluate_with_context(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", auto_adjust=False)

        # If multi-indexed (due to multiple tickers or metadata), flatten it
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(0)

        print(f"📊 Raw data for {ticker}:")
        print(df.tail())

        if df.empty or df.isnull().values.any():
            raise ValueError(f"No valid data for {ticker} — DataFrame is empty or has NaNs")

        candle = detect_candle_pattern(df)

        sma20 = df['Close'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else df['Close'].mean()
        sma50 = df['Close'].rolling(window=50).mean().iloc[-1] if len(df) >= 50 else df['Close'].mean()
        rsi = 50  # Placeholder for future calc
        volume = df['Volume'].iloc[-1]
        avgvol = df['Volume'].mean()

        macd = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
        macd_signal = macd.ewm(span=9).mean()
        macd_trend = "Bullish crossover" if macd.iloc[-1] > macd_signal.iloc[-1] else "Bearish crossover"

        trend_type = "Uptrend" if sma20 > sma50 else "Downtrend"
        catalyst = "Volume spike" if volume > 1.3 * avgvol else "None"

        rec = "BUY" if trend_type == "Uptrend" and macd_trend == "Bullish crossover" else "NEUTRAL"

        breakdown = {
            "Technical Pattern": 2 if rec == "BUY" else 1,
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
            "recommendation": rec,
            "pattern": rec.title(),
            "catalyst": catalyst,
            "candle_pattern": candle,
            "indicators": {
                "RSI": round(rsi, 2),
                "MACD": macd_trend,
                "SMA20_vs_SMA50": trend_type,
                "Volume": f"{volume:,} vs {avgvol:,}"
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
