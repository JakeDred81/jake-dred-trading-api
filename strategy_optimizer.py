# Strategy Optimizer – Analyzes log data for win rates and R:R by strategy/pattern

import re
from collections import defaultdict
from datetime import datetime

def parse_performance_log(filepath="performance_log.txt"):
    data = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            try:
                date_str = line.split("]")[0].replace("[", "")
                date = datetime.strptime(date_str, "%Y-%m-%d")
                ticker = line.split("]")[1].split("–")[0].strip()
                status = "Win" if "Win" in line else "Loss" if "Loss" in line else "Breakeven"
                pnl = float(re.search(r"P/L: \$(\-?\d+\.?\d*)", line).group(1))
                rr_match = re.search(r"R:R: (\d+\.?\d*)", line)
                rr = float(rr_match.group(1)) if rr_match else 0
                pct_match = re.search(r"\((\-?\d+\.?\d*)%\)", line)
                pct_return = float(pct_match.group(1)) if pct_match else 0
                data.append((ticker, status, pnl, pct_return, rr))
            except:
                continue
    return data

def parse_strategy_context(filepath="trade_log.txt"):
    context = {}
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("[") and "–" in lines[i]:
                ticker_line = lines[i]
                details_line = lines[i + 1] if i + 1 < len(lines) else ""
                try:
                    ticker = ticker_line.split("]")[1].split()[0]
                    pattern = re.search(r"Pattern: ([^/]+)", details_line).group(1).strip()
                    strategy = re.search(r"Strategy: ([^/]+)", details_line).group(1).strip()
                    context[ticker.upper()] = (pattern, strategy)
                except:
                    continue
    return context

def analyze():
    perf_data = parse_performance_log()
    context_data = parse_strategy_context()

    results = defaultdict(lambda: {
        "count": 0,
        "wins": 0,
        "total_rr": 0,
        "total_pct": 0,
        "pnl": 0
    })

    for ticker, status, pnl, pct, rr in perf_data:
        pattern, strategy = context_data.get(ticker, ("Unknown", "Unknown"))
        key = f"{pattern} / {strategy}"

        results[key]["count"] += 1
        results[key]["wins"] += 1 if status == "Win" else 0
        results[key]["total_rr"] += rr
        results[key]["total_pct"] += pct
        results[key]["pnl"] += pnl

    print("📊 Strategy Performance Breakdown")
    print("======================================")
    for strat, stats in sorted(results.items(), key=lambda x: x[1]["pnl"], reverse=True):
        count = stats["count"]
        wins = stats["wins"]
        avg_rr = round(stats["total_rr"] / count, 2)
        avg_pct = round(stats["total_pct"] / count, 2)
        win_rate = round((wins / count) * 100, 2)
        pnl = round(stats["pnl"], 2)

        print(f"{strat}")
        print(f"  Trades: {count} | Win Rate: {win_rate}% | Avg R:R: {avg_rr} | Avg Return: {avg_pct}% | Total P/L: ${pnl}")
        print("")

if __name__ == "__main__":
    analyze()
