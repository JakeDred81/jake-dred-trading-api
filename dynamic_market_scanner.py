# dynamic_market_scanner.py (fully upgraded)

from tradingview_ta import TA_Handler, Interval, Exchange
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
        handler = TA_Handler(
            symbol=ticker,
            screener="america",
            exchange="NASDAQ",
            interval=Interval.INTERVAL_1_DAY
        )
        analysis = handler.get_analysis()

        df = yf.download(ticker, period="5d", interval="1d")
        candle = detect_candle_pattern(df)

        summary = analysis.summary
        indicators = analysis.indicators
        rec = summary.get("RECOMMENDATION", "NEUTRAL")
        rsi = indicators.get("RSI", 0)
        macd = indicators.get("MACD.macd", 0)
        macd_signal = indicators.get("MACD.signal", 0)
        sma20 = indicators.get("SMA20", 0)
        sma50 = indicators.get("SMA50", 0)
        volume = indicators.get("volume", 0)
        avgvol = indicators.get("avgvol", 1)

        macd_trend = "Bullish crossover" if macd > macd_signal else "Bearish crossover"
        trend_type = "Uptrend" if sma20 > sma50 else "Downtrend"
        catalyst = "Volume spike" if volume > 1.3 * avgvol else "None"

        breakdown = {
            "Technical Pattern": 2 if rec in ["BUY", "STRONG_BUY"] else 1,
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
        return {"error": str(e)}
