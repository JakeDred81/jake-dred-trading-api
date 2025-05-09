from dynamic_market_scanner import evaluate_with_context
from trade_score_evaluator import score_trade

def run_auto_scan(ticker):
    '''
    Full dynamic scan: returns the result dict from evaluate_with_context.
    '''
    return evaluate_with_context(ticker)

def run_manual_scan(ticker):
    '''
    Manual stub scan: returns (score, breakdown).
    '''
    total, breakdown = score_trade(ticker)
    return total, breakdown
