# Module: Daily Review Workflow – Jake Dred’s Trading Toolbox

from datetime import datetime, timedelta

def run_daily_review(journal, portfolio, alerts):
    print("\n🧠 Jake Dred’s Daily Review –", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print("\n1. 📊 Market Scanner (Simulated)")
    from market_scanner import run_market_scanner
    run_market_scanner()

    print("\n2. 📝 Trade Journal Summary")
    if not journal:
        print("No trades logged.")
    else:
        for trade in journal[-5:]:  # show last 5 entries
            print(f"[{trade['Date']}] {trade['Ticker']} – Entry: {trade['Entry']}, Score: {trade['Score']}, Result: {trade['Result'] or 'Open'}")

    print("\n3. 💼 Portfolio Exposure")
    total_equity = 2000  # can be adjusted manually
    from portfolio_exposure_monitor import portfolio_summary
    portfolio_summary(total_equity)

    print("\n4. 🔔 Active Alerts")
    if not alerts:
        print("No alerts set.")
    else:
        for a in alerts:
            print(f"[{a['Date']}] {a['Type']} – {a['Symbol'] or 'General'}: {a['Condition']}")
            if a['Notes']:
                print(f"  Notes: {a['Notes']}")
            print("---")

    print("\n5. 📈 Performance Snapshot")
    from performance_dashboard import generate_dashboard
    generate_dashboard(journal)
