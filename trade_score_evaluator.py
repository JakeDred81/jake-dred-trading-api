# Module 2: Trade Score Evaluator – Jake Dred’s Trading Toolbox

import random

def evaluate_trade(ticker):
    score_components = {
        'Technical Pattern': random.randint(0, 2),
        'Trend & Momentum': random.randint(0, 2),
        'News/Catalyst': random.randint(0, 2),
        'Fundamentals': random.randint(0, 2),
        'Risk/Reward Profile': random.randint(0, 2)
    }

    total_score = sum(score_components.values())
    rating = (
        'Strong Setup' if total_score >= 7 else
        'Watchlist' if total_score >= 5 else
        'Skip'
    )

    result = {
        'Ticker': ticker.upper(),
        'Score': total_score,
        'Rating': rating,
        'Breakdown': score_components
    }

    print(f"Evaluating {result['Ticker']}...")
    print(f"Score: {result['Score']} ({result['Rating']})")
    print(f"Breakdown: {result['Breakdown']}")
    print("---")

# Example usage
evaluate_trade("TSLA")
