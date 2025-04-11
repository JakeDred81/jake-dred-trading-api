
from tradingview_ta import TA_Handler, Interval
from trade_score_evaluator import evaluate_trade as score_trade

def evaluate_with_context(ticker):
    print(f"Evaluating {ticker}...")

    analysis = TA_Handler(
        symbol=ticker,
        exchange="NASDAQ",
        screener="america",
        interval=Interval.INTERVAL_1_DAY
    ).get_analysis()

    score, breakdown = score_trade(ticker)

    print(f"Score: {score} ({'Strong Setup' if score >= 6 else 'Skip'})")
    print(f"Breakdown: {breakdown}")
    print("---")

    return {
        'ticker': ticker,
        'score': score,
        'breakdown': breakdown,
        'summary': analysis.summary
    }
