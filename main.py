import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, jsonify
from run_scan import run_auto_scan

app = Flask(__name__)

@app.route('/autoscan', methods=['GET'])
def autoscan():
    run_auto_scan()
    return jsonify({"status": "Auto scan completed"})

if __name__ == '__main__':
    app.run(debug=True)
