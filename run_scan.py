# run_scan.py

from dynamic_market_scanner import evaluate_with_context

tickers = ["TSLA", "AAPL", "NVDA", "AMD", "QQQ", "MSFT"]

print("🚀 Running full market scan...\n")

for ticker in tickers:
    result = evaluate_with_context(ticker)
    
    print(f"📊 {ticker}")
    print(f"Score: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Pattern: {result.get('pattern', 'None')}")
    print(f"Catalyst: {result.get('catalyst', 'None')}")
    print(f"Candle Pattern: {result.get('candle_pattern', 'None')}")
    
    print("Indicators:")
    for k, v in result.get("indicators", {}).items():
        print(f"  - {k}: {v}")

    print("Breakdown:")
    for k, v in result.get("breakdown", {}).items():
        print(f"  - {k}: {v}")
    
    print("Playbook:")
    playbook = result.get("playbook", {})
    if isinstance(playbook, dict):
        print(f"  - Entry: {playbook.get('entry', 'N/A')}")
        print(f"  - Stop: {playbook.get('stop', 'N/A')}")
        print(f"  - Target: {playbook.get('target', 'N/A')}")
        print("  - Options:")
        for style, strat in playbook.get("options", {}).items():
            print(f"     • {style.capitalize()}: {strat}")
    
    if "error" in result:
        print(f"⚠️ Error: {result['error']}")
    
    print("\n" + "-"*50 + "\n")
