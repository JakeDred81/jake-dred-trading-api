from market_scanner import scan_market
from dynamic_market_scanner import evaluate_with_context
from tradingview_data import get_movers
from alerts_triggers import check_alerts
from trade_score_evaluator import score_trade

def run_auto_scan():
    tickers = get_movers()
    results = []

    for ticker in tickers:
        print(f"Evaluating {ticker}...")
        context = evaluate_with_context(ticker)
        score, breakdown = score_trade(ticker, context)
        results.append({
            'ticker': ticker,
            'score': score,
            'breakdown': breakdown
        })
        print(f"Score: {score} ({'Strong Setup' if score >= 7 else 'Watchlist' if score >= 5 else 'Skip'})")
        print(f"Breakdown: {breakdown}")
        print("---")

    check_alerts(results)
    return results


def run_manual_scan(ticker):
    print(f"Evaluating {ticker}...")
    context = evaluate_with_context(ticker)
    score, breakdown = score_trade(ticker, context)

    result = {
        'ticker': ticker,
        'score': score,
        'breakdown': breakdown
    }

    print(f"Score: {score} ({'Strong Setup' if score >= 7 else 'Watchlist' if score >= 5 else 'Skip'})")
    print(f"Breakdown: {breakdown}")
    print("---")

    return result
