# Real yfinance-based screener
import yfinance as yf

def get_screened_tickers(min_price=10, min_volume=1_000_000, limit=10):
    universe = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'AMZN', 'META', 'AMD']
    filtered = []
    for symbol in universe:
        try:
            data = yf.Ticker(symbol).info
            price = data.get('regularMarketPrice', 0)
            volume = data.get('averageVolume', 0)
            if price >= min_price and volume >= min_volume:
                filtered.append((symbol, price, volume))
        except Exception as e:
            continue
    filtered.sort(key=lambda x: x[2], reverse=True)
    return [sym[0] for sym in filtered[:limit]]
