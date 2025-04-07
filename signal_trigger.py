# Realtime Signal Trigger – alerts on strong setups
import time
from datetime import datetime
from dynamic_market_scanner import evaluate_with_context

TOP_TICKERS = ['TSLA', 'NVDA', 'AAPL', 'AMZN', 'AMD', 'MSFT', 'META', 'GOOGL']

def run_signal_scan():
    alerts = []
    for ticker in TOP_TICKERS:
        result = evaluate_with_context(ticker)
        if result["score"] >= 7:
            alerts.append(result)
    
    if alerts:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("alerts_log.txt", "a", encoding="utf-8") as f:
            f.write(f"📡 Signal Alert – {timestamp}\n")
            for alert in alerts:
                f.write(f"{alert['ticker']} – Score: {alert['score']} | Pattern: {alert['pattern']} | Catalyst: {alert['catalyst']}\n")
            f.write("\n")
        print(f"🔔 {len(alerts)} alerts triggered and saved to alerts_log.txt")
    else:
        print("✅ No strong setups at this time.")

if __name__ == "__main__":
    run_signal_scan()
