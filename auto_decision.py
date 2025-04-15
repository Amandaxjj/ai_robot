# auto_decision.py

import json
import os
from get_stock_data import fetch_stock_data  # 你自己写的获取数据函数
from news_sentiment import get_news_sentiment_signal
from data_signal import analyze_lightweight
from buy_sell_decision import final_trade_decision

def run_auto_pipeline(ticker: str):
    print(f"📈 正在分析股票：{ticker}")

    # Step 1：抓取股票数据并保存为 JSON
    stock_data = fetch_stock_data(ticker)
    json_path = f"{ticker}_stock_data.json"
    with open(json_path, "w") as f:
        json.dump({ticker: stock_data}, f)

    # Step 2：新闻情绪分析
    news_result = get_news_sentiment_signal(ticker)
    news_signal = news_result["signal"]
    print(f"[新闻情绪] {news_signal.upper()}（指数: {news_result['score']}）")

    # Step 3：技术面分析
    data_result = analyze_lightweight(ticker, stock_data[ticker])
    data_signal = data_result["final_decision"]
    print(f"[数据分析] {data_signal} | 原因: {', '.join(data_result['reasons']) or '无'}")

    # Step 4：综合决策
    final = final_trade_decision(news_signal, data_signal)
    print(f"\n🎯 最终交易决策：{final}")

    # 自动清理临时文件
    if os.path.exists(json_path):
        os.remove(json_path)

if __name__ == "__main__":
    ticker = input("请输入股票代号（如 AAPL）: ").strip().upper()
    run_auto_pipeline(ticker)
