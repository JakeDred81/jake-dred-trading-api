from tradingview_ta import TA_Handler, Interval, Exchange
from datetime import datetime
import random

def evaluate_with_context(ticker, exchange='NASDAQ', screener='america', interval=Interval.DAILY):
    '''
    Fetches live TA data from TradingView; on error falls back to random stub.
    Returns a dict:
      ticker, score, breakdown, summary, fetched_at
    '''
    fetched_at = datetime.utcnow().isoformat() + "Z"
    try:
        handler = TA_Handler(
            symbol=ticker,
            exchange=exchange,
            screener=screener,
            interval=interval
        )
        analysis = handler.get_analysis()
        indicators = analysis.indicators
        # Example breakdown using buying/selling signals
        breakdown = {
            'Technical Pattern': indicators.get('RECOMMENDATION_COUNT_BUY', 0),
            'Trend & Momentum': int(indicators.get('RSI', 0) > 50),
            'News/Catalyst': 1 if analysis.summary.get('RECOMMENDATION') != 'NEUTRAL' else 0,
            'Fundamentals': 0,  # placeholder
            'Risk/Reward Profile': 0  # placeholder
        }
        score = sum(breakdown.values())
        summary = analysis.summary
    except Exception:
        # Fallback stub if TradingView data fails
        breakdown = {
            'Technical Pattern': random.randint(0,2),
            'Trend & Momentum': random.randint(0,2),
            'News/Catalyst': random.randint(0,2),
            'Fundamentals': random.randint(0,2),
            'Risk/Reward Profile': random.randint(0,2)
        }
        score = sum(breakdown.values())
        summary = {'RECOMMENDATION': 'NEUTRAL'}
    return {
        'ticker': ticker,
        'score': score,
        'breakdown': breakdown,
        'summary': summary,
        'fetched_at': fetched_at
    }
