
from flask import Flask, jsonify
from src.run_scan import run_auto_scan

app = Flask(__name__)

@app.route('/autoscan', methods=['GET'])
def autoscan():
    run_auto_scan()
    return jsonify({"status": "Auto scan completed"})

if __name__ == '__main__':
    app.run(debug=True)
