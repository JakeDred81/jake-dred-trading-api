# Performance Tracker – Log P/L, percent return, R:R

from datetime import datetime

def log_performance(ticker, entry_price, exit_price, stop_price, target_price, position_size=1):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Calculations
    pnl = round((exit_price - entry_price) * position_size, 2)
    pct_return = round(((exit_price - entry_price) / entry_price) * 100, 2)
    risk = entry_price - stop_price
    reward = target_price - entry_price
    rr_ratio = round(reward / risk, 2) if risk != 0 else "∞"

    # Status
    status = "Win" if exit_price > entry_price else "Loss" if exit_price < entry_price else "Breakeven"
    line = (f"[{timestamp}] {ticker.upper()} – {status} | Entry: {entry_price} → Exit: {exit_price} | "
            f"P/L: ${pnl} ({pct_return}%) | R:R: {rr_ratio}\n")

    try:
        with open("performance_log.txt", "a", encoding="utf-8") as f:
            f.write(line)
        print(f"📈 Performance logged for {ticker.upper()} – {status} (${pnl}, {pct_return}%)")
    except Exception as e:
        print(f"❌ Failed to log performance: {str(e)}")
