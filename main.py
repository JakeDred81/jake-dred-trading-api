from flask import Flask, jsonify, request
from run_scan import run_auto_scan, run_manual_scan

app = Flask(__name__)

@app.route('/')
def home():
    return 'Jake Dred API is Live'

@app.route('/scan/auto')
def scan_auto():
    results = run_auto_scan()
    return jsonify(results)

@app.route('/scan')
def scan_manual():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'No ticker provided'}), 400
    results = run_manual_scan(ticker)
    return jsonify(results)
