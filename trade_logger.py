# Trade Logger – Logs formatted trade entries to trade_log.txt

from datetime import datetime

def log_trade(ticker, entry_price, stop_price, target_price, score, pattern, strategy, outcome="Open"):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    line1 = f"[{timestamp}] {ticker.upper()} Long @ {entry_price} → Stop {stop_price} / Target {target_price} / Score {score}\n"
    line2 = f"Pattern: {pattern} / Strategy: {strategy} / Outcome: {outcome}\n\n"

    try:
        with open("trade_log.txt", "a", encoding="utf-8") as file:
            file.write(line1)
            file.write(line2)
        print(f"✅ Trade logged for {ticker.upper()}")
    except Exception as e:
        print(f"❌ Failed to log trade: {str(e)}")
