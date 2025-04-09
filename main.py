# main.py

from flask import Flask, request, jsonify
from run_scan import run_auto_scan

app = Flask(__name__)

@app.route("/")
def health():
    return "Jake Dred's Trading API is online."

@app.route("/scan", methods=["POST"])
def scan():
    try:
        results = run_auto_scan()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/signals", methods=["GET"])
def signals():
    try:
        results = run_auto_scan()
        strong_setups = [r for r in results if r["recommendation"] == "STRONG"]
        return jsonify(strong_setups), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
