class AssetManager:
    def __init__(self, initial_cash):
        # 初始化现金和持股信息
        self.cash = initial_cash
        self.stocks = {}  # 存储持有的股票
        self.total_asset = initial_cash  # 初始总资产

    def buy_stock(self, stock_code, stock_name, quantity, price_per_unit):
        """买入股票"""
        total_price = quantity * price_per_unit
        
        if total_price > self.cash:
            print(f"错误：账户现金不足，无法购买 {stock_name}。")
            return
        
        # 更新持股信息
        if stock_code in self.stocks:
            self.stocks[stock_code]['quantity'] += quantity
        else:
            self.stocks[stock_code] = {
                'name': stock_name,
                'quantity': quantity,
                'price_per_unit': price_per_unit
            }
        
        # 扣除现金，并更新总资产
        self.cash -= total_price
        self.update_total_asset()

    def sell_stock(self, stock_code, quantity, sell_price_per_unit):
        """卖出股票"""
        if stock_code not in self.stocks or self.stocks[stock_code]['quantity'] < quantity:
            print(f"错误：没有足够的 {stock_code} 股票卖出")
            return
        
        # 更新持股数量
        self.stocks[stock_code]['quantity'] -= quantity
        if self.stocks[stock_code]['quantity'] == 0:
            del self.stocks[stock_code]  # 如果卖完了，删除该股票
        
        # 更新现金并计算总资产
        total_sell_value = quantity * sell_price_per_unit
        self.cash += total_sell_value
        self.update_total_asset()

    def deposit_cash(self, amount):
        """存入现金"""
        self.cash += amount
        self.update_total_asset()
        print(f"成功存入 {amount} 美元。当前现金：{self.cash} 美元")

    def withdraw_cash(self, amount):
        """提取现金"""
        if amount > self.cash:
            print(f"错误：账户现金不足，无法提取 {amount} 美元。")
            return
        
        self.cash -= amount
        self.update_total_asset()
        print(f"成功提取 {amount} 美元。当前现金：{self.cash} 美元")

    def update_total_asset(self):
        """更新总资产（现金 + 持股市值）"""
        self.total_asset = self.cash
        for stock in self.stocks.values():
            stock_value = stock['quantity'] * stock['price_per_unit']
            self.total_asset += stock_value

    def get_stock_summary(self):
        """获取持股情况摘要"""
        summary = {}
        for stock_code, stock_info in self.stocks.items():
            stock_value = stock_info['quantity'] * stock_info['price_per_unit']
            summary[stock_code] = {
                'stock_name': stock_info['name'],
                'quantity': stock_info['quantity'],
                'price_per_unit': stock_info['price_per_unit'],
                'total_value': stock_value
            }
        return summary

    def get_asset_summary(self):
        """获取资产摘要，包括现金和总资产"""
        return {
            'cash': self.cash,
            'total_asset': self.total_asset,
            'stocks_summary': self.get_stock_summary()
        }
