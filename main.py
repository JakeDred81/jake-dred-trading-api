from flask import Flask, request, jsonify
from run_scan import run_auto_scan, run_manual_scan
from datetime import datetime

app = Flask(__name__)

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

    # Execute the appropriate scan
    if context:
        result = run_auto_scan(ticker, context)
    else:
        result = run_manual_scan(ticker)

    # Parse out score & breakdown from result
    if isinstance(result, dict):
        score = result.get("score")
        breakdown = result.get("breakdown")
    else:
        # Fallback for tuple/list results
        try:
            score, breakdown = result
        except Exception:
            # Fallback: take first two elements
            score = result[0]
            breakdown = result[1]

    return jsonify({
        "ticker": ticker,
        "score": score,
        "breakdown": breakdown,
        "fetched_at": datetime.utcnow().isoformat() + "Z"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
