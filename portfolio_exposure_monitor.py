# Module 4: Portfolio Exposure Monitor – Jake Dred’s Trading Toolbox

portfolio = []

def add_position(ticker, capital_allocated, sector, is_margin_used=False):
    position = {
        'Ticker': ticker.upper(),
        'Capital': capital_allocated,
        'Sector': sector,
        'Margin': is_margin_used
    }
    portfolio.append(position)
    print(f"📌 Added position: {ticker.upper()} – ${capital_allocated} in {sector} sector {'(Margin)' if is_margin_used else ''}")

def remove_position(ticker):
    global portfolio
    portfolio = [p for p in portfolio if p['Ticker'] != ticker.upper()]
    print(f"✅ Removed position: {ticker.upper()}")

def portfolio_summary(total_equity):
    total_allocated = sum(p['Capital'] for p in portfolio)
    margin_used = sum(p['Capital'] for p in portfolio if p['Margin'])
    exposure_by_sector = {}
    for p in portfolio:
        exposure_by_sector[p['Sector']] = exposure_by_sector.get(p['Sector'], 0) + p['Capital']

    print("\n💼 Portfolio Exposure Summary:")
    print(f"Total Capital Allocated: ${total_allocated} / ${total_equity} ({(total_allocated / total_equity) * 100:.2f}%)")
    print(f"Margin Usage: ${margin_used}")
    print("Sector Breakdown:")
    for sector, capital in exposure_by_sector.items():
        print(f" - {sector}: ${capital}")
    if total_allocated > total_equity:
        print("⚠️ Overexposed: Allocated capital exceeds portfolio equity!")
