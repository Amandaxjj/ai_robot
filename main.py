# main.py
from asset_manager import AssetManager
from stock_manager import StockManager
from position_management import PositionController

from get_stock_data import fetch_stock_data
from news_sentiment import get_news_sentiment_signal
from data_signal import analyze_lightweight
from buy_sell_decision import final_trade_decision

START_CASH = 10000

# ---- 0. 初始化 ----
asset_mgr  = AssetManager(START_CASH)
stock_mgr  = StockManager()
pos_ctrl   = PositionController(stock_mgr, buy_mode='fixed')

def run_once(ticker: str):
    # 1) 拉行情
    stock_dict = fetch_stock_data(ticker)          # {'AAPL': {...}}
    snap       = stock_dict[ticker]
    price      = snap["current_price"]

    # 2) 得到交易信号
    news_sig   = get_news_sentiment_signal(ticker)["signal"]
    data_sig   = analyze_lightweight(ticker, snap)["final_decision"]
    final_sig  = final_trade_decision(news_sig, data_sig)   # BUY / SELL / HOLD

    # 3) 持仓决策
    cash       = asset_mgr.cash
    total_ast  = asset_mgr.total_asset

    if final_sig == "BUY":
        qty = pos_ctrl.decide_buy_quantity(cash, price, total_ast)
        if qty > 0:
            asset_mgr.buy_stock(ticker, snap["name"], qty, price)
            pos_ctrl.update_holding(ticker,  qty, price)

    elif final_sig == "SELL":
        qty = pos_ctrl.decide_sell_quantity(ticker, price, sell_signal=True)
        if qty > 0:
            asset_mgr.sell_stock(ticker, qty, price)
            pos_ctrl.update_holding(ticker, -qty, price)

    # 4) 输出账户现状
    summary = asset_mgr.get_asset_summary()
    print("\n=== 当前账户快照 ===")
    print(f"现金: {summary['cash']:.2f}")
    print(f"总资产: {summary['total_asset']:.2f}")
    for code, info in summary['stocks_summary'].items():
        print(f"- {code}: {info['quantity']} 股 @ {info['price_per_unit']} => {info['total_value']:.2f}")

if __name__ == "__main__":
    while True:
        code = input("\n请输入股票代码(回车退出): ").strip().upper()
        if not code:
            break
        run_once(code)
