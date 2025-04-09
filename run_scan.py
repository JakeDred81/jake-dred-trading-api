# run_scan.py

import yfinance as yf
from datetime import datetime, timedelta

def run_auto_scan():
    tickers = ["TSLA", "AAPL", "NVDA", "AMD", "QQQ", "MSFT"]
    results = []

    for ticker in tickers:
        df = yf.download(ticker, period="5d", interval="1d")
        print(f"\n📊 Raw data for {ticker}:")
        print(df.tail())

        if df.empty or len(df) < 2:
            continue

        indicators = {}
        close_prices = df["Close"]

        # RSI (simple placeholder)
        change = close_prices.diff().dropna()
        gain = change[change > 0].mean()
        loss = -change[change < 0].mean()
        rs = gain / loss if loss != 0 else 0.01
        rsi = 100 - (100 / (1 + rs))
        indicators["RSI"] = round(rsi, 2)

        # MACD (simplified)
        ema12 = close_prices.ewm(span=12).mean()
        ema26 = close_prices.ewm(span=26).mean()
        macd = ema12 - ema26
        indicators["MACD"] = "Bearish crossover" if macd.iloc[-1] < macd.iloc[-2] else "Bullish crossover"

        # Trend
        sma20 = close_prices.rolling(window=20).mean()
        sma50 = close_prices.rolling(window=50).mean()
        indicators["SMA20_vs_SMA50"] = "Downtrend" if sma20.iloc[-1] < sma50.iloc[-1] else "Uptrend"

        # Volume comparison
        vol = df["Volume"]
        avg_vol = vol[:-1].mean()
        indicators["Volume"] = f"{vol.iloc[-1]:,} vs {avg_vol:,.1f}"

        print(f"🧪 DEBUG — {ticker}")
        print(f"  RSI: {indicators.get('RSI')}")
        print(f"  MACD: {indicators.get('MACD')}")
        print(f"  SMA20_vs_SMA50: {indicators.get('SMA20_vs_SMA50')}")
        print(f"  Volume: {indicators.get('Volume')}")

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
