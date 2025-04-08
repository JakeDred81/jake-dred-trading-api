from dynamic_market_scanner import evaluate_with_context

def run_auto_scan():
    tickers = ["TSLA", "AAPL", "NVDA", "AMD", "QQQ", "MSFT"]
    print("🚀 Running full market scan...\n")
    for ticker in tickers:
        try:
            result = evaluate_with_context(ticker)
            print(f"📊 {ticker}")
            print(f"Score: {result['score']}")
            print(f"Recommendation: {result['recommendation']}")
            print(f"Pattern: {result['pattern']}")
            print("Breakdown:")
            for k, v in result["breakdown"].items():
                print(f"  - {k}: {v}")
            print()
        except Exception as e:
            print(f"❌ Error scanning {ticker}: {e}")