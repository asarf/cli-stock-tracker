import yfinance as yf

indices = {
    # North America
    "USA": {"name": "S&P 500", "ticker": "^GSPC"},
    "USA-NASDAQ": {"name": "NASDAQ", "ticker": "^IXIC"},
    "USA-DOW": {"name": "Dow Jones", "ticker": "^DJI"},
    "CANADA": {"name": "S&P/TSX", "ticker": "^GSPTSE"},
    "MEXICO": {"name": "IPC", "ticker": "^MXX"},
    
    # Europe
    "UK": {"name": "FTSE 100", "ticker": "^FTSE"},
    "GERMANY": {"name": "DAX", "ticker": "^GDAXI"},
    "FRANCE": {"name": "CAC 40", "ticker": "^FCHI"},
    "SPAIN": {"name": "IBEX 35", "ticker": "^IBEX"},
    "ITALY": {"name": "FTSE MIB", "ticker": "FTSEMIB.MI"},
    "SWITZERLAND": {"name": "SMI", "ticker": "^SSMI"},
    "NETHERLANDS": {"name": "AEX", "ticker": "^AEX"},
    
    # Asia-Pacific
    "JAPAN": {"name": "Nikkei 225", "ticker": "^N225"},
    "CHINA": {"name": "Shanghai Composite", "ticker": "000001.SS"},
    "CHINA-HK": {"name": "Hang Seng", "ticker": "^HSI"},
    "SOUTH KOREA": {"name": "KOSPI", "ticker": "^KS11"},
    "INDIA": {"name": "NIFTY 50", "ticker": "^NSEI"},
    "AUSTRALIA": {"name": "ASX 200", "ticker": "^AXJO"},
    "SINGAPORE": {"name": "STI", "ticker": "^STI"},
    "BRAZIL": {"name": "Bovespa", "ticker": "^BVSP"},
}

def fetch_indices_data():
    print("Fetching global market data...")
    data = []
    for country, info in indices.items():
        print(f"  Getting data for {country} - {info['name']}...")
        ticker = yf.Ticker(info["ticker"])
        hist = ticker.history(period="1d", interval="1m")
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            prev_close = ticker.info['previousClose']
            pct_change = ((current_price - prev_close) / prev_close) * 100
            data.append({
                "country": country,
                "index_name": info["name"],
                "ticker": info["ticker"],
                "current_value": round(current_price, 2),
                "percentage_change": round(pct_change, 2),
            })
    return sorted(data, key=lambda x: abs(x['percentage_change']), reverse=True)