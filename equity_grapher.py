# Equity Curve Grapher – plots cumulative P/L from performance_log.txt

import matplotlib.pyplot as plt
from datetime import datetime
import os

def parse_performance_log(filepath="performance_log.txt"):
    data = []
    if not os.path.exists(filepath):
        print("⚠️ No performance log found.")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("[") and "]" in line and "P/L:" in line:
                try:
                    date_str = line.split("]")[0][1:]
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    pl_str = line.split("P/L: $")[1].split(" ")[0]
                    pnl = float(pl_str.replace(",", ""))
                    data.append((date, pnl))
                except:
                    continue
    return data

def plot_equity_curve(data):
    if not data:
        print("⚠️ No data to plot.")
        return

    data.sort()
    dates = [d[0] for d in data]
    cumulative_pnl = []
    total = 0
    for _, pnl in data:
        total += pnl
        cumulative_pnl.append(total)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, cumulative_pnl, marker='o')
    plt.title("Equity Curve – Cumulative P/L")
    plt.xlabel("Date")
    plt.ylabel("Total P/L ($)")
    plt.grid(True)
    plt.tight_layout()

    filename = "equity_curve.png"
    plt.savefig(filename)
    plt.close()
    print(f"📈 Equity curve saved as {filename}")

if __name__ == "__main__":
    trades = parse_performance_log()
    plot_equity_curve(trades)
