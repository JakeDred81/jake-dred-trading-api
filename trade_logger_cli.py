# Interactive Trade Logger (CLI)
from trade_logger import log_trade

def prompt_trade():
    print("📝 New Trade Entry")
    ticker = input("Ticker: ").upper()
    entry = float(input("Entry Price: "))
    stop = float(input("Stop Loss: "))
    target = float(input("Target Price: "))
    score = int(input("Trade Score (1–10): "))
    pattern = input("Pattern (e.g., Breakout, Pullback): ")
    strategy = input("Strategy (e.g., Bull Call Spread, Naked Call): ")
    outcome = input("Outcome (Open/Closed): ") or "Open"

    log_trade(ticker, entry, stop, target, score, pattern, strategy, outcome)

if __name__ == "__main__":
    prompt_trade()
