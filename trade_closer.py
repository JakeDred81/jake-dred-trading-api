# Close a trade and append the outcome to the journal
from datetime import datetime

def close_trade(ticker, exit_note="Closed", status="Win"):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    line = f"[{timestamp}] {ticker.upper()} – Closed: {status} / {exit_note}\n\n"

    try:
        with open("trade_log.txt", "a", encoding="utf-8") as f:
            f.write(line)
        print(f"✅ Trade closed for {ticker.upper()} – Status: {status}")
    except Exception as e:
        print(f"❌ Failed to close trade: {str(e)}")
