from flask import Flask, jsonify
from flasgger import Swagger
from run_scan import run_auto_scan
from yahoo_screener import get_top_volume_tickers

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
def home():
    """
    Home Route
    ---
    get:
      summary: Root check
      responses:
        200:
          description: Returns a message confirming service is live.
    """
    return "Jake Dred's Trading Toolbox is live."

@app.route("/scan", methods=["GET"])
def scan():
    """
    Manual Scan
    ---
    get:
      summary: Run manual scan on predefined tickers
      responses:
        200:
          description: List of trade setups
    """
    return jsonify(run_auto_scan())

@app.route("/autoscan", methods=["GET"])
def autoscan():
    """
    Auto Scan
    ---
    get:
      summary: Dynamic scan using top tickers from Yahoo
      responses:
        200:
          description: List of high-volume trade setups
    """
    try:
        tickers = get_top_volume_tickers(min_price=10, min_volume=1_000_000, limit=20)
        results = run_auto_scan(tickers=tickers)
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/health", methods=["GET"])
def health():
    """
    Health Check
    ---
    get:
      summary: Returns API health
      responses:
        200:
          description: Status OK
    """
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
