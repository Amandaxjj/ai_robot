# main_decision.py
import json
from news_sentiment import get_news_sentiment_signal
from data_signal import analyze_lightweight

def final_trade_decision(news_signal: str, data_decision: str) -> str:
    if news_signal == "positive" and "BUY" in data_decision:
        return "BUY"
    elif news_signal == "negative" and "SELL" in data_decision:
        return "SELL"
    else:
        return "HOLD"

def main(ticker: str, data_path: str):
    # 获取新闻情绪信号
    news_result = get_news_sentiment_signal(ticker)
    news_signal = news_result["signal"]
    print(f"[新闻情绪] {news_signal.upper()} | 情绪指数: {news_result['score']}")

    # 获取数据分析决策
    with open(data_path, "r") as f:
        stock_data = json.load(f)
    data_result = analyze_lightweight(ticker, stock_data[ticker])
    data_decision = data_result["final_decision"]
    print(f"[数据分析] {data_decision} | 原因: {', '.join(data_result['reasons']) or '无'}")

    # 综合判断最终交易决策
    final = final_trade_decision(news_signal, data_decision)
    print(f"\n🎯 最终交易决策：{final}")

if __name__ == "__main__":
    ticker = input("输入股票代号（如 AAPL）: ").strip().upper()
    path = input("输入 JSON 数据文件路径（如 AAPL_data.json）: ").strip()
    main(ticker, path)
