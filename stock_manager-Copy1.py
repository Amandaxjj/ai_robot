import pandas as pd

class StockManager:
    def __init__(self):
        self.stock_df = pd.DataFrame([
            {"代码": "AAPL", "标签": "科技", "是否持仓": False, "持仓数量": 0, "成本价": None},
            {"代码": "MSFT", "标签": "科技", "是否持仓": False, "持仓数量": 0, "成本价": None},
            {"代码": "TSLA", "标签": "成长", "是否持仓": False, "持仓数量": 0, "成本价": None},
            {"代码": "NVDA", "标签": "AI",   "是否持仓": False, "持仓数量": 0, "成本价": None},
            {"代码": "AMZN", "标签": "消费", "是否持仓": False, "持仓数量": 0, "成本价": None},
            {"代码": "GOOG", "标签": "科技", "是否持仓": False, "持仓数量": 0, "成本价": None},
            {"代码": "META", "标签": "社交", "是否持仓": False, "持仓数量": 0, "成本价": None},
        ])

    def handle_input(self, pack):
        stock_code, cash_delta = pack
        # 添加新股票
        if stock_code != 0 and stock_code not in self.stock_df["代码"].values:
            self.stock_df.loc[len(self.stock_df)] = {
                "代码": stock_code,
                "标签": "自定义",
                "是否持仓": False,
                "持仓数量": 0,
                "成本价": None
            }
        return cash_delta  # 把资金变动交给资产模块处理

    def get_symbols(self):
        return self.stock_df["代码"].tolist()

    def get_stock_df(self):
        return self.stock_df


