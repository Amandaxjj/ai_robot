# position_controller.py (升级版 with StockManager 兼容)

from datetime import datetime

class PositionController:
    def __init__(self, stock_manager, buy_mode='fixed', fixed_pct=0.08, max_pct=0.12, total_stocks=10):
        self.stock_manager = stock_manager  # 接入外部StockManager对象
        self.buy_mode = buy_mode  # 'fixed' or 'equal_weight'
        self.fixed_pct = fixed_pct  # 固定买入比例，比如8%
        self.max_pct = max_pct  # 单股最大持仓比例，比如12%
        self.total_stocks = total_stocks  # 用于equal_weight模式

    def get_holding(self, symbol):
        df = self.stock_manager.get_stock_df()
        row = df[df['代码'] == symbol]
        if row.empty:
            return None
        return {
            'quantity': int(row['持仓数量'].values[0]),
            'buy_price': row['成本价'].values[0]
        } if row['是否持仓'].values[0] else None

    def update_holding(self, symbol, quantity_change, price):
        df = self.stock_manager.get_stock_df()
        idx = df[df['代码'] == symbol].index[0]
        current_qty = int(df.at[idx, '持仓数量'])

        new_qty = current_qty + quantity_change
        if new_qty <= 0:
            df.at[idx, '是否持仓'] = False
            df.at[idx, '持仓数量'] = 0
            df.at[idx, '成本价'] = None
        else:
            df.at[idx, '是否持仓'] = True
            df.at[idx, '持仓数量'] = new_qty
            if quantity_change > 0:
                df.at[idx, '成本价'] = price  # 简化处理：不加权平均

    def decide_buy_quantity(self, cash, price, total_asset):
        if self.buy_mode == 'fixed':
            max_invest = total_asset * self.fixed_pct
        elif self.buy_mode == 'equal_weight':
            max_invest = total_asset * 0.8 / self.total_stocks
        else:
            raise ValueError("Invalid buy mode")

        actual_cash = min(cash, max_invest)
        quantity = int(actual_cash // price)
        return quantity

    def decide_add_quantity(self, symbol, cash, price, total_asset):
        holding = self.get_holding(symbol)
        if not holding:
            return 0

        current_value = holding['quantity'] * price
        max_value = total_asset * self.max_pct

        if current_value >= max_value:
            return 0

        allowable_add_value = max_value - current_value
        actual_cash = min(cash, allowable_add_value)
        quantity = int(actual_cash // price)
        return quantity

    def decide_sell_quantity(self, symbol, current_price, sell_signal=False):
        holding = self.get_holding(symbol)
        if not holding:
            return 0

        buy_price = holding['buy_price']
        quantity = holding['quantity']
        change_pct = (current_price - buy_price) / buy_price if buy_price else 0
        min_holding_qty = int(quantity * 0.2)

        qty_to_sell = 0
        if change_pct >= 0.25:
            qty_to_sell = max(quantity - min_holding_qty, 0)
        elif change_pct >= 0.15:
            qty_to_sell = int(quantity * 0.5)
        elif change_pct <= -0.10:
            qty_to_sell = max(quantity - min_holding_qty, 0)
        elif change_pct <= -0.05:
            qty_to_sell = int(quantity * 0.3)
        elif sell_signal:
            qty_to_sell = int(quantity * 0.2)

        return qty_to_sell
