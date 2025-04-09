# main.py

from flask import Flask, jsonify
from run_scan import run_auto_scan
from scanner_output_parser import format_scan_result

app = Flask(__name__)

@app.route("/")
def health_check():
    return jsonify({"status": "Jake Dred Trading API is live."})

@app.route("/scan", methods=["POST"])
def scan():
    try:
        scan_results = run_auto_scan()
        formatted = [format_scan_result(r) for r in scan_results]
        return jsonify({"scan_results": "\n\n".join(formatted)})
    except Exception as e:
        return jsonify({"error": f"Scan failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0")
