"""
run_scan.py - orchestrate manual and automatic market scans.
"""

from dynamic_market_scanner import evaluate_with_context
from trade_score_evaluator import score_trade

def run_auto_scan(ticker, context=None):
    """
    Perform a dynamic market scan for a given ticker using evaluate_with_context.
    Returns a dict containing scan results.
    """
    # Get dynamic scan results (dict with keys like 'ticker', 'score', etc.)
    result = evaluate_with_context(ticker)
    return result

def run_manual_scan(ticker):
    """
    Perform a manual scan for a single ticker using score_trade.
    Returns a tuple (score, breakdown_dict).
    """
    score, breakdown = score_trade(ticker)
    return score, breakdown
