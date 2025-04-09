# main.py

from flask import Flask, jsonify
from run_scan import run_auto_scan
from yahoo_screener import get_top_volume_tickers

app = Flask(__name__)

@app.route("/")
def home():
    return "Jake Dred's Trading Toolbox is live."

@app.route("/scan")
def scan():
    return jsonify(run_auto_scan())

@app.route("/autoscan", methods=["GET"])
def autoscan():
    try:
        # Dynamically pull top tickers
        tickers = get_top_volume_tickers(min_price=10, min_volume=1_000_000, limit=20)
        results = run_auto_scan(tickers=tickers)
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
