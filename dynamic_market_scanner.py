
from trade_score_evaluator import score_trade
from pattern_playbook import detect_patterns
from data_handler import get_realtime_data

tickers = ['SOXL', 'TQQQ', 'TSLA', 'NVDA', 'SPY', 'QQQ']

data = get_realtime_data(tickers)

results = []

for ticker, stats in data.items():
    close = stats['close']
    volume = stats['volume']
    rsi = stats['rsi']
    change = stats['change_percent']

    patterns = detect_patterns(ticker, close)
    score = score_trade(close, volume, rsi, change, patterns)

    results.append({
        'ticker': ticker,
        'close': close,
        'volume': volume,
        'rsi': rsi,
        'change': change,
        'patterns': patterns,
        'score': score
    })

results = sorted(results, key=lambda x: x['score'], reverse=True)

for res in results:
    print(res)
