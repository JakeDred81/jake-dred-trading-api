# Daily Review Commander – UTF-8 safe version

from auto_scan_bridge import run_auto_scan

def run_journal_summary():
    print("\n📓 Trade Journal Summary:")
    try:
        with open("trade_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                print("No trades logged yet.")
            else:
                print("".join(lines[-5:]))
    except FileNotFoundError:
        print("No journal file found.")

def run_portfolio_check():
    print("\n💼 Portfolio Exposure Monitor:")
    try:
        with open("portfolio_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                print("No positions logged.")
            else:
                print("".join(lines))
    except FileNotFoundError:
        print("No portfolio log found.")

def run_alerts_check():
    print("\n🔔 Alerts Triggered:")
    try:
        with open("alerts_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                print("No alerts set.")
            else:
                print("".join(lines))
    except FileNotFoundError:
        print("No alert file found.")

def run_performance_dashboard():
    print("\n📈 Performance Dashboard:")
    try:
        with open("performance_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                print("No performance data.")
            else:
                print("".join(lines[-10:]))
    except FileNotFoundError:
        print("No performance data found.")

def run_daily_review():
    print("🧠 Jake Dred's Daily Review – Live Tactical Feed")
    print("===============================================")
    run_auto_scan()
    run_journal_summary()
    run_portfolio_check()
    run_alerts_check()
    run_performance_dashboard()
    print("===============================================")
    print("Review Complete. Stay sharp, stay deadly.")

run_daily_review()
