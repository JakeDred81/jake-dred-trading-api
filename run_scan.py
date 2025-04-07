from auto_scan_bridge import run_auto_scan

# Run the full screener → scanner pipeline
run_auto_scan(min_price=10, min_volume=1_000_000, limit=10)
