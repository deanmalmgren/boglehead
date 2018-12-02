from fund import Fund


class Portfolio(object):

    def __init__(self, funds_list, proportion_list):
        self.funds = funds_list
        self.proportions = proportion_list

        if len(self.funds) != len(self.proportions):
            raise IndexError('funds and proportions must be same length')
        if sum(proportion_list) != 1.0:
            raise ValueError('proportions should add to 1')

        for i, fund in enumerate(self.funds):
            if not isinstance(fund, Fund):
                fund = Fund(fund)
                self.funds[i] = fund

    def gain(self, date):
        g = 0.0
        for fund, proportion in zip(self.funds, self.proportions):
            g += fund.gain(date) * proportion
        return g



if __name__ == '__main__':
    portfolio = Portfolio(
        ['VBMFX', 'VFINX', 'VISVX', 'VMVIX'],
        [0.2, 0.4, 0.2, 0.2],
    )

    print portfolio.gain('2018-11-28')
