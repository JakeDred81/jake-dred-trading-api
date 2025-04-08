from flask import Flask, request, jsonify
from tradingview_ta import TA_Handler, Interval, Exchange
from datetime import datetime
from trade_logger import log_trade
from performance_tracker import log_performance
from combined_trade_closer import close_and_log
from dynamic_market_scanner import evaluate_with_context
from strategy_optimizer import analyze as run_strategy_analysis
from signal_trigger import run_signal_scan

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Jake Dred Trading Assistant API is Live."

@app.route("/scan", methods=["GET", "POST"])
def scan():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Ticker is required"}), 400
    try:
        result = evaluate_with_context(ticker.upper())
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/log_trade", methods=["POST"])
def log_trade_api():
    data = request.json
    try:
        log_trade(
            data["ticker"],
            float(data["entry"]),
            float(data["stop"]),
            float(data["target"]),
            int(data["score"]),
            data["pattern"],
            data["strategy"],
            data.get("outcome", "Open")
        )
        return jsonify({"message": "✅ Trade logged"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/close_trade", methods=["POST"])
def close_trade_api():
    data = request.json
    try:
        close_and_log(
            data["ticker"],
            float(data["entry"]),
            float(data["exit"]),
            float(data["stop"]),
            float(data["target"]),
            float(data.get("size", 1))
        )
        return jsonify({"message": "✅ Trade closed and performance logged"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/log_performance", methods=["POST"])
def log_performance_api():
    data = request.json
    try:
        log_performance(
            data["ticker"],
            float(data["entry"]),
            float(data["exit"]),
            float(data["stop"]),
            float(data["target"]),
            float(data.get("size", 1))
        )
        return jsonify({"message": "📈 Performance logged"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/strategy_review", methods=["GET"])
def strategy_review():
    try:
        import io
        import sys
        buffer = io.StringIO()
        sys.stdout = buffer
        run_strategy_analysis()
        sys.stdout = sys.__stdout__
        output = buffer.getvalue()
        return jsonify({"strategy_review": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/signals", methods=["GET"])
def signal_check():
    try:
        run_signal_scan()
        return jsonify({"message": "📡 Signal scan completed."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
