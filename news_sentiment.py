import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import re

# 初始化情绪分析模型（英文）
sentiment_pipeline = pipeline("sentiment-analysis")

def fetch_news_headlines(ticker, max_results=20):
    """
    爬取Yahoo Finance相关新闻标题（英文）
    """
    url = f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 抓取新闻标题（h3标签中的文字）
    headlines = []
    for item in soup.find_all("h3"):
        text = item.get_text()
        if text and text not in headlines:
            headlines.append(text.strip())
        if len(headlines) >= max_results:
            break
    return headlines

def analyze_sentiment(text_list):
    """
    对新闻标题列表进行情绪分析
    """
    results = sentiment_pipeline(text_list)
    return [
        {"text": text, "label": res["label"], "score": round(res["score"], 2)}
        for text, res in zip(text_list, results)
    ]

def summarize_sentiment(results):
    """
    汇总情绪结果，输出总情绪判断和得分
    """
    if not results:
        return "neutral", 0.0

    sentiment_score = sum(
        r["score"] if r["label"] == "POSITIVE" else -r["score"]
        for r in results
    ) / len(results)

    # 情绪信号判断
    if sentiment_score > 0.3:
        signal = "positive"
    elif sentiment_score < -0.3:
        signal = "negative"
    else:
        signal = "neutral"

    return signal, round(sentiment_score, 2)

def get_news_sentiment_signal(ticker):
    """
    主函数：输入股票代码，返回情绪信号、得分和详情
    """
    headlines = fetch_news_headlines(ticker)
    if not headlines:
        return {"signal": "neutral", "score": 0.0, "reason": "No headlines found."}
    results = analyze_sentiment(headlines)
    signal, score = summarize_sentiment(results)
    return {
        "signal": signal,
        "score": score,
        "details": results
    }

# 示例调用：
if __name__ == "__main__":
    ticker = input("输入股票代号（如 AAPL）: ")
    sentiment_result = get_news_sentiment_signal(ticker)
    print("\n新闻情绪分析结果：")
    print(f"情绪信号：{sentiment_result['signal']}")
    print(f"情绪指数：{sentiment_result['score']}")
    print("\n详细分析：")
    for r in sentiment_result.get("details", []):
        print(f"- {r['text']} → {r['label']} ({r['score']})")
