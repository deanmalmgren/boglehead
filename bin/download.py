"""
Download data from Yahoo Finance
"""

import datetime

import yfinance

from boglehead.fund import ALL_SYMBOLS, Fund


for symbol in ALL_SYMBOLS:
    print(symbol)
    fund = Fund(symbol, load_history=False)
    data = yfinance.download(tickers=symbol, period="max")
    data.to_csv(fund.history_filename)
