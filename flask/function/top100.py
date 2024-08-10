import yfinance as yf
from data.py import company
# 定义股票代码
ticker = input("what")
stock = yf.Ticker(ticker)
info = stock.info

# 查询总股价
shares_outstanding = info.get("sharesOutstanding")

# 打印结果
print(shares_outstanding)
