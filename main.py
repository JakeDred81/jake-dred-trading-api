from flask import Flask, request, jsonify
from run_scan import run_auto_scan, run_manual_scan

app = Flask(__name__)

@app.route('/')
def home():
    return "Jake Dred API is Live"

@app.route('/healthz')
def healthz():
    # Simple health-check endpoint for keep-alive pings
    return "OK", 200

@app.route('/scan')
def scan():
    ticker = request.args.get('ticker')
    context = request.args.get('context', None)
    if context:
        score, breakdown = run_auto_scan(ticker, context)
    else:
        score, breakdown = run_manual_scan(ticker)
    return jsonify({"ticker": ticker, "score": score, "breakdown": breakdown})

if __name__ == "__main__":
    # For local development only; Render uses Gunicorn
    app.run(host="0.0.0.0", port=5000)
