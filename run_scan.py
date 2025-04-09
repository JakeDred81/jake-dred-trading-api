# run_scan.py

import yfinance as yf
from datetime import datetime, timedelta

def run_auto_scan():
    tickers = ["TSLA", "AAPL", "NVDA", "AMD", "QQQ", "MSFT"]
    results = []

    for ticker in tickers:
        df = yf.download(ticker, period="60d", interval="1d")
        print(f"\n📊 Raw data for {ticker}:")
        print(df.tail())

        if df.empty or len(df) < 30:
            continue

        indicators = {}
        close_prices = df["Close"]

        # RSI (14-day)
        delta = close_prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        indicators["RSI"] = round(rsi.iloc[-1], 2)

        # MACD
        ema12 = close_prices.ewm(span=12, adjust=False).mean()
        ema26 = close_prices.ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()

        if macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2]:
            indicators["MACD"] = "Bullish crossover"
        elif macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-2] >= signal_line.iloc[-2]:
            indicators["MACD"] = "Bearish crossover"
        else:
            indicators["MACD"] = "Flat"

        # Trend
        sma20 = close_prices.rolling(window=20).mean()
        sma50 = close_prices.rolling(window=50).mean()
        indicators["SMA20_vs_SMA50"] = "Downtrend" if sma20.iloc[-1] < sma50.iloc[-1] else "Uptrend"

        # Volume comparison
        vol = df["Volume"]
        avg_vol = vol[:-1].mean()
        indicators["Volume"] = f"{vol.iloc[-1]:,} vs {avg_vol:,.1f}"

        print(f"🧪 DEBUG — {ticker}")
        for key, val in indicators.items():
            print(f"  {key}: {val}")

        breakdown = {
            "Technical Pattern": 1,
            "Trend & Momentum": 1,
            "News/Catalyst": 1,
            "Fundamentals": 1,
            "Risk/Reward Profile": 1
        }

        playbook = {
            "entry": "Breakout entry above resistance with volume confirmation",
            "stop": "Place below breakout base or prior pivot",
            "target": "Run to measured move or recent high",
            "options": {
                "conservative": "Vertical bull call spread",
                "aggressive": "Long call with delta 0.40+ and 2-3 week expiry"
            }
        }

        scan = {
            "ticker": ticker,
            "score": 5,
            "recommendation": "NEUTRAL",
            "pattern": "Neutral",
            "catalyst": "None",
            "candle_pattern": "None",
            "indicators": indicators,
            "breakdown": breakdown,
            "playbook": playbook
        }

        results.append(scan)

    return results
