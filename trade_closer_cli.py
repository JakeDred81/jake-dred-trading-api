# CLI Trade Closer – Interactive closer + optional performance logging
from combined_trade_closer import close_and_log

def prompt_close_trade():
    print("📉 Close a Trade")

    ticker = input("Ticker: ").upper()
    entry = float(input("Entry Price: "))
    exit_price = float(input("Exit Price: "))
    stop = float(input("Stop Price: "))
    target = float(input("Target Price: "))
    size = input("Position Size (default = 1): ")
    size = float(size) if size else 1

    close_and_log(ticker, entry, exit_price, stop, target, size)

if __name__ == "__main__":
    prompt_close_trade()
