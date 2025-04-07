# Dynamic Market Scanner – Final version with callable interface
from tradingview_ta import TA_Handler, Interval, Exchange

def evaluate_with_context(ticker):
    handler = TA_Handler(
        symbol=ticker,
        screener="america",
        exchange="NASDAQ",
        interval=Interval.INTERVAL_1_DAY
    )

    analysis = handler.get_analysis()
    indicators = analysis.indicators
    summary = analysis.summary

    price = indicators.get("close")
    sma20 = indicators.get("SMA20")
    rsi = indicators.get("RSI")
    macd = indicators.get("MACD.macd")
    signal = indicators.get("MACD.signal")
    rec = summary.get("RECOMMENDATION", "NEUTRAL")

    pattern = "Breakout" if price > sma20 * 1.01 else "Pullback" if 0.99 < price / sma20 < 1.01 else "None"
    pattern_score = 2 if pattern in ["Breakout", "Pullback"] else 1
    trend_score = 2 if rsi > 50 and macd > signal else 1
    catalyst_score = 2 if rec in ["BUY", "STRONG_BUY"] else 1
    fundamental_score = 1
    rr_score = 1

    total_score = pattern_score + trend_score + catalyst_score + fundamental_score + rr_score
    recommendation = "BUY" if total_score >= 7 else "NEUTRAL" if total_score >= 5 else "SELL"

    return {
        "ticker": ticker,
        "score": total_score,
        "recommendation": recommendation,
        "pattern": pattern,
        "catalyst": rec in ["BUY", "STRONG_BUY"],
        "breakdown": {
            "Technical Pattern": pattern_score,
            "Trend & Momentum": trend_score,
            "News/Catalyst": catalyst_score,
            "Fundamentals": fundamental_score,
            "Risk/Reward Profile": rr_score
        }
    }
