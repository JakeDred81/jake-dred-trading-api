# run_scan.py

from dynamic_market_scanner import evaluate_with_context

# List of high-liquidity tickers to scan
DEFAULT_TICKERS = ["AAPL", "TSLA", "NVDA", "AMD", "SPY", "QQQ", "AMZN", "GOOGL", "META", "MSFT"]

def run_auto_scan(tickers=DEFAULT_TICKERS):
    results = []
    for ticker in tickers:
        print(f"📈 Scanning {ticker}...")
        result = evaluate_with_context(ticker)
        results.append(result)
    return results
