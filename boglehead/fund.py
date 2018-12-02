import sys
import os
import csv


class Fund(object):

    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.historical_date_reference = {}
        self.historical_close_prices = []
        self.historical_dividends = []

        self.load_history()

    @property
    def history_filename(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(this_dir, 'data', self.symbol + '.csv')

    def load_history(self, filename=None):
        filename = filename or self.history_filename
        with open(filename, 'r') as stream:
            stream.readline()
            reader = csv.reader(stream)
            for row in reader:
                date = row[0]
                close_price = float(row[4])
                # adj_close_price = float(row[5])
                self.historical_date_reference[date] = \
                    len(self.historical_close_prices)
                self.historical_close_prices.append(close_price)

    def gain(self, date):
        """daily gain percentage"""
        i = self.historical_date_reference[date]
        if i > 0:
            close1 = self.historical_close_prices[i]
            close0 = self.historical_close_prices[i-1]
        return (close1 - close0) / close0


if __name__ == '__main__':
    fund = Fund('vfinx')
    fund.load_history()
