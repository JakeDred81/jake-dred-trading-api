from tradingview_ta import TA_Handler, Interval, Exchange

def get_movers(tickers):
    movers = []

    for symbol in tickers:
        try:
            analysis = TA_Handler(
                symbol=symbol,
                screener="america",
                exchange="NASDAQ",
                interval=Interval.INTERVAL_1_DAY
            ).get_analysis()

            recommendation = analysis.summary["RECOMMENDATION"]

            if recommendation in ["STRONG_BUY", "BUY"]:
                movers.append({
                    "symbol": symbol,
                    "recommendation": recommendation
                })

        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    return movers
