# Upgraded Market Scanner – Catalyst & Pattern Detection Enabled

from tradingview_ta import TA_Handler, Interval, Exchange
import random

def get_real_analysis(symbol, exchange='NASDAQ', screener='america', interval='1d'):
    interval_map = {
        '1m': Interval.INTERVAL_1_MINUTE,
        '5m': Interval.INTERVAL_5_MINUTES,
        '15m': Interval.INTERVAL_15_MINUTES,
        '30m': Interval.INTERVAL_30_MINUTES,
        '1h': Interval.INTERVAL_1_HOUR,
        '4h': Interval.INTERVAL_4_HOURS,
        '1d': Interval.INTERVAL_1_DAY,
        '1w': Interval.INTERVAL_1_WEEK,
        '1M': Interval.INTERVAL_1_MONTH
    }

    handler = TA_Handler(
        symbol=symbol.upper(),
        screener=screener,
        exchange=exchange,
        interval=interval_map.get(interval.lower(), Interval.INTERVAL_1_DAY)
    )

    try:
        analysis = handler.get_analysis()
        return analysis
    except Exception as e:
        return None

def detect_pattern(analysis):
    rsi = analysis.indicators.get("RSI")
    price = analysis.indicators.get("close")
    sma20 = analysis.indicators.get("SMA20")
    sma50 = analysis.indicators.get("SMA50")

    if price and sma20 and price > sma20 * 1.01:
        return "Breakout"
    elif price and sma20 and 0.99 < price / sma20 < 1.01:
        return "Pullback"
    elif price and sma20 and abs(price - sma20) < 0.5 and abs(price - sma50) < 0.5:
        return "Consolidation"
    return "None"

def check_catalyst(ticker):
    # Placeholder logic – return True if ticker is in mock earnings list or simulated spike
    earnings_watch = ['TSLA', 'NVDA', 'AAPL']
    volume_spike = random.choice([True, False])
    return ticker in earnings_watch or volume_spike

def evaluate_with_context(ticker):
    analysis = get_real_analysis(ticker)
    if not analysis:
        return {
            'Ticker': ticker,
            'Score': 0,
            'Rating': 'Data Unavailable',
            'Breakdown': {},
            'Recommendation': 'Unavailable',
            'Pattern': 'N/A',
            'Catalyst': 'N/A'
        }

    has_catalyst = check_catalyst(ticker)
    pattern = detect_pattern(analysis)

    score_components = {
        'Technical Pattern': 2 if pattern in ["Breakout", "Pullback"] else 1,
        'Trend & Momentum': 2 if analysis.indicators.get("RSI", 0) > 50 and analysis.indicators.get("MACD.macd", 0) > analysis.indicators.get("MACD.signal", 0) else 1,
        'News/Catalyst': 2 if has_catalyst else 1,
        'Fundamentals': 1,  # Placeholder
        'Risk/Reward Profile': 1  # Placeholder
    }

    total_score = sum(score_components.values())
    rating = 'Strong Setup' if total_score >= 7 else 'Watchlist' if total_score >= 5 else 'Skip'

    return {
        'Ticker': ticker,
        'Score': total_score,
        'Rating': rating,
        'Breakdown': score_components,
        'Recommendation': analysis.summary['RECOMMENDATION'],
        'Pattern': pattern,
        'Catalyst': 'Yes' if has_catalyst else 'No'
    }

def run_advanced_scanner():
    tickers = ['AAPL', 'NVDA', 'TSLA', 'SPY', 'AMD', 'QQQ']
    results = [evaluate_with_context(ticker) for ticker in tickers]
    results.sort(key=lambda x: x['Score'], reverse=True)

    for result in results:
        print(f"{result['Ticker']} - Score: {result['Score']} ({result['Rating']})")
        print(f"Recommendation: {result['Recommendation']}")
        print(f"Pattern: {result['Pattern']} | Catalyst: {result['Catalyst']}")
        print(f"Breakdown: {result['Breakdown']}")
        print("---")
