#run.py
from flask import Flask, request, render_template,redirect
import yfinance as yf
import os
import pandas as pd
import mplfinance as mpf
import matplotlib
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from scroll import url_fun, create_driver, open_url, scroll_to_end, get_company_names
from function.rsi import main as rsi_main
from function.rsiforcdr import main as rsi_mains
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta


app = Flask(__name__,static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/ability')
def ability():
    return render_template('self.html')

@app.route('/search', methods=['POST'])
def search():
    stock = request.form.get('stock')
    ticker = yf.Ticker(stock)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    stock_data = yf.download(stock, start=start_date, end=end_date)
    selected_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]




    csv_file = f'{stock}.csv'
    csv_path = os.path.join(app.static_folder, csv_file)
    img_filename = f'{stock}.png'
    img_path = os.path.join(app.static_folder, img_filename)

    if os.path.exists(csv_path):
        selected_data.to_csv(csv_path, mode='a', header=False)
    else:
        selected_data.to_csv(csv_path)
    generate_plot(selected_data, stock, img_path)
    return render_template('mar.html', stock=stock, img_path=img_filename)
    
    
def generate_plot(data, stock, path):
    mpf.plot(data, type='candle', volume=True, style='charles', 
                title=f'{stock} K线图', ylabel='价格', ylabel_lower='交易量', 
                mav=(20, 50), savefig=path)
@app.route('/mar')
def mar():
    return render_template('mar.html')
@app.route('/rsi',methods=['GET', 'POST'])
def rsi():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    low_rsi_stocks = loop.run_until_complete(rsi_main())
    return render_template('rsi.html',first=low_rsi_stocks)
@app.route('/cdr',methods=['GET', 'POST'])
def cdr():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    low_rsi_stocks = loop.run_until_complete(rsi_mains())
    return render_template('cdr.html',first=low_rsi_stocks)

@app.route('/logic1')
def logic1():
    return render_template('logic1.html')

@app.route('/logic2')
def logic2():
    return render_template('logic2.html')

@app.route('/logic3')
def logic3():
    return render_template('logic3.html')
@app.route('/companyindex')
def companyindex():
        return render_template('company/gdg.html')
        #return redirect("https://www.youtube.com/watch?v=8aHfeZdbrpM&t=11s")
@app.route('/company',methods=['GET','POST'])
def company():
    if request.method == 'POST':
        basic='https://www.google.ca/maps/search/software+company/@'
        address = request.form['address']
        z=request.form['z']
        page=request.form['page']
        page=int(page)
        if address and z:
            url=url_fun(basic,address,z)
            driver=create_driver()
            open_url(driver,url)
            end=scroll_to_end(driver,page)
            if end:
                end="get the end"
            else:
                end="have more company position"
            name=get_company_names(driver)
            driver.quit()
        else:
            return render_template('company/wrong.html')
 
    return render_template('company/company.html', name = name,end=end)
@app.route('/bird')
def bird():
    return redirect("https://youtu.be/jsGQNRdLhRo")
@app.route('/a')
def b():
    return render_template('company/index2.html')
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 500))
    app.run(host='0.0.0.0', port=port)
