# Yahoo Screener Module – Pull Tickers Based on Liquidity & Price
import yfinance as yf

def get_screened_tickers(min_price=10, min_volume=1_000_000, limit=10):
    # Example large-cap tickers to screen (expandable)
    universe = [
        'AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'AMZN', 'META', 'AMD',
        'NFLX', 'INTC', 'BA', 'JPM', 'WMT', 'XOM', 'CVX', 'T', 'KO', 'PEP',
        'DIS', 'PYPL', 'CRM', 'SNOW', 'UBER', 'LULU', 'SHOP', 'FDX', 'ORCL',
        'MU', 'SPY', 'QQQ'
    ]

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

    filtered.sort(key=lambda x: x[2], reverse=True)  # sort by volume
    top_symbols = [sym[0] for sym in filtered[:limit]]

    print(f"📈 Top {limit} tickers screened from Yahoo Finance:")
    for sym, price, volume in filtered[:limit]:
        print(f" - {sym} | Price: ${price:.2f} | Avg Vol: {volume:,}")
    return top_symbols
