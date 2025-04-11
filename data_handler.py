
import requests
import yfinance as yf

TRADINGVIEW_URL = "https://scanner.tradingview.com/america/scan"

def pull_tradingview_data(tickers):
    payload = {
        "symbols": {
            "tickers": tickers,
            "query": {"types": []}
        },
        "columns": ["close", "volume", "rsi", "change"]
    }

    try:
        response = requests.post(TRADINGVIEW_URL, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        results = {}
        for item in data.get('data', []):
            symbol = item.get('s')
            d = item.get('d', [])
            results[symbol] = {
                'close': d[0],
                'volume': d[1],
                'rsi': d[2],
                'change_percent': d[3]
            }
        return results

    except Exception as e:
        print(f"TradingView pull failed: {e}")
        return None

def pull_yf_data(tickers):
    results = {}
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="1d", interval="1m")
            if not hist.empty:
                last = hist.iloc[-1]
                results[ticker] = {
                    'close': last['Close'],
                    'volume': last['Volume'],
                    'rsi': 50,  # Placeholder
                    'change_percent': ((last['Close'] - hist.iloc[0]['Open']) / hist.iloc[0]['Open']) * 100
                }
        except Exception as e:
            print(f"yfinance pull failed for {ticker}: {e}")
    return results

def get_realtime_data(tickers):
    data = pull_tradingview_data(tickers)
    if data:
        return data
    else:
        print("Falling back to yfinance...")
        return pull_yf_data(tickers)
