# Close a trade and log P/L in one go
from datetime import datetime
from performance_tracker import log_performance

def close_and_log(ticker, entry, exit, stop, target, size=1):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    status = "Win" if exit > entry else "Loss" if exit < entry else "Breakeven"
    line = f"[{timestamp}] {ticker.upper()} – Closed: {status} / Exit @ {exit}\n\n"

    try:
        with open("trade_log.txt", "a", encoding="utf-8") as f:
            f.write(line)
        print(f"✅ Trade closed for {ticker.upper()} – Status: {status}")
        log_performance(ticker, entry, exit, stop, target, size)
    except Exception as e:
        print(f"❌ Failed to close and log: {str(e)}")
