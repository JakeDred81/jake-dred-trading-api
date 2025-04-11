# Weekly Trade Summary – Jake Dred’s Trading Toolbox

from datetime import datetime, timedelta

def summarize_weekly_performance(journal):
    if not journal:
        print("No trades logged.")
        return

    one_week_ago = datetime.now() - timedelta(days=7)
    recent_trades = [t for t in journal if datetime.strptime(t['Date'], '%Y-%m-%d %H:%M:%S') >= one_week_ago]

    if not recent_trades:
        print("No trades recorded in the last 7 days.")
        return

    wins = sum(1 for t in recent_trades if t['Result'] and t['Result'].lower() == 'win')
    losses = sum(1 for t in recent_trades if t['Result'] and t['Result'].lower() == 'loss')
    total = wins + losses
    avg_score = sum(t['Score'] for t in recent_trades if t['Score'] is not None) / len(recent_trades)
    high_score = max(recent_trades, key=lambda t: t['Score'])
    low_score = min(recent_trades, key=lambda t: t['Score'])

    print("📊 Weekly Trade Performance Summary")
    print(f"Total Trades: {total}")
    print(f"Wins: {wins} | Losses: {losses} | Win Rate: {wins / total * 100:.2f}%" if total > 0 else "No closed trades to analyze.")
    print(f"Average Score: {avg_score:.2f}")
    print(f"Highest Scoring Trade: {high_score['Ticker']} (Score: {high_score['Score']})")
    print(f"Lowest Scoring Trade: {low_score['Ticker']} (Score: {low_score['Score']})")
