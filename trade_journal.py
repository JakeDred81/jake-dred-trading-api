# Module 3: Trade Journal – Jake Dred’s Trading Toolbox

from datetime import datetime

# In-memory journal (can be replaced with persistent storage later)
trade_journal = []

def log_trade(ticker, entry_price, stop_loss, target_price, trade_score, notes):
    trade = {
        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Ticker': ticker.upper(),
        'Entry': entry_price,
        'Stop': stop_loss,
        'Target': target_price,
        'Score': trade_score,
        'Pre-Notes': notes,
        'Exit': None,
        'Result': None,
        'Post-Notes': None
    }
    trade_journal.append(trade)
    print(f"✅ Logged trade for {ticker.upper()}")

def close_trade(ticker, exit_price, result, post_notes):
    for trade in reversed(trade_journal):
        if trade['Ticker'] == ticker.upper() and trade['Exit'] is None:
            trade['Exit'] = exit_price
            trade['Result'] = result
            trade['Post-Notes'] = post_notes
            print(f"📌 Closed trade for {ticker.upper()}")
            return
    print(f"⚠️ No open trade found for {ticker.upper()}")

def show_trades():
    print("\n📓 Trade Journal Summary:")
    for trade in trade_journal:
        print(f"[{trade['Date']}] {trade['Ticker']}: Score {trade['Score']}")
        print(f"Entry: {trade['Entry']} | Stop: {trade['Stop']} | Target: {trade['Target']}")
        print(f"Pre-Trade Notes: {trade['Pre-Notes']}")
        if trade['Exit']:
            print(f"Exit: {trade['Exit']} | Result: {trade['Result']}")
            print(f"Post-Trade Notes: {trade['Post-Notes']}")
        else:
            print("Status: Open Trade")
        print("---")
