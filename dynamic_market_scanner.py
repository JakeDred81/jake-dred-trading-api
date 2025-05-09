# Updated dynamic_market_scanner.py
from tradingview_ta import TA_Handler, Interval, Exchange
import random

def get_real_analysis(symbol, exchange='NASDAQ', screener='america', interval='1d'):
    handler = TA_Handler(
        symbol=symbol,
        exchange=exchange,
        screener=screener,
        interval=interval
    )
    analysis = handler.get_analysis()
    return analysis

def evaluate_with_context(ticker):
    try:
        analysis = get_real_analysis(ticker)
        indicators = analysis.indicators
        summary = analysis.summary
        score = summary.get('BUY', 0) - summary.get('SELL', 0)
        breakdown = {
            'Technical Pattern': int(indicators.get('RSI', 0) > 50),
            'Trend & Momentum': int(indicators.get('MACD.macd', 0) > indicators.get('MACD.signal', 0)),
            'News/Catalyst': random.randint(0, 2),
            'Fundamentals': random.randint(0, 2),
            'Risk/Reward Profile': random.randint(0, 2)
        }
        total = sum(breakdown.values())
        return total, breakdown
    except Exception as e:
        # Fallback to manual random scan
        breakdown = {
            'Technical Pattern': random.randint(0,2),
            'Trend & Momentum': random.randint(0,2),
            'News/Catalyst': random.randint(0,2),
            'Fundamentals': random.randint(0,2),
            'Risk/Reward Profile': random.randint(0,2)
        }
        total = sum(breakdown.values())
        return total, breakdown
