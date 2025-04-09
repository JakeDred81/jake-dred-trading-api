# run_scan.py

from dynamic_market_scanner import evaluate_with_context

tickers = ["TSLA", "AAPL", "NVDA", "AMD", "QQQ", "MSFT"]

def run_auto_scan():
    scan_results = []

    print("🚀 Running full market scan...\n")

    for ticker in tickers:
        try:
            result = evaluate_with_context(ticker)
            result["ticker"] = ticker  # Include ticker for external modules
            scan_results.append(result)
        except Exception as e:
            scan_results.append({
                "ticker": ticker,
                "error": str(e)
            })

    return scan_results
