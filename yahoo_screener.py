# yahoo_screener.py

import yfinance as yf

def get_top_volume_tickers(min_price=10, min_volume=1_000_000, limit=20):
    tickers = ["AAPL", "TSLA", "NVDA", "AMD", "SPY", "QQQ", "AMZN", "GOOGL", "META", "MSFT"]
    filtered = []

    for ticker in tickers:
        try:
            data = yf.download(ticker, period="5d", interval="1d", progress=False)
            if data.empty:
                continue

            latest = data.iloc[-1]
            price = latest["Close"]
            volume = latest["Volume"]

            if price >= min_price and volume >= min_volume:
                filtered.append((ticker, volume))
        except Exception:
            continue

    sorted_tickers = sorted(filtered, key=lambda x: x[1], reverse=True)
    return [t[0] for t in sorted_tickers[:limit]]
