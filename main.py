from flask import Flask, request, jsonify, send_from_directory
import os
from run_scan import run_auto_scan, run_manual_scan
from datetime import datetime

app = Flask(__name__)

# Serve the OpenAPI spec for plugin import
@app.route('/openapi.json')
def openapi_spec():
    return send_from_directory(os.path.dirname(__file__), 'openapi.json')

@app.route('/')
def home():
    return "Jake Dred API is Live"

@app.route('/healthz')
def healthz():
    return "OK", 200

@app.route('/scan')
def scan():
    ticker = request.args.get('ticker')
    context = request.args.get('context', None)
    if context == 'auto':
        result = run_auto_scan(ticker)
    else:
        result = run_manual_scan(ticker)

    # Normalize result: if tuple (score, breakdown), convert to dict
    if isinstance(result, tuple) and len(result) == 2:
        score, breakdown = result
        payload = {
            "ticker": ticker,
            "score": score,
            "breakdown": breakdown,
        }
    elif isinstance(result, dict):
        payload = result.copy()
    else:
        return jsonify({"error": "Unexpected scan result format"}), 500

    payload["fetched_at"] = datetime.utcnow().isoformat() + "Z"
    return jsonify(payload)

@app.route('/autoscan')
def autoscan():
    ticker = request.args.get('ticker')
    result = run_auto_scan(ticker)

    # Normalize result as above
    if isinstance(result, tuple) and len(result) == 2:
        score, breakdown = result
        payload = {
            "ticker": ticker,
            "score": score,
            "breakdown": breakdown,
        }
    elif isinstance(result, dict):
        payload = result.copy()
    else:
        return jsonify({"error": "Unexpected autoscan result format"}), 500

    payload["fetched_at"] = datetime.utcnow().isoformat() + "Z"
    return jsonify(payload)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
