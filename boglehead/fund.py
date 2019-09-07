import sys
import os
import csv

import numpy

# all index funds from https://investor.vanguard.com/mutual-funds/list
ALL_SYMBOLS = [
    "VFIAX",
    "VBIAX",
    "VTMGX",
    "VDADX",
    "VGAVX",
    "VEMAX",
    "VEUSX",
    "VEXAX",
    "VFWAX",
    "VFSAX",
    "VFTAX",
    "VGRLX",
    "VIGAX",
    "VHYAX",
    "VBILX",
    "VICSX",
    "VSIGX",
    "VIAAX",
    "VIHAX",
    "VLCAX",
    "VSCGX",
    "VASGX",
    "VASIX",
    "VSMGX",
    "VBLAX",
    "VLTCX",
    "VLGSX",
    "VMGMX",
    "VIMAX",
    "VMVAX",
    "VMBSX",
    "VPADX",
    "VGSLX",
    "VBIRX",
    "VSCSX",
    "VTAPX",
    "VSBSX",
    "VSGAX",
    "VSMAX",
    "VSIAX",
    "VTXVX",
    "VTWNX",
    "VTTVX",
    "VTHRX",
    "VTTHX",
    "VFORX",
    "VTIVX",
    "VFIFX",
    "VFFVX",
    "VTTSX",
    "VLXVX",
    "VTINX",
    "VTEAX",
    "VTMFX",
    "VTCLX",
    "VTMSX",
    "VBTLX",
    "VTABX",
    "VTIAX",
    "VTSAX",
    "VTWAX",
    "VVIAX",
]


def load_all_funds():
    all_funds = []
    for symbol in ALL_SYMBOLS:
        all_funds.append(Fund(symbol))
    return all_funds


class Fund(object):

    def __init__(self, symbol, load_history=True):
        self.symbol = symbol.upper()
        self.price = 0.0
        self.units = 0.0
        self.historical_date_reference = {}
        self.historical_close_prices = []
        self.historical_dividends = []

        if load_history:
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

    def min_date(self):
        return min(self.historical_date_reference.keys())

    def gain(self, date):
        """daily gain percentage"""
        i = self.historical_date_reference[date]
        if i > 0:
            close1 = self.historical_close_prices[i]
            close0 = self.historical_close_prices[i-1]
        return (close1 - close0) / close0

    def simulate_date(self, date):
        """simulate the value gain based on a historical `date`"""
        self.price = (1 + self.gain(date)) * self.price

    def value(self):
        return self.price * self.units

    def correlation(self, other):
        if not isinstance(other, Fund):
            raise TypeError("can only calculate correlations on another Fund")

        dates = set(self.historical_date_reference.keys())
        other_dates = set(other.historical_date_reference.keys())
        dates.intersection_update(other_dates)
        dates = list(dates)

        self_prices = []
        other_prices = []
        for date in sorted(dates):
            i = self.historical_date_reference[date]
            self_prices.append(self.historical_close_prices[i])
            i = other.historical_date_reference[date]
            other_prices.append(other.historical_close_prices[i])
        c = numpy.corrcoef(self_prices, other_prices)
        return c[0,1]


if __name__ == '__main__':
    fund = Fund('vfinx')
    fund.load_history()
