# main.py

from flask import Flask, jsonify
from run_scan import run_auto_scan

app = Flask(__name__)

@app.route("/")
def home():
    return "Jake Dred's Trading Toolbox is live."

@app.route("/scan")
def scan():
    return jsonify(run_auto_scan())

@app.route("/autoscan", methods=["GET"])
def autoscan():
    try:
        results = run_auto_scan()
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
