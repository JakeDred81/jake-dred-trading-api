import json
import os


ALERTS_FILE = "alerts.json"


def load_alerts():
    if not os.path.exists(ALERTS_FILE):
        return []

    with open(ALERTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_alerts(alerts):
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=4)


def add_alert(symbol, condition, note=""):
    alerts = load_alerts()
    alerts.append({"symbol": symbol, "condition": condition, "note": note})
    save_alerts(alerts)


def remove_alert(symbol, condition):
    alerts = load_alerts()
    alerts = [a for a in alerts if not (a["symbol"] == symbol and a["condition"] == condition)]
    save_alerts(alerts)


def list_alerts():
    return load_alerts()


# NEW REQUIRED FUNCTION FOR run_scan.py
def check_alerts(tickers):
    alerts_triggered = []

    alerts = load_alerts()

    for alert in alerts:
        if alert["symbol"] in tickers:
            alerts_triggered.append({
                "symbol": alert["symbol"],
                "condition": alert["condition"],
                "note": alert.get("note", "")
            })

    return alerts_triggered
