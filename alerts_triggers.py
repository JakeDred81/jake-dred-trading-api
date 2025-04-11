# Module 5: Alerts & Triggers – Jake Dred’s Trading Toolbox

from datetime import datetime

alerts = []

def set_alert(alert_type, symbol=None, condition=None, notes=None):
    alert = {
        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Type': alert_type,
        'Symbol': symbol.upper() if symbol else None,
        'Condition': condition,
        'Notes': notes
    }
    alerts.append(alert)
    print(f"🔔 Alert set: {alert_type} for {symbol.upper() if symbol else 'General'} – {condition}")

def list_alerts():
    if not alerts:
        print("No alerts set.")
        return

    print("\n📡 Active Alerts:")
    for a in alerts:
        print(f"[{a['Date']}] {a['Type']} – {a['Symbol'] or 'General'}: {a['Condition']}")
        if a['Notes']:
            print(f"  Notes: {a['Notes']}")
        print("---")

# Example usage:
# set_alert('Earnings', 'NVDA', 'Earnings report due May 20', 'Watch for volatility spike.')
# set_alert('VIX Spike', None, 'VIX > 20', 'Scale back risk exposure.')
# list_alerts()
