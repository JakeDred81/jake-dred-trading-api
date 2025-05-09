# Updated run_scan.py
from dynamic_market_scanner import evaluate_with_context
import random

def run_manual_scan(ticker):
    # Simple stub manual scan
    from trade_score_evaluator import score_trade
    return score_trade(ticker)

def run_auto_scan(ticker):
    # Auto scan using dynamic scanner
    return evaluate_with_context(ticker)
