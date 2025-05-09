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
        # autoscan logic when context flag is set
        score, breakdown = run_auto_scan(ticker)
    else:
        score, breakdown = run_manual_scan(ticker)
    return jsonify({
        "ticker": ticker,
        "score": score,
        "breakdown": breakdown,
        "fetched_at": datetime.utcnow().isoformat() + "Z"
    })

@app.route('/autoscan')
def autoscan():
    ticker = request.args.get('ticker')
    score, breakdown = run_auto_scan(ticker)
    return jsonify({
        "ticker": ticker,
        "score": score,
        "breakdown": breakdown,
        "fetched_at": datetime.utcnow().isoformat() + "Z"
    })

if __name__ == "__main__":
    # Use PORT env var if provided by hosting service
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
