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
    
    if context:
        result = run_auto_scan(ticker, context)
        # Ensure dict result
        if isinstance(result, dict):
            result["fetched_at"] = datetime.utcnow().isoformat() + "Z"
            return jsonify(result)
        # Fallback unpack tuple/list
        try:
            score, breakdown = result
            return jsonify({
                "ticker": ticker,
                "score": score,
                "breakdown": breakdown,
                "fetched_at": datetime.utcnow().isoformat() + "Z"
            })
        except Exception:
            return jsonify({"error": "Invalid scan result format"}), 500
    else:
        try:
            score, breakdown = run_manual_scan(ticker)
            return jsonify({
                "ticker": ticker,
                "score": score,
                "breakdown": breakdown,
                "fetched_at": datetime.utcnow().isoformat() + "Z"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/autoscan')
def autoscan():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "ticker query param required"}), 400
    # Always use the dynamic scanner
    result = run_auto_scan(ticker, context=True)
    if isinstance(result, dict):
        result["fetched_at"] = datetime.utcnow().isoformat() + "Z"
        return jsonify(result)
    else:
        try:
            score, breakdown = result
            return jsonify({
                "ticker": ticker,
                "score": score,
                "breakdown": breakdown,
                "fetched_at": datetime.utcnow().isoformat() + "Z"
            })
        except Exception:
            return jsonify({"error": "Invalid scan result format"}), 500

if __name__ == "__main__":
    # For local development only; Render uses Gunicorn
    app.run(host="0.0.0.0", port=5000)
