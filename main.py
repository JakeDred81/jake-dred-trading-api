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
    try:
        if context == 'auto':
            score, breakdown = run_auto_scan(ticker)
        else:
            score, breakdown = run_manual_scan(ticker)
        return jsonify({
            "ticker": ticker,
            "score": score,
            "breakdown": breakdown,
            "fetched_at": datetime.utcnow().isoformat() + "Z"
        })
    except Exception as e:
        app.logger.error(f"Scan error for {ticker}: {e}")
        return jsonify({
            "error": f"Scan failed for {ticker}: {str(e)}"
        }), 500

@app.route('/autoscan')
def autoscan():
    ticker = request.args.get('ticker')
    try:
        score, breakdown = run_auto_scan(ticker)
        return jsonify({
            "ticker": ticker,
            "score": score,
            "breakdown": breakdown,
            "fetched_at": datetime.utcnow().isoformat() + "Z"
        })
    except Exception as e:
        app.logger.error(f"Autoscan error for {ticker}: {e}")
        try:
            score, breakdown = run_manual_scan(ticker)
            return jsonify({
                "ticker": ticker,
                "score": score,
                "breakdown": breakdown,
                "fetched_at": datetime.utcnow().isoformat() + "Z",
                "note": "Returned manual scan as fallback"
            })
        except Exception as e2:
            app.logger.error(f"Fallback manual scan also failed for {ticker}: {e2}")
            return jsonify({
                "error": f"Autoscan failed: {str(e)}; fallback manual scan also failed: {str(e2)}"
            }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
