# CSV Importer – Bulk imports trades and logs into journal + performance

import csv
from datetime import datetime
from trade_logger import log_trade
from performance_tracker import log_performance

def import_trades_from_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        imported = 0

        for row in reader:
            try:
                ticker = row["ticker"].upper()
                entry = float(row["entry"])
                stop = float(row["stop"])
                target = float(row["target"])
                exit_price = float(row["exit"])
                score = int(row["score"])
                pattern = row["pattern"]
                strategy = row["strategy"]
                outcome = row.get("outcome", "Closed")
                size = float(row.get("size", 1))

                log_trade(ticker, entry, stop, target, score, pattern, strategy, outcome)
                log_performance(ticker, entry, exit_price, stop, target, size)
                imported += 1

            except Exception as e:
                print(f"⚠️ Error importing row: {row} → {e}")

    print(f"✅ {imported} trades imported and logged.")

if __name__ == "__main__":
    import_trades_from_csv("trades.csv")
