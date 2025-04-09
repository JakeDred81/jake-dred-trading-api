# dynamic_market_scanner.py

import yfinance as yf
import pandas as pd

def detect_candle_pattern(df):
    if len(df) < 3:
        return "Insufficient data"

    latest = df.iloc[-2]
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

def evaluate_with_context(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", auto_adjust=False)
        print(f"📊 Raw data for {ticker}:\n{df.tail()}")

        if df.empty or df.isnull().values.any():
            raise ValueError(f"No valid data for {ticker} — DataFrame is empty or has NaNs")

        candle = detect_candle_pattern(df)
        close = df['Close']
        volume = df['Volume'].iloc[-1]
        avgvol = df['Volume'].mean()

        # Indicators
        sma20 = close.rolling(window=20).mean().iloc[-1] if len(close) >= 20 else close.mean()
        sma50 = close.rolling(window=50).mean().iloc[-1] if len(close) >= 50 else close.mean()

        macd_line = close.ewm(span=12).mean() - close.ewm(span=26).mean()
        macd_signal = macd_line.ewm(span=9).mean()
        macd_trend = "Bullish crossover" if macd_line.iloc[-1] > macd_signal.iloc[-1] else "Bearish crossover"

        trend_type = "Uptrend" if sma20 > sma50 else "Downtrend"
        catalyst = "Volume spike" if volume > 1.3 * avgvol else "None"

        recommendation = "BUY" if trend_type == "Uptrend" and macd_trend == "Bullish crossover" else "NEUTRAL"

        breakdown = {
            "Technical Pattern": 2 if recommendation == "BUY" else 1,
            "Trend & Momentum": 2 if trend_type == "Uptrend" else 1,
            "News/Catalyst": 2 if catalyst != "None" else 1,
            "Fundamentals": 1,
            "Risk/Reward Profile": 1
        }

        score = sum(breakdown.values())

        return {
            "ticker": ticker,
            "score": score,
            "recommendation": recommendation,
            "pattern": recommendation.title(),
            "catalyst": catalyst,
            "candle_pattern": candle,
            "indicators": {
                "RSI": 50,
                "MACD": macd_trend,
                "SMA20_vs_SMA50": trend_type,
                "Volume": f"{volume:,} vs {avgvol:,.0f}"
            },
            "breakdown": breakdown,
            "playbook": {
                "entry": "Breakout entry above resistance with volume confirmation",
                "stop": "Place below breakout base or prior pivot",
                "target": "Run to measured move or recent high",
                "options": {
                    "conservative": "Vertical bull call spread",
                    "aggressive": "Long call with delta 0.40+ and 2-3 week expiry"
                }
            }
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "score": 0,
            "recommendation": "ERROR",
            "pattern": "None",
            "breakdown": {},
            "candle_pattern": "None",
            "indicators": {},
            "playbook": {},
            "error_msg": str(e)
        }
