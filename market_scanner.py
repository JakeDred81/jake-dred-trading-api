from tradingview_ta import TA_Handler, Interval, Exchange
import yfinance as yf

def scan_market(tickers):
    results = []

    for symbol in tickers:
        try:
            analysis = TA_Handler(
                symbol=symbol,
                screener="america",
                exchange="NASDAQ",
                interval=Interval.INTERVAL_1_DAY
            ).get_analysis()

            stock_info = yf.Ticker(symbol).info

            result = {
                "symbol": symbol,
                "recommendation": analysis.summary["RECOMMENDATION"],
                "moving_averages": analysis.moving_averages,
                "oscillators": analysis.oscillators,
                "price": stock_info.get("regularMarketPrice", "N/A"),
                "shortName": stock_info.get("shortName", "N/A"),
                "sector": stock_info.get("sector", "N/A"),
                "industry": stock_info.get("industry", "N/A")
            }

            results.append(result)

        except Exception as e:
            print(f"Error scanning {symbol}: {e}")

    return results
