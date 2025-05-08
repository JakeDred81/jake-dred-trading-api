import random

def score_trade(ticker, context=None):
    """
    Simplest stub: ignore context, pick random scores in each category,
    sum them up, and return (total_score, breakdown_dict).
    """
    breakdown = {
        'Technical Pattern':    random.randint(0, 2),
        'Trend & Momentum':     random.randint(0, 2),
        'News/Catalyst':        random.randint(0, 2),
        'Fundamentals':         random.randint(0, 2),
        'Risk/Reward Profile':  random.randint(0, 2),
    }
    total = sum(breakdown.values())
    return total, breakdown

# (Optional) keep your old evaluate_trade for quick CLI testing:
def evaluate_trade(ticker):
    total, breakdown = score_trade(ticker)
    rating = ('Strong Setup' if total >= 7
              else 'Watchlist' if total >= 5
              else 'Skip')
    print(f"Evaluating {ticker.upper()}…")
    print(f"Score: {total} ({rating})")
    print(f"Breakdown: {breakdown}")
    print("---")
    return total, breakdown
