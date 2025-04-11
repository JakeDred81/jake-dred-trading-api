# Screener-to-Scanner Bridge – Auto Scan Top Setups from Yahoo Finance

from yahoo_screener import get_screened_tickers
from dynamic_market_scanner import evaluate_with_context

def run_auto_scan(min_price=10, min_volume=1_000_000, limit=10):
    tickers = get_screened_tickers(min_price=min_price, min_volume=min_volume, limit=limit)
    print("\n🚀 Running Full Auto-Scan on Top Screened Tickers...\n")
    
    results = [evaluate_with_context(ticker) for ticker in tickers]
    results.sort(key=lambda x: x['Score'], reverse=True)

    for result in results:
        print(f"{result['Ticker']} - Score: {result['Score']} ({result['Rating']})")
        print(f"Recommendation: {result['Recommendation']}")
        print(f"Pattern: {result['Pattern']} | Catalyst: {result['Catalyst']}")
        print(f"Breakdown: {result['Breakdown']}")
        print("📘 Playbook:")
        for key, value in result['Playbook'].items():
            print(f" - {key}: {value}")
        print("---")
