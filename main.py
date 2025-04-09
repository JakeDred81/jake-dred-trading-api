# main.py — Flask API for Trading Scanner (fixed version)

from flask import Flask, jsonify
from dynamic_market_scanner import evaluate_with_context

app = Flask(__name__)

@app.route("/scan", methods=["POST"])
def scan():
    tickers = ["TSLA", "AAPL", "NVDA", "AMD", "QQQ", "MSFT"]
    results = []

    print("🚀 Running full market scan...\n")

    for ticker in tickers:
        result = evaluate_with_context(ticker)
        results.append(result)

    return jsonify(scan_results=results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
