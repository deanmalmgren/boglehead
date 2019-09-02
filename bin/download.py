"""
Download data from Yahoo Finance
"""

import datetime

import yfinance

from boglehead.fund import ALL_FUNDS, Fund


for symbol, inception_date in ALL_FUNDS:
    print(symbol)
    fund = Fund(symbol, load_history=False)
    data = yfinance.download(tickers=symbol, period="max")
    data.to_csv(fund.history_filename)
