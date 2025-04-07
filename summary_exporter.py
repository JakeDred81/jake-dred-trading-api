# Summary Exporter – Dumps recent trades + performance into a report file

from datetime import datetime, timedelta

def read_file_lines(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def extract_last_week(lines):
    cutoff = datetime.now() - timedelta(days=7)
    out = []
    current_block = []

    for line in lines:
        if line.strip().startswith("[") and "]" in line:
            try:
                timestamp = line.split("]")[0].replace("[", "")
                date_obj = datetime.strptime(timestamp, "%Y-%m-%d")
                if date_obj >= cutoff:
                    if current_block:
                        out.extend(current_block)
                    current_block = [line]
                else:
                    current_block = []
            except:
                current_block = []
        else:
            current_block.append(line)
    out.extend(current_block)
    return out

def generate_summary():
    trade_lines = read_file_lines("trade_log.txt")
    perf_lines = read_file_lines("performance_log.txt")

    recent_trades = extract_last_week(trade_lines)
    recent_performance = extract_last_week(perf_lines)

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"weekly_summary_{date_str}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("📝 Weekly Trade Summary (Last 7 Days)\n")
        f.write("=====================================\n\n")
        f.writelines(recent_trades)
        f.write("\n📈 Performance Log\n")
        f.write("=====================================\n\n")
        f.writelines(recent_performance)

    print(f"✅ Summary exported to {filename}")

if __name__ == "__main__":
    generate_summary()
