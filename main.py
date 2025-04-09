# main.py

from flask import Flask, request, jsonify
from run_scan import run_auto_scan
from scanner_output_parser import format_scan_result

app = Flask(__name__)

@app.route("/")
def health_check():
    return "Jake Dred's Trading API is live! 🔥"

@app.route("/scan", methods=["POST"])
def scan():
    try:
        data = request.get_json()
        scan_results = run_auto_scan()
        formatted = [format_scan_result(s) for s in scan_results]
        return jsonify({"results": formatted})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/signals", methods=["GET"])
def get_signals():
    try:
        scan_results = run_auto_scan()
        return jsonify(scan_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
