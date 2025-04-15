# 导入资产管理模块
from asset_manager import AssetManager

# 1. 初始化资产管理器，初始现金为 10000 美元（已经默认设置）
asset_manager = AssetManager(10000)

# 2. 测试存入现金（这里你可以跳过这一步，因为默认有10000现金）
# 如果你希望存入额外的现金，可以继续使用 deposit_cash 测试
# asset_manager.deposit_cash(5000)

print("---- 存入现金测试 ----")
asset_manager.deposit_cash(5000)  # 存入 5000 美元
print(asset_manager.get_asset_summary())  # 打印资产摘要

# 3. 测试买入股票（例如苹果公司 AAPL）
print("---- 买入股票测试 ----")
asset_manager.buy_stock("AAPL", "苹果公司", 100, 145.30)  # 买入 100 股苹果股票，单价 145.30 美元
print(asset_manager.get_asset_summary())  # 打印资产摘要

# 4. 测试卖出股票（例如特斯拉 TSLA）
print("---- 卖出股票测试 ----")
asset_manager.sell_stock("TSLA", 50, 700.00)  # 假设你有 50 股 TSLA，卖出它
print(asset_manager.get_asset_summary())  # 打印资产摘要

# 5. 测试提取现金
print("---- 提取现金测试 ----")
asset_manager.withdraw_cash(2000)  # 提取 2000 美元
print(asset_manager.get_asset_summary())  # 打印资产摘要

# 6. 测试买入股票时现金不足的情况
print("---- 买入股票时现金不足测试 ----")
asset_manager.buy_stock("AAPL", "苹果公司", 100, 5000)  # 假设你没有足够现金买 100 股苹果
print(asset_manager.get_asset_summary())  # 打印资产摘要
