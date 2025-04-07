# Real bridge between screener and scanner
from yahoo_screener import get_screened_tickers
from dynamic_market_scanner import run_dynamic_scanner

def run_auto_scan(min_price=10, min_volume=1_000_000, limit=10):
    tickers = get_screened_tickers(min_price, min_volume, limit)
    print("\nAuto scanning the following tickers:")
    print(tickers)
    run_dynamic_scanner(tickers)
