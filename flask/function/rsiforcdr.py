import aiohttp
import asyncio
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from .data import company_codes
company_code = [
    'ABBV', 'AMD', 'GOOGL', 'AMZN', 'AAPL', 'BAC', 'BRK-B', 'BA', 'CVX', 'CSCO',
    'C', 'KO', 'COST', 'CVS', 'XOM', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JPM',
    'MA', 'MCD', 'META', 'MSFT', 'NFLX', 'NKE', 'NVDA', 'PYPL', 'PFE', 'PG', 'CRM', 'SBUX'
]
now = datetime.now()
aend = now - timedelta(days=1)
astart = aend - timedelta(days=25)

start_date = astart.strftime('%Y-%m-%d')
end_date = aend.strftime('%Y-%m-%d')

async def fetch_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end, interval="1d")
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

async def calculate_rsi(ticker, data, window):
    try:
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    except Exception as e:
        print(f"Error calculating RSI for {ticker}: {e}")
        return None

async def process_stock(ticker, start, end):
    data = await fetch_data(ticker, start, end)
    if data is None or data.empty:
        print(f"No data for {ticker}")
        return None, None
    data['RSI'] = await calculate_rsi(ticker, data, 14)
    if data['RSI'] is None or data['RSI'].isna().all():
        print(f"RSI cannot be calculated for {ticker}")
        return None, None
    # iloc[-1] is the method of the panda to get the last the newest rsi of the stock 
    last_rsi = data['RSI'].iloc[-1]
    return ticker, last_rsi

async def main():
    low_rsi_stock = []
    #  return the ticker and last_rsi all not invalid stock name and the number
    tasks = [process_stock(ticker, start_date, end_date) for ticker in company_code]
    #  这个task 就是创建task 然后一起运行 协程
    results = await asyncio.gather(*tasks)
    
    for ticker, last_rsi in results:
        if ticker is not None and last_rsi is not None and last_rsi <= 50:
            low_rsi_stock.append((ticker, last_rsi))

    return low_rsi_stock

if __name__ == "__main__":
    asyncio.run(main())