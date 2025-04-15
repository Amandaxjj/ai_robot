# analyze_light.py
import json
import pandas as pd

def calculate_rsi(prices, period=7):
    prices = pd.Series(prices)
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def analyze_lightweight(stock_name, data):
    history = data["history"]
    closes = [v["close"] for k, v in sorted(history.items())][-5:]
    current_price = data["current_price"]
    ma5 = pd.Series(closes).mean()
    price_vs_ma5 = (current_price - ma5) / ma5 * 100
    rsi = calculate_rsi(closes)
    percent_change = data.get("percent_change", 0)

    decision = "🧊 HOLD"
    reasons = []

    if rsi < 30 and current_price < ma5:
        decision = "🍀 BUY"
        reasons = ["RSI < 30", "Price below MA5"]
    elif rsi > 70 and current_price > ma5:
        decision = "💣 SELL"
        reasons = ["RSI > 70", "Price above MA5"]

    return {
        "stock": stock_name,
        "final_decision": decision,
        "reasons": reasons,
        "metrics": {
            "Current Price": round(current_price, 2),
            "MA5": round(ma5, 2),
            "RSI": round(rsi, 2),
            "Price vs MA5 %": round(price_vs_ma5, 2),
            "Percent Change": round(percent_change, 2)
        }
    }

if __name__ == "__main__":
    path = input("输入 JSON 文件路径（如 AAPL_stock_data.json）: ")
    with open(path, "r") as f:
        stock_data = json.load(f)
    ticker = list(stock_data.keys())[0]
    result = analyze_lightweight(ticker, stock_data[ticker])
    print(json.dumps(result, indent=2, ensure_ascii=False))
