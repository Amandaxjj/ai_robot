from pydantic import BaseModel
import yfinance
from openai import OpenAI
from article_fetcher import fetch_article

openai_client = OpenAI()


def fetch_news_for_ticker(ticker):
    """
    fetch news for a ticker from yahoo finance
    example response json in sample_news_nvda.json
    """
    ticker = yfinance.Ticker(ticker)
    news = ticker.news
    return news


def summarize_news(article, ticker: yfinance.Ticker):
    """
    summarize a given news article for making financial decision
    """
    system_prompt = f"""
You are an experienced financial analyst specializing in stock market analysis.
You are good at reading news articles and extracting the key points that are important for making trading decisions.
You will be given a news article and a stock ticker.
Your task is to read the article carefully and critically, then extract the key points from the news article and summarize them in a comprehensive and informative bullet point list. This bullet point list will be used for making trading decisions by a retail investor.
"""
    user_prompt = f"""
<article>
{article}
</article>

---

Please analyze the news article given above for the stock ticker {ticker}.
"""
    response = openai_client.responses.create(
        model="gpt-4.1-mini",
        instructions=system_prompt,
        input=user_prompt,
    )
    return response.output_text


class TradingAnalysis(BaseModel):
    sentiment: float
    reason: str
    decision: str
    confidence: int
    action: str


def make_trading_decision(summaries, ticker):
    """
    make a trading decision based on the summaries
    """
    system_prompt = f"""
You are an experienced professional stock trader. You are good at making long term (span of weeks) trading decisions based on news articles.
You will be given a list of news summaries and a stock ticker.
Your task is to read the news summaries carefully and critically, then give a market sentiment evaluation for the stock.
Your evaluation should be based on the news summaries and the stock ticker. The evaluation output should be a numeric value between -1 and 1 where -1 is the most bearish and 1 is the most bullish.
Your output should be a JSON object with the following fields:
- sentiment: a numeric value between -1 and 1
- reason: a short explanation for the sentiment
- decision: a short trading decision based on the sentiment
- confidence: a numeric value between 0 and 100
- action: a short action to take based on the sentiment
"""
    user_prompt = f"""
<summaries>
{"\n\n---\n\n".join([f"Title: {s['title']}\nYahoo Finance Summary: {s['yf_summary']}\nNews Summary: {s['news_summary']}" for s in summaries])}
</summaries>

<stock_ticker>
{ticker}
</stock_ticker>

Please make a market sentiment evaluation for the stock {ticker} based on the news summaries.
"""
    print(user_prompt)
    response = openai_client.responses.parse(
        model="gpt-4.1",
        instructions=system_prompt,
        input=user_prompt,
        text_format=TradingAnalysis,
    )
    return response.output_text, response.output_parsed


if __name__ == "__main__":
    from datetime import datetime
    import json
    ticker = input("输入股票代号（如 AAPL）: ")
    news = fetch_news_for_ticker(ticker)
    summaries = []
    for article in news:
        try:
            if article["content"]["contentType"] != "STORY":
                continue  # only process story type articles
            url = article["content"]["canonicalUrl"]["url"]
            print(url)
            article_content = fetch_article(url)
            print(article_content)
            summary = summarize_news(article_content, ticker)
            print(summary)
            summaries.append({
                "title": article["content"]["title"],
                "yf_summary": article["content"]["summary"],
                "news_summary": summary
            })
        except Exception as e:
            print(f"Error fetching article {article['content']['canonicalUrl']['url']}: {e}")
    print(summaries)
    save_path = f"news_summaries_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(save_path, "w") as f:
        json.dump(summaries, f)
    print(f"Summaries saved to {save_path}")
    trading_decision_text, trading_decision_parsed = make_trading_decision(summaries, ticker)
    print(trading_decision_text)
    print(trading_decision_parsed)
    save_path = f"trading_decision_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(save_path, "w") as f:
        f.write(trading_decision_parsed.model_dump_json(indent=2))
    print(f"Trading decision saved to {save_path}")
