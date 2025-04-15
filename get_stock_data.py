import yfinance as yf
import json

def fetch_stock_data(ticker_symbol, period="7d", interval="1d"):
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period, interval=interval)

    def to_python_type(val):
        if hasattr(val, 'item'):
            return val.item()
        return val

    data = {
        "name": ticker.info.get("shortName", ticker_symbol),
        "ticker": ticker_symbol,
        "current_price": to_python_type(hist["Close"][-1]),
        "percent_change": to_python_type((hist["Close"][-1] - hist["Close"][-2]) / hist["Close"][-2] * 100),
        "volume": to_python_type(hist["Volume"][-1]),
        "pe_ratio": to_python_type(ticker.info.get("trailingPE", None)),
        "pb_ratio": to_python_type(ticker.info.get("priceToBook", None)),
        "dividend_yield": to_python_type(ticker.info.get("dividendYield", None)),
        "history": {}
    }

    for date, row in hist.iterrows():
        data["history"][str(date.date())] = {
            "open": to_python_type(round(row["Open"], 2)),
            "high": to_python_type(round(row["High"], 2)),
            "low": to_python_type(round(row["Low"], 2)),
            "close": to_python_type(round(row["Close"], 2)),
            "volume": to_python_type(int(row["Volume"]))
        }

    return {ticker_symbol: data}

if __name__ == "__main__":
    ticker = input("输入股票代码（如 AAPL）: ")
    data = fetch_stock_data(ticker)
    with open(f"{ticker}_stock_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"数据保存至：{ticker}_stock_data.json")
