# Module: Performance Dashboard – Jake Dred’s Trading Toolbox

from datetime import datetime, timedelta

def generate_dashboard(journal):
    if not journal:
        print("No trades logged.")
        return

    total_wins = 0
    total_losses = 0
    total_capital = 0
    trade_days = {}

    equity_curve = []
    current_equity = 10000  # Starting simulated balance
    base_equity = current_equity

    for trade in journal:
        trade_date = datetime.strptime(trade['Date'], '%Y-%m-%d %H:%M:%S').date()
        key = str(trade_date)
        trade_days[key] = trade_days.get(key, 0) + 1

        capital = trade['Entry']
        total_capital += capital

        if trade['Result']:
            if trade['Result'].lower() == 'win':
                current_equity += capital * 0.1  # Simulated gain
                total_wins += 1
            elif trade['Result'].lower() == 'loss':
                current_equity -= capital * 0.05  # Simulated loss
                total_losses += 1
        equity_curve.append((str(trade_date), current_equity))

    avg_capital = total_capital / len(journal)
    total_trades = total_wins + total_losses

    print("📊 Performance Dashboard")
    print(f"Starting Equity: ${base_equity:,.2f}")
    print(f"Current Equity: ${current_equity:,.2f}")
    print(f"Total Trades: {total_trades}")
    print(f"Win Rate: {(total_wins / total_trades) * 100:.2f}%" if total_trades > 0 else "Win Rate: N/A")
    print(f"Average Capital at Risk per Trade: ${avg_capital:,.2f}")
    print(f"Trade Frequency (days with trades): {len(trade_days)}")
    print("Equity Curve (simulated):")
    for date, value in equity_curve[-7:]:
        print(f"  {date}: ${value:,.2f}")
