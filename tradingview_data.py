# Module: TradingView Technical Analysis – Jake Dred’s Trading Toolbox

from tradingview_ta import TA_Handler, Interval, Exchange

def get_tradingview_analysis(symbol, exchange='NASDAQ', screener='america', interval='1d'):
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
        print(f"🔍 TradingView Technical Summary for {symbol.upper()} ({interval}):")
        print(f"Recommendation: {analysis.summary['RECOMMENDATION']}")
        print("Indicators:")
        for ind, val in analysis.indicators.items():
            print(f" - {ind}: {val}")
    except Exception as e:
        print(f"⚠️ Error fetching analysis for {symbol.upper()}: {str(e)}")
